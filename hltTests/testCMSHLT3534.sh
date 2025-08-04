#!/bin/bash -ex

run(){

  https_proxy=http://cmsproxy.cms:3128/ \
  hltGetConfiguration "${2}" \
   --globaltag 142X_mcRun3_2025_realistic_v7 \
   --mc \
   --no-prescale \
   --output minimal \
   --max-events 3000 \
   --input /store/mc/Run3Winter25Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/142X_mcRun3_2025_realistic_v7-v2/130000/f180085b-343d-4d33-9bda-e859a0c8d4dd.root \
   --eras Run3_2025 --l1-emulator uGT --l1 L1Menu_Collisions2025_v1_3_0_xml \
   --paths "AlCa_PFJet40_*","HLT_DoubleMu3_TkMu_DsTau3Mu_v*","HLT_DisplacedMu24_MediumChargedIsoDisplacedPFTauHPS24_v*" \
   > "${1}".py

  cat <<@EOF >> "${1}".py

process.options.numberOfThreads = 8
process.options.numberOfStreams = 8

process.hltOutputMinimal.fileName = "${1}.root"
process.hltOutputMinimal.outputCommands += [
    "keep *_hltPFMuonMerging_*_*",
    "keep *_hltPFMuonMergingSerialSync_*_*",
    "keep *_hltDiMuonMergingIter01TkMu_*_*",
    "keep *_hltPFMuonMergingForDisplTau_*_*",
]
@EOF

  cmsRun "${1}".py &> "${1}".log
}

run testCMSHLT3534_hlt1 /dev/CMSSW_15_0_0/GRun/V103
run testCMSHLT3534_hlt2 /users/missirol/test/dev/CMSSW_15_0_0/CMSHLT_3534/Test21/GRun/V3
