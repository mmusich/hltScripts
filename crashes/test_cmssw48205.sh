#!/bin/bash -ex

# Get the run number from the first argument
RUN_NUMBER=392669

# Define the directory with the given run number
DIR="/store/group/tsg/FOG/error_stream_root/run${RUN_NUMBER}"

file_list="$DIR/run392669_ls0110_index000333_fu-c2b02-06-01_pid3861299.root"

# Print the result
echo "$file_list"

hltGetConfiguration run:$RUN_NUMBER \
		    --globaltag 150X_dataRun3_HLT_v1 \
		    --data \
		    --no-prescale \
		    --no-output \
		    --max-events -1 \
		    --paths "HLT_DiPFJetAve180_PPSMatch_Xi0p3_QuadJet_Max2ProtPerRP_v*" \
		    --input $file_list  > hlt_${RUN_NUMBER}.py

cat <<@EOF >> hlt_${RUN_NUMBER}.py
process.GlobalTag.recordsToDebug = cms.untracked.vstring()
del process.MessageLogger
process.load('FWCore.MessageService.MessageLogger_cfi')  
process.options.wantSummary = True
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
@EOF

# Run cmsRun with the generated configuration
for i in $(seq -w 1 100); do
    echo "Starting run $i..."
    log_file="log_${i}.txt"
    cmsRun hlt_${RUN_NUMBER}.py > "$log_file" 2>&1
    status=$?
    echo "Run $i finished with exit code $status" >> "$log_file"
    echo "Finished run $i (exit code $status)"
done

