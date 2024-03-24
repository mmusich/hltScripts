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

#foo CMSHLT3096_TimingTest02_Ref1_V03_try1 /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3096/TimingTest_02/Ref1/GRun/V3
#foo CMSHLT3096_TimingTest02_Ref1_V03_try2 /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3096/TimingTest_02/Ref1/GRun/V3
#
#foo CMSHLT3096_TimingTest02_Tar1_V03_try1 /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3096/TimingTest_02/Tar1/GRun/V3
#foo CMSHLT3096_TimingTest02_Tar1_V03_try2 /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3096/TimingTest_02/Tar1/GRun/V3

#foo CMSHLT3096_TimingTest05_Ref1_V02_try1 /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3096/TimingTest_05/Ref1/GRun/V2
#foo CMSHLT3096_TimingTest05_Ref1_V02_try2 /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3096/TimingTest_05/Ref1/GRun/V2
#
#foo CMSHLT3096_TimingTest05_Tar1_V02_try1 /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3096/TimingTest_05/Tar1/GRun/V2
#foo CMSHLT3096_TimingTest05_Tar1_V02_try2 /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3096/TimingTest_05/Tar1/GRun/V2

for ntry in {1..2}; do

  foo CMSHLT3096_TimingTest07_Ref1_V02_try"${ntry}" /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3096/TimingTest_07/Ref1/GRun/V2
  foo CMSHLT3096_TimingTest07_Tar1_V02_try"${ntry}" /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3096/TimingTest_07/Tar1/GRun/V2

done; unset nnn;
