#!/bin/bash -ex

execmd="hltGetConfiguration /dev/CMSSW_15_0_0/HIon/V114"
execmd+=" --no-prescale --no-output"
execmd+=" --paths HLTriggerFirstPath,HLTriggerFinalPath,HLTAnalyzerEndpath"
execmd+=" --eras Run3_2025"
execmd+=" --globaltag 150X_dataRun3_HLT_v1 --data"
execmd+=" --input file:/eos/cms/store/hidata/OORun2025/IonPhysics0/RAW/v1/000/394/217/00000/85627bb3-139a-4230-a196-f0b20de864ed.root"
execmd+=" --max-events 1"

run(){
  jobLabel="${1}"
  date && echo "${jobLabel}"
  ${execmd} ${@:2} > hltData_"${jobLabel}".py

  cat <<@EOF >> hltData_"${jobLabel}".py

process.hltL1TGlobalSummary.DumpTrigResults = True
@EOF

  cmsRun hltData_"${jobLabel}".py &> hltData_"${jobLabel}".log
  grep L1_MinimumBiasHF1_OR_BptxAND hltData_"${jobLabel}".log > hltData_"${jobLabel}"_L1MinimumBiasHF1ORBptxAND.txt
  date
}

run ref
run L1TEmulGT   --l1-emulator uGT
run L1TEmulFull --l1-emulator Full

diff hltData_ref_L1MinimumBiasHF1ORBptxAND.txt hltData_L1TEmulFull_L1MinimumBiasHF1ORBptxAND.txt
