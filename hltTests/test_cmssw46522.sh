#!/bin/bash -ex

# run 387440, LSs 1-30
INPUTFILE=root://eoscms.cern.ch//eos/cms/store/group/tsg/STORM/RAW/Run2024J_HIEphemeralHLTPhysics_run387440/235844d9-333c-43a9-9c92-b1ce47ce19d1.root

HLTMENU=/cdaq/physics/Run2024HI/v1.0.0/HLT/V7

rm -rf run387440*

# create 1 file with 100 events from LS 15
convertToRaw -f 100 -l 100 -r 387440:15 -o . -- "${INPUTFILE}"

tmpfile=$(mktemp)
hltConfigFromDB --configName --adg "${HLTMENU}" > "${tmpfile}"
sed -i 's|process = cms.Process( "HLT" )|from Configuration.Eras.Era_Run3_cff import Run3\nprocess = cms.Process( "HLT", Run3 )|g' "${tmpfile}"
cat <<@EOF >> "${tmpfile}"

process.load('run387440_cff')

process.hltOnlineBeamSpotESProducer.timeThreshold = int(1e6)

process.options.wantSummary = True
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

# override the GlobalTag, connection string and pfnPrefix
from Configuration.AlCa.GlobalTag import GlobalTag as customiseGlobalTag
process.GlobalTag = customiseGlobalTag(
    process.GlobalTag,
    globaltag = "141X_dataRun3_HLT_v1",
    conditions = "L1Menu_CollisionsHeavyIons2024_v1_0_5_xml,L1TUtmTriggerMenuRcd,frontier://FrontierProd/CMS_CONDITIONS,,9999-12-31 23:59:59.000"
)

# run the Full L1T emulator, then repack the data into a new RAW collection, to be used by the HLT
from HLTrigger.Configuration.CustomConfigs import L1REPACK
process = L1REPACK(process, "uGT")

# remove all output streams
streamPaths = [pathName for pathName in process.finalpaths_()]
for foo in streamPaths:
    process.__delattr__(foo)

# # to run using the same HLT prescales as used online in LS 231
# process.PrescaleService.forceDefault = True
@EOF
edmConfigDump "${tmpfile}" > hlt.py
rm -rf "${tmpfile}"

cmsRun hlt.py &> hlt.log

fastHadd add -o output_streamDQMHistograms.pb run387440/run*_ls*_streamDQMHistograms_pid*.pb
fastHadd convert -o output_streamDQMHistograms.root output_streamDQMHistograms.pb

rm -rf run387440* output_streamDQMHistograms.pb
