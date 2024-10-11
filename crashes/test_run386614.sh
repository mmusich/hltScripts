#!/bin/bash -ex

#in CMSSW_14_0_15_patch1

hltGetConfiguration run:386614 \
		    --globaltag 140X_dataRun3_HLT_v3 \
		    --data \
		    --no-prescale \
		    --no-output \
		    --max-events -1 \
		    --input /store/group/tsg/FOG/error_stream_root/run386614/run386614_ls0055_index000003_fu-c2b02-33-01_pid4022333.root,/store/group/tsg/FOG/error_stream_root/run386614/run386614_ls0055_index000005_fu-c2b04-26-01_pid18256.root,/store/group/tsg/FOG/error_stream_root/run386614/run386614_ls0055_index000019_fu-c2b04-26-01_pid18256.root,/store/group/tsg/FOG/error_stream_root/run386614/run386614_ls0055_index000027_fu-c2b02-33-01_pid4022333.root,/store/group/tsg/FOG/error_stream_root/run386614/run386614_ls0055_index000033_fu-c2b04-26-01_pid18256.root,/store/group/tsg/FOG/error_stream_root/run386614/run386614_ls0055_index000062_fu-c2b02-12-01_pid399919.root,/store/group/tsg/FOG/error_stream_root/run386614/run386614_ls0055_index000078_fu-c2b02-12-01_pid399919.root,/store/group/tsg/FOG/error_stream_root/run386614/run386614_ls0055_index000156_fu-c2b02-33-01_pid4022422.root,/store/group/tsg/FOG/error_stream_root/run386614/run386614_ls0056_index000023_fu-c2b03-34-01_pid3391489.root,/store/group/tsg/FOG/error_stream_root/run386614/run386614_ls0056_index000046_fu-c2b03-34-01_pid3391489.root,/store/group/tsg/FOG/error_stream_root/run386614/run386614_ls0056_index000101_fu-c2b14-11-01_pid2066514.root,/store/group/tsg/FOG/error_stream_root/run386614/run386614_ls0056_index000138_fu-c2b01-36-01_pid984863.root,/store/group/tsg/FOG/error_stream_root/run386614/run386614_ls0056_index000152_fu-c2b01-36-01_pid984863.root,/store/group/tsg/FOG/error_stream_root/run386614/run386614_ls0057_index000266_fu-c2b01-12-01_pid3143597.root,/store/group/tsg/FOG/error_stream_root/run386614/run386614_ls0057_index000277_fu-c2b01-12-01_pid3143597.root > hlt_386614.py

cat <<@EOF >> hlt_386614.py
process.options.wantSummary = True
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
@EOF

cmsRun hlt_386614.py &> hlt_386614.log
