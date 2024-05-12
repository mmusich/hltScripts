#!/bin/bash -ex

# CMSSW_14_0_6_MULTIARCHS

run=$1

hltGetConfiguration run:${run} \
  --globaltag 140X_dataRun3_HLT_v3 \
  --data \
  --no-prescale \
  --no-output \
  --max-events -1 \
  --input file:converted.root  > hlt.py

cat <<@EOF >> hlt.py
process.options.wantSummary = True

process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
@EOF

for inputfile in $(eos ls /eos/cms/store/group/tsg/FOG/error_stream_root/run${run}/ | grep '\.root$'); do
    outputfile="${inputfile%.root}"
    cp hlt.py hlt_toRun.py
    sed -i "s/file:converted\.root/\/store\/group\/tsg\/FOG\/error_stream_root\/run${run}\/${inputfile}/g" hlt_toRun.py
    cmsRun hlt_toRun.py &> "${outputfile}.log"
done
