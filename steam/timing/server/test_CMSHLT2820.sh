#!/bin/bash

[ $# -eq 1 ] || exit 1

EXE="python3 submit.py --cmssw CMSSW_13_0_6"
EXE+=" --event-type Run2023 --input-sample Run367771 --l1menu L1Menu_Collisions2023_v1_1_0-d1_xml"
EXE+=" --threads 32 --streams 24 --nrevents 30000 --jobs 8 --host srv-b1b07-16-01"

cd ${1}

for try in {0..2}; do
  ${EXE} /dev/CMSSW_13_0_0/GRun/V111 --tag _GRunV111_try"${try}"
  ${EXE} /users/missirol/test/dev/CMSSW_13_0_0/tmp/test16/tmp01/GRun/V2 --tag _GRunV111_withoutEXOTriggersWithRun2PixelTracking_try"${try}"
  ${EXE} /users/missirol/test/dev/CMSSW_13_0_0/tmp/test16/tmp02/GRun/V2 --tag _GRunV111_withoutEXODisplacedTauTrigger_try"${try}"
done
