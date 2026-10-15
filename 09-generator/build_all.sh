#!/bin/bash
# Rebuild the whole kit in dependency order: logo -> icons/states -> marketing ->
# marketing (incl. Flat stickers) -> samples -> guideline HTML/PDF -> download zips.
# sync_kit copies fresh artwork to where the HTML templates read it (see sync_kit.py).
set -euo pipefail
cd "$(dirname "$0")"
for step in build_logo build_guides build_icons sync_kit build_marketing sync_kit build_samples build_play build_appstore build_guide build_zips; do
  echo "== $step"
  ./run.sh "$step.py"
done
