#!/bin/bash

jobTag=git
# hltMenu=/users/tsheng/JLT_JIRA_3116_Rep_V72/V1 # shows discrep
# hltMenu=/users/tsheng/JLT_JIRA_3116_Rep_V72/V3 # shows discrep
# hltMenu=/users/tsheng/JLT_JIRA_3116_Rep_V72/V4 # error
hltMenu=/users/tsheng/JLT_JIRA_3116_Rep_V72/V5 # testing

check_log () {
  grep '0 HLT_PPRefDmesonTrackingGlobal_Dpt25_v' $1 | grep TrigReport
}

run(){
  echo $2
  cp $1 $2.py
  cat <<EOF >> $2.py

process.options.numberOfThreads = 4
process.options.numberOfStreams = 0

process.hltOutputMinimal.outputCommands += [
  'keep *_hltFullIter*_*_*',
]

process.hltOutputMinimal.fileName = '${2}.root'
EOF

  [ -e "${2}.root" ] && rm "${2}.root"
  cmsRun "${2}".py &> "${2}".log
  check_log "${2}".log
}

remove_tag(){
    # These parameters are not present in CMSSW_14_0_9
    # sed -i '/AXOL1TLModelVersion/d' ${2}.py
    sed -i '/CICADAInputTag/d' ${1}.py
    sed -i '/acceptedCombinations/d' ${1}.py
    sed -i '/l1EGCand/d' ${1}.py
}

hltGetCmd="hltGetConfiguration ${hltMenu}"
hltGetCmd+=" --globaltag auto:run3_mc_PRef --mc --unprescale --output minimal --max-events -1"
# hltGetCmd+=" --input /store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STORM/debug/170324_reproIssueWithPRef/RelVal_DigiL1Raw_PRef_MC.root"
hltGetCmd+=" --input file:/afs/cern.ch/work/s/soohwan/public/ForTzuAn/step2_PU10.root"

#echo $hltGetCmd

configLabel=hlt_"${jobTag}"_onlyPPRefDmesonTrackingGlobal
#echo "${configLabel}".py
${hltGetCmd} --paths HLT_PPRefDmesonTrackingGlobal_Dpt25_v3 > "${configLabel}".py
remove_tag ${configLabel}
for job_i in {0..10}; do run "${configLabel}".py "${configLabel}"_"${job_i}"; done; unset job_i;

configLabel=hlt_"${jobTag}"_full
${hltGetCmd} > "${configLabel}".py
remove_tag ${configLabel}
for job_i in {0..10}; do run "${configLabel}".py "${configLabel}"_"${job_i}"; done; unset job_i;
