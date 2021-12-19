#!/bin/bash -ex

ConfDBDir=/dev/CMSSW_12_3_0

hltTableNames=(
  GRun
#  HIon
#  PIon
#  PRef
)

inputFileDATA=/store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/2E066536-5CF2-B340-A73B-209640F29FF6.root
inputFileMC=/store/relval/CMSSW_12_2_0_pre2/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/122X_mcRun3_2021_realistic_v1-v1/2580000/5541adab-cc2d-4401-b069-8140c90078c8.root

###

OUTDIR="${1}"

([ "x${OUTDIR}" != "x" ] && [ ! -d "${OUTDIR}" ]) || exit 1
mkdir -p "${OUTDIR}" && cd "${OUTDIR}"

for hltTable in "${hltTableNames[@]}"; do
  hltMenu="${ConfDBDir}"/"${hltTable}"

  hltGetConfCommonArgs="v3/run3:${hltMenu} --max-events 10"
  hltGetConfCommonArgs+=" --no-output --unprescale"
  # proxy to connect to CERN network
  hltGetConfCommonArgs+=" --dbproxy"

  cfgBaseName=hlt_"${hltTable}"

  hltGetConfiguration ${hltGetConfCommonArgs} \
    --input "${inputFileDATA}" --data --globaltag auto:run3_hlt --eras Run2_2018 \
    --customise \
 HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input\
,HLTrigger/Configuration/customizeHLTforPatatrack.customizeHLTforPatatrack\
    > "${cfgBaseName}"_DATA_1.py
  edmConfigDump "${cfgBaseName}"_DATA_1.py > "${cfgBaseName}"_DATA_1_dump.py

  hltGetConfiguration ${hltGetConfCommonArgs} \
    --input "${inputFileDATA}" --data --globaltag auto:run3_hlt --eras Run2_2018 \
    --customise \
 HLTrigger/Configuration/customizeHLTforPatatrack.customizeHLTforPatatrack\
,HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input\
    > "${cfgBaseName}"_DATA_2.py
  edmConfigDump "${cfgBaseName}"_DATA_2.py > "${cfgBaseName}"_DATA_2_dump.py

  hltGetConfiguration ${hltGetConfCommonArgs} \
    --input "${inputFileDATA}" --data --globaltag auto:run3_hlt --eras Run2_2018 \
    --customise \
 HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input\
    > "${cfgBaseName}"_DATA_3.py
  edmConfigDump "${cfgBaseName}"_DATA_3.py > "${cfgBaseName}"_DATA_3_dump.py

  unset hltGetConfCommonArgs cfgBaseName
  unset hltMenu
done
unset hltTable
unset OUTDIR ConfDBDir hltTableNames inputFileDATA inputFileMC
