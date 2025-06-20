#!/bin/bash

hltGetConfiguration run:392524 \
  --globaltag 150X_dataRun3_HLT_v1 \
  --data \
  --no-prescale \
  --no-output \
  --max-events -1 \
  --input /store/group/tsg/FOG/debug/250525_run392524/run392524_ls0215_index000145.root \
  > hlt.py

cat <<@EOF >> hlt.py

process.options.wantSummary = True
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

process.source.skipEvents = cms.untracked.uint32(49)

del process.MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
@EOF
