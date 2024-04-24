#!/bin/bash -ex

hltGetConfiguration run:378981 \
  --globaltag 140X_dataRun3_HLT_v3 \
  --data \
  --no-prescale \
  --no-output \
  --max-events -1 \
  --input foo.root \
  > hlt.py

for file_i in $(ls /eos/cms/store/group/tsg/FOG/debug/240405_run378981/files/*.root); do
  fff=$(basename "${file_i}")
  label=${fff/.root/}
  rm -rf "${label}"
  mkdir -p "${label}"
  cp hlt.py "${label}"/hlt_"${label}".py

  cat <<@EOF >> "${label}"/hlt_"${label}".py

process.options.wantSummary = True
process.source.fileNames = ['file:${file_i}']
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

process.options.accelerators = ["*"]

process.hltL1MuonNoL2SelectorNoVtx.L1MinPt = 0.001

if hasattr(process, 'MessageLogger'):
    del process.MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
@EOF

  CUDA_LAUNCH_BLOCKING=1 \
  cmsRun "${label}"/hlt_"${label}".py &> "${label}"/hlt_"${label}".log || true

done
unset file_i fff label
