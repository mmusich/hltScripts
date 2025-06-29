#!/bin/bash

hltLabel=testCMSHLT3574

hltGetConfiguration \
  /dev/CMSSW_15_0_0/GRun/V89 \
  --globaltag 150X_dataRun3_HLT_v1 \
  --data \
  --unprescale \
  --output minimal \
  --max-events 1000 \
  --input /store/data/Run2025C/JetMET0/RAW/v1/000/393/461/00000/8679bae3-9fe8-4ec6-99f4-c1120ce36d1d.root \
  --paths MC_*Tracking* \
  > "${hltLabel}".py

cat <<@EOF >> "${hltLabel}".py
process.options.numberOfThreads = 1
process.hltOutputMinimal.outputCommands += [
  'keep *_hltDoubletRecoveryPFlowCtfWithMaterialTracks_*_HLTX',
  'keep *_hltMergedTracks_*_HLTX',
]
process.hltOutputMinimal.fileName = '${hltLabel}.root'

del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')
@EOF

cmsRun "${hltLabel}".py 2>&1 | tee "${hltLabel}".log
