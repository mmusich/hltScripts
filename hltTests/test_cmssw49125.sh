#!/bin/bash -x

RUN_NUMBER=398308

hltGetConfiguration \
  run:"${RUN_NUMBER}" \
  --globaltag 150X_dataRun3_HLT_v1 \
  --data \
  --no-prescale \
  --no-output \
  --max-events 100 \
  --paths DQM_Pixel* \
  --input /store/group/tsg/FOG/error_stream_root/run398308/run398308_ls0169_index000384_fu-c2b14-17-01_pid4164345.root \
  > hlt_"${RUN_NUMBER}".py

cat <<@EOF >> hlt_"${RUN_NUMBER}".py
process.options.wantSummary = False
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

#process.hltSiPixelClustersSoA.DoDigiMorphing = False
#process.hltSiPixelClustersSoASerialSync.DoDigiMorphing = False
@EOF

cmsRun hlt_"${RUN_NUMBER}".py &> hlt_"${RUN_NUMBER}".log

compute-sanitizer --tool=racecheck --racecheck-report=all \
cmsRun hlt_"${RUN_NUMBER}".py &> hlt_"${RUN_NUMBER}"_racecheck.log

compute-sanitizer --tool=memcheck \
cmsRun hlt_"${RUN_NUMBER}".py &> hlt_"${RUN_NUMBER}"_memcheck.log

compute-sanitizer --tool=initcheck \
cmsRun hlt_"${RUN_NUMBER}".py &> hlt_"${RUN_NUMBER}"_initcheck.log

compute-sanitizer --tool=synccheck \
cmsRun hlt_"${RUN_NUMBER}".py &> hlt_"${RUN_NUMBER}"_synccheck.log
