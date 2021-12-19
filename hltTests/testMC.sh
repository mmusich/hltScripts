#!/bin/bash -ex

OUTDIR="${1}"

mkdir -p "${OUTDIR}"
cd "${OUTDIR}"

hltMenu="${2}" #"${ConfDBDir}"/"${hltTable}"

hltGetConfCommonArgs="${hltMenu} --max-events 10"
# test only L1-Trigger re-emulation (without HLT paths, output files, and PrescaleService)
hltGetConfCommonArgs+=" --output full --unprescale"
# proxy to connect to CERN network
hltGetConfCommonArgs+=" --dbproxy"

cfgBaseName=hlt #_"${3}"

inputFileDATA=/store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/2E066536-5CF2-B340-A73B-209640F29FF6.root
inputFileMC=/store/relval/CMSSW_12_2_0_pre2/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/122X_mcRun3_2021_realistic_v1-v1/2580000/5541adab-cc2d-4401-b069-8140c90078c8.root

###     if [ "x${l1tEmu}" != "xFullMC" ]; then
###       hltGetConfiguration ${hltGetConfCommonArgs} \
###        --input "${inputFileDATA}" --data --globaltag auto:run3_hlt \
###        --customise HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input \
###        > "${cfgBaseName}"_DATA.py
### 
###       # check syntax of expanded configuration
###       (edmConfigDump "${cfgBaseName}"_DATA.py | grep -v 'L1T WARN: ') > "${cfgBaseName}"_DATA_dump.py
###       (edmConfigDump --prune "${cfgBaseName}"_DATA.py | grep -v 'L1T WARN: ') > "${cfgBaseName}"_DATA_dumpPruned.py
### #!!      python3 "${cfgBaseName}"_DATA_dump.py
### #!!
### #!!      # test configuration
### #!!      cmsRun "${cfgBaseName}"_DATA.py &> "${cfgBaseName}"_DATA.log
###     fi

hltGetConfiguration ${hltGetConfCommonArgs} \
 --input "${inputFileMC}" --mc --globaltag auto:run3_mc_GRun \
 > "${cfgBaseName}"_MC.py

# check syntax of expanded configurations
edmConfigDump "${cfgBaseName}"_MC.py > "${cfgBaseName}"_MC_dump.py
edmConfigDump --prune "${cfgBaseName}"_MC.py > "${cfgBaseName}"_MC_dumpPruned.py

# test configuration
cmsRun "${cfgBaseName}"_MC.py &> "${cfgBaseName}"_MC.log

unset inputFileDATA inputFileMC hltMenu hltGetConfCommonArgs cfgBaseName
