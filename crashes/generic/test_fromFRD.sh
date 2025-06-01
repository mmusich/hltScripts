#!/bin/bash

# cmsrel CMSSW_15_0_6
# cd CMSSW_15_0_6/src
# cmsenv
# # save this file as testFromRAW.sh
# chmod u+x test_fromFRD.sh
# ./test_fromFRD.sh 392669 4 # runNumber nThreads

[ $# -eq 2 ] || exit 1

RUNNUM="${1}"
NUMTHREADS="${2}"

ERRDIR=/eos/cms/store/group/tsg/FOG/error_stream
RUNDIR="${ERRDIR}"/run"${RUNNUM}"

for dirPath in $(ls -d "${RUNDIR}"*); do
  # require at least one non-empty FRD file
  [ $(cd "${dirPath}" ; find -maxdepth 1 -size +0 | grep .raw | wc -l) -gt 0 ] || continue
  runNumber="${dirPath: -6}"
  JOBTAG=test_run"${runNumber}"
  HLTMENU="--runNumber ${runNumber}"
  hltConfigFromDB ${HLTMENU} > "${JOBTAG}".py
  cat <<EOF >> "${JOBTAG}".py
process.options.numberOfThreads = ${NUMTHREADS}
process.options.numberOfStreams = 0
del process.PrescaleService
del process.MessageLogger
process.load('FWCore.MessageService.MessageLogger_cfi')
import os
import glob
process.source.fileListMode = True
process.source.fileNames = sorted([foo for foo in glob.glob("${dirPath}/*raw") if os.path.getsize(foo) > 0])
process.EvFDaqDirector.buBaseDir = "${ERRDIR}"
process.EvFDaqDirector.runNumber = ${runNumber}
process.hltDQMFileSaverPB.runNumber = ${runNumber}
# remove paths containing OutputModules
streamPaths = [pathName for pathName in process.endpaths_()]
for foo in streamPaths:
    process.__delattr__(foo)
EOF
  rm -rf run"${runNumber}"
  mkdir run"${runNumber}"
  echo "run${runNumber} .."
  cmsRun "${JOBTAG}".py &> "${JOBTAG}".log
  echo "run${runNumber} .. done (exit code: $?)"
  unset runNumber
done
unset dirPath
