#!/usr/bin/env bash
# Pull Kaggle datasets used for SFT bulk volume + benign smoke test.
# Requires: pip install kaggle ; ~/.kaggle/kaggle.json API token (kaggle.com/settings)
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p raw

# TODO: confirm exact slugs on kaggle.com before running -- these are the search targets,
# not verified exact owner/slug strings yet.
kaggle datasets download -d databricks/databricks-dolly-15k -p raw/dolly --unzip || true
kaggle datasets download -d cynthiarempel/banking77 -p raw/banking77 --unzip || true
# Malay/BM corpus -- search "bahasa malaysia text" on Kaggle and fill in the slug below
# kaggle datasets download -d <owner>/<slug> -p raw/malay-corpus --unzip

echo "Downloaded to ./raw/ -- subsample down to a few hundred rows per source before use."
