#!/bin/bash

hltGetConfiguration \
  /dev/CMSSW_15_0_0/GRun/V60 \
  --globaltag 142X_mcRun3_2025_realistic_v7 \
  --mc \
  --unprescale \
  --output minimal \
  --max-events 300 \
  --input /store/mc/Run3Winter25Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/142X_mcRun3_2025_realistic_v7-v2/130000/f180085b-343d-4d33-9bda-e859a0c8d4dd.root \
  --paths MC*Tracking* \
  --eras Run3_2025 --l1-emulator uGT --l1 L1Menu_Collisions2025_v1_0_0_xml \
  > hlt01.py

# hlt01
cat <<@EOF >> hlt01.py
process.options.numberOfThreads = 1
process.hltOutputMinimal.outputCommands += ['keep recoTracks_*_*_HLTX']
process.hltOutputMinimal.fileName = 'hlt01.root'

process.hltIter0PFlowCkfTrackCandidatesMkFit.minGoodStripCharge = cms.PSet(
    refToPSet_ = cms.string( "HLTSiStripClusterChargeCutNone" )
)
@EOF
cmsRun hlt01.py &> hlt01.log

# hlt02
cp hlt01.py hlt02.py
cat <<@EOF >> hlt02.py
process.hltOutputMinimal.fileName = 'hlt02.root'

process.hltIter0PFlowCkfTrackCandidatesMkFit.minGoodStripCharge = cms.PSet(
    refToPSet_ = cms.string( "HLTSiStripClusterChargeCutLoose" )
)
@EOF
cmsRun hlt02.py &> hlt02.log
