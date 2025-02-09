#!/bin/bash

hltLabel=hlt
hltMenu=run:388769
globalTag=141X_dataRun3_HLT_v2

hltGetConfiguration \
  "${hltMenu}" \
  --globaltag "${globalTag}" \
  --data \
  --no-prescale \
  --no-output \
  --max-events 1 \
  --input root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run388769/run388769_ls0186_index000175_fu-c2b03-06-01_pid4137691.root \
  --path HLT_HIUPC_DoubleEG5_BptxAND_SinglePixelTrack_MaxPixelTrack_v* \
  > "${hltLabel}".py

cat <<@EOF >> "${hltLabel}".py
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')

process.source.skipEvents = cms.untracked.uint32( 90 )
@EOF

cmsRun "${hltLabel}".py &> "${hltLabel}".log
