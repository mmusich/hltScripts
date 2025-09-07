#!/bin/bash -ex

execmd="hltGetConfiguration /dev/CMSSW_15_0_0/HIon/V114"
execmd+=" --no-prescale --no-output"
execmd+=" --paths HLTriggerFirstPath,HLTriggerFinalPath,HLTAnalyzerEndpath"
execmd+=" --eras Run3_2024"
execmd+=" --globaltag 150X_dataRun3_HLT_v1 --data"
execmd+=" --input file:/eos/cms/store/user/cmsbuild/store/hidata/HIRun2024B/HIForward0/RAW/v1/000/388/784/00000/a277c6d8-c445-4d2b-a45c-0e74e4ed8ce8.root"
execmd+=" --max-events 20000"

run(){
  jobLabel="${1}"
  date && echo "${jobLabel}"
  ${execmd} ${@:2} > hltData_"${jobLabel}".py
  cmsRun hltData_"${jobLabel}".py &> hltData_"${jobLabel}".log
  grep L1_ZDC hltData_"${jobLabel}".log > hltData_"${jobLabel}"_L1ZDC.txt
  date
}

run ref \
 --customise HLTrigger/Configuration/CustomConfigs.customiseHLTforHIonRepackedRAW

run L1TEmulGT \
 --customise HLTrigger/Configuration/CustomConfigs.customiseL1THLTforHIonRepackedRAW \
 --l1-emulator uGT

run L1TEmulFull \
 --customise HLTrigger/Configuration/CustomConfigs.customiseL1THLTforHIonRepackedRAW \
 --l1-emulator Full

diff hltData_ref_L1ZDC.txt hltData_L1TEmulFull_L1ZDC.txt
