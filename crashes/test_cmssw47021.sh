#!/bin/bash

# cmsrel CMSSW_15_0_0_pre1
# cd CMSSW_15_0_0_pre1/src
# cmsenv

hltLabel=hlt
hltMenu=/dev/CMSSW_14_2_0/HIon/V11
globalTag=141X_dataRun3_HLT_v2

hltGetConfiguration \
  "${hltMenu}" \
  --globaltag "${globalTag}" \
  --data \
  --no-prescale \
  --no-output \
  --max-events 1 \
  --input root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run388769/run388769_ls0254_index000051_fu-c2b05-16-01_pid4080142.root \
  --path HLT_HIUPC_ZDC1nOR_MBHF1AND_PixelTrackMultiplicity40400_v* \
  > "${hltLabel}".py

cat <<@EOF >> "${hltLabel}".py
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

process.options.accelerators = ['*']

del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')

process.source.skipEvents = cms.untracked.uint32( 64 )
@EOF

CUDA_LAUNCH_BLOCKING=1 \
cmsRun "${hltLabel}".py &> "${hltLabel}".log
