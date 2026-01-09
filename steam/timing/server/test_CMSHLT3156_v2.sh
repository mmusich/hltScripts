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

foo0(){
  ${EXE} "${1}" --tag _"${2}" --no-numa-affinity --no-cpu-affinity
}

foo1(){
  ${EXE} "${1}" --tag _"${2}" --no-numa-affinity --cpu-affinity
}

foo2(){
  ${EXE} "${1}" --tag _"${2}" --numa-affinity --no-cpu-affinity
}

foo3(){
  ${EXE} "${1}" --tag _"${2}" --numa-affinity --cpu-affinity
}

for ntry in {1..2}; do

  foo0 run:380384 CMSHLT3156_hltMenuRun380384_NnCn_try"${ntry}"
  foo1 run:380384 CMSHLT3156_hltMenuRun380384_NnCy_try"${ntry}"
  foo2 run:380384 CMSHLT3156_hltMenuRun380384_NyCn_try"${ntry}"
  foo3 run:380384 CMSHLT3156_hltMenuRun380384_NyCy_try"${ntry}"

done
unset nnn
