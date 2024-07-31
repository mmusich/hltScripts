#!/bin/bash

## use old HLT menu (HCAL Legacy/CUDA)
#hltMenu="run:383631"
#hltLabel=hlt_oldMenu_cpu

## use latest HLT menu (HCAL Alpaka)
#hltMenu="run:383830"
#hltLabel=hlt_newMenu_cpu

# use latest HLT menu (HCAL Alpaka)
hltMenu="adg:/cdaq/test/missirol/dev/CMSSW_14_0_0/tmp/240731_cmssw45595/Test01/HLT/V2"
hltLabel=hlt_fixMenu_cpu

https_proxy=http://cmsproxy.cms:3128/ \
hltGetConfiguration "${hltMenu}" \
  --globaltag 140X_dataRun3_HLT_v3 \
  --no-prescale \
  --output minimal \
  --max-events 1 \
  --paths DQM_Hcal* \
  --input root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run383830/run383830_ls0083_index000316_fu-c2b01-26-01_pid4060272.root \
  > "${hltLabel}".py

cat <<@EOF >> "${hltLabel}".py
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

process.source.skipEvents = cms.untracked.uint32( 74 )

#process.options.accelerators = ['cpu']

process.hltHcalConsumerCPU = cms.EDAnalyzer("GenericConsumer",
    eventProducts = cms.untracked.vstring('hltHbhereco'),
)

process.dummyPath = cms.Path(
    process.HLTDoLocalHcalSequence
  + process.HLTPFHcalClustering
  + process.hltHcalConsumerCPU
)

process.schedule = cms.Schedule( process.dummyPath, process.MinimalOutput )

del process.MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.hltOutputMinimal.fileName = '${hltLabel}.root'

process.hltOutputMinimal.outputCommands = [
   'drop *',
   'keep *_hltHbhereco_*_*',
]
@EOF

CUDA_LAUNCH_BLOCKING=1 \
cmsRun "${hltLabel}".py &> "${hltLabel}".log
