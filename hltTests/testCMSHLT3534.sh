#!/bin/bash -ex

maxEvents=-1
skipEvents=0

run(){

  https_proxy=http://cmsproxy.cms:3128/ \
  hltGetConfiguration "${2}" \
   --globaltag 142X_mcRun3_2025_realistic_v7 \
   --mc \
   --no-prescale \
   --output minimal \
   --max-events "${maxEvents}" \
   --input \
/store/mc/Run3Winter25Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/142X_mcRun3_2025_realistic_v7-v2/130000/f180085b-343d-4d33-9bda-e859a0c8d4dd.root,\
/store/mc/Run3Winter25Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/142X_mcRun3_2025_realistic_v7-v2/130000/fee54b2e-e89c-4321-b2b3-e435a2c4ba79.root,\
/store/mc/Run3Winter25Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/142X_mcRun3_2025_realistic_v7-v2/130000/ffa44d93-e86c-46ba-94d7-2b60b2b05b2f.root,\
/store/mc/Run3Winter25Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/142X_mcRun3_2025_realistic_v7-v2/130000/ffa7eed1-0f84-4624-b881-0e6c904e487f.root,\
/store/mc/Run3Winter25Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/142X_mcRun3_2025_realistic_v7-v2/130000/ffee558e-eea1-4898-9839-1e7ffe6b0fa1.root \
   --eras Run3_2025 --l1-emulator uGT --l1 L1Menu_Collisions2025_v1_3_0_xml \
   --paths "AlCa_PFJet40_*","HLT_DoubleMu3_TkMu_DsTau3Mu_v*","HLT_DisplacedMu24_MediumChargedIsoDisplacedPFTauHPS24_v*" \
   > "${1}".py

  cat <<@EOF >> "${1}".py

process.source.skipEvents = cms.untracked.uint32( ${skipEvents} )

del process.dqmOutput

process.options.accelerators = ['cpu']

process.options.numberOfThreads = 1
process.options.numberOfStreams = 1

process.hltSiStripRawToClustersFacility.onDemand = False

process.hltOutputMinimal.fileName = "${1}.root"
process.hltOutputMinimal.outputCommands += [
    "keep *_hltSiStripRawToClustersFacility*_*_*",
    "keep *_hltMergedTracks_*_*",
    "keep *_hltMergedTracksSerialSync_*_*",
    "keep *_hltIterL3MuonTracks_*_*",
    "keep *_hltIterL3MuonTracksSerialSync_*_*",
    "keep *_hltIterL3MuonAndMuonFromL1Merged_*_*",
    "keep *_hltIter4MergedWithIter0ForTau_*_*",
    "keep *_hltPFMuonMerging_*_*",
    "keep *_hltPFMuonMergingSerialSync_*_*",
    "keep *_hltDiMuonMergingIter01TkMu_*_*",
    "keep *_hltPFMuonMergingForDisplTau_*_*",
]
@EOF

  cmsRun "${1}".py &> "${1}".log
}

run testCMSHLT3534_hlt1 /dev/CMSSW_15_0_0/GRun/V110
run testCMSHLT3534_hlt2 /users/missirol/test/dev/CMSSW_15_0_0/CMSHLT_3534/Test31/GRun/V3
