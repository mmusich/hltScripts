#!/bin/bash -ex

# cmsrel CMSSW_15_0_9 
# cd CMSSW_15_0_9_patch1/src
# cmsenv
# scram b

RUNNUMBER=392642 # 2025 EphemeralHLTPhysics
LUMISECTION=174 # 174 - 187

# LS 174 
INPUTFILES="\
    root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics0/RAW/v1/000/392/642/00000/06ac627c-f97b-40ed-a279-16fdcf990c2c.root 
    root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics1/RAW/v1/000/392/642/00000/8ec096b9-1293-4ee7-8e27-369889a521ff.root 
    root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics2/RAW/v1/000/392/642/00000/e39b2b26-9b68-40e7-8e2d-c259637ea5d3.root 
    root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics3/RAW/v1/000/392/642/00000/5f25f30f-1372-4875-ac25-0f437f2590be.root 
    root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics4/RAW/v1/000/392/642/00000/ddcb337e-3536-4361-b69a-02ba755b9eb0.root 
    root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics5/RAW/v1/000/392/642/00000/e7512b2b-d00a-4d71-924d-9563c2b36c18.root 
    root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics6/RAW/v1/000/392/642/00000/7dd68eaf-bb9b-456e-9318-961c3903c84a.root 
    root://eoscms.cern.ch//store/data/Run2025C/EphemeralHLTPhysics7/RAW/v1/000/392/642/00000/a7b5720c-aa47-4783-b838-dce20b7130ee.root"

rm -rf run${RUNNUMBER}*

# run on 23000 events of given LS, without event limits per input file
convertToRaw -l 1000 -r ${RUNNUMBER}:${LUMISECTION} -o . -- ${INPUTFILES}

tmpfile=$(mktemp)
hltConfigFromDB --configName /users/jprendi/ScoutingOnlineDQM/Test0/HLT/V2 > dump.py

cat <<@EOF >> dump.py
process.load("run${RUNNUMBER}_cff")
del process.PrescaleService
del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.GlobalTag.globaltag = cms.string('150X_dataRun3_HLT_v1')
process.options.numberOfThreads = 32
process.options.numberOfStreams = 32
process.options.wantSummary = True
# # to run using the same HLT prescales as used online
# process.PrescaleService.forceDefault = True
@EOF

edmConfigDump dump.py > hlt.py

bash -c 'echo $$ > cmsrun.pid; exec cmsRun hlt.py &> hlt.log'
job_pid=$(cat cmsrun.pid)
echo "cmsRun is running with PID: $job_pid"

# remove input files to save space
rm -f run392642/run392642_ls0*_index*.*

# prepare the files by concatenating the .ini and .dat files
mkdir -p prepared
cat run392642/run392642_ls0000_streamDQMOnlineScouting_pid${job_pid}.ini run392642/run392642_ls0174_streamDQMOnlineScouting_pid${job_pid}.dat > prepared/run392642_ls0174_streamDQMOnlineScouting_pid${job_pid}.dat
