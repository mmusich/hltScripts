#!/bin/bash

# cmsrel CMSSW_13_0_5_patch1
# cd CMSSW_13_0_5_patch1/src
# cmsenv

JOBTAG=test_cmssw41512_v01

HLTMENU="--adg /cdaq/test/missirol/test/2023/week18/CMSLITOPS_411/Test02/HLT"

INPUTDIR=/eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/FOG/error_stream/run366727

hltConfigFromDB --configName ${HLTMENU} > "${JOBTAG}".py

for dirPath in $(ls -d "${INPUTDIR}"*); do
  # require at least one non-empty FRD file
  [ $(cd "${dirPath}" ; find -maxdepth 1 -size +0 | grep .raw | wc -l) -gt 0 ] || continue

  runNumber="${dirPath: -6}"
  cp "${JOBTAG}".py "${JOBTAG}"_run"${runNumber}".py
  cat <<EOF >> "${JOBTAG}"_run"${runNumber}".py
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
process.options.wantSummary = True

process.hltOnlineBeamSpotESProducer.timeThreshold = int(1e6)

del process.MessageLogger
process.load('FWCore.MessageService.MessageLogger_cfi')

import os
import glob
process.source.fileListMode = True
process.source.fileNames = sorted([foo for foo in glob.glob("${dirPath}/*raw") if os.path.getsize(foo) > 0])
process.source.eventChunkSize = 200
process.source.eventChunkBlock = 200
process.source.numBuffers = 1
process.source.maxBufferedFiles = 1

process.EvFDaqDirector.runNumber = ${runNumber}
EOF
  rm -rf run"${runNumber}"
  mkdir run"${runNumber}"
  echo run"${runNumber}" ..
  cmsRun "${JOBTAG}"_run"${runNumber}".py &> "${JOBTAG}"_run"${runNumber}".log
  echo "run${runNumber} .. done (exit code: $?)"
  unset runNumber
done
unset dirPath
