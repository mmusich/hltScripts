#!/bin/bash

timing_dir=timing
[ $# -lt 1 ] || timing_dir="${1}"

EXE="python3 submit.py --cmssw CMSSW_14_0_4"
EXE+=" --threads 32 --streams 24 --nrevents 30000 --jobs 8 --host srv-b1b07-16-01 --repeats 3"

EXE1=${EXE}
EXE1+=" --l1menu L1Menu_Collisions2024_v0_0_0_xml --event-type Run2023 --input-sample Run370293"

EXE2=${EXE}
EXE2+=" --l1menu L1Menu_Collisions2024_v0_0_0_displacedSingleMu --event-type Run2023 --input-sample Run370293"

cd "${timing_dir}"

if [ ! -f submit.py ]; then
  exit 1
fi

foo1(){
  ${EXE1} "${1}" --tag _"${2}"
}

foo2(){
  ${EXE2} "${1}" --tag _"${2}"
}

for ntry in {1..2}; do

  foo1 /users/missirol/test/dev/CMSSW_14_0_0/tmp/240331_ThroughputMeasurements/TimingTest_01/GRun/V3 CMSHLT3122_240331_ThroughputMeasurements_TimingTest01_V03_skim000_try"${ntry}"
  foo2 /users/missirol/test/dev/CMSSW_14_0_0/tmp/240331_ThroughputMeasurements/TimingTest_01/GRun/V3 CMSHLT3122_240331_ThroughputMeasurements_TimingTest01_V03_skim000displacedSingleMu_try"${ntry}"

done
unset nnn
