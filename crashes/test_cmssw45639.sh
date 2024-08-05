#!/bin/bash -ex

# CMSSW_14_0_13_MULTIARCHS

hltGetConfiguration run:384069 \
--globaltag 140X_dataRun3_HLT_v3 \
--data \
--no-prescale \
--no-output \
--max-events -1 \
--input '/store/group/tsg/FOG/error_stream_root/run384069/run384069_ls0689_index000033_fu-c2b04-35-01_pid2378323.root,/store/group/tsg/FOG/error_stream_root/run384069/run384069_ls0689_index000067_fu-c2b04-35-01_pid2378323.root' > hlt.py

cat <<@EOF >> hlt.py
del process.MessageLogger
process.load('FWCore.MessageService.MessageLogger_cfi')  
process.options.wantSummary = True
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
process.source.skipEvents = cms.untracked.uint32( 44 )
#process.hltOnlineBeamSpotESProducer.timeThreshold = int(0)
#process.options.accelerators = ['cpu']
@EOF

cmsRun hlt.py &> hlt.log


