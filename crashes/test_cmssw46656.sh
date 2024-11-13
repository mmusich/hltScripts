#!/bin/bash -ex

# cmsrel CMSSW_14_1_4_patch3
# cd CMSSW_14_1_4_patch3/src
# cmsenv

hltGetConfiguration run:388037 \
		    --globaltag 141X_dataRun3_HLT_v1 \
		    --data \
		    --no-prescale \
		    --no-output \
		    --max-events -1 \
		    --input /store/group/tsg/FOG/error_stream_root/run388037/run388037_ls0133_index000200_fu-c2b05-14-01_pid3769082.root,/store/group/tsg/FOG/error_stream_root/run388037/run388037_ls0133_index000203_fu-c2b05-14-01_pid3769082.root,/store/group/tsg/FOG/error_stream_root/run388037/run388037_ls0133_index000214_fu-c2b05-14-01_pid3769082.root > hlt_388037.py

cat <<@EOF >> hlt_388037.py
process.options.wantSummary = True
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
@EOF

cmsRun hlt_388037.py &> hlt_388037.log
