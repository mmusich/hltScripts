#!/bin/bash

set -euo pipefail
#set -x

# List of run numbers
runs=(
    #377893 # The GlobalAlgBlk unpacker result vector is empty, but is not receiving the first expected header ID!
    #378039 # The GlobalAlgBlk unpacker result vector is empty, but is not receiving the first expected header ID!
    #378113 # The GlobalAlgBlk unpacker result vector is empty, but is not receiving the first expected header ID!
    #378366 # see https://github.com/cms-sw/cmssw/issues/44541
    #378369 # see https://github.com/cms-sw/cmssw/issues/44541
    378906
    378940
    378981
    378985
    378993
    378994
    379154
    379174
    380115
    380360
    380399
    380466
    380513
    380531
    380624
    381067
    381147
    381443
    381479
    381543
    381544
    381549
    382250
    382461
    382580
    382594
    382617
    382654
    383034
    383155
    383162
    383219
    383254
    383255
    383363
    383368
    383377
    383468
    383485
    383631
    383669
    383812
    383814
    383830
    383834
    384069
    386614
    386872
    386951
    388037
    388317
    388390
    388401
    388402
    388419
    388769
    388770
)

base_dir="/store/group/tsg/FOG/error_stream_root/run"
global_tag="150X_dataRun3_HLT_v1"
eos_cmd="eos"

# Generate base config only once
base_config="hlt_base.py"
hltGetConfiguration /dev/CMSSW_15_0_0/GRun \
  --globaltag ${global_tag} \
  --data \
  --no-prescale \
  --no-output \
  --max-events -1 \
  --eras Run3_2024 --l1-emulator uGT --l1 L1Menu_Collisions2025_v1_0_0_xml \
  --input dummy.root > ${base_config}

# Append constant options
cat <<@EOF >> ${base_config}
del process.MessageLogger
process.load('FWCore.MessageService.MessageLogger_cfi')  
process.options.wantSummary = True
process.options.numberOfThreads = 8
process.options.numberOfStreams = 8
@EOF

# Loop over runs
for run in "${runs[@]}"; do
  export MALLOC_CONF=junk:true

  input_dir="${base_dir}${run}"
  root_files=$(${eos_cmd} find -f "/eos/cms${input_dir}" -name "*.root" | awk '{print "root://eoscms.cern.ch/" $0}' | paste -sd, -)

  if [ -z "${root_files}" ]; then
    echo "No root files found for run ${run} in directory ${input_dir}."
    continue
  fi

  # Copy base config and create a run-specific config
  run_config="hlt_run${run}.py"
  cp ${base_config} ${run_config}

  # Overwrite the fileNames block by appending a new assignment at the end
  echo "process.source.fileNames = cms.untracked.vstring(" >> ${run_config}
  IFS=',' read -ra FILE_ARRAY <<< "$root_files"
  for f in "${FILE_ARRAY[@]}"; do
      echo "    '${f}'," >> ${run_config}
  done
  echo ")" >> ${run_config}

  # Run cmsRun
  log_file="hlt_run${run}.log"
  echo "Starting cmsRun for run ${run}"
  if cmsRun ${run_config} &> ${log_file}; then
    echo "Run ${run} finished successfully."
  else
    echo "Run ${run} failed. See log: ${log_file}"
  fi
done
