#!/bin/bash

hltGetConfiguration /dev/CMSSW_14_0_0/HLT \
   --globaltag auto:phase1_2024_realistic \
   --mc \
   --no-prescale \
   --max-events 100 \
   --input /store/mc/Run3Winter24Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/133X_mcRun3_2024_realistic_v8-v2/80000/dc984f7f-2e54-48c4-8950-5daa848b6db9.root \
   --customise HLTrigger/Configuration/customizeHLTforAlpaka.customizeHLTforAlpaka \
   > tmp.py

edmConfigDump tmp.py > hlt_alpaka_test01.py
