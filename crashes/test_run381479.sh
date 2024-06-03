#!/bin/bash

hltGetConfiguration run:381479 \
  --globaltag 140X_dataRun3_HLT_v3 \
  --no-prescale \
  --no-output \
  --max-events -1 \
  --input \
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run381479/run381479_ls0229_index000391_fu-c2b01-19-01_pid1861586.root,\
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run381479/run381479_ls0229_index000427_fu-c2b01-19-01_pid1861586.root \
  > hlt.py

cat <<@EOF >> hlt.py
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

#process.source.skipEvents = cms.untracked.uint32( 56 )

del process.MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
@EOF

cmsRun hlt.py &> hlt.log
