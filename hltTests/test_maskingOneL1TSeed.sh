#!/bin/bash

hltGetConfiguration /dev/CMSSW_14_0_0/GRun \
   --globaltag 140X_dataRun3_HLT_v3 \
   --data \
   --unprescale \
   --output minimal \
   --max-events 200 \
   --input /store/data/Run2024E/EphemeralHLTPhysics0/RAW/v1/000/381/150/00000/54c756e0-542f-409d-ab60-7ef416273792.root \
   --paths MC_AK4PFJets_v27 \
   > hlt.py

cat <<@EOF >> hlt.py
process.hltPreMCAK4PFJets = cms.EDFilter( "TriggerResultsFilter",
    usePathStatus = cms.bool( False ),
    hltResults = cms.InputTag( "" ),
    l1tResults = cms.InputTag( "hltGtStage2Digis" ),
    l1tIgnoreMaskAndPrescale = cms.bool( False ),
    throw = cms.bool( True ),
    triggerConditions = cms.vstring( 'L1_* MASKING L1_SingleMu10_SQ14_BMTF MASKING L1_SingleMu11_SQ14_BMTF' )
)

process.hltOutputMinimal = cms.OutputModule( "PoolOutputModule",
    fileName = cms.untracked.string( "output.root" ),
    fastCloning = cms.untracked.bool( False ),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string( 'RAW' ),
        filterName = cms.untracked.string( '' )
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring( 'MC_AK4PFJets_v27' )
    ),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_hltParticleFlow_*_*',
    )
)

del process.hltAK4PFJetCollection20Filter
@EOF

cmsRun hlt.py &> hlt.log
