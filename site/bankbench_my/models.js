/* BankBench shared model catalogue loader.
 * Fetches each provider's LIVE /models list via /api/proxy (so a retired id can
 * never be offered again) and keeps OpenRouter to cheap/free models only.
 *
 * BBModels.list(provider,key)      -> Promise<string[]>
 * BBModels.detailed(provider,key)  -> Promise<row[]>
 * BBModels.fill(sel,provider,key,opts) -> Promise<row[]>
 * BBModels.bindFilter(inputEl, sel)
 * BBModels.state(provider)         -> 'live' | 'fallback'
 *
 * row = { id, free, price, vendor, nim }
 *   price = USD per MILLION tokens (prompt+completion), null when unknown
 *
 * opts: current, onlyCheap (default true), maxPrice (default 1.0),
 *       includeCustom (default true)
 */
(function () {
  var PROXY = '/api/proxy?target=';
  var DEFAULT_MAX_PRICE = 1.0;
  var bases = {
    openrouter: 'https://openrouter.ai/api/v1',
    nvidia: 'https://integrate.api.nvidia.com/v1'
  };
  var fallback = {
    openrouter: ['deepseek/deepseek-v4.1-flash', 'openai/gpt-4o-mini',
      'google/gemini-2.5-flash', 'meta-llama/llama-3.1-8b-instruct',
      'mistralai/mistral-nemo', 'openai/gpt-oss-20b'],
    nvidia: ['deepseek-ai/deepseek-v4.1-flash', 'meta/llama-3.1-8b-instruct',
      'nvidia/nemotron-3.5-lightning-30b-a3b', 'openai/gpt-oss-20b',
      'mistralai/mistral-7b-instruct-v0.3']
  };
  var cache = {}, cacheState = {};

  function vendorOf(id) { var i = id.indexOf('/'); return i > 0 ? id.slice(0, i) : 'other'; }

  function isTextOut(m) {
    var a = m.architecture || {}, om = a.output_modalities;
    if (om && om.length) return om.indexOf('text') !== -1;
    return String(a.modality || '').slice(-6) === '->text';
  }

  function combPrice(m) {
    var p = m.pricing || {}, a = parseFloat(p.prompt), b = parseFloat(p.completion);
    if (isNaN(a) || isNaN(b) || a < 0 || b < 0) return null; // -1 = variable router
    return a * 1e6 + b * 1e6;
  }

  async function refresh(provider, key) {
    var base = bases[provider];
    if (!base) return [];
    var headers = {};
    if (key) headers.Authorization = 'Bearer ' + key;
    try {
      var res = await fetch(PROXY + encodeURIComponent(base + '/models'), { headers: headers });
      if (!res.ok) throw new Error('HTTP ' + res.status);
      var json = await res.json();
      var src = (json.data || []).filter(function (m) { return m && m.id; });
      var rows;
      if (provider === 'openrouter') {
        rows = src.filter(isTextOut).map(function (m) {
          var price = combPrice(m);
          if (price === null) return null;
          return { id: m.id, free: price === 0, price: price, vendor: vendorOf(m.id) };
        }).filter(Boolean);
      } else {
        rows = src.map(function (m) {
          return { id: m.id, free: false, price: null, vendor: vendorOf(m.id), nim: true };
        });
      }
      if (!rows.length) throw new Error('empty list');
      cache[provider] = rows;
      cacheState[provider] = 'live';
    } catch (e) {
      console.warn('[BBModels] live fetch failed for ' + provider + ':', e.message);
      cache[provider] = (fallback[provider] || []).map(function (id) {
        return { id: id, free: provider === 'nvidia', price: null, vendor: vendorOf(id), nim: provider === 'nvidia' };
      });
      cacheState[provider] = 'fallback';
    }
    return cache[provider];
  }

  function detailed(provider, key) {
    if (cache[provider]) return Promise.resolve(cache[provider]);
    return refresh(provider, key);
  }
  function list(provider, key) {
    return detailed(provider, key).then(function (r) { return r.map(function (x) { return x.id; }); });
  }
  function state(provider) { return cacheState[provider] || 'unknown'; }
  function maxPriceDefault() { return DEFAULT_MAX_PRICE; }

  // free first, then cheapest, then alphabetical — so the useful ones are on top
  function order(a, b) {
    if (a.free !== b.free) return a.free ? -1 : 1;
    var ap = a.price === null ? Infinity : a.price, bp = b.price === null ? Infinity : b.price;
    if (ap !== bp) return ap - bp;
    return a.id < b.id ? -1 : a.id > b.id ? 1 : 0;
  }

  function label(r) {
    if (r.free) return r.id + '  · free';
    if (r.nim) return r.id + '  · NIM free-tier';
    if (r.price === 0) return r.id + '  · free';
    return r.id + '  · $' + r.price.toFixed(3) + '/Mtok';
  }

  function keep(row, onlyCheap, maxPrice) {
    if (!onlyCheap) return true;
    if (row.nim) return true;              // NVIDIA = free credit tier
    if (row.free) return true;
    if (row.price === null) return false;  // unknown price: hide unless showing all
    return row.price <= maxPrice;
  }

  async function fill(sel, provider, key, opts) {
    opts = opts || {};
    var onlyCheap = opts.onlyCheap !== false;
    var maxPrice = typeof opts.maxPrice === 'number' ? opts.maxPrice : DEFAULT_MAX_PRICE;
    var all = await detailed(provider, key);
    var rows = all.filter(function (r) { return keep(r, onlyCheap, maxPrice); }).sort(order);

    var prev = sel.value;
    var want = opts.current || (sel.dataset && sel.dataset.savedValue) || prev || '';

    sel.innerHTML = '';
    var ph = document.createElement('option');
    ph.value = '';
    ph.textContent = '— ' + rows.length + ' of ' + all.length + ' models' +
      (onlyCheap ? ' (cheap & free)' : '') + ' —';
    sel.appendChild(ph);

    var groups = {};
    rows.forEach(function (r) { (groups[r.vendor] = groups[r.vendor] || []).push(r); });
    Object.keys(groups).sort().forEach(function (v) {
      var og = document.createElement('optgroup');
      og.label = v;
      groups[v].forEach(function (r) {
        var o = document.createElement('option');
        o.value = r.id;
        o.textContent = label(r);
        og.appendChild(o);
      });
      sel.appendChild(og);
    });

    if (opts.includeCustom !== false) {
      var co = document.createElement('option');
      co.value = '__custom__';
      co.textContent = 'Other (type a model id)…';
      sel.appendChild(co);
    }

    if (want) {
      var exists = Array.prototype.some.call(sel.options, function (o) { return o.value === want; });
      sel.value = exists ? want : '__custom__';
    }
    if (sel.dataset) sel.dataset.savedValue = want;
    return rows;
  }

  function bindFilter(inputEl, sel) {
    inputEl.addEventListener('input', function () {
      var q = inputEl.value.trim().toLowerCase();
      Array.prototype.forEach.call(sel.querySelectorAll('option'), function (o) {
        if (!o.value || o.value === '__custom__') return;
        o.hidden = q ? o.textContent.toLowerCase().indexOf(q) === -1 : false;
      });
      Array.prototype.forEach.call(sel.querySelectorAll('optgroup'), function (g) {
        var any = Array.prototype.some.call(g.querySelectorAll('option'), function (o) { return !o.hidden; });
        g.hidden = !any;
      });
    });
  }

  /* --- API key hygiene ---
     OpenRouter replies "Missing Authentication header" (401) to ANY malformed
     Authorization value, so a paste slip looks identical to a real auth fault.
     Seen triggers: empty Bearer, raw key with no "Bearer " prefix,
     "Bearer Bearer x", surrounding quotes, inner whitespace, literal
     "undefined". Stripping them here means the header is always well formed. */
  function cleanKey(raw) {
    var k = String(raw == null ? '' : raw);
    k = k.replace(/^\s*(authorization|api[-_ ]?key)\s*[:=]\s*/i, '');
    k = k.replace(/^\s*bearer\s+/i, '');
    k = k.trim().replace(/^["']|["']$/g, '');
    // API keys are printable ASCII. Drop EVERY other character: this removes
    // newlines, non-breaking spaces and invisible zero-width characters that
    // survive trim() and \s, and which make the header unparseable upstream.
    k = k.replace(/[^\x21-\x7E]/g, '');
    if (/^(undefined|null|none|true|false)$/i.test(k)) return '';
    return k;
  }

  /* How many characters had to be thrown away, so the UI can say so out loud
     instead of silently fixing it. */
  function keyDiagnostics(raw) {
    var original = String(raw == null ? '' : raw);
    var junk = original.split('').filter(function (ch) { return !/[\x20-\x7E\t\n\r]/.test(ch); }).length;
    return { cleaned: cleanKey(original), stripped: junk };
  }

  function keyPrefix(provider) {
    return provider === 'nvidia' ? 'nvapi-' : 'sk-or-v1-';
  }

  /* '' when the key looks usable, otherwise a plain-English explanation. */
  function keyWarning(provider, cleaned) {
    if (!cleaned) return 'No API key saved yet.';
    var want = keyPrefix(provider);
    if (cleaned.indexOf(want) !== 0) {
      return 'Does not look like an ' + provider + ' key — expected it to start with "' + want + '".';
    }
    return '';
  }

  window.BBModels = {
    bases: bases, list: list, detailed: detailed, refresh: refresh,
    fill: fill, bindFilter: bindFilter, state: state,
    cleanKey: cleanKey, keyPrefix: keyPrefix, keyWarning: keyWarning,
    keyDiagnostics: keyDiagnostics,
    vendorOf: vendorOf, maxPriceDefault: maxPriceDefault
  };
})();
