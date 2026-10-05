#!/usr/bin/env python3
"""CETALab Uni pilot — dedup + descriptive stats for poster rubric sections.

Reads:  "Cetavals Uni - Result.csv"
Writes: output/stats.json  (+ prints human-readable summary)

Dedup rule: keep FIRST occurrence per participant_id (exact-duplicate rows are
resubmission artefacts, not distinct respondents).
"""
import csv, json, statistics as st, os, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "..", "Cetavals Uni - Result.csv")
OUT = os.path.join(HERE, "stats.json")

STATES = ["yaqeen", "zann", "shak", "wahm"]
# Islamic-epistemic certainty ladder: yaqeen=certain .. wahm=illusion
STATE_ORDER = {"yaqeen": 3, "zann": 2, "shak": 1, "wahm": 0}

def load_dedup(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    seen, uniq = set(), []
    for r in rows:
        pid = r["participant_id"].strip()
        if pid in seen:
            continue
        seen.add(pid)
        uniq.append(r)
    return rows, uniq

def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None

def pct(n, d):
    return round(100.0 * n / d, 1) if d else None

def main():
    rows, u = load_dedup(CSV_PATH)
    n = len(u)
    out = {"raw_rows": len(rows), "n_unique": n,
           "duplicate_rows": len(rows) - n}

    # ---- duration (minutes) ----
    from datetime import datetime
    durs = []
    for r in u:
        try:
            a = datetime.fromisoformat(r["started_at"].replace("Z", "+00:00"))
            b = datetime.fromisoformat(r["finished_at"].replace("Z", "+00:00"))
            durs.append((b - a).total_seconds() / 60.0)
        except Exception:
            pass
    if durs:
        out["duration_min"] = {"mean": round(st.mean(durs), 1),
                               "median": round(st.median(durs), 1),
                               "min": round(min(durs), 1),
                               "max": round(max(durs), 1)}

    # ---- pre-survey ----
    out["pre_ai_use_freq"] = dict(Counter(r["pre_ai_use_freq"] for r in u))
    out["pre_heard_four_states"] = dict(Counter(r["pre_heard_four_states"] for r in u))
    pre_scale = ["pre_detect_unreliable", "pre_trust_ai_sourcing",
                 "pre_check_citations", "pre_know_confident_vs_correct"]
    out["pre_scale_means"] = {c: round(st.mean([num(r[c]) for r in u if num(r[c]) is not None]), 2)
                              for c in pre_scale}

    # ---- calibration: 10 items ----
    item_acc = {}          # qN -> % exact (distance 0)
    tot_exact = 0
    tot_items = 0
    conf_correct = 0       # claimed yaqeen AND distance 0
    conf_total = 0         # claimed yaqeen
    for i in range(1, 11):
        uk, dk = f"q{i}_user", f"q{i}_distance"
        exact = sum(1 for r in u if num(r[dk]) == 0)
        item_acc[f"q{i}"] = {"exact": exact, "pct": pct(exact, n),
                             "mean_distance": round(st.mean([num(r[dk]) for r in u if num(r[dk]) is not None]), 2)}
        tot_exact += exact
        tot_items += n
        for r in u:
            if r[uk] == "yaqeen":
                conf_total += 1
                if num(r[dk]) == 0:
                    conf_correct += 1
    out["item_accuracy"] = item_acc
    out["calibration_overall_pct"] = pct(tot_exact, tot_items)
    out["overconfidence"] = {
        "claimed_yaqeen": conf_total,
        "of_which_wrong": conf_total - conf_correct,
        "overconfidence_pct": pct(conf_total - conf_correct, conf_total),
        "yaqeen_accuracy_pct": pct(conf_correct, conf_total),
    }

    # ---- module_correct (0-7) ----
    mc = [num(r["module_correct"]) for r in u if num(r["module_correct"]) is not None]
    out["module_correct"] = {
        "mean": round(st.mean(mc), 2), "median": round(st.median(mc), 1),
        "max": int(max(mc)), "min": int(min(mc)),
        "dist": dict(sorted(Counter(int(x) for x in mc).items())),
        "pct_ge5": pct(sum(1 for x in mc if x >= 5), len(mc)),
    }

    # ---- post constructs (1-5) ----
    post = ["post_detect_unreliable", "post_trust_ai_sourcing", "post_check_citations",
            "post_know_confident_vs_correct", "post_wahm_comprehension",
            "post_nondeterminism_comprehension", "post_verify_likelihood",
            "post_module_helped", "post_module_relevant", "post_stayed_with_you",
            "post_surprised"]
    out["post_means"] = {c: round(st.mean([num(r[c]) for r in u if num(r[c]) is not None]), 2)
                         for c in post if any(num(r[c]) is not None for r in u)}
    out["post_wahm_comprehension_dist"] = dict(Counter(r["post_wahm_comprehension"] for r in u))
    out["post_nondeterminism_dist"] = dict(Counter(r["post_nondeterminism_comprehension"] for r in u))
    out["post_verify_dist"] = dict(Counter(r["post_verify_likelihood"] for r in u))
    out["post_module_helped_dist"] = dict(Counter(r["post_module_helped"] for r in u))

    # ---- pre/post behaviour deltas ----
    def paired_mean(col_pre, col_post):
        a = [(num(r[col_pre]), num(r[col_post])) for r in u]
        a = [(x, y) for x, y in a if x is not None and y is not None]
        return {"pre": round(st.mean([x for x, _ in a]), 2),
                "post": round(st.mean([y for _, y in a]), 2),
                "n": len(a)}
    out["deltas"] = {
        "detect_unreliable": paired_mean("pre_detect_unreliable", "post_detect_unreliable"),
        "trust_ai_sourcing": paired_mean("pre_trust_ai_sourcing", "post_trust_ai_sourcing"),
        "check_citations": paired_mean("pre_check_citations", "post_check_citations"),
        "know_confident_vs_correct": paired_mean("pre_know_confident_vs_correct", "post_know_confident_vs_correct"),
    }

    # ---- why-AI-is-unreliable theme count (free text) ----
    theme_keys = {"nondeterminism": ["different answer", "different answers", "same prompt",
                                     "inconsistent", "non-determin", "palatau"],
                  "fabrication": ["fabricat", "made up", "nonexistent", "own fatwa",
                                  "own source", "not have the authority", "manipulat"],
                  "false_confidence": ["confiden", "convincing", "certainty", "believe ai 100"]}
    themes = defaultdict(int)
    for r in u:
        blob = " ".join([r.get("post_surprised", "") or "",
                         r.get("post_fatwa_scenario", "") or "",
                         r.get("post_stayed_with_you", "") or ""]).lower()
        for k, keys in theme_keys.items():
            if any(kk in blob for kk in keys):
                themes[k] += 1
    out["themes"] = {k: {"n": v, "pct": pct(v, n)} for k, v in themes.items()}

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    # ---- print summary ----
    print(f"RAW rows: {out['raw_rows']}   UNIQUE participants (N): {out['n_unique']}   dupes removed: {out['duplicate_rows']}")
    if "duration_min" in out:
        print(f"Duration (min): mean {out['duration_min']['mean']}, median {out['duration_min']['median']}, range {out['duration_min']['min']}-{out['duration_min']['max']}")
    print("\nPre AI-use frequency:", out["pre_ai_use_freq"])
    print("Pre heard four states:", out["pre_heard_four_states"])
    print("Pre scale means:", out["pre_scale_means"])
    print(f"\nCalibration (10 items): overall exact-match = {out['calibration_overall_pct']}%")
    for q, v in out["item_accuracy"].items():
        print(f"  {q}: {v['pct']}% exact  (mean dist {v['mean_distance']})")
    o = out["overconfidence"]
    print(f"\nOverconfidence: claimed yaqeen {o['claimed_yaqeen']}x, wrong {o['of_which_wrong']}x "
          f"-> overconfident {o['overconfidence_pct']}% ; yaqeen-accurate {o['yaqeen_accuracy_pct']}%")
    print("\nModule quiz (0-7):", out["module_correct"])
    print("\nPost means (1-5):", out["post_means"])
    print("post_wahm_comprehension:", out["post_wahm_comprehension_dist"])
    print("post_nondeterminism:", out["post_nondeterminism_dist"])
    print("post_verify_likelihood:", out["post_verify_dist"])
    print("post_module_helped:", out["post_module_helped_dist"])
    print("\nDeltas pre->post:", json.dumps(out["deltas"], indent=2))
    print("\nThemes:", out["themes"])
    print(f"\nWrote {OUT}")

if __name__ == "__main__":
    main()
