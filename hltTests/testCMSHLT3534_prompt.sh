#!/bin/bash -ex

#hltMenu=/dev/CMSSW_15_0_0/GRun/V103
hltMenu=/users/missirol/test/dev/CMSSW_15_0_0/CMSHLT_3534/Test21/GRun/V3

jobLabel=testCMSHLT3534
hltLabel="${jobLabel}"_hlt
promptLabel="${jobLabel}"_prompt

inputFile=root://eoscms.cern.ch//eos/cms/store/data/Run2025D/EGamma0/RAW/v1/000/394/959/00000/906d7971-ad62-4927-ad21-8c5691d5dfda.root
maxEvents=300

https_proxy=http://cmsproxy.cms:3128/ \
hltGetConfiguration "${hltMenu}" \
 --process HLTX \
 --globaltag 150X_dataRun3_HLT_v1 \
 --data \
 --no-prescale \
 --output all \
 --max-events "${maxEvents}" \
 --input "${inputFile}" \
 > "${hltLabel}".py

cat <<@EOF >> "${hltLabel}".py

process.options.numberOfThreads = 8
process.options.numberOfStreams = 8

streamPaths = [foo for foo in process.endpaths_() if foo.endswith('Output') and foo != 'HLTMonitorOutput']
for foo in streamPaths:
    process.__delattr__(foo)

process.hltOutputHLTMonitor.fileName = "${hltLabel}.root"

process.hltOutputHLTMonitor.outputCommands += [
#    "drop *_hltSiStripRawToClustersFacilityForMkFit_*_*",
]
@EOF

cmsRun "${hltLabel}".py &> "${hltLabel}".log

python3 Configuration/DataProcessing/test/RunPromptReco.py \
  --scenario=ppEra_Run3_2025 \
  --global-tag 150X_dataRun3_Express_v2 \
  --lfn=file:"${hltLabel}".root \
  --reco \
  --dqm \
  --dqmSeq=@HLTMon

#  --alcarecos=TkAlHLTTracks+TkAlHLTTracksZMuMu+PromptCalibProdSiPixelAliHLTHGC \

cat <<@EOF >> RunPromptRecoCfg.py

#process.pathALCARECOTkAlHLTTracks = cms.EndPath(process.seqALCARECOTkAlHLTTracks+process.ALCARECOTkAlHLTTracksDQM)
#process.pathALCARECOTkAlHLTTracksZMuMu = cms.EndPath(process.seqALCARECOTkAlHLTTracksZMuMu+process.ALCARECOTkAlHLTTracksZMuMuDQM)
#process.pathALCARECOPromptCalibProdSiPixelAliHLTHGMinBias = cms.EndPath(process.seqALCARECOPromptCalibProdSiPixelAliHLTHG)
#process.pathALCARECOPromptCalibProdSiPixelAliHLTHGDiMu = cms.EndPath(process.seqALCARECOPromptCalibProdSiPixelAliHLTHGDiMu)

process.options.wantSummary = True

alcaPaths = [foo for foo in process.paths_() if foo.startswith('pathALCARECO')]
for foo in alcaPaths:
    process.__delattr__(foo)
@EOF

edmConfigDump RunPromptRecoCfg.py > "${promptLabel}".py

sed -i 's|"TriggerResults","","HLT"|"TriggerResults","","HLTX"|g' "${promptLabel}".py

cmsRun "${promptLabel}".py &> "${promptLabel}".log
