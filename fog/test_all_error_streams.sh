#!/bin/bash

# List of run numbers
runs=(377893
      378039
      378113
      378366
      378369
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
      383363
      383368
      383377)

# Base directory for input files on EOS
base_dir="/store/group/tsg/FOG/error_stream_root/run"

# Global tag for the HLT configuration
global_tag="140X_dataRun3_HLT_v3"

# EOS command (adjust this if necessary for your environment)
eos_cmd="eos"

# Loop over each run number
for run in "${runs[@]}"; do
  # Set the MALLOC_CONF environment variable
  # export MALLOC_CONF=junk:true

  # Construct the input directory path
  input_dir="${base_dir}${run}"

  # Find all root files in the input directory on EOS
  root_files=$(${eos_cmd} find -f "/eos/cms${input_dir}" -name "*.root" | awk '{print "root://eoscms.cern.ch/" $0}' | paste -sd, -)

  # Check if there are any root files found
  if [ -z "${root_files}" ]; then
    echo "No root files found for run ${run} in directory ${input_dir}."
    continue
  fi

  # Create filenames for the HLT configuration and log file
  hlt_config_file="hlt_run${run}.py"
  hlt_log_file="hlt_run${run}.log"

  # Generate the HLT configuration file
  hltGetConfiguration /online/collisions/2024/2e34/v1.4/HLT/V2 \
    --globaltag ${global_tag} \
    --data \
    --eras Run3 \
    --l1-emulator uGT \
    --l1 L1Menu_Collisions2024_v1_3_0_xml \
    --no-prescale \
    --no-output \
    --max-events -1 \
    --input ${root_files} > ${hlt_config_file}

  # Append additional options to the configuration file
  cat <<@EOF >> ${hlt_config_file}
del process.MessageLogger
process.load('FWCore.MessageService.MessageLogger_cfi')  
process.options.wantSummary = True
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
@EOF

# Run the HLT configuration with cmsRun and redirect output to log file
cmsRun ${hlt_config_file} &> ${hlt_log_file}

done
