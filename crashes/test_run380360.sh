#!/bin/bash -ex

[ $# -ge 2 ] || exit 1

hltGetConfiguration run:380360 \
  --globaltag 140X_dataRun3_HLT_v3 \
  --data \
  --no-prescale \
  --no-output \
  --max-events -1 \
  --input "${1}" \
  > "${2}".py

cat <<@EOF >> "${2}".py
process.options.wantSummary = True

process.options.numberOfThreads = 8
process.options.numberOfStreams = 0
@EOF

cmsRun "${2}".py &> "${2}".log
