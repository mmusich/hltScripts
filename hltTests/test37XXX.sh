#!/bin/bash

#if [ ! -f hlt_cfg.py ]; then

  hltGetConfiguration /dev/CMSSW_12_3_0/GRun --dbproxy \
    --globaltag auto:phase1_2021_realistic \
    --mc \
    --unprescale \
    --eras Run3 \
    --input /store/mc/Run3Summer21DRPremix/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/120X_mcRun3_2021_realistic_v6-v2/2540000/b354245e-d8bc-424d-b527-58815586a6a5.root \
    --output minimal \
    --max-events 100 \
   > hlt_cfg.py

  echo -e "\nprocess.options.numberOfThreads = 1" >> hlt_cfg.py
#fi

#if [ ! -f hlt_cfgDump.py ]; then
  edmConfigDump hlt_cfg.py > hlt_cfgDump.py
#fi

cmsRun hlt_cfgDump.py &> hlt_cfgDump.log
