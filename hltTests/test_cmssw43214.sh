#!/bin/bash

execmd="hltGetConfiguration /dev/CMSSW_14_0_0/HIon --no-prescale --no-output --max-events 100"
execmd+=" --paths HLTriggerFirstPath,HLTriggerFinalPath,HLTAnalyzerEndpath"

#${execmd} \
#  --customise HLTrigger/Configuration/CustomConfigs.customiseHLTforHIonRepackedRAWPrime \
#  --input file:/eos/cms/store/user/cmsbuild/store/hidata/HIRun2023A/HIPhysicsRawPrime0/RAW/v1/000/375/491/00000/de963321-c0a0-49fb-b771-1a312a69db03.root \
#  --globaltag 140X_dataRun3_HLT_v3 \
#  --data \
#  > hltData_ref.py && cmsRun hltData_ref.py >& hltData_ref.log
#
#${execmd} \
#  --customise HLTrigger/Configuration/CustomConfigs.customiseL1THLTforHIonRepackedRAWPrime \
#  --input file:/eos/cms/store/user/cmsbuild/store/hidata/HIRun2023A/HIPhysicsRawPrime0/RAW/v1/000/375/491/00000/de963321-c0a0-49fb-b771-1a312a69db03.root \
#  --globaltag 140X_dataRun3_HLT_v3 \
#  --data \
#  --eras Run3 --l1-emulator uGT \
#  > hltData_L1uGT.py && cmsRun hltData_L1uGT.py >& hltData_L1uGT.log
#
#${execmd} \
#  --customise HLTrigger/Configuration/CustomConfigs.customiseL1THLTforHIonRepackedRAWPrime \
#  --input file:/eos/cms/store/user/cmsbuild/store/hidata/HIRun2023A/HIPhysicsRawPrime0/RAW/v1/000/375/491/00000/de963321-c0a0-49fb-b771-1a312a69db03.root \
#  --globaltag 140X_dataRun3_HLT_v3 \
#  --data \
#  --eras Run3 --l1-emulator Full \
#  > hltData_L1Full.py && cmsRun hltData_L1Full.py >& hltData_L1Full.log

${execmd} \
  --input /store/relval/CMSSW_14_0_0/RelValPyquen_DiJet_pt80to120_5362GeV_2023/GEN-SIM-DIGI-RAW-HLTDEBUG/PU_140X_mcRun3_2023_realistic_HI_v3_STD_HIN_PU-v1/2580000/8dda8ff3-5f50-4698-8834-24f2a31a8bf3.root \
  --globaltag 140X_mcRun3_2023_realistic_HI_v3 \
  --mc \
  > hltMC_ref.py && cmsRun hltMC_ref.py &> hltMC_ref.log

${execmd} \
  --input /store/relval/CMSSW_14_0_0/RelValPyquen_DiJet_pt80to120_5362GeV_2023/GEN-SIM-DIGI-RAW-HLTDEBUG/PU_140X_mcRun3_2023_realistic_HI_v3_STD_HIN_PU-v1/2580000/8dda8ff3-5f50-4698-8834-24f2a31a8bf3.root \
  --globaltag 140X_mcRun3_2023_realistic_HI_v3 \
  --mc \
  --eras Run3 --l1-emulator uGT \
  > hltMC_L1uGT.py && cmsRun hltMC_L1uGT.py &> hltMC_L1uGT.log

${execmd} \
  --input /store/relval/CMSSW_14_0_0/RelValPyquen_DiJet_pt80to120_5362GeV_2023/GEN-SIM-DIGI-RAW-HLTDEBUG/PU_140X_mcRun3_2023_realistic_HI_v3_STD_HIN_PU-v1/2580000/8dda8ff3-5f50-4698-8834-24f2a31a8bf3.root \
  --globaltag 140X_mcRun3_2023_realistic_HI_v3 \
  --mc \
  --eras Run3 --l1-emulator FullMC \
  > hltMC_L1FullMC.py && cmsRun hltMC_L1FullMC.py &> hltMC_L1FullMC.log
