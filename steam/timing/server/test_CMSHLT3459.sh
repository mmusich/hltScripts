#!/bin/bash

timing_dir=timing
[ $# -lt 1 ] || timing_dir="${1}"

EXE1="python3 submit.py"
EXE1+=" --threads 32 --streams 24 --nrevents 40100 --jobs 8 --host srv-b1b07-16-01 --repeats 4"
EXE1+=" --numa-affinity --gpu-affinity --no-cpu-affinity"
EXE1+=" --l1menu L1Menu_Collisions2024_v1_3_0-d1_xml --event-type Run2024 --input-sample Run386593"
EXE1+=" --cmssw CMSSW_15_0_4_patch3"
EXE1+=" --pull-requests cms-tsg-storm:devel_customizeHLTfor2025Studies_from_CMSSW_15_0_3"

EXE2="${EXE1}"

EXE1+=" --globaltag 150X_dataRun3_HLT_forTriggerStudies_v4"
EXE2+=" --globaltag 150X_dataRun3_HLT_forTriggerStudies_v5"

EXE1+=" --customise HLTrigger/Configuration/customizeHLTfor2025Studies.customizeHLTfor2024L1TMenu"
EXE2+=" --customise HLTrigger/Configuration/customizeHLTfor2025Studies.customizeHLTfor2024L1TMenu,HLTrigger/Configuration/customizeHLTfor2025Studies.customizeHLTfor2025Studies"

cd "${timing_dir}"

if [ ! -f submit.py ]; then
  exit 1
fi

for ntry in {0..1}; do

#  ${EXE1} /users/missirol/test/dev/CMSSW_15_0_0/CMSHLT_3459/Test04/GRun/V1 --tag _250420_TestCMSHLT3549_Test04_V1_try"${ntry}" 
#  ${EXE1} /users/missirol/test/dev/CMSSW_15_0_0/CMSHLT_3459/Test04/GRun/V3 --tag _250420_TestCMSHLT3549_Test04_V3_try"${ntry}" 

  ${EXE1} /users/missirol/test/dev/CMSSW_15_0_0/CMSHLT_3459/Test05/GRun/V1 --tag _250420_TestCMSHLT3549_Test05_V1_try"${ntry}" 
  ${EXE1} /users/missirol/test/dev/CMSSW_15_0_0/CMSHLT_3459/Test05/GRun/V2 --tag _250420_TestCMSHLT3549_Test05_V2_try"${ntry}" 

done
unset nnn
