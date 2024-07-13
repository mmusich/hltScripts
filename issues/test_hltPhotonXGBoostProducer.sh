#!/bin/bash -ex

addOnTests.py -t hlt_mc_GRun

jobTag=threads4
hltMenu=/dev/CMSSW_14_0_0/GRun/V141

check_log () {
  grep '0 HLT_DiphotonMVA14p25_Tight_Mass90_v' $1 | grep TrigReport
}

run(){
  echo $2
  cp $1 $2.py
  cat <<EOF >> $2.py

process.options.numberOfThreads = 4
process.options.numberOfStreams = 0

process.hltOutputMinimal.fileName = '${2}.root'
EOF
  cmsRun "${2}".py &> "${2}".log
  check_log "${2}".log
}

hltGetCmd="hltGetConfiguration ${hltMenu}"
hltGetCmd+=" --globaltag auto:run3_mc_GRun --mc --unprescale --output minimal --max-events -1"
hltGetCmd+=" --input file:addOnTests/hlt_mc_GRun/RelVal_Raw_GRun_MC.root"

#echo $hltGetCmd

configLabel=hlt_"${jobTag}"_onlyDiphotonMVA14p25_Tight_Mass90
#echo "${configLabel}".py
${hltGetCmd} --paths HLT_DiphotonMVA14p25_Tight_Mass90_v1 > "${configLabel}".py
for job_i in {0..9}; do run "${configLabel}".py "${configLabel}"_"${job_i}"; done; unset job_i;

configLabel=hlt_"${jobTag}"_full
${hltGetCmd} > "${configLabel}".py
for job_i in {0..9}; do run "${configLabel}".py "${configLabel}"_"${job_i}"; done; unset job_i;
