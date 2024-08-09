#!/bin/bash -ex

# cmsrel CMSSW_14_0_14_MULTIARCHS
# cd CMSSW_14_0_14_MULTIARCHS/src
# git cms-addpkg DQM/Integration
# mkdir DQM/Integration/data
# cmsenv
# scram b

# run 362321, LSs 231-232
INPUTFILE=root://eoscms.cern.ch//eos/cms/store/user/cmsbuild//store/hidata/HIRun2022A/HITestRaw0/RAW/v1/000/362/321/00000/f467ee64-fc64-47a6-9d8a-7ca73ebca2bd.root

HLTMENU=/dev/CMSSW_14_0_0/HIon/V173

rm -rf run362321*

# run on 100 events of LS 231, with 100 events per input file
convertToRaw -f 100 -l 100 -r 362321:231 -s rawDataRepacker -o . -- "${INPUTFILE}"

tmpfile=$(mktemp)
hltConfigFromDB --configName "${HLTMENU}" > "${tmpfile}"
sed -i 's|process = cms.Process( "HLT" )|from Configuration.Eras.Era_Run3_cff import Run3\nprocess = cms.Process( "HLT", Run3 )|g' "${tmpfile}"
cat <<@EOF >> "${tmpfile}"
process.load('run362321_cff')
process.hltOnlineBeamSpotESProducer.timeThreshold = int(1e6)

# override the GlobalTag, connection string and pfnPrefix
from Configuration.AlCa.GlobalTag import GlobalTag as customiseGlobalTag
process.GlobalTag = customiseGlobalTag(
    process.GlobalTag,
    globaltag = "140X_dataRun3_HLT_v3",
    conditions = "L1Menu_CollisionsHeavyIons2023_v1_1_5_xml,L1TUtmTriggerMenuRcd,frontier://FrontierProd/CMS_CONDITIONS,,9999-12-31 23:59:59.000"
)

# run the Full L1T emulator, then repack the data into a new RAW collection, to be used by the HLT
from HLTrigger.Configuration.CustomConfigs import L1REPACK
process = L1REPACK(process, "uGT")

# to run without any HLT prescales
del process.PrescaleService

command_to_remove = 'keep FEDRawDataCollection_rawDataCollector_*_*'
if command_to_remove in process.hltOutputHIDQM.outputCommands:
   process.hltOutputHIDQM.outputCommands.remove(command_to_remove)

# # to run using the same HLT prescales as used online in LS 231
# process.PrescaleService.forceDefault = True
@EOF
edmConfigDump "${tmpfile}" > hlt.py

#cmsRun hlt.py &> hlt.log

# remove input files to save space
#rm -f run362321/run362321_ls0*_index*.*

cat run362321/run362321_ls0000_streamHIDQM_pid918575.ini run362321/run362321_ls0231_streamHIDQM_pid918575.dat > DQM/Integration/data/run362321/run362321_ls0231_streamHIDQM_pid918575.dat
cp -pr run362321/run362321_ls0231_streamHIDQM_pid918575.jsn DQM/Integration/data/run362321

# then run with e.g. 
# cmsRun DQM/Integration/python/clients/mutracking_dqm_sourceclient-live_cfg.py runInputDir=./DQM/Integration/data/ runNumber=362321 runkey=hi_run scanOnce=True datafnPosition=4 
