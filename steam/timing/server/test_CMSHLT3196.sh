#!/bin/bash

timing_dir=timing
[ $# -lt 1 ] || timing_dir="${1}"

EXE="python3 submit.py"
EXE+=" --threads 32 --streams 24 --nrevents 40100 --jobs 8 --host srv-b1b07-16-01 --repeats 3"
EXE+=" --l1menu L1Menu_Collisions2024_v1_1_0-d1_xml --event-type Run2024 --input-sample Run379660"
EXE+=" --cmssw CMSSW_14_0_6_MULTIARCHS"

cd "${timing_dir}"

if [ ! -f submit.py ]; then
  exit 1
fi

foo(){
  ${EXE} "${1}" --tag _"${2}"
}

for ntry in {1..2}; do

#  foo /users/missirol/test/dev/CMSSW_14_0_0/tmp/240509_SiStripClusterChargeCut/TimingTest_01/Ref1/GRun/V2 240509_SiStripClusterChargeCut_Test01_Ref1_V2_try"${ntry}"
#  foo /users/missirol/test/dev/CMSSW_14_0_0/tmp/240509_SiStripClusterChargeCut/TimingTest_01/Tar1/GRun/V2 240509_SiStripClusterChargeCut_Test01_Tar1_V2_try"${ntry}"
  foo /users/missirol/test/dev/CMSSW_14_0_0/tmp/240509_SiStripClusterChargeCut/TimingTest_01/Tar2/GRun/V2 240509_SiStripClusterChargeCut_Test01_Tar2_V2_try"${ntry}"

done
unset nnn
