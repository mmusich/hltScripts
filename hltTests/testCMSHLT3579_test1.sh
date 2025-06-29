#!/bin/bash

hltIntegrationTests \
  /users/missirol/test/dev/CMSSW_15_0_0/CMSHLT_3579/Test01/LumiScan/V4 \
  -n 100 \
  --input /store/mc/Run3Winter25Digi/DYTo2L-2Jets_Par-MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/GEN-SIM-RAW/142X_mcRun3_2025_realistic_v7-v2/2540006/f71683dd-876e-47ef-ad46-1be5a3fd19b0.root \
  --mc \
  -x "--globaltag 142X_mcRun3_2025_realistic_v7" \
  -x "--eras Run3 --l1-emulator uGT --l1 L1Menu_Collisions2025_v1_2_0_xml" \
  -p "*Scouting*SingleMuon*","*Scouting*ZeroBias*" \
  -d output_hltIntegTests_CMSHLT3579 2>&1 | tee output_hltIntegTests_CMSHLT3579.txt
