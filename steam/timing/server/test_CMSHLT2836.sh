#!/bin/bash

[ $# -eq 1 ] || exit 1

cd ${1}

if [ ! -f submit.py ]; then
  exit 1
fi

submit(){
  sleep 1 && python3 submit.py $@
}

OPTS="--cmssw CMSSW_13_0_10"
OPTS+=" --event-type Run2023 --input-sample Run370293 --l1menu L1Menu_Collisions2023_v1_2_0-d1_xml"
OPTS+=" --threads 32 --streams 24 --nrevents 30000 --jobs 8 --host srv-b1b07-16-01"

for try in {2..3}; do
  for grun in 1 2 3; do
    submit ${OPTS} /users/missirol/test/dev/CMSSW_13_0_0/CMSHLT_2836/Test01/GRun/V"${grun}" --tag _CMSHLT2836_GRunV"${grun}"_try"${try}"
  done
done

# for fff in $(ls /eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STEAM/timing_server_results/missirol/CMSSW_13_0_10_1300GRunV*_try*.20230721_*/cmsRun*.stderr | sort -u); do echo $fff; grep FastReport ${fff} | grep total | tail -1; done; unset fff;
