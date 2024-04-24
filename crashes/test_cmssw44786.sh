#!/bin/bash

jobLabel=test_cmssw44786

runNumber=379617 # Alpaka
#runNumber=379660 # CUDA

if [ ! -f "${jobLabel}"_cfg.py ]; then

  https_proxy=http://cmsproxy.cms:3128/ \
  hltGetConfiguration run:"${runNumber}" \
    --globaltag 140X_dataRun3_HLT_v3 \
    --data \
    --no-prescale \
    --no-output \
    --paths AlCa_PFJet40_v* \
    --max-events 1 \
    --input root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/debug/240417_run379617/run379617_ls0329_index000242_fu-c2b02-12-01_pid3327112.root \
    > "${jobLabel}"_cfg.py

  cat <<@EOF >> "${jobLabel}"_cfg.py

del process.hltL1sZeroBias

if hasattr(process, 'HLTAnalyzerEndpath'):
    del process.HLTAnalyzerEndpath

try:
    del process.MessageLogger
    process.load('FWCore.MessageLogger.MessageLogger_cfi')
    process.MessageLogger.cerr.enableStatistics = False
except:
    pass

process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

process.source.skipEvents = cms.untracked.uint32( 86 )

process.options.accelerators = ['cpu']
#process.options.accelerators = ['gpu-nvidia']
process.options.wantSummary = False
@EOF
fi

CUDA_LAUNCH_BLOCKING=1 \
cmsRun "${jobLabel}"_cfg.py &> "${jobLabel}".log
