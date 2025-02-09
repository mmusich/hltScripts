#!/bin/bash

hltConfigFromDB --configName /dev/CMSSW_14_2_0/GRun/V12 > hlt.py

cp /eos/cms/store/group/tsg/STEAM/timing_server/samples/srv-b1b07-16-01_samples/Run386593_HLTPhysics/run386593_cff.py .
sed -i 's|/data/timing/data/Run386593_HLTPhysics|/eos/cms/store/group/tsg/STEAM/timing_server/samples/srv-b1b07-16-01_samples/Run386593_HLTPhysics|g' run386593_cff.py

cat <<@EOF >> hlt.py

# set total number of events to be processed
process.maxEvents.input = 360

# set number of concurrent threads and events (CMSSW streams)
process.options.numberOfThreads = 16
process.options.numberOfStreams = 12

# print job statistics after event loop
process.options.wantSummary = True

# use default configuration of MessageLogger
del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')

# set input files
process.load('run386593_cff')

# remove check on timestamp of online-beamspot payloads
process.hltOnlineBeamSpotESProducer.timeThreshold = int(1e6)

# same source settings as used online
process.source.eventChunkSize = 200
process.source.eventChunkBlock = 200
process.source.numBuffers = 4
process.source.maxBufferedFiles = 2

# set number of concurrent luminosity sections
process.options.numberOfConcurrentLuminosityBlocks = 2

# write a JSON file with the timing information
if hasattr(process, 'FastTimerService'):
    process.FastTimerService.writeJSONSummary = True

# remove HLTAnalyzerEndpath if present
if hasattr(process, 'HLTAnalyzerEndpath'):
    del process.HLTAnalyzerEndpath

# set GlobalTag (calibrations)
process.GlobalTag.globaltag = '150X_dataRun3_HLT_v1'

## set prescale column (HLT prescales)
#process.PrescaleService.lvl1DefaultLabel = '2p0E34'
#process.PrescaleService.forceDefault = True

# remove HLT prescales
del process.PrescaleService

# apply extra customisations specific to the CMSSW release in use
from HLTrigger.Configuration.customizeHLTforCMSSW import customizeHLTforCMSSW
process = customizeHLTforCMSSW(process)

# modify pixel-track-reconstruction parameters to increase throughput
process.hltPixelTracksSoA.CAThetaCutBarrel = 0.00111685053
process.hltPixelTracksSoA.CAThetaCutForward = 0.00249872683
process.hltPixelTracksSoA.hardCurvCut = 0.695091509
process.hltPixelTracksSoA.dcaCutInnerTriplet = 0.0419242041
process.hltPixelTracksSoA.dcaCutOuterTriplet = 0.293522194
process.hltPixelTracksSoA.phiCuts = [
    832, 379, 481, 765, 1136,
    706, 656, 407, 1212, 404,
    699, 470, 652, 621, 1017,
    616, 450, 555, 572
]
@EOF

edmConfigDump hlt.py > hlt_dump.py

for ntry in {00..19}; do

  rm -rf run386593
  echo hlt_dump_try"${ntry}"
  cmsRun hlt_dump.py &> hlt_dump_try"${ntry}".log
  grep -inrl fstreamer hlt_dump_try"${ntry}".log

done
unset ntry

rm -rf run386593
rm -rf run386593_cff.py
rm -rf resources.json
rm -rf hlt.py hlt_dump.py
rm -rf __pycache__
