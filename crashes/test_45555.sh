#!/bin/bash -ex

# CMSSW_14_0_11_MULTIARCHS

hltGetConfiguration run:383631 \
--globaltag 140X_dataRun3_HLT_v3 \
--data \
--no-prescale \
--no-output \
--max-events -1 \
--input '/store/group/tsg/FOG/error_stream_root/run383631/run383631_ls0444_index000423_fu-c2b14-43-01_pid675389.root,/store/group/tsg/FOG/error_stream_root/run383631/run383631_ls0445_index000025_fu-c2b14-43-01_pid675389.root,/store/group/tsg/FOG/error_stream_root/run383631/run383631_ls0666_index000047_fu-c2b14-43-01_pid675067.root,/store/group/tsg/FOG/error_stream_root/run383631/run383631_ls0445_index000002_fu-c2b14-43-01_pid675389.root,/store/group/tsg/FOG/error_stream_root/run383631/run383631_ls0666_index000027_fu-c2b14-43-01_pid675067.root,/store/group/tsg/FOG/error_stream_root/run383631/run383631_ls0666_index000065_fu-c2b14-43-01_pid675067.root' > hlt.py

cat <<@EOF >> hlt.py
#del process.MessageLogger
#process.load('FWCore.MessageService.MessageLogger_cfi')  
#process.options.wantSummary = True
#process.options.numberOfThreads = 1
#process.options.numberOfStreams = 0
process.hltOnlineBeamSpotESProducer.timeThreshold = int(0)
#process.options.accelerators = ['cpu']
process.options.wantSummary = True
process.options.numberOfThreads = 32
process.options.numberOfStreams = 32
@EOF

cmsRun hlt.py &> hlt.log


