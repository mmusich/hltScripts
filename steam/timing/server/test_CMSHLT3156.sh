#!/bin/bash

timing_dir=timing
[ $# -lt 1 ] || timing_dir="${1}"

EXE="python3 submit.py"
EXE+=" --threads 32 --streams 24 --nrevents 40100 --jobs 8 --host srv-b1b07-16-01 --repeats 3"
EXE+=" --cmssw CMSSW_14_0_5_patch1 --globaltag 140X_dataRun3_HLT_v3"

EXE1=${EXE}
EXE1+=" --l1menu L1Menu_Collisions2024_v1_0_0-d1_xml --event-type Run2024 --input-sample Run379530"

EXE2=${EXE}
EXE2+=" --l1menu L1Menu_Collisions2024_v1_1_0-d1_xml --event-type Run2024 --input-sample Run379660"

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

  foo1 run:379530 CMSHLT3156_2404423_run379530_try"${ntry}"
  foo2 run:379660 CMSHLT3156_2404423_run379660_try"${ntry}"

done
unset nnn
