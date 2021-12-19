#!/bin/bash

if [ ! -f hlt_cfg.py ]; then

  hltGetConfiguration /dev/CMSSW_12_3_0/GRun --dbproxy \
    --globaltag auto:phase1_2021_realistic \
    --mc \
    --unprescale \
    --eras Run3 \
    --input /store/mc/Run3Summer21DRPremix/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/120X_mcRun3_2021_realistic_v6-v2/2540000/b354245e-d8bc-424d-b527-58815586a6a5.root \
    --output minimal \
    --max-events 2 \
   > hlt_cfg.py

  cat <<EOF >> hlt_cfg.py
process.hltBTagPFDeepCSV4p06Single = cms.EDFilter("HLTSumPFJetTag",
    saveTags = cms.bool(True),
    TriggerType = cms.int32(86),
    Jets = cms.InputTag("hltPFJetForBtag"),
    JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
    MaxTag = cms.double(999999.0),
    MinJetToSum = cms.int32( 1 ),
    MaxJetToSum = cms.int32( 2 ),
    MinTag = cms.double(0.3),
    UseMeanValue = cms.bool(True),
#    MatchByDeltaR = cms.bool(False),
#    MaxDeltaR = cms.double(0.3),
)

process.hltPFJetForBtagCopy = process.hltPFJetForBtag.clone()

process.hltBTagPFDeepCSV4p06SingleDoubleCopy = process.hltBTagPFDeepCSV4p06Single.clone(
    Jets = 'hltPFJetForBtagCopy',
)

theIndex = process.MC_PFBTagDeepCSV_v10.index(process.hltBTagPFDeepCSV4p06Single)
process.MC_PFBTagDeepCSV_v10.insert(theIndex+1, process.hltBTagPFDeepCSV4p06SingleDoubleCopy)
process.MC_PFBTagDeepCSV_v10.insert(theIndex+1, process.hltPFJetForBtagCopy)
EOF
fi

if [ ! -f hlt_cfgDump.py ]; then
  edmConfigDump hlt_cfg.py > hlt_cfgDump.py
fi

cmsRun hlt_cfgDump.py &> hlt_cfgDump.log
