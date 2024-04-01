#!/bin/bash

timing_dir=timing
[ $# -lt 1 ] || timing_dir="${1}"

EXE="python3 submit.py"
EXE+=" --l1menu L1Menu_Collisions2024_v0_0_0_xml --event-type Run2023 --input-sample Run370293"
EXE+=" --threads 32 --streams 24 --nrevents 30000 --jobs 8 --host srv-b1b07-16-01 --repeats 5"

EXE1="${EXE}"
EXE1+=" --cmssw CMSSW_14_0_X_2024-03-28-2300"

EXE2="${EXE}"
EXE2+=" --cmssw CMSSW_14_0_MULTIARCHS_X_2024-03-28-2300"

cd "${timing_dir}"

if [ ! -f submit.py ]; then
  exit 1
fi

foo1() {
  ${EXE1} "${2}" --tag _"${1}"
}

foo2() {
  ${EXE2} "${2}" --tag _"${1}"
}

for ntry in {1..2}; do

  foo1 240331_ThroughputMeasurements_TimingTest01_V03_try"${ntry}" /users/missirol/test/dev/CMSSW_14_0_0/tmp/240331_ThroughputMeasurements/TimingTest_01/GRun/V3
  foo2 240331_ThroughputMeasurements_TimingTest01_V03_try"${ntry}" /users/missirol/test/dev/CMSSW_14_0_0/tmp/240331_ThroughputMeasurements/TimingTest_01/GRun/V3

#  foo1 240331_ThroughputMeasurements_TimingTest02_V02_try"${ntry}" /users/missirol/test/dev/CMSSW_14_0_0/tmp/240331_ThroughputMeasurements/TimingTest_02/GRun/V2
#  foo1 240331_ThroughputMeasurements_TimingTest02_V03_try"${ntry}" /users/missirol/test/dev/CMSSW_14_0_0/tmp/240331_ThroughputMeasurements/TimingTest_02/GRun/V3

#  foo1 240331_ThroughputMeasurements_TimingTest03_V02_try"${ntry}" /users/missirol/test/dev/CMSSW_14_0_0/tmp/240331_ThroughputMeasurements/TimingTest_03/GRun/V2
#  foo1 240331_ThroughputMeasurements_TimingTest03_V03_try"${ntry}" /users/missirol/test/dev/CMSSW_14_0_0/tmp/240331_ThroughputMeasurements/TimingTest_03/GRun/V3

done; unset nnn;
