#!/bin/bash -ex

# cmsrel
# cd /src
# cmsenv
# scram b

# run 362321, LSs 231-232
INPUTFILE=root://eoscms.cern.ch//eos/cms/store/user/cmsbuild//store/hidata/HIRun2022A/HITestRaw0/RAW/v1/000/362/321/00000/f467ee64-fc64-47a6-9d8a-7ca73ebca2bd.root

HLTMENU=/dev/CMSSW_15_0_0/HIon

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
    globaltag = "150X_dataRun3_HLT_v1",
    conditions = "L1Menu_CollisionsHeavyIons2024_v1_0_6_xml,L1TUtmTriggerMenuRcd,frontier://FrontierProd/CMS_CONDITIONS,,9999-12-31 23:59:59.000"
)

# run the Full L1T emulator, then repack the data into a new RAW collection, to be used by the HLT
from HLTrigger.Configuration.CustomConfigs import L1REPACK
process = L1REPACK(process, "uGT")

# to run without any HLT prescales
del process.PrescaleService

# # to run using the same HLT prescales as used online in LS 231
# process.PrescaleService.forceDefault = True
@EOF
edmConfigDump "${tmpfile}" > hlt.py

cmsRun hlt.py &> hlt.log

# remove input files to save space
rm -f run362321/run362321_ls0*_index*.*

#######################################################
# After this, prepare the streamer files with the following recipe:
#######################################################

mv run362321 source
mkdir -p run362321
cp source/run362321_ls0231_streamHIDQM_*.jsn run362321
for file in source/run362321_ls0000_streamHIDQM_*.ini; do
    # Extract the variable part in place of '*'
    variable_part=$(basename "$file" | sed 's/^run362321_ls0000_streamHIDQM_//; s/\.ini$//')

    # Concatenate files with the same variable part
    cat "source/run362321_ls0000_streamHIDQM_${variable_part}.ini" \
        "source/run362321_ls0231_streamHIDQM_${variable_part}.dat" \
        > "run362321/run362321_ls0231_streamHIDQM_${variable_part}.dat"
done

# edit the jsn file to not have 2 "0"s in it.
# finally run the client
# mkdir upload
# cmsRun DQM/Integration/python/clients/sistrip_approx_dqm_sourceclient-live_cfg.py runInputDir=. outputBaseDir=./output runNumber=362321 runkey=hi_run scanOnce=True
