#!/bin/bash -e

# Tested with CMSSW_14_0_22

[ $# -eq 1 ] || exit 1

hltLabel="${1}"

inputFile=/eos/user/m/missirol/test_cmssw49056_Run2024_Muon_vbfHighMjjFailingHLT.root

thisDir=$(dirname -- "${BASH_SOURCE[0]}")

echo "Downloading HLT menu ..."
hltGetConfiguration /dev/CMSSW_14_0_0/GRun/V182 \
  --process HLTX --no-prescale --no-output \
  --data --globaltag 140X_dataRun3_HLT_v3 \
  --max-events 1 \
  --input file:"${inputFile}" \
  --paths="HLT_VBF_*,HLTAnalyzerEndpath" \
  > "${hltLabel}".py

cat <<@EOF >> "${hltLabel}".py
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
process.options.wantSummary = True

del process.dqmOutput
del process.MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.L1TGlobalSummary = cms.untracked.PSet()

process.hltL1TGlobalSummary.DumpTrigResults = True
process.hltL1TGlobalSummary.DumpTrigSummary = False

process.hltL1TGlobalSummaryEmul = process.hltL1TGlobalSummary.clone(
    AlgInputTag = 'hltGtStage2ObjectMap',
    ExtInputTag = 'hltGtStage2ObjectMap',
)

process.HLTAnalyzerEndpath += process.hltL1TGlobalSummaryEmul
@EOF

rm -f "${hltLabel}".log

for event_i in {0..19}; do
  echo "------------------------" 2>&1 | tee -a "${hltLabel}".log
  echo "${hltLabel}"_"${event_i}" 2>&1 | tee -a "${hltLabel}".log
  echo "------------------------" 2>&1 | tee -a "${hltLabel}".log

  cat <<@EOF > "${hltLabel}"_"${event_i}".py
from ${hltLabel} import cms, process
process.source.skipEvents = cms.untracked.uint32(${event_i})
@EOF

  cmsRun "${hltLabel}"_"${event_i}".py >> "${hltLabel}".log 2>&1
  rm -f "${hltLabel}"_"${event_i}".py

  "${thisDir}"/hltFWLite_exa01.py -i "${inputFile}" -v 999 -s "${event_i}" -n 1 \
    >> "${hltLabel}".log 2>&1
done

rm -rf "${hltLabel}".py __pycache__
