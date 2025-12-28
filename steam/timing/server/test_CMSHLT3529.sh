#!/bin/bash

timing_dir=timing
[ $# -lt 1 ] || timing_dir="${1}"

EXE="python3 submit.py"
EXE+=" --threads 32 --streams 24 --nrevents 40100 --jobs 8 --host srv-b1b07-16-01 --repeats 4"
EXE+=" --numa-affinity --gpu-affinity --no-cpu-affinity"
EXE+=" --l1menu L1Menu_Collisions2024_v1_3_0-d1_xml --event-type Run2024 --input-sample Run386593"
EXE+=" --cmssw CMSSW_15_0_4_patch3"
EXE+=" --pull-requests cms-tsg-storm:devel_customizeHLTfor2025Studies_from_CMSSW_15_0_3"
EXE+=" --globaltag 150X_dataRun3_HLT_forTriggerStudies_v3"
EXE+=" --customise HLTrigger/Configuration/customizeHLTfor2025Studies.customizeHLTfor2024L1TMenu,HLTrigger/Configuration/customizeHLTfor2025Studies.customizeHLTfor2025Studies"

cd "${timing_dir}"

if [ ! -f submit.py ]; then
  exit 1
fi

for ntry in {0..1}; do

  ${EXE} /users/missirol/test/dev/CMSSW_15_0_0/CMSHLT_3529/Test01/GRun/V4 --tag _250427_TestCMSHLT3529_Test01_V4_try"${ntry}" 
  ${EXE} /users/missirol/test/dev/CMSSW_15_0_0/CMSHLT_3529/Test01/GRun/V6 --tag _250427_TestCMSHLT3529_Test01_V6_try"${ntry}" 

done
unset nnn
