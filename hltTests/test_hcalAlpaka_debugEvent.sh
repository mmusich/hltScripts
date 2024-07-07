#!/bin/bash

https_proxy=http://cmsproxy.cms:3128/ \
hltGetConfiguration /dev/CMSSW_14_0_0/GRun/V153 \
  --globaltag 140X_dataRun3_HLT_v3 \
  --data \
  --no-prescale \
  --output minimal \
  --max-events 1 \
  --paths HLT_PFHT250_QuadPFJet25_v*,AlCa*CPUOnly*,HLT_UncorrectedJetE30_NoBPTX_v* \
  --input root://eoscms.cern.ch//eos/cms/store/data/Run2024F/EphemeralHLTPhysics0/RAW/v1/000/382/250/00000/01c65bda-8c01-4e3d-9f66-72f705e4e8e9.root \
  > hlt_Legacy.py

cat <<@EOF >> hlt_Legacy.py
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
process.options.wantSummary = True

for foo in ['HLTAnalyzerEndpath', 'dqmOutput', 'MessageLogger']:
    if hasattr(process, foo):
        process.__delattr__(foo)

process.load('FWCore.MessageLogger.MessageLogger_cfi')

process.source.eventsToProcess = cms.untracked.VEventRange("382250:194:216051612")

process.options.accelerators = ['cpu']

process.hltOutputMinimal.outputCommands = [
   'drop *',
   'keep *_hltHcalDigis_*_*',
   'keep *_hltHbhereco_*_*',
   'keep *_hltAK4PFJets_*_*',
   'keep *_hltAK4PFJetsCorrected_*_*',
   'keep *_hltCaloTower*_*_*',
   'keep *_hltParticleFlow_*_*',
   'keep *_hltFixedGrid*_*_*',
   'keep *_hltPFHTJet25_*_*',
]
@EOF
cmsRun hlt_Legacy.py &> hlt_Legacy.log
mv output.root hlt_Legacy.root

cat <<@EOF > hlt_AlpakaSerialSync.py
from hlt_Legacy import cms, process

from HLTrigger.Configuration.customizeHLTforAlpaka import customizeHLTforAlpaka
process = customizeHLTforAlpaka(process)
@EOF
cmsRun hlt_AlpakaSerialSync.py &> hlt_AlpakaSerialSync.log
mv output.root hlt_AlpakaSerialSync.root

cat <<@EOF > hlt_AlpakaGPU.py
from hlt_Legacy import cms, process

from HLTrigger.Configuration.customizeHLTforAlpaka import customizeHLTforAlpaka
process = customizeHLTforAlpaka(process)

process.options.accelerators = ['*']
@EOF
cmsRun hlt_AlpakaGPU.py &> hlt_AlpakaGPU.log
mv output.root hlt_AlpakaGPU.root

cat <<@EOF > hlt_CUDA.py
from hlt_Legacy import cms, process

process.options.accelerators = ['*']
@EOF
cmsRun hlt_CUDA.py &> hlt_CUDA.log
mv output.root hlt_CUDA.root
