#!/bin/bash -ex                                                                                       
RUNNUMBER=362321
LUMISECTION=231
NEVENTS=5000

# cmsrel CMSSW_15_1_0_patch2
# cd CMSSW_15_1_0_patch2/src/
# cmsenv
# cmsenv                                                                                                                                                                                                   
# scram b                                                                                                                                   

INPUTFILE=root://eoscms.cern.ch//eos/cms//store/user/cmsbuild/store/hidata/HIRun2022A/HITestRaw0/RAW/v1/000/362/321/00000/f467ee64-fc64-47a6-9d8a-7ca73ebca2bd.root 
rm -rf run${RUNNUMBER}*

# run on 100 events of LS 131, with 100 events per input file                                                                                             
convertToRaw -f ${NEVENTS} -l ${NEVENTS} -r ${RUNNUMBER}:${LUMISECTION} -s rawDataRepacker -o . -- "${INPUTFILE}"

tmpfile=$(mktemp)
hltConfigFromDB --configName /users/musich/tests/dev/CMSSW_15_1_0/CMSHLT-3147/HIon > "${tmpfile}"
#hltConfigFromDB --configName /dev/CMSSW_15_1_0/HIon/V14 > "${tmpfile}"
sed -i 's|process = cms.Process( "HLT" )|from Configuration.Eras.Era_Run3_cff import Run3\nprocess = cms.Process( "HLT", Run3 )|g' "${tmpfile}"
cat <<@EOF >> "${tmpfile}"
process.load("run${RUNNUMBER}_cff")

# to run without any HLT prescales                                                  
del process.PrescaleService
del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')

# override the GlobalTag, connection string and pfnPrefix
from Configuration.AlCa.GlobalTag import GlobalTag as customiseGlobalTag
process.GlobalTag = customiseGlobalTag(
    process.GlobalTag,
    globaltag = "150X_dataRun3_HLT_v1",
    conditions = "L1Menu_CollisionsHeavyIons2024_v1_0_6_xml,L1TUtmTriggerMenuRcd,frontier://FrontierProd/CMS_CONDITIONS,,9999-12-31 23:59:59.000"
)

# run the Full L1T emulator, then repack the data into a new RAW collection, to be used by the HLT
from HLTrigger.Configuration.CustomConfigs import L1REPACK
process = L1REPACK(process, "uGT")

process.options.numberOfThreads = 32
process.options.numberOfStreams = 32

process.options.wantSummary = True
# process.PrescaleService.forceDefault = True

## just output the GPU vs CPU output
streamPaths = [foo for foo in process.endpaths_() if foo.endswith('Output')]
streamPaths.remove('HIDQMGPUvsCPUOutput')
for foo in streamPaths:
    process.__delattr__(foo)
@EOF
edmConfigDump "${tmpfile}" > hlt.py

cmsRun hlt.py &> hlt.log

bash -c 'echo $$ > cmsrun.pid; exec cmsRun hlt.py &> hlt.log'
job_pid=$(cat cmsrun.pid)
echo "cmsRun is running with PID: $job_pid"

# remove input files to save space
rm -f run362321/run362321_ls0*_index*.*

# prepare the files by concatenating the .ini and .dat files
mkdir -p preparedHIon

cat run362321/run362321_ls0000_streamHIDQMGPUvsCPU_pid${job_pid}.ini run362321/run362321_ls0231_streamHIDQMGPUvsCPU_pid${job_pid}.dat > preparedHIon/run362321_ls0231_streamHIDQMGPUvsCPU_pid${job_pid}.dat
cp run362321/run362321_ls0231_streamHIDQMGPUvsCPU_pid${job_pid}.jsn preparedHIon/run362321_ls0231_streamHIDQMGPUvsCPU_pid${job_pid}_prep.jsn

# now remove the extra 0

input="preparedHIon/run362321_ls0231_streamHIDQMGPUvsCPU_pid${job_pid}_prep.jsn"
output="preparedHIon/run362321_ls0231_streamHIDQMGPUvsCPU_pid${job_pid}.jsn"

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

rm -fr preparedHIon/run362321_ls0231_streamHIDQMGPUvsCPU_pid${job_pid}_prep.jsn
rm -fr preparedHIon/run362321_ls0231_streamHIDQMGPUvsCPU_pid${job_pid}.ini
