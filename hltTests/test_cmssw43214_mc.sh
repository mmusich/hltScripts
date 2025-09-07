#!/bin/bash -ex

execmd="hltGetConfiguration /dev/CMSSW_15_0_0/HIon/V114"
execmd+=" --no-prescale --no-output"
execmd+=" --paths HLTriggerFirstPath,HLTriggerFinalPath,HLTAnalyzerEndpath"
execmd+=" --eras Run3_2024"
execmd+=" --globaltag 141X_mcRun3_2024_realistic_HI_v13 --mc"
execmd+=" --input /store/relval/CMSSW_15_0_0/RelValPyquen_GammaJet_pt20_5362GeV_2024/GEN-SIM-DIGI-RAW-HLTDEBUG/PU_141X_mcRun3_2024_realistic_HI_v13_STD_2024HIN_PU-v1/2580000/4c6ef0a2-390b-45cf-9387-2433ab7d22e7.root"
execmd+=" --max-events -1"

run(){
  jobLabel="${1}"
  date && echo "${jobLabel}"
  ${execmd} ${@:2} > hltMC_"${jobLabel}".py
  cmsRun hltMC_"${jobLabel}".py &> hltMC_"${jobLabel}".log
  grep L1_ZDC hltMC_"${jobLabel}".log > hltMC_"${jobLabel}"_L1ZDC.txt
  date
}

run ref
run L1TEmulGT   --l1-emulator uGT
run L1TEmulFull --l1-emulator Full

diff hltMC_ref_L1ZDC.txt hltMC_L1TEmulFull_L1ZDC.txt
