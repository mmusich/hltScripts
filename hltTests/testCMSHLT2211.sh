#!/bin/bash -ex

BASECMD="hltGetConfiguration --dbproxy /users/missirol/test/dev/CMSSW_12_3_0/CMSHLT_2211/Reference2/HLT"
BASECMD+=" --globaltag auto:phase1_2021_realistic --mc --unprescale --eras Run3 --output none --max-events 100"

BASECFGNAME=testCMSHLT2211

function hltJob(){
  ${BASECMD} --paths HLTriggerFirstPath,HLTriggerFinalPath,HLTAnalyzerEndpath,"${2}"_v* --input "${1}" > "${BASECFGNAME}"_"${2}".py
  cmsRun "${BASECFGNAME}"_"${2}".py &> "${BASECFGNAME}"_"${2}".log
}

INPUTFILE01=/store/mc/Run3Summer21DRPremix/HTo2LongLivedTo4b_MH-1000_MFF-450_CTau-100000mm_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/120X_mcRun3_2021_realistic_v6-v2/2550000/c00b73f9-8906-466e-9123-3a842ac80ccd.root
INPUTFILE02=/store/mc/Run3Summer21DRPremix/DisplacedMuons_Pt-10to30_Dxy0to3000-gun/GEN-SIM-DIGI-RAW/120X_mcRun3_2021_realistic_v6-v2/80000/1781d40d-0bb9-4999-b4cd-fa0d15e9b769.root
INPUTFILE03=/store/mc/Run3Summer21DRPremix/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/120X_mcRun3_2021_realistic_v6-v2/2540000/b354245e-d8bc-424d-b527-58815586a6a5.root

#hltJob "${INPUTFILE01}" HLT_L1MET_DTCluster50
#hltJob "${INPUTFILE01}" HLT_L1MET_DTClusterNoMB1S50
#hltJob "${INPUTFILE01}" HLT_CaloMET60_DTCluster50
#hltJob "${INPUTFILE01}" HLT_CaloMET60_DTClusterNoMB1S50
#hltJob "${INPUTFILE01}" HLT_L1CSCShower_DTCluster50
#hltJob "${INPUTFILE01}" HLT_L1CSCShower_DTCluster75
#hltJob "${INPUTFILE01}" HLT_CscCluster_Loose
#hltJob "${INPUTFILE01}" HLT_CscCluster_Medium
#hltJob "${INPUTFILE01}" HLT_CscCluster_Tight
#hltJob "${INPUTFILE03}" HLT_Mu20NoFiltersNoVtxDisplaced_Photon20_CaloCustomId
#hltJob "${INPUTFILE01}" HLT_L1Mu6HT240
#hltJob "${INPUTFILE01}" HLT_HT430_DisplacedDijet30_Inclusive1PtrkShortSig5
#hltJob "${INPUTFILE01}" HLT_HT430_DisplacedDijet35_Inclusive1PtrkShortSig5
#hltJob "${INPUTFILE01}" HLT_HT430_DisplacedDijet40_Inclusive1PtrkShortSig5
#hltJob "${INPUTFILE01}" HLT_Mu6HT240_DisplacedDijet30_Inclusive0PtrkShortSig5
#hltJob "${INPUTFILE01}" HLT_Mu6HT240_DisplacedDijet30_Inclusive1PtrkShortSig5_DisplacedLoose
#hltJob "${INPUTFILE01}" HLT_Mu6HT240_DisplacedDijet35_Inclusive0PtrkShortSig5 
#hltJob "${INPUTFILE01}" HLT_Mu6HT240_DisplacedDijet35_Inclusive1PtrkShortSig5_DisplacedLoose
#hltJob "${INPUTFILE01}" HLT_Mu6HT240_DisplacedDijet40_Inclusive0PtrkShortSig5
#hltJob "${INPUTFILE01}" HLT_Mu6HT240_DisplacedDijet40_Inclusive1PtrkShortSig5_DisplacedLoose
#hltJob "${INPUTFILE02}" HLT_DoubleL2Mu23NoVtx_2Cha
#hltJob "${INPUTFILE02}" HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed
#hltJob "${INPUTFILE02}" HLT_DoubleL2Mu10NoVtx_2Cha_PromptL3Mu0Veto
#hltJob "${INPUTFILE02}" HLT_DoubleL3Mu10NoVtx_Displaced
#hltJob "${INPUTFILE01}" HLT_HT430_DelayedJet40_DoubleDelay0p5nsTrackless
#hltJob "${INPUTFILE01}" HLT_HT430_DelayedJet40_SingleDelay1nsTrackless
#hltJob "${INPUTFILE01}" HLT_HT430_DelayedJet40_DoubleDelay1nsTrackless
#hltJob "${INPUTFILE01}" HLT_HT430_DelayedJet40_SingleDelay2nsTrackless
#hltJob "${INPUTFILE03}" HLT_PFMET105_IsoTrk50
#hltJob "${INPUTFILE03}" HLT_PFMET110_PFJet100
#hltJob "${INPUTFILE03}" HLT_MET105_IsoTrk50
hltJob "${INPUTFILE01}" HLT_PFMET110_PFJet100_looseRecoiling
hltJob "${INPUTFILE01}" HLT_DoubleMediumChargedIsoDisplacedPFTauHPS32_Trk1_eta2p1
