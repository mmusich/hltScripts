#!/bin/bash

timing_dir=timing
[ $# -lt 1 ] || timing_dir="${1}"

EXE="python3 submit.py --cmssw CMSSW_14_0_0"
#EXE+=" --pull-requests silviodonato:customizeHLTFor2023 --customise  HLTrigger/Configuration/customizeHLTFor2023.customizeHLTFor2023L1TMenu_v1_1_0"
EXE+=" --l1menu L1Menu_Collisions2024_v0_0_0_xml --event-type Run2023 --input-sample Run370293"
EXE+=" --threads 32 --streams 24 --nrevents 30000 --jobs 8 --host srv-b1b07-16-01 --repeats 3"

cd "${timing_dir}"

if [ ! -f submit.py ]; then
  exit 1
fi

foo(){
  ${EXE} "${2}" --tag _"${1}"
}

foo CMSHLT3089_Test01_V01_try1 /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3089/Test01/GRun/V1
foo CMSHLT3089_Test01_V01_try2 /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3089/Test01/GRun/V1

foo CMSHLT3089_Test01_V02_try1 /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3089/Test01/GRun/V2
foo CMSHLT3089_Test01_V02_try2 /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3089/Test01/GRun/V2
