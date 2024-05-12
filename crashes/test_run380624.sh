#!/bin/bash -ex

# CMSSW_14_0_6_MULTIARCHS

hltGetConfiguration run:380624 \
--globaltag 140X_dataRun3_HLT_v3 \
--data \
--no-prescale \
--no-output \
--max-events -1 \
--input \
/store/group/tsg/FOG/error_stream_root/run380624/run380624_ls0411_index000136_fu-c2b01-12-01_pid2375140.root,\
/store/group/tsg/FOG/error_stream_root/run380624/run380624_ls0411_index000145_fu-c2b01-12-01_pid2375140.root,\
/store/group/tsg/FOG/error_stream_root/run380624/run380624_ls0411_index000164_fu-c2b01-12-01_pid2375140.root \
 > hlt.py

cat <<@EOF >> hlt.py
process.options.wantSummary = True
process.options.numberOfThreads = 8
process.options.numberOfStreams = 6
@EOF

cmsRun hlt.py &> hlt.log
