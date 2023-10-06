#!/bin/bash

jobTag=threads4_test01
hltMenu=/dev/CMSSW_13_2_0/HIon
pathName=HLT_HICsAK4PFJet60Eta1p5_Centrality_30_100_v

nJobs=80

check_log () {
  grep "0 ${pathName}" $1 | grep TrigReport | head -1
}

run(){
  echo $2
  cp $1 $2.py
  cat <<EOF >> $2.py
del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')

process.options.numberOfThreads = 16
process.options.numberOfStreams = 0

process.hltOutputMinimal.outputCommands += [
  'keep *_hlt*_*_*',
  'drop *_hltEcalDigisLegacy_*_*',
  'drop *_hltEcalUncalibRecHitLegacy_*_*',
  'drop *_hltHbherecoLegacy_*_*',
]

process.hltOutputMinimal.fileName = '${2}.root'
EOF
  cmsRun "${2}".py &> "${2}".log
  check_log "${2}".log
}

hltGetCmd="hltGetConfiguration ${hltMenu}"
hltGetCmd+=" --globaltag auto:run3_mc_HIon --mc --unprescale --output minimal --max-events -1"
hltGetCmd+=" --input file:RelVal_Raw_HIon_MC.root"

configLabel=hlt_"${jobTag}"
${hltGetCmd} --paths "${pathName}"* > "${configLabel}".py
for job_i in $(eval echo "{1..$nJobs}"); do
  run "${configLabel}".py "${configLabel}"_"${job_i}"
done
unset job_i
