#!/bin/bash

hltGetConfiguration run:383162 \
   --data --globaltag 140X_dataRun3_HLT_v3 \
   --no-prescale --no-output \
   --max-events -1 \
   --input \
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run383034/run383034_ls0064_index000136_fu-c2b03-22-01_pid295746.root,\
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run383034/run383034_ls0064_index000141_fu-c2b03-22-01_pid295746.root,\
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run383155/run383155_ls0942_index000173_fu-c2b14-33-01_pid712221.root,\
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run383155/run383155_ls0942_index000190_fu-c2b14-33-01_pid712221.root,\
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run383162/run383162_ls0309_index000082_fu-c2b14-15-01_pid928899.root,\
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run383162/run383162_ls0309_index000103_fu-c2b14-15-01_pid928899.root,\
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run383162/run383162_ls0595_index000278_fu-c2b02-13-01_pid3260369.root,\
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run383162/run383162_ls0595_index000305_fu-c2b02-13-01_pid3260369.root,\
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run383162/run383162_ls0595_index000332_fu-c2b02-13-01_pid3260369.root,\
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run383162/run383162_ls0660_index000089_fu-c2b14-35-01_pid920671.root,\
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run383162/run383162_ls0660_index000093_fu-c2b14-35-01_pid920671.root,\
root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run383162/run383162_ls0660_index000117_fu-c2b14-35-01_pid920671.root\
   > hlt.py

cat <<@EOF >> hlt.py

process.options.numberOfThreads = 32
process.options.numberOfStreams = 24

#del process.MessageLogger
#process.load('FWCore.MessageLogger.MessageLogger_cfi')
@EOF

CUDA_LAUNCH_BLOCKING=1 \
cmsRun hlt.py &> hlt.log
