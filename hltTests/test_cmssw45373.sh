#!/bin/bash

# cmsrel CMSSW_14_0_11_MULTIARCHS
# cd CMSSW_14_0_11_MULTIARCHS/src
# cmsenv
# git cms-init --ssh
# git cms-remote add stahlleiton --ssh
# git cms-addpkg HLTrigger/special
# git checkout stahlleiton/HLT_UPC_CMSSW_14_1_X HLTrigger/special/plugins/HLTPixelTrackFilter.cc
# scram b

hltGetConfiguration /dev/CMSSW_14_0_0/GRun/V153 \
  --globaltag 140X_dataRun3_HLT_v3 \
  --data \
  --unprescale \
  --output minimal \
  --max-events 100 \
  --input /store/data/Run2024F/EphemeralHLTPhysics0/RAW/v1/000/382/250/00000/755afa10-e31c-41ba-afcd-8ab567a6951b.root \
  --paths MC_AK4PFJets_v27,HLTriggerFinalPath \
  > hlt0.py

cat <<@EOF >> hlt0.py

process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

process.hltPixelTrackCands = cms.EDProducer( "ConcreteChargedCandidateProducer",
    src = cms.InputTag( "hltPixelTracks" ),
    particleType = cms.string( "pi+" )
)

process.hltOutputMinimal.outputCommands += [
    'keep trigger*_*_*_*',
]

process.hltPixelTrackCandsFilter = cms.EDFilter( "HLTPixelTrackFilter",
    saveTags = cms.bool( True ),
    pixelTracks = cms.InputTag( "hltPixelTrackCands" ),
    minPixelTracks = cms.uint32( 1 ),
    maxPixelTracks = cms.uint32( 9999999 ),
)

process.MC_AK4PFJets_v27.insert(-2, process.hltPixelTrackCands)
process.MC_AK4PFJets_v27.insert(-2, process.hltPixelTrackCandsFilter)

del process.hltAK4PFJetCollection20Filter
@EOF
cmsRun hlt0.py &> hlt0.log
mv output.root hlt0.root

cp hlt0.py hlt1.py
cat <<@EOF >> hlt1.py

process.hltPixelTrackCandsFilter.saveTags = False
@EOF
cmsRun hlt1.py &> hlt1.log
mv output.root hlt1.root

wget https://gist.githubusercontent.com/missirol/aed4d65ac12365fe27e72df3edc22193/raw/61d8aac29a02ce7cbbc8702c470de37df8db055f/hltFWLite_exa01.py -O printTriggerEvent.py
chmod u+x printTriggerEvent.py

./printTriggerEvent.py -v 10 -i hlt0.root > hlt0_triggerObjects.txt
./printTriggerEvent.py -v 10 -i hlt1.root > hlt1_triggerObjects.txt

edmEventSize -v hlt0.root > hlt0_eventSize.txt
edmEventSize -v hlt1.root > hlt1_eventSize.txt
