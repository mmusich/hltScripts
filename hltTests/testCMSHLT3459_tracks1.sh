#!/bin/bash

for hltVer in 4; do

  hltLabel=hlt"${hltVer}"
  hltGetConfiguration \
    /users/missirol/test/dev/CMSSW_15_0_0/CMSHLT_3459/Test04/GRun/V"${hltVer}" \
    --globaltag 142X_mcRun3_2025_realistic_v7 \
    --mc \
    --unprescale \
    --output minimal \
    --max-events 300 \
    --input /store/mc/Run3Winter25Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/142X_mcRun3_2025_realistic_v7-v2/130000/f180085b-343d-4d33-9bda-e859a0c8d4dd.root \
    --paths MC*Tracking* \
    --eras Run3_2025 --l1-emulator uGT --l1 L1Menu_Collisions2025_v1_0_0_xml \
    > "${hltLabel}".py

  cat <<@EOF >> "${hltLabel}".py
process.options.numberOfThreads = 1
process.hltOutputMinimal.outputCommands += ['keep recoTracks_*_*_HLTX']
process.hltOutputMinimal.fileName = '${hltLabel}.root'
@EOF

  cmsRun "${hltLabel}".py &> "${hltLabel}".log

  unset hltLabel
done
unset hltVer
