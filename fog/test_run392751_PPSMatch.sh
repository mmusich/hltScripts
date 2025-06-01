#!/bin/bash

INPUTF=file:/eos/cms/store/group/tsg/FOG/debug/250531_run392751/run392751_ls0057_streamPhysicsJetMET0_StorageManager.dat
#INPUTF=file:/eos/cms/store/group/tsg/FOG/debug/250531_run392751/run392751_ls0079_streamPhysicsJetMET0_StorageManager.dat

hltGetConfiguration \
 run:392751 \
 --globaltag 150X_dataRun3_HLT_v1 \
 --no-output \
 --no-prescale \
 --max-events 1000 \
 --paths HLT_*PPSMatch*_v* \
 --input "${INPUTF}" \
 > hlt.py

cat <<@EOF >> hlt.py
process.source = cms.Source("NewEventStreamFileReader",
  fileNames = cms.untracked.vstring(process.source.fileNames)
)

process.hltL1sSingleJet170IorSingleJet180IorSingleJet200 = cms.EDFilter( "TriggerResultsFilter",
    usePathStatus = cms.bool( False ),
    hltResults = cms.InputTag( "TriggerResults::HLT" ),
    l1tResults = cms.InputTag( "" ),
    l1tIgnoreMaskAndPrescale = cms.bool( False ),
    throw = cms.bool( True ),
    triggerConditions = cms.vstring( 'HLT_DiPFJetAve180_PPSMatch_Xi0p3_QuadJet_Max2ProtPerRP_v*' )
)
@EOF

cmsRun hlt.py 2>&1 | tee hlt.log
