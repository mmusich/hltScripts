#!/bin/bash

outTag=PostPR_TestGEM

for l1tEmu in Full FullMC Full2015Data uGT; do
  cfgBaseName=hlt_l1tEmu"${l1tEmu}"

  if [ ! -f "${cfgBaseName}"_DATA.py ]; then
    hltGetConfiguration /dev/CMSSW_12_2_0/GRun --dbproxy \
     --input /store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/2E066536-5CF2-B340-A73B-209640F29FF6.root \
     --data --globaltag auto:run3_hlt --unprescale --customise HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input \
     --l1-emulator "${l1tEmu}" --dbproxy > "${cfgBaseName}"_DATA.py
  fi

  if [ ! -f "${cfgBaseName}"_MC.py ]; then
    hltGetConfiguration /dev/CMSSW_12_2_0/GRun --dbproxy \
     --input /store/relval/CMSSW_12_2_0_pre2/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/122X_mcRun3_2021_realistic_v1-v1/2580000/5541adab-cc2d-4401-b069-8140c90078c8.root \
     --mc --globaltag auto:run3_mc_GRun --unprescale \
     --l1-emulator "${l1tEmu}" --dbproxy > "${cfgBaseName}"_MC.py
  fi

  (edmConfigDump "${cfgBaseName}"_DATA.py | grep -v 'L1T WARN: ') > "${cfgBaseName}"_DATA_dump_"${outTag}".py
  (edmConfigDump --prune "${cfgBaseName}"_DATA.py | grep -v 'L1T WARN: ') > "${cfgBaseName}"_DATA_dumpPruned_"${outTag}".py

  (edmConfigDump "${cfgBaseName}"_MC.py | grep -v 'L1T WARN: ') > "${cfgBaseName}"_MC_dump_"${outTag}".py
  (edmConfigDump --prune "${cfgBaseName}"_MC.py | grep -v 'L1T WARN: ') > "${cfgBaseName}"_MC_dumpPruned_"${outTag}".py
done
unset l1tEmu
