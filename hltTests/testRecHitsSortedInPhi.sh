#!/bin/bash

outDir=tmpTest11834

for theJobId in {1..40}; do
  theJobId=$(printf "%02d" ${theJobId})
  echo step2_"${theJobId}"
  mkdir -p "${outDir}"/"${theJobId}"
  cd "${outDir}"/"${theJobId}"
  cp -p ../../step2.py .
  cmsRun step2.py &> step2_"${theJobId}".log
  cd "${OLDPWD}"
  [ $(grep -ie TrajectoryNaN -e RecHitsSortedInPhi -e 'fatal system signal' "${OLDPWD}"/step2_"${theJobId}".log | wc -l) -gt 0 ] || (rm -rf "${OLDPWD}")
done; unset theJobId
unset outDir
