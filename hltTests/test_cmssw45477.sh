#!/bin/bash

runNumber=383219

jobLabel=test_run"${runNumber}"

inputFilesStr=""
delim=""
for foo in $(ls /eos/cms/store/group/tsg/FOG/error_stream_root/run383219/*); do
  inputFilesStr+="${delim}root://eoscms.cern.ch/${foo}"
  delim=","
done
unset delim

#https_proxy=http://cmsproxy.cms:3128/ \
hltGetConfiguration run:"${runNumber}" \
  --globaltag 140X_dataRun3_HLT_v3 \
  --data \
  --no-prescale \
  --no-output \
  --max-events -1 \
  --paths "DQM_Hcal*,HLT_Random_*" \
  --input "${inputFilesStr}" \
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

process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

#process.source.skipEvents = cms.untracked.uint32( 86 )

del process.hltTriggerType
del process.hltL1sDQMHcalReconstruction

#process.options.accelerators = ['cpu']
#process.options.accelerators = ['gpu-nvidia']
process.options.wantSummary = True
@EOF

CUDA_LAUNCH_BLOCKING=1 \
cmsRun "${jobLabel}"_cfg.py &> "${jobLabel}".log
