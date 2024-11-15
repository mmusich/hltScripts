#!/bin/bash -ex

INPUTDIR=/afs/cern.ch/work/m/missirol/public/fog/error_stream/run375440

hltGetConfiguration \
  run:388317 \
  --globaltag 141X_dataRun3_HLT_v1 \
  --data \
  --no-prescale \
  --no-output \
  --paths HLT_HIMinimumBiasHF1ANDZDC1nOR_v* \
  --input file:tmp.root \
   > hlt.py

for inputfile in $(ls "${INPUTDIR}"/*.root); do
  jobLabel=hlt_$(basename ${inputfile/.root/})
  echo "${jobLabel} ..."
  cp hlt.py "${jobLabel}".py
  cat <<@EOF >> "${jobLabel}".py
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

del process.MessageLogger
process.load('FWCore.MessageService.MessageLogger_cfi')  
process.source.fileNames = ["file:${inputfile}"]
@EOF
  cmsRun "${jobLabel}".py &> "${jobLabel}".log
done
unset inputfile jobLabel
