#!/bin/bash -ex

# List of run numbers
runs=(
    388769
    388770
)

# Base directory for input files on EOS
base_dir="/store/group/tsg/FOG/error_stream_root/run"

# Global tag for the HLT configuration
global_tag="141X_dataRun3_HLT_v2"

# EOS command (adjust this if necessary for your environment)
eos_cmd="eos"

# Loop over each run number
for run in "${runs[@]}"; do

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
  hltGetConfiguration run:${run} \
    --globaltag ${global_tag} \
    --data \
    --no-prescale \
    --no-output \
    --max-events -1 \
    --path HLT_HIUPC_DoubleEG5_BptxAND_SinglePixelTrack_MaxPixelTrack_v* \
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

