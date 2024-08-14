#!/bin/bash

[ $# -ge 1 ] || exit 1

hltLabel=hlt
outDir="${1}"

[ ! -d "${outDir}" ] || exit 1

mkdir -p "${outDir}"
cd "${outDir}"

inputFile=root://eoscms.cern.ch//eos/cms/store/group/tsg/STEAM/validations/GPUVsCPU/240814/raw_pickevents.root

hltPath=HLT_PFMET120_PFMHT120_IDTight_v

https_proxy=http://cmsproxy.cms:3128/ \
hltGetConfiguration /dev/CMSSW_14_0_0/GRun/V173 \
  --globaltag 140X_dataRun3_HLT_v3 \
  --data \
  --no-prescale \
  --output minimal \
  --max-events -1 \
  --paths ${hltPath}* \
  --input "${inputFile}" \
  > "${hltLabel}"_AlpakaSerialSync.py

cat <<@EOF >> "${hltLabel}"_AlpakaSerialSync.py
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
process.options.wantSummary = True

#process.source.skipEvents = cms.untracked.uint32(4)

for foo in ['HLTAnalyzerEndpath', 'dqmOutput', 'MessageLogger']:
    if hasattr(process, foo):
        process.__delattr__(foo)

process.load('FWCore.MessageLogger.MessageLogger_cfi')

process.source.eventsToProcess = cms.untracked.VEventRange(
    '381065:341:637243639',
    '381065:317:581313290',
)

process.options.accelerators = ['cpu']

process.hltOutputMinimal.outputCommands = [
   'drop *',
   'keep *_TriggerResults_*_*',
#   'keep *_hltHcalDigis_*_*',
   'keep *_hltHbhereco_*_*',
   'keep *_hltSiPixelRecHits_*_*',
   'keep *_hltPixelTracks_*_*',
   'keep *_hltPixelVertices_*_*',
#   'keep *_hltAK4PFJets_*_*',
#   'keep *_hltAK4PFJetsCorrected_*_*',
#   'keep *_hltCaloTower*_*_*',
#   'keep *_hltParticleFlow_*_*',
#   'keep *_hltFixedGrid*_*_*',
#   'keep *_hltParticleFlowCluster*_*_*',
   'keep *_hltEgammaCandidates_*_*',
   'keep *_hltEgammaGsfTracks_*_*',
   'keep *_hltEgammaGsfTrackVars_*_*',
#   'keep *_hltPFHTJet25_*_*',
]
@EOF
cmsRun "${hltLabel}"_AlpakaSerialSync.py &> "${hltLabel}"_AlpakaSerialSync.log
mv output.root "${hltLabel}"_AlpakaSerialSync.root

cat <<@EOF > "${hltLabel}"_AlpakaGPU.py
from ${hltLabel}_AlpakaSerialSync import cms, process

process.options.accelerators = ['*']

process.hltEcalDigisSoA.alpaka.backend = 'serial_sync'
process.hltEcalUncalibRecHitSoA.alpaka.backend = 'serial_sync'
#process.hltHbheRecoSoA.alpaka.backend = 'serial_sync'
process.hltParticleFlowRecHitHBHESoA.alpaka.backend = 'serial_sync'
process.hltParticleFlowClusterHBHESoA.alpaka.backend = 'serial_sync'
process.hltOnlineBeamSpotDevice.alpaka.backend = 'serial_sync'
process.hltSiPixelClustersSoA.alpaka.backend = 'serial_sync'
process.hltSiPixelRecHitsSoA.alpaka.backend = 'serial_sync'
process.hltPixelTracksSoA.alpaka.backend = 'serial_sync'
process.hltPixelVerticesSoA.alpaka.backend = 'serial_sync'
@EOF
cmsRun "${hltLabel}"_AlpakaGPU.py &> "${hltLabel}"_AlpakaGPU.log
mv output.root "${hltLabel}"_AlpakaGPU.root
