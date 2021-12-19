#!/bin/bash -ex

BASECMD="hltGetConfiguration --dbproxy /dev/CMSSW_12_3_0/HLT"
BASECMD+=" --globaltag auto:phase1_2021_realistic --mc --unprescale --eras Run3 --output minimal --max-events 100"
BASECMD+=" --l1-emulator FullMC --l1 L1Menu_Collisions2022_v1_0_0_xml"

BASECFGNAME=testCMSHLT2268

function hltJob(){
  ${BASECMD} --paths HLTriggerFirstPath,HLTriggerFinalPath,HLTAnalyzerEndpath,"${2}"_v* --input "${1}" > "${BASECFGNAME}"_"${2}".py
  cmsRun "${BASECFGNAME}"_"${2}".py &> "${BASECFGNAME}"_"${2}".log
}

INPUTFILE01=/store/mc/Run3Summer21DRPremix/HTo2LongLivedTo4b_MH-1000_MFF-450_CTau-100000mm_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/120X_mcRun3_2021_realistic_v6-v2/2550000/c00b73f9-8906-466e-9123-3a842ac80ccd.root
INPUTFILE02=/store/mc/Run3Summer21DRPremix/DisplacedMuons_Pt-10to30_Dxy0to3000-gun/GEN-SIM-DIGI-RAW/120X_mcRun3_2021_realistic_v6-v2/80000/1781d40d-0bb9-4999-b4cd-fa0d15e9b769.root
INPUTFILE03=/store/mc/Run3Summer21DRPremix/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/120X_mcRun3_2021_realistic_v6-v2/2540000/b354245e-d8bc-424d-b527-58815586a6a5.root

hltJob "${INPUTFILE03}" HLT_IsoMu24
