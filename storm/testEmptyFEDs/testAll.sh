#!/bin/bash -ex

# Function to generate HLT configuration and customize the script
generate_hlt_config() {
  local output_script=$1
  local input_file=$2
  local replace_raw_data=$3

  hltGetConfiguration /dev/CMSSW_14_0_0/GRun/V169 \
                      --data \
                      --unprescale \
                      --globaltag 140X_dataRun3_HLT_v3 \
                      --max-events 100 \
                      --eras Run3_2024 \
                      --l1-emulator uGT \
                      --output minimal \
                      --l1 L1Menu_Collisions2024_v1_3_0_xml \
                      --input "${input_file}" > "${output_script}"

  if [ "$replace_raw_data" = true ]; then
    sed -i 's/rawDataCollector/rawDataNOTracker/g' "${output_script}"
  fi

  cat <<@EOF >> "${output_script}"
try:
    del process.MessageLogger
    process.load('FWCore.MessageLogger.MessageLogger_cfi')
    process.MessageLogger.cerr.enableStatistics = False
except:
    pass
process.hltGtStage2Digis.InputLabel = cms.InputTag( "rawDataCollector" )
@EOF
}

# Generate the first HLT configuration script with custom input and rawData modification
generate_hlt_config "hltDataNoTracker.py" "file:tmp.root" true

# Run the first HLT configuration script
cmsRun hltDataNoTracker.py &> hlt.log &
mv output.root output_noTracker.root

# Generate the second HLT configuration script with another custom input
generate_hlt_config "hlt.py" "root://eoscms.cern.ch//eos/cms/store/data/Run2024F/EphemeralHLTPhysics0/RAW/v1/000/382/250/00000/d69c0220-8282-496c-8e88-2fb663a43ea5.root" false

# Run the second HLT configuration script
cmsRun hlt.py &> hlt2.log
