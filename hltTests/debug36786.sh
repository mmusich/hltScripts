#!/bin/bash -e

[ $# -eq 2 ] || exit 1

mkdir -p "${1}"
cd "${1}"

if [ ! -d "${2}" ]; then
  scram p CMSSW "${2}"
  cd "${2}"/src
  eval `scram runtime -sh`
  git cms-init --ssh
  scram b
else
  cd "${2}"/src
  eval `scram runtime -sh`
  scram b
fi

inputEdmFile="${CMSSW_BASE}"/src/11634.0_TTbar_14TeV+2021+TTbar_14TeV_TuneCP5_GenSim+Digi+RecoNano+HARVESTNano+ALCA/step2.root

if [ ! -f "${inputEdmFile}" ]; then
  runTheMatrix.py -l 11634.0
fi

inputEdmFile=file:"${inputEdmFile}"

hltGetConfiguration /dev/CMSSW_12_3_0/GRun --dbproxy \
 --mc --globaltag auto:phase1_2021_realistic --input "${inputEdmFile}" \
 --process HLTX --output none --unprescale --max-events 1 \
 --l1-emulator uGT \
 > test1_hlt_uGT.py
(cmsRun test1_hlt_uGT.py &> test1_hlt_uGT.log) || true

cp test1_hlt_uGT.py test2_hlt_uGT.py
echo -e "\ndel process.hltGetConditions" >> test2_hlt_uGT.py
(cmsRun test2_hlt_uGT.py &> test2_hlt_uGT.log) || true

hltGetConfiguration /dev/CMSSW_12_3_0/GRun --dbproxy \
 --mc --globaltag auto:phase1_2021_realistic --input "${inputEdmFile}" \
 --process HLTX --output none --unprescale --max-events 1 \
 > test1_hlt_noL1T.py
(cmsRun test1_hlt_noL1T.py &> test1_hlt_noL1T.log) || true

#cmsDriver.py step0 --no_exec --python_file test3_l1tFullMC_cfg.py -s L1REPACK:FullMC --conditions auto:phase1_2021_realistic -n 5 --geometry DB:Extended --era Run3 --no_output \
# --filein "${inputEdmFile}"
#edmConfigDump --prune test3_l1tFullMC_cfg.py > test3_l1tFullMC_cfgDump.py
#cmsRun test3_l1tFullMC_cfgDump.py &> test3_l1tFullMC_cfgDump.log
