#!/bin/bash -ex

inputFileData=file:/eos/cms/store/user/cmsbuild/store/hidata/HIRun2024B/HIForward0/RAW/v1/000/388/784/00000/a277c6d8-c445-4d2b-a45c-0e74e4ed8ce8.root

execmd="hltGetConfiguration /dev/CMSSW_15_0_0/HIon/V114"
execmd+=" --no-prescale --no-output"
execmd+=" --paths HLTriggerFirstPath,HLTriggerFinalPath,HLTAnalyzerEndpath"
execmd+=" --customise HLTrigger/Configuration/CustomConfigs.customiseHLTforHIonRepackedRAW"
execmd+=" --globaltag 150X_dataRun3_HLT_v1 --data"
execmd+=" --input ${inputFileData}"
execmd+=" --max-events 10000"

run(){
  jobLabel="${1}"
  date && echo "${jobLabel}"
  ${execmd} ${@:2} > hltData_"${jobLabel}".py
  cmsRun hltData_"${jobLabel}".py &> hltData_"${jobLabel}".log
  grep L1_ZDC hltData_"${jobLabel}".log > hltData_"${jobLabel}"_L1ZDC.txt
  date
}

run ref
run L1TEmulGT   --l1-emulator uGT
run L1TEmulFull --l1-emulator Full

diff hltData_ref_L1ZDC.txt hltData_L1TEmulFull_L1ZDC.txt

#${execmd} \
#  --input /store/relval/CMSSW_14_0_0/RelValPyquen_DiJet_pt80to120_5362GeV_2023/GEN-SIM-DIGI-RAW-HLTDEBUG/PU_140X_mcRun3_2023_realistic_HI_v3_STD_HIN_PU-v1/2580000/8dda8ff3-5f50-4698-8834-24f2a31a8bf3.root \
#  --globaltag 140X_mcRun3_2023_realistic_HI_v3 \
#  --mc \
#  > hltMC_ref.py && cmsRun hltMC_ref.py &> hltMC_ref.log
#
#${execmd} \
#  --input /store/relval/CMSSW_14_0_0/RelValPyquen_DiJet_pt80to120_5362GeV_2023/GEN-SIM-DIGI-RAW-HLTDEBUG/PU_140X_mcRun3_2023_realistic_HI_v3_STD_HIN_PU-v1/2580000/8dda8ff3-5f50-4698-8834-24f2a31a8bf3.root \
#  --globaltag 140X_mcRun3_2023_realistic_HI_v3 \
#  --mc \
#  --eras Run3 --l1-emulator uGT \
#  > hltMC_L1uGT.py && cmsRun hltMC_L1uGT.py &> hltMC_L1uGT.log
#
#${execmd} \
#  --input /store/relval/CMSSW_14_0_0/RelValPyquen_DiJet_pt80to120_5362GeV_2023/GEN-SIM-DIGI-RAW-HLTDEBUG/PU_140X_mcRun3_2023_realistic_HI_v3_STD_HIN_PU-v1/2580000/8dda8ff3-5f50-4698-8834-24f2a31a8bf3.root \
#  --globaltag 140X_mcRun3_2023_realistic_HI_v3 \
#  --mc \
#  --eras Run3 --l1-emulator FullMC \
#  > hltMC_L1FullMC.py && cmsRun hltMC_L1FullMC.py &> hltMC_L1FullMC.log
