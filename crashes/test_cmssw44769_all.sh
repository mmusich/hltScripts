#!/bin/bash

[ $# -eq 2 ] || exit 1

fileNames=($(cat "${1}"))

rm -rf "${2}"
mkdir -p "${2}"
cp "${1}" "${2}"
cd "${2}"

https_proxy=http://cmsproxy.cms:3128/ \
hltGetConfiguration run:379617 \
  --globaltag 140X_dataRun3_HLT_v3 \
  --data \
  --no-prescale \
  --no-output \
  --max-events -1 \
  --input foo.root > hlt.py

cat <<@EOF >> hlt.py

if hasattr(process, 'HLTAnalyzerEndpath'):
    del process.HLTAnalyzerEndpath

for out_mod_label, out_mod in process.outputModules_().items():
  try: out_mod.SelectEvents.SelectEvents = ['HLTriggerFirstPath']
  except: pass

del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')

process.options.numberOfThreads = 32
process.options.numberOfStreams = 32

process.options.wantSummary = True
@EOF

for fileName in "${fileNames[@]}"; do

  jobLabel=$(basename ${fileName})
  jobLabel=${jobLabel/.root/}

  cp hlt.py "${jobLabel}"_cfg.py

  cat <<@EOF >> "${jobLabel}"_cfg.py

process.source.fileNames = ["root://eoscms.cern.ch//eos/cms/${fileName}"]
@EOF

  echo "${jobLabel} ..."
  cmsRun "${jobLabel}"_cfg.py &> "${jobLabel}".log
  exitCode=$?
  [ ${exitCode} -eq 0 ] || echo "${jobLabel}".log >> failed.txt
  echo "${jobLabel} ... done (exit code: ${exitCode})"

done
unset fileName
