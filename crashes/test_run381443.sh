#!/bin/bash

hltGetConfiguration run:381443 \
  --globaltag 140X_dataRun3_HLT_v3 \
  --no-prescale \
  --no-output \
  --max-events -1 \
  --input \
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run381443/run381443_ls0984_index000038_fu-c2b03-20-01_pid245753.root,\
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run381443/run381443_ls0984_index000072_fu-c2b03-20-01_pid245753.root\
  > hlt.py

cat <<@EOF >> hlt.py
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

#process.source.skipEvents = cms.untracked.uint32( 56 )

del process.MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
@EOF

cmsRun hlt.py &> hlt.log
