#!/bin/bash

jobTag=threads4_printPixRegsAndInactiveAreas
hltMenu=/dev/CMSSW_13_0_0/GRun/V152

check_log () {
  grep '0 HLT_PFJet140_v' $1 | grep TrigReport | head -1
}

run(){
  echo $2
  cp $1 $2.py
  cat <<EOF >> $2.py
del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')

#process.hltSiStripRawToClustersFacility.onDemand = False

process.hltDoubletRecoveryPixelLayersAndRegions.debug = True

process.options.numberOfThreads = 4
process.options.numberOfStreams = 0

process.hltOutputMinimal.outputCommands += [
  'keep *_hltSiPixelDigis_*_*',
  'keep *_hltSiPixelClusters_*_*',
  'keep *_hltSiStrip*_*_*',
  'keep *_hltPixelTracks_*_*',
  'keep *_hlt*PixelVertices_*_*',

  'keep *_hltOnlineBeam*_*_*',
  'keep *_hltIter0*_*_*',
  'keep *_hltDoubletRecovery*_*_*',
  'keep *_hltMergedTracks_*_*',
]

process.hltOutputMinimal.fileName = '${2}.root'
EOF
  cmsRun "${2}".py &> "${2}".log
  check_log "${2}".log
}

hltGetCmd="hltGetConfiguration ${hltMenu}"
hltGetCmd+=" --globaltag auto:run3_mc_GRun --mc --unprescale --output minimal --max-events -1"
hltGetCmd+=" --l1 L1Menu_Collisions2023_v1_3_0_xml"
hltGetCmd+=" --input file:/afs/cern.ch/work/m/missirol/public/tsg-storm/250723_reproIssueWithGRunV152/RelVal_Raw_GRun_MC.root"

configLabel=hlt_"${jobTag}"_onlyPFJet140
${hltGetCmd} --paths HLT_PFJet140_v* > "${configLabel}".py
for job_i in {0..4}; do run "${configLabel}".py "${configLabel}"_"${job_i}"; done; unset job_i;

#configLabel=hlt_"${jobTag}"_full
#${hltGetCmd} > "${configLabel}".py
#for job_i in {0..4}; do run "${configLabel}".py "${configLabel}"_"${job_i}"; done; unset job_i;
