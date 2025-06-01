#!/bin/bash -ex                                                                                                                                                                                             

# cmsrel CMSSW_15_0_6                                                                                                                                                                                       
# cd CMSSW_15_0_6/src                                                                                                                                                                                       
# cmsenv                                                                                                                                                                                                    

[ $# -ge 1 ] || exit 1

# Get the run number from the first argument                                                                                                                                                                
RUN_NUMBER=$1

# Define the directory with the given run number                                                                                                                                                            
DIR="/store/group/tsg/FOG/error_stream_root/run${RUN_NUMBER}/"

# Generate a comma-separated list of the full file paths                                                                                                                                                    
file_list=$(ls "/eos/cms$DIR" | awk -v dir="$DIR" '{print dir $0}' | paste -sd "," -)

# Print the result                                                                                                                                                                                          
echo "$file_list"

#export MALLOC_CONF=junk:true

hltGetConfiguration \
 run:${RUN_NUMBER} \
 --globaltag 150X_dataRun3_HLT_v1 \
 --data \
 --no-prescale \
 --no-output \
 --max-events -1 \
 --input $file_list  > hlt_${RUN_NUMBER}.py

cat <<@EOF >> hlt_${RUN_NUMBER}.py
process.GlobalTag.recordsToDebug = cms.untracked.vstring()

process.options.wantSummary = True
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
@EOF

# Run cmsRun with the generated configuration
cmsRun hlt_${RUN_NUMBER}.py &> hlt_${RUN_NUMBER}.log
