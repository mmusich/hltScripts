#!/bin/bash -ex

# CMSSW_14_0_12_MULTIARCHS

hltGetConfiguration run:383830 \
		    --globaltag 140X_dataRun3_HLT_v3 \
		    --data \
		    --no-prescale \
		    --no-output \
		    --max-events -1 \
		    --input /store/group/tsg/FOG/error_stream_root/run383830/run383830_ls0083_index000316_fu-c2b01-26-01_pid4060272.root > hlt.py

cat <<@EOF >> hlt.py
try:
    del process.MessageLogger
    process.load('FWCore.MessageLogger.MessageLogger_cfi')
    process.MessageLogger.cerr.enableStatistics = False
except:
    pass

process.source.skipEvents = cms.untracked.uint32( 74 )
process.options.wantSummary = True
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
#process.options.accelerators = ['cpu']
#process.options.accelerators = ['gpu-nvidia']
@EOF

cmsRun hlt.py &> hlt.log
