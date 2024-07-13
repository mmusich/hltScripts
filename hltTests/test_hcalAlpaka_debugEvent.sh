#!/bin/bash

[ $# -ge 1 ] || exit 1

hltLabel="${1}"

#inputFile=root://eoscms.cern.ch//eos/cms/store/data/Run2024F/EphemeralHLTPhysics0/RAW/v1/000/382/250/00000/01c65bda-8c01-4e3d-9f66-72f705e4e8e9.root
inputFile=root://eoscms.cern.ch//eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check01/pickEvents_EphemeralHLTPhysics_run381065_RAW_cmssw44910.root

#hltPath=HLT_PFHT250_QuadPFJet25_v
hltPath=HLT_SingleEle8_v

https_proxy=http://cmsproxy.cms:3128/ \
hltGetConfiguration /dev/CMSSW_14_0_0/GRun/V153 \
  --globaltag 140X_dataRun3_HLT_v3 \
  --data \
  --no-prescale \
  --output minimal \
  --max-events -1 \
  --paths ${hltPath}*,AlCa_PFJet40_*,HLT_UncorrectedJetE30_NoBPTX_v* \
  --input "${inputFile}" \
  > "${hltLabel}"_Legacy.py

cat <<@EOF >> "${hltLabel}"_Legacy.py
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
process.options.wantSummary = True

for foo in ['HLTAnalyzerEndpath', 'dqmOutput', 'MessageLogger']:
    if hasattr(process, foo):
        process.__delattr__(foo)

process.load('FWCore.MessageLogger.MessageLogger_cfi')

#process.source.eventsToProcess = cms.untracked.VEventRange("382250:194:216051612")

process.options.accelerators = ['cpu']

process.hltOutputMinimal.outputCommands = [
   'drop *',
   'keep *_TriggerResults_*_*',
#   'keep *_hltHcalDigis_*_*',
   'keep *_hltHbhereco_*_*',
#   'keep *_hltAK4PFJets_*_*',
#   'keep *_hltAK4PFJetsCorrected_*_*',
#   'keep *_hltCaloTower*_*_*',
#   'keep *_hltParticleFlow_*_*',
#   'keep *_hltFixedGrid*_*_*',
#   'keep *_hltParticleFlowCluster*_*_*',
#   'keep *_hltEgammaCandidates_*_*',
#   'keep *_hltEgammaGsfTracks_*_*',
#   'keep *_hltPFHTJet25_*_*',
]
@EOF
cmsRun "${hltLabel}"_Legacy.py &> "${hltLabel}"_Legacy.log
mv output.root "${hltLabel}"_Legacy.root

cat <<@EOF > "${hltLabel}"_AlpakaSerialSync.py
from ${hltLabel}_Legacy import cms, process

from HLTrigger.Configuration.customizeHLTforAlpaka import customizeHLTforAlpaka
process = customizeHLTforAlpaka(process)
@EOF
cmsRun "${hltLabel}"_AlpakaSerialSync.py &> "${hltLabel}"_AlpakaSerialSync.log
mv output.root "${hltLabel}"_AlpakaSerialSync.root

cat <<@EOF > "${hltLabel}"_AlpakaGPU.py
from ${hltLabel}_Legacy import cms, process

from HLTrigger.Configuration.customizeHLTforAlpaka import customizeHLTforAlpaka
process = customizeHLTforAlpaka(process)

process.options.accelerators = ['*']
@EOF
cmsRun "${hltLabel}"_AlpakaGPU.py &> "${hltLabel}"_AlpakaGPU.log
mv output.root "${hltLabel}"_AlpakaGPU.root

cat <<@EOF > "${hltLabel}"_CUDA.py
from ${hltLabel}_Legacy import cms, process

process.options.accelerators = ['*']
@EOF
cmsRun "${hltLabel}"_CUDA.py &> "${hltLabel}"_CUDA.log
mv output.root "${hltLabel}"_CUDA.root
