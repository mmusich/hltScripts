#!/bin/bash -ex

# CMSSW_14_0_9_patch2_MULTIARCHS + merging locall #45342.

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
  hltGetConfiguration run:${run} \
    --globaltag ${global_tag} \
    --data \
    --no-prescale \
    --no-output \
    --max-events -1 \
    --input ${root_files} > ${hlt_config_file}

  # Append additional options to the configuration file
  cat <<@EOF >> ${hlt_config_file}
del process.MessageLogger
process.load('FWCore.MessageService.MessageLogger_cfi')  
process.MessageLogger.CUDAService = {}
process.MessageLogger.AlpakaService = {}
process.load('HeterogeneousCore.CUDAServices.CUDAService_cfi')
from HeterogeneousCore.AlpakaServices.AlpakaServiceCudaAsync_cfi import AlpakaServiceCudaAsync as _AlpakaServiceCudaAsync
process.AlpakaServiceCudaAsync = _AlpakaServiceCudaAsync.clone(
    verbose = True,
    hostAllocator = dict(
	binGrowth = 2,
	minBin = 8,                           # 256 bytes
	maxBin = 30,                          #   1 GB
	maxCachedBytes = 64*1024*1024*1024,   #  64 GB
	maxCachedFraction = 0.8,              # or 80%, whatever is less
	fillAllocations = True,
	fillAllocationValue = 0xA5,
	fillReallocations = True,
	fillReallocationValue = 0x69,
	fillDeallocations = True,
	fillDeallocationValue = 0x5A,
	fillCaches = True,
	fillCacheValue = 0x96
    ),
    deviceAllocator = dict(
	binGrowth = 2,
	minBin = 8,                           # 256 bytes
	maxBin = 30,                          #   1 GB
	maxCachedBytes = 8*1024*1024*1024,    #   8 GB
	maxCachedFraction = 0.8,              # or 80%, whatever is less
	fillAllocations = True,
	fillAllocationValue = 0xA5,
	fillReallocations = True,
	fillReallocationValue = 0x69,
	fillDeallocations = True,
	fillDeallocationValue = 0x5A,
	fillCaches = True,
	fillCacheValue = 0x96
    )
)
process.options.wantSummary = True
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
@EOF

# Run the HLT configuration with cmsRun and redirect output to log file
cmsRun ${hlt_config_file} &> ${hlt_log_file}

done
