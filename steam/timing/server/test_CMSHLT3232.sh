#!/bin/bash

timing_dir=timing
[ $# -lt 1 ] || timing_dir="${1}"

EXE="python3 submit.py"
EXE+=" --threads 32 --streams 24 --nrevents 40100 --jobs 8 --host srv-b1b07-16-01 --repeats 4"
EXE+=" --l1menu L1Menu_Collisions2024_v1_2_0-d1_xml --event-type Run2024 --input-sample Run381065"
EXE+=" --cmssw CMSSW_14_0_8_MULTIARCHS"
EXE+=" --numa-affinity --gpu-affinity --no-cpu-affinity"

cd "${timing_dir}"

if [ ! -f submit.py ]; then
  exit 1
fi

foo(){
  ${EXE} "${1}" --tag _"${2}"
}

for ntry in {0..1}; do

  foo run:381065 240608_testCMSHLT3232_test01_try"${ntry}"

done
unset nnn
