#!/bin/bash -ex

# List of run numbers
runs=(
  380399
  380624
  381067
  381190
  381286
  381443
  381479
  381417
  381543
  381544
)

# Base directory for input files on EOS
base_dir="/store/group/tsg/FOG/error_stream_root/run"

# Global tag for the HLT configuration
global_tag="140X_dataRun3_HLT_v3"

# EOS command (adjust this if necessary for your environment)
eos_cmd="eos"

# Initialize the root_files variable
root_files=""

# Loop over each run number
for run in "${runs[@]}"; do
  # Construct the input directory path
  input_dir="${base_dir}${run}"

  # Find all root files in the input directory on EOS
  run_root_files=$(${eos_cmd} find -f "/eos/cms${input_dir}" -name "*.root" | awk '{print "root://eoscms.cern.ch/" $0}' | paste -sd, -)

  # Check if there are any root files found
  if [ -z "${run_root_files}" ]; then
    echo "No root files found for run ${run} in directory ${input_dir}."
    continue
  fi

  # Append the run_root_files to the root_files variable
  if [ -z "${root_files}" ]; then
    root_files="${run_root_files}"
  else
    root_files="${root_files},${run_root_files}"
  fi
done

# Print the combined root_files variable
echo "All root files: ${root_files}"

# Generate the HLT configuration file
hltGetConfiguration /online/collisions/2024/2e34/v1.4/HLT/V2 \
    --globaltag ${global_tag} \
    --data \
    --eras Run3 \
    --l1-emulator uGT \
    --l1 L1Menu_Collisions2024_v1_3_0_xml \
    --no-prescale \
    --output minimal \
    --max-events -1 \
    --input ${root_files} > hlt_data.py

cat <<@EOF >> hlt_data.py
process.options.wantSummary = True
process.options.numberOfThreads = 32
process.options.numberOfStreams = 32
process.options.accelerators = ['cpu']
@EOF

# Loop to run the command 10 times
for i in {1..2}; do
  # Define the log file name and output file name based on the index
  log_file="hlt_data_${i}.log"
  output_file="output_${i}.root"

  # Run the cmsRun command and redirect output to the log file
  cmsRun hlt_data.py >& "$log_file"

  # Move the output file to the new name
  mv output.root "$output_file"
done
