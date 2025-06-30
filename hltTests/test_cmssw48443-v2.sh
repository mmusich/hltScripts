#!/bin/bash

jobTag=threads4
hltMenu=/dev/CMSSW_15_0_0/GRun/V96

check_log () {
  grep '0 HLT_AK8PFJetFwd40_v' $1 | grep TrigReport
}

run(){
  echo $2
  cp $1 $2.py
  cat <<EOF >> $2.py

process.options.numberOfThreads = 4
process.options.numberOfStreams = 0

# process.hltOutputMinimal.outputCommands += [
#   'keep *_hltSiPixelDigis_*_*',		
#   'keep *_hltSiPixelClusters_*_*',
#   'keep *_hltSiStrip*_*_*',
#   'keep *_hltPixelTracks_*_*',
#   'keep *_hlt*PixelVertices_*_*',

#   'keep *_hltOnlineBeam*_*_*',
#   'keep *_hltIter0*_*_*',
#   'keep *_hltDoubletRecovery*_*_*',
#   'keep *_hltMergedTracks_*_*',
# ]

process.hltOutputMinimal.fileName = '${2}.root'
EOF
  cmsRun "${2}".py &> "${2}".log
  check_log "${2}".log
}

hltGetCmd="hltGetConfiguration ${hltMenu}"
hltGetCmd+=" --globaltag auto:run3_hlt_relval --unprescale --output minimal --max-events 100"
hltGetCmd+=" --eras Run3_2025 --l1-emulator uGT --l1 L1Menu_Collisions2025_v1_2_0_xml"
hltGetCmd+=" --input file:/eos/cms/store/data/Run2024F/ParkingDoubleMuonLowMass0/RAW/v1/000/382/258/00000/0ad672e7-3358-4f27-b36b-3238a162e4fa.root"

#echo $hltGetCmd

configLabel=hlt_"${jobTag}"_only_HLT_AK8PFJetFwd40
#echo "${configLabel}".py
${hltGetCmd} --paths HLT_AK8PFJetFwd40_v30 > "${configLabel}".py
for job_i in {0..10}; do run "${configLabel}".py "${configLabel}"_"${job_i}"; done; unset job_i;

configLabel=hlt_"${jobTag}"_full
${hltGetCmd} > "${configLabel}".py
for job_i in {0..10}; do run "${configLabel}".py "${configLabel}"_"${job_i}"; done; unset job_i;
