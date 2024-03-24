#!/bin/bash

timing_dir=timing
[ $# -lt 1 ] || timing_dir="${1}"

EXE="python3 submit.py --cmssw CMSSW_14_0_X_2024-03-22-2300"
EXE+=" --l1menu L1Menu_Collisions2024_v0_0_0_xml --event-type Run2023 --input-sample Run370293"
EXE+=" --threads 32 --streams 24 --nrevents 30000 --jobs 8 --host srv-b1b07-16-01 --repeats 5"

cd "${timing_dir}"

if [ ! -f submit.py ]; then
  exit 1
fi

foo(){
  ${EXE} "${2}" --tag _"${1}"
}

for ntry in {1..3}; do

  foo SiStripClustersOnDemand_TimingTest01_Ref1_V02_try"${ntry}" /users/missirol/test/dev/CMSSW_14_0_0/tmp/240323_SiStripClustersOnDemand/TimingTest_01/Ref1/GRun/V2
  foo SiStripClustersOnDemand_TimingTest01_Tar1_V02_try"${ntry}" /users/missirol/test/dev/CMSSW_14_0_0/tmp/240323_SiStripClustersOnDemand/TimingTest_01/Tar1/GRun/V2

done; unset nnn;
