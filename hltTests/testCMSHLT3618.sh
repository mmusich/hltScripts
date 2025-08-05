#!/bin/bash -ex

hltLabel=testCMSHLT3618
hltLabel1="${hltLabel}"_hlt1
hltLabel2="${hltLabel}"_hlt2

https_proxy=http://cmsproxy.cms:3128/ \
hltGetConfiguration /dev/CMSSW_15_0_0/GRun/V108 \
  --globaltag 150X_dataRun3_HLT_v1 \
  --data \
  --no-prescale \
  --output all \
  --max-events -1 \
  --input root://eoscms.cern.ch//eos/cms/store/data/Run2025D/EphemeralHLTPhysics0/RAW/v1/000/394/959/00000/e000826b-a109-464e-8829-2470d68d613f.root \
  > "${hltLabel1}".py

# hltLabel1
cat <<@EOF >> "${hltLabel1}".py

process.options.accelerators = ['cpu']

process.options.numberOfThreads = 32
process.options.numberOfStreams = 32

process.options.wantSummary = False

del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 500

del process.dqmOutput
streamPaths = [foo for foo in process.endpaths_() if foo.endswith('Output')]
streamPaths.remove('DQMOutput')
streamPaths.remove('HLTMonitorOutput')
for foo in streamPaths:
    process.__delattr__(foo)
@EOF

cp "${hltLabel1}".py "${hltLabel2}".py

cat <<@EOF >> "${hltLabel1}".py

process.hltOutputDQM.fileName = "${hltLabel1}_DQM.root"
process.hltOutputHLTMonitor.fileName = "${hltLabel1}_HLTMonitor.root"
@EOF

cmsRun "${hltLabel1}".py 2>&1 | tee "${hltLabel1}".log

# hltLabel2
cat <<@EOF >> "${hltLabel2}".py

process.hltOutputDQM.fileName = "${hltLabel2}_DQM.root"
process.hltOutputHLTMonitor.fileName = "${hltLabel2}_HLTMonitor.root"
process.hltOutputDQM.outputCommands += ["keep *_hltPFMuonMerging_*_*"]
process.hltOutputHLTMonitor.outputCommands += ["keep *_hltTrimmedPixelVertices_*_*"]
@EOF

cmsRun "${hltLabel2}".py 2>&1 | tee "${hltLabel2}".log
