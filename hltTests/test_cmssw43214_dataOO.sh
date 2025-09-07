#!/bin/bash -ex

execmd="hltGetConfiguration /dev/CMSSW_15_0_0/PIon/V114"
execmd+=" --no-prescale --no-output"
execmd+=" --paths HLTriggerFirstPath,HLTriggerFinalPath,HLTAnalyzerEndpath"
execmd+=" --eras Run3_2025"
execmd+=" --globaltag 150X_dataRun3_HLT_v1 --data"
execmd+=" --input file:/eos/cms/store/hidata/OORun2025/HLTPhysics/RAW/v1/000/394/209/00000/4c637e8f-2d3c-4c6b-8c91-346f76c21e44.root"
execmd+=" --max-events 200"

hltLabel=hltDataOO

run(){
  jobLabel="${1}"
  date && echo "${jobLabel}"
  ${execmd} ${@:2} > "${hltLabel}"_"${jobLabel}".py
  cmsRun "${hltLabel}"_"${jobLabel}".py &> "${hltLabel}"_"${jobLabel}".log
  grep L1_ZDC "${hltLabel}"_"${jobLabel}".log > "${hltLabel}"_"${jobLabel}"_L1ZDC.txt
  date
}

run ref
run L1TEmulGT   --l1-emulator uGT
run L1TEmulFull --l1-emulator Full

diff "${hltLabel}"_ref_L1ZDC.txt "${hltLabel}"_L1TEmulFull_L1ZDC.txt
