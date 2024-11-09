#!/bin/bash -ex

# cmsrel CMSSW_14_1_4_patch3
# cd CMSSW_14_1_4_patch3/src
# cmsenv
# scram b

# run 387968, LS 
INPUTFILE=root://eoscms.cern.ch//eos/cms/tier0/store/hidata/HIRun2024A/HIMinimumBias0/RAW/v1/000/387/968/00000/779d1a75-b20c-4ad6-ab4a-4e049fe61765.root

HLTMENU=/dev/CMSSW_14_1_0/HIon/V44

rm -rf run387968*

# run on 100 events of LS 100-110, with 100 events per input file
convertToRaw -f 100 -l 100 -r 387968:100 -s rawDataRepacker -o . -- "${INPUTFILE}"

tmpfile=$(mktemp)
hltConfigFromDB --configName "${HLTMENU}" > "${tmpfile}"
sed -i 's|process = cms.Process( "HLT" )|from Configuration.Eras.Era_Run3_cff import Run3\nprocess = cms.Process( "HLT", Run3 )|g' "${tmpfile}"
cat <<@EOF >> "${tmpfile}"
process.load('run387968_cff')
process.hltOnlineBeamSpotESProducer.timeThreshold = int(1e6)

# override the GlobalTag, connection string and pfnPrefix
from Configuration.AlCa.GlobalTag import GlobalTag as customiseGlobalTag
process.GlobalTag = customiseGlobalTag(
    process.GlobalTag,
    globaltag = "141X_dataRun3_HLT_v1",
    conditions = "L1Menu_CollisionsHeavyIons2024_v1_0_5_xml,L1TUtmTriggerMenuRcd,frontier://FrontierProd/CMS_CONDITIONS,,9999-12-31 23:59:59.000"
)

process.datasets.HIOnlineMonitor += 'HLT_HIZeroBias_FirstCollisionAfterAbortGap_v14'
process.hltDatasetHIOnlineMonitor.triggerConditions = cms.vstring('HLT_HICentrality50100MinimumBiasHF1AND_Beamspot_v1','HLT_HIZeroBias_FirstCollisionAfterAbortGap_v14')
process.options.wantSummary = cms.untracked.bool(True)
process.hltL1sCentrality50100MinimumBiasHF1ANDBptxAND.L1SeedsLogicalExpression = cms.string('L1GlobalDecision')
#'L1_Centrality_30_100_MinimumBiasHF1_AND_BptxAND'),

process.hltOutputHIDQM.outputCommands += [
    'keep *_hltSiPixelClustersAfterSplittingPPOnAA_*_*',
    'keep *_hltPixelTracksPPOnAA_*_*',
    'keep *_hltHITrackingSiStripRawToClustersFacilityFullZeroSuppression_*_*',
    'keep *_hltDoubletRecoveryPFlowTrackSelectionHighPurityPPOnAA_*_*',
    'keep *_hltPixelVerticesPPOnAA_*_*',
    'keep *_hltTrimmedPixelVerticesPPOnAA_*_*',
    'keep *_hltVerticesPFFilterPPOnAA_*_*',
    'keep *_hltPFMuonMergingPPOnAA_*_*'
]

# run the Full L1T emulator, then repack the data into a new RAW collection, to be used by the HLT
from HLTrigger.Configuration.CustomConfigs import L1REPACK
process = L1REPACK(process, "uGT")

# Multi-threading
process.options.numberOfConcurrentLuminosityBlocks = 2      # default: 2
process.options.numberOfStreams = 32                        # default: 32
process.options.numberOfThreads = 32                        # default: 32

# to run without any HLT prescales
del process.PrescaleService

# to reset the MessageLogger (and print at every event)
del process.MessageLogger
process.load('FWCore.MessageService.MessageLogger_cfi')  

# # to run using the same HLT prescales as used online in LS 231
# process.PrescaleService.forceDefault = True
@EOF
edmConfigDump "${tmpfile}" > hlt.py

cmsRun hlt.py &> hlt.log

# remove input files to save space
rm -f run387968/run387968_ls0*_index*.*

#######################################################
# After this, prepare the streamer files with the following recipe:
#######################################################

mv run387968 source
mkdir -p run387968
cp source/run387968_ls0100_streamHIDQM_*.jsn run387968
for file in source/run387968_ls0000_streamHIDQM_*.ini; do
    # Extract the variable part in place of '*'
    variable_part=$(basename "$file" | sed 's/^run387968_ls0000_streamHIDQM_//; s/\.ini$//')

    # Concatenate files with the same variable part
    cat "source/run387968_ls0000_streamHIDQM_${variable_part}.ini" \
        "source/run387968_ls0100_streamHIDQM_${variable_part}.dat" \
        > "run387968/run387968_ls0100_streamHIDQM_${variable_part}.dat"
done

# edit the jsn file to not have 2 "0"s in it.
# finally run the client
# cmsRun DQM/Integration/python/clients/hlt_dqm_sourceclient-live_cfg.py runInputDir=. outputBaseDir=./output runNumber=387968 runkey=hi_run scanOnce=True
