#!/bin/bash -ex

ConfDBDir=/dev/CMSSW_12_3_0

hltTableNames=(
  GRun/V8
  GRun/V24
#  PIon
#  PRef
)

inputFileDATA=/store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/2E066536-5CF2-B340-A73B-209640F29FF6.root
inputFileMC=/store/relval/CMSSW_12_2_0_pre2/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/122X_mcRun3_2021_realistic_v1-v1/2580000/5541adab-cc2d-4401-b069-8140c90078c8.root

###

OUTDIR="${1}"

[ "x${OUTDIR}" != "x" ] || exit 1
mkdir -p "${OUTDIR}" && cd "${OUTDIR}"

for hltTable in "${hltTableNames[@]}"; do
  hltMenu="${ConfDBDir}"/"${hltTable}"

  hltGetConfCommonArgs="v3/run3:${hltMenu} --max-events 10"
  hltGetConfCommonArgs+=" --output all --unprescale"
  # proxy to connect to CERN network
  hltGetConfCommonArgs+=" --dbproxy"

  for extraLabel in "" "_PrePR" "_PrePR2"; do

    cfgBaseName=hlt_"${hltTable////_}""${extraLabel}"

    [ -f "${cfgBaseName}"_MC_1.py ] || \
    hltGetConfiguration ${hltGetConfCommonArgs} \
      --input "${inputFileMC}" --mc --globaltag auto:run3_mc_GRun --eras Run3 \
      --customise HLTrigger/Configuration/customizeHLTforPatatrack"${extraLabel}".customizeHLTforPatatrack \
      > "${cfgBaseName}"_MC_1.py
    edmConfigDump "${cfgBaseName}"_MC_1.py > "${cfgBaseName}"_MC_1_dump.py

    [ -f "${cfgBaseName}"_DATA_1.py ] || \
    hltGetConfiguration ${hltGetConfCommonArgs} \
      --input "${inputFileDATA}" --data --globaltag auto:run3_hlt --eras Run2_2018 \
      --customise HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input,HLTrigger/Configuration/customizeHLTforPatatrack"${extraLabel}".customizeHLTforPatatrack \
      > "${cfgBaseName}"_DATA_1.py
    edmConfigDump "${cfgBaseName}"_DATA_1.py > "${cfgBaseName}"_DATA_1_dump.py

    [ -f "${cfgBaseName}"_DATA_2.py ] || \
    hltGetConfiguration ${hltGetConfCommonArgs} \
      --input "${inputFileDATA}" --data --globaltag auto:run3_hlt --eras Run2_2018 \
      --customise HLTrigger/Configuration/customizeHLTforPatatrack"${extraLabel}".customizeHLTforPatatrack,HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input \
      > "${cfgBaseName}"_DATA_2.py
    edmConfigDump "${cfgBaseName}"_DATA_2.py > "${cfgBaseName}"_DATA_2_dump.py

    [ -f "${cfgBaseName}"_DATA_3.py ] || \
    hltGetConfiguration ${hltGetConfCommonArgs} \
      --input "${inputFileDATA}" --data --globaltag auto:run3_hlt --eras Run2_2018 \
      --customise HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input \
      > "${cfgBaseName}"_DATA_3.py
    edmConfigDump "${cfgBaseName}"_DATA_3.py > "${cfgBaseName}"_DATA_3_dump.py

    unset cfgBaseName
  done
  unset extraLabel

  unset hltMenu hltGetConfCommonArgs
done
unset hltTable
unset OUTDIR ConfDBDir hltTableNames inputFileDATA inputFileMC
