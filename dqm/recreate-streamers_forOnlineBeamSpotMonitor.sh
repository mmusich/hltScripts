#!/bin/bash -ex

# cmsrel CMSSW_15_1_X_2025-02-19-2300 
# cd CMSSW_15_1_X_2025-02-19-2300/src
# git cms-addpkg HLTrigger/Configuration
# git remote add mmusich git@github.com:mmusich/cmssw.git
# git fetch mmusich
# git cherry-pick c751843605c5e7bc2e9095276088bb9b721dcbe8
# cmsenv
# scram b

RUNNUMBER=381594
LUMISECTION=1000

INPUTFILE=root://eoscms.cern.ch//store/express/Run2024E/ExpressPhysics/FEVT/Express-v1/000/381/594/00000/1e2c895f-a250-45be-a7ff-ee95e636a6e9.root
rm -rf run${RUNNUMBER}*

# run on 1000 events of LS 1000, with 1000 events per input file
convertToRaw -f 1000 -l 1000 -r ${RUNNUMBER}:${LUMISECTION} -o . -- "${INPUTFILE}"

tmpfile=$(mktemp)
hltConfigFromDB --runNumber "${RUNNUMBER}" > "${tmpfile}"
cat <<@EOF >> "${tmpfile}"
process.load("run${RUNNUMBER}_cff")
process.hltOnlineBeamSpotESProducer.timeThreshold = int(1e6)

# to run without any HLT prescales
del process.PrescaleService
del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')

process.options.numberOfThreads = 32
process.options.numberOfStreams = 32

process.options.wantSummary = True
# # to run using the same HLT prescales as used online in LS 1000
# process.PrescaleService.forceDefault = True

# apply extra customisations specific to the CMSSW release in use
from HLTrigger.Configuration.customizeHLTforCMSSW import customizeHLTforCMSSW
process = customizeHLTforCMSSW(process)

process.hltOutputDQM.outputCommands = cms.untracked.vstring( 'drop *',
							     'keep *_hltOnlineBeamSpot_*_*')
@EOF
edmConfigDump "${tmpfile}" > hlt.py

cmsRun hlt.py &> hlt.log

# remove input files to save space
rm -f run381594/run381594_ls0*_index*.*

#######################################################
# After this, prepare the streamer files with the following recipe:
#######################################################

mv run381594 source
mkdir -p run381594
cp source/run381594_ls1000_streamDQM_*.jsn run381594
for file in source/run381594_ls0000_streamDQM_*.ini; do
    # Extract the variable part in place of '*'
    variable_part=$(basename "$file" | sed 's/^run381594_ls0000_streamDQM_//; s/\.ini$//')

    # Concatenate files with the same variable part
    cat "source/run381594_ls0000_streamDQM_${variable_part}.ini" \
        "source/run381594_ls1000_streamDQM_${variable_part}.dat" \
        > "run381594/run381594_ls1000_streamDQM_${variable_part}.dat"
done

# edit the jsn file to not have 2 "0"s in it.
# finally run the client
# mkdir upload
# cmsRun DQM/Integration/python/clients/onlinebeammonitor_dqm_sourceclient-live_cfg.py runInputDir=. outputBaseDir=./output runNumber=381594 runkey=pp_run scanOnce=True

