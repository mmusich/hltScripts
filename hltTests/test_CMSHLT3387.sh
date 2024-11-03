#!/bin/bash -ex

# run 387440, LSs 1-30
INPUTFILE=root://eoscms.cern.ch//eos/cms/store/group/tsg/STORM/RAW/Run2024J_HIEphemeralHLTPhysics_run387440/235844d9-333c-43a9-9c92-b1ce47ce19d1.root

HLTMENU=/users/missirol/test/dev/CMSSW_14_1_0/CMSHLT_3359/Test01/HLT/V1

rm -rf run387440*

# create 1 file with 100 events from LS 15-20
convertToRaw -f 1000 -l 1000 -r 387440:15-387440:19 -o . -- "${INPUTFILE}"

tmpfile=$(mktemp)
hltConfigFromDB --configName "${HLTMENU}" > "${tmpfile}"
cat <<@EOF >> "${tmpfile}"

process.load('run387440_cff')

process.hltOnlineBeamSpotESProducer.timeThreshold = int(1e6)

del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 50

process.options.wantSummary = True
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

del process.PrescaleService

process.FastTimerService.dqmTimeRange = 30000
process.FastTimerService.enableDQMbyPath = True
process.FastTimerService.dqmPathTimeRange = 30000
process.FastTimerService.dqmPathTimeResolution = 1000
process.FastTimerService.dqmPathMemoryRange = 1000000
process.FastTimerService.dqmPathMemoryResolution = 25000

# remove all output streams
streamPaths = [pathName for pathName in process.finalpaths_()]
for foo in streamPaths:
    process.__delattr__(foo)
@EOF
edmConfigDump "${tmpfile}" > hlt.py
rm -rf "${tmpfile}"

cmsRun hlt.py &> hlt.log

fastHadd add -o output_streamDQMHistograms.pb run387440/run*_ls*_streamDQMHistograms_pid*.pb
fastHadd convert -o output_streamDQMHistograms.root output_streamDQMHistograms.pb

rm -rf run387440/*.raw
