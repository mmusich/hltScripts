#!/bin/bash

timing_dir=timing
[ $# -lt 1 ] || timing_dir="${1}"

EXE="python3 submit.py"
EXE+=" --threads 32 --streams 24 --nrevents 40100 --jobs 8 --host srv-b1b07-16-01 --repeats 4"
EXE+=" --l1menu L1Menu_Collisions2024_v1_3_0-d1_xml --event-type Run2024 --input-sample Run386593"
EXE+=" --cmssw CMSSW_15_0_4"
EXE+=" --numa-affinity --gpu-affinity --no-cpu-affinity"

cd "${timing_dir}"

if [ ! -f submit.py ]; then
  exit 1
fi

foo(){
  ${EXE} "${2}" --tag _"${1}"
}

for ntry in {0..1}; do

  foo 250411_TestLowPtDoubleEG_Test07_V1_try"${ntry}" /users/missirol/test/dev/CMSSW_15_0_0/tmp/250411_TestLowPtDoubleEG/Test07/GRun/V1
  foo 250411_TestLowPtDoubleEG_Test07_V2_try"${ntry}" /users/missirol/test/dev/CMSSW_15_0_0/tmp/250411_TestLowPtDoubleEG/Test07/GRun/V2

done
unset nnn
