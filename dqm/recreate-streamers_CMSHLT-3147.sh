#!/bin/bash -ex                                                                                       
RUNNUMBER=397813
LUMISECTION=131
NEVENTS=25

# cmsrel CMSSW_15_1_X_2025-10-22-2300
# cd CMSSW_15_1_X_2025-10-22-2300/src/
# cmsenv
# git cms-addpkg DataFormats/TrackSoA DataFormats/TrackingRecHitSoA DQM/Integration
# git remote add AdrianoDee git@github.com:AdrianoDee/cmssw.git; git fetch AdrianoDee
# git cherry-pick 1eb24e6536182945d6f7ac55fedc023a9f0d4410
# git cherry-pick 9a3ef9ae14f452aa15d3f868b97c63f6b996b1dc
# cmsenv                                                                                                                                                                                                   
# scram b                                                                                                                                   

INPUTFILE=root://eoscms.cern.ch//eos/cms/store/express/Run2025F/ExpressPhysics/FEVT/Express-v2/000/397/813/00000/f95a79f9-18ef-48f1-951a-2ae78c1a107f.root
rm -rf run${RUNNUMBER}*

# run on 100 events of LS 131, with 100 events per input file                                                                                             
convertToRaw -f ${NEVENTS} -l ${NEVENTS} -r ${RUNNUMBER}:${LUMISECTION} -o . -- "${INPUTFILE}"

tmpfile=$(mktemp)
hltConfigFromDB --configName /users/musich/tests/dev/CMSSW_15_1_0/CMSHLT-3147/GRun > "${tmpfile}"
cat <<@EOF >> "${tmpfile}"
process.load("run${RUNNUMBER}_cff")

# to run without any HLT prescales                                                  
del process.PrescaleService
del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')

process.options.numberOfThreads = 32
process.options.numberOfStreams = 32

process.options.wantSummary = True
process.GlobalTag.globaltag = cms.string( "150X_dataRun3_HLT_v1" )
# # to run using the same HLT prescales as used online in LS 1000                                                                                                                                          
# process.PrescaleService.forceDefault = True

from HLTrigger.Configuration.common import *
def customizeHLTFor49149(process):
    ca_producers_pp = ['CAHitNtupletAlpakaPhase1@alpaka','alpaka_serial_sync::CAHitNtupletAlpakaPhase1']
    for ca_producer in ca_producers_pp:
        for prod in producers_by_type(process, ca_producer):
            if hasattr(prod, 'geometry'):
                g = getattr(prod, 'geometry')
                g.startingPairs = cms.vuint32( [i for i in range(8)] + [i for i in range(13,19)])
                setattr(prod, 'geometry', g) 
    return process 

process = customizeHLTFor49149(process)
@EOF
edmConfigDump "${tmpfile}" > hlt.py

cmsRun hlt.py &> hlt.log

bash -c 'echo $$ > cmsrun.pid; exec cmsRun hlt.py &> hlt.log'
job_pid=$(cat cmsrun.pid)
echo "cmsRun is running with PID: $job_pid"

# remove input files to save space
rm -f run397813/run397813_ls0*_index*.*

# prepare the files by concatenating the .ini and .dat files
mkdir -p prepared

cat run397813/run397813_ls0000_streamDQMGPUvsCPU_pid${job_pid}.ini run397813/run397813_ls0131_streamDQMGPUvsCPU_pid${job_pid}.dat > prepared/run397813_ls0131_streamDQMGPUvsCPU_pid${job_pid}.dat
cp run397813/run397813_ls0131_streamDQMGPUvsCPU_pid${job_pid}.jsn prepared/run397813_ls0131_streamDQMGPUvsCPU_pid${job_pid}_prep.jsn

# now remove the extra 0

input="prepared/run397813_ls0131_streamDQMGPUvsCPU_pid${job_pid}_prep.jsn"
output="prepared/run397813_ls0131_streamDQMGPUvsCPU_pid${job_pid}.jsn"

jq '
  .data as $d |
  .data = (
    reduce range(0; $d|length) as $i ([]; 
      if ($i > 0 and .[-1] == "0" and $d[$i] == "0") 
      then . 
      else . + [$d[$i]] 
      end
    )
  )
' "$input" > "$output"
