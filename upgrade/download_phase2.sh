#!/usr/bin/env bash
set -euo pipefail

# Usage: ./download_phase2.sh [YEAR] [MONTH] [CMSSW_TAG]
# Defaults are taken from your example URL.
YEAR="${1:-2025}"
MONTH="${2:-11}"
CMSSW="${3:-CMSSW_16_0_X}"

BASE_URL="https://cmssdt.cern.ch/circles/web/hlt-p2-timing"
ARCH="el8_amd64_gcc13"

# Zero-pad month (e.g. 7 -> 07)
MONTH=$(printf "%02d" "$MONTH")

# Directory where files will be stored
OUTDIR="${YEAR}-${MONTH}"
mkdir -p "$OUTDIR"

for DAY in $(seq -w 1 31); do
  for IB in 1100 2300; do
    TAG="${CMSSW}_${YEAR}-${MONTH}-${DAY}-${IB}"
    URL="${BASE_URL}/${TAG}/${ARCH}/Phase2Timing_resources_NGT.json"
    OUTFILE="${OUTDIR}/Phase2Timing_resources_NGT_${TAG}.json"

    echo "Trying ${URL}"
    if curl -fsS "${URL}" -o "${OUTFILE}"; then
      echo "  -> Downloaded to ${OUTFILE}"
    else
      echo "  -> Not found (removing partial file if any)"
      rm -f "${OUTFILE}"
    fi
  done
done
