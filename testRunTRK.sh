#!/bin/bash -ex

OUTDIR=tmp_testRunTRK

rm -rf "${OUTDIR}"
mkdir "${OUTDIR}"
cd "${OUTDIR}"

commonOpts="--max-events 20 --output minimal --unprescale --input /store/relval/CMSSW_12_2_0_pre2/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/122X_mcRun3_2021_realistic_v1-v1/2580000/5541adab-cc2d-4401-b069-8140c90078c8.root --mc --globaltag auto:run3_mc_GRun --eras Run3"

hltGetConfiguration --dbproxy /dev/CMSSW_12_3_0/GRun/V4 ${commonOpts} --customise HLTrigger/Configuration/customizeHLTforRun3.TRK_newTracking,HLTrigger/Configuration/customizeHLTforPatatrack.customizeHLTforPatatrack \
 > hlt_new_pog.py
echo "process.options.numberOfThreads = 1" >> hlt_new_pog.py
echo "process.schedule.remove( process.AlCa_LumiPixelsCounts_Random_v2 )" >> hlt_new_pog.py
echo "process.hltOutputMinimal.outputCommands += ['keep *_hltMergedTracks_*_*']" >> hlt_new_pog.py
echo "process.hltOutputMinimal.fileName = 'output_hlt_new_pog.root'" >> hlt_new_pog.py

hltGetConfiguration --dbproxy /users/missirol/test/dev/CMSSW_12_3_0/CMSHLT_2187/IntegTest_v01/GRun ${commonOpts} --customise HLTrigger/Configuration/customizeHLTforPatatrack.customizeHLTforPatatrack \
 > hlt_new_storm.py
echo "process.options.numberOfThreads = 1" >> hlt_new_storm.py
echo "process.hltOutputMinimal.outputCommands += ['keep *_hltMergedTracks_*_*']" >> hlt_new_storm.py
echo "process.hltOutputMinimal.fileName = 'output_hlt_new_storm.root'" >> hlt_new_storm.py

python3 hlt_new_pog.py
python3 hlt_new_storm.py

edmConfigDump hlt_new_pog.py > hlt_new_pog_dump.py
edmConfigDump hlt_new_storm.py > hlt_new_storm_dump.py

cmsRun hlt_new_pog.py &> hlt_new_pog.log
cmsRun hlt_new_storm.py &> hlt_new_storm.log
