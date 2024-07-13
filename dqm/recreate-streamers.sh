#!/bin/bash -ex

RUNNUMBER=381594
LUMISECTION=1000

# cmsrel CMSSW_14_0_9_MULTIARCHS
# cd CMSSW_14_0_9_MULTIARCHS/src
# cmsenv
# scram b

# The biggest I could find, lumisection 5
INPUTFILE=root://eoscms.cern.ch//store/express/Run2024E/ExpressPhysics/FEVT/Express-v1/000/381/594/00000/1e2c895f-a250-45be-a7ff-ee95e636a6e9.root
rm -rf run${RUNNUMBER}*

# run on 10000 events of LS 5, with 500 events per input file
convertToRaw -f 500 -l 5000 -r ${RUNNUMBER}:${LUMISECTION} -o . -- "${INPUTFILE}"

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
# # to run using the same HLT prescales as used online in LS 231
# process.PrescaleService.forceDefault = True
@EOF
edmConfigDump "${tmpfile}" > hlt.py

cmsRun hlt.py &> hlt.log

# # remove input files to save space
# rm -f run${RUNNUMBER}/run${RUNNUMBER}_ls0*_index*.*
