#!/bin/bash

l1tEmu=Full
outBaseName=test2_MC_L1TEmu"${l1tEmu}"

hltGetConfiguration /dev/CMSSW_12_2_0/GRun --dbproxy \
 --input /store/relval/CMSSW_12_2_0_pre2/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/122X_mcRun3_2021_realistic_v1-v1/2580000/5541adab-cc2d-4401-b069-8140c90078c8.root \
 --mc --globaltag auto:run3_mc_GRun --unprescale --output none \
 --paths HLTriggerFirstPath,HLTriggerFinalPath \
 --l1-emulator "${l1tEmu}" --dbproxy > "${outBaseName}".py

(edmConfigDump         "${outBaseName}".py | grep -v 'L1T WARN: ') > "${outBaseName}"_dump.py
(edmConfigDump --prune "${outBaseName}".py | grep -v 'L1T WARN: ') > "${outBaseName}"_dumpPruned.py
