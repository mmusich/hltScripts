#!/bin/bash

jobLabel=test_run380115

runNumber=380115

if [ ! -f "${jobLabel}"_cfg.py ]; then

  https_proxy=http://cmsproxy.cms:3128/ \
  hltGetConfiguration run:"${runNumber}" \
    --globaltag 140X_dataRun3_HLT_v3 \
    --data \
    --no-prescale \
    --no-output \
    --max-events -1 \
    --input \
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run380115/run380115_ls0338_index000079_fu-c2b03-28-01_pid1451372.root,\
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run380115/run380115_ls0338_index000104_fu-c2b03-28-01_pid1451372.root \
    > "${jobLabel}"_cfg.py

  cat <<@EOF >> "${jobLabel}"_cfg.py

#if hasattr(process, 'HLTAnalyzerEndpath'):
#    del process.HLTAnalyzerEndpath

try:
    del process.MessageLogger
    process.load('FWCore.MessageLogger.MessageLogger_cfi')
    process.MessageLogger.cerr.enableStatistics = False
except:
    pass

#process.options.numberOfThreads = 1
#process.options.numberOfStreams = 0

#process.source.skipEvents = cms.untracked.uint32( 86 )

#process.options.accelerators = ['cpu']
#process.options.accelerators = ['gpu-nvidia']
process.options.wantSummary = False
@EOF
fi

CUDA_LAUNCH_BLOCKING=1 \
cmsRun "${jobLabel}"_cfg.py &> "${jobLabel}".log
