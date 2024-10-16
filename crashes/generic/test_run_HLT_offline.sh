#!/bin/bash -ex

# Check if the run number is provided as an argument
if [ $# -lt 1 ]; then
    echo "Usage: $0 <run_number>"
    exit 1
fi

# Get the run number from the first argument
RUN_NUMBER=$1

# Define the directory with the given run number
DIR="/store/group/tsg/FOG/error_stream_root/run${RUN_NUMBER}/"

# Generate a comma-separated list of the full file paths
file_list=$(ls "/eos/cms$DIR" | awk -v dir="$DIR" '{print dir $0}' | paste -sd "," -)

# Print the result
echo "$file_list"

hltGetConfiguration run:$RUN_NUMBER \
		    --globaltag 140X_dataRun3_HLT_v3 \
		    --data \
		    --no-prescale \
		    --no-output \
		    --max-events -1 \
		    --input $file_list  > hlt_${RUN_NUMBER}.py

cat <<@EOF >> hlt_${RUN_NUMBER}.py
process.options.wantSummary = True
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
@EOF

# Run cmsRun with the generated configuration
cmsRun hlt_${RUN_NUMBER}.py &> hlt_${RUN_NUMBER}.log
