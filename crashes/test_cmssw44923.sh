#!/bin/bash

https_proxy=http://cmsproxy.cms:3128/ \
hltGetConfiguration run:384187 \
  --globaltag 140X_dataRun3_HLT_v3 \
  --no-prescale \
  --no-output \
  --max-events 100 \
  --paths DQM_Pixel* \
  --input root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run383669/run383669_ls0482_index000395_fu-c2b14-17-01_pid137066.root \
  > hlt.py

cat <<@EOF >> hlt.py
process.options.numberOfThreads = 32
process.options.numberOfStreams = 24

#process.source.skipEvents = cms.untracked.uint32( 56 )

del process.MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
@EOF

compute-sanitizer --tool=racecheck --racecheck-report=all \
cmsRun hlt.py &> hlt.log
