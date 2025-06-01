#!/bin/bash

cmsDriver.py l1Ntuple -s L1REPACK:Full \
 --python_filename l1t_L1REPACK_Full_base.py --dump_python -n 1500 \
 --era Run3_2025 --data --conditions 150X_dataRun3_HLT_v1 \
 --filein /store/data/Run2024I/EphemeralHLTPhysics5/RAW/v1/000/386/593/00000/545e47b2-a41e-46d6-a9e3-8c6d26fb3ea1.root \
 --processName HLT2 --no_output --no_exec

cp l1t_L1REPACK_Full_base.py l1t_L1REPACK_Full.py

cat <<@EOF >> l1t_L1REPACK_Full.py

## Import the GMT Raw to Digi module
#import EventFilter.L1TRawToDigi.gmtStage2Digis_cfi
#process.unpackGMT = EventFilter.L1TRawToDigi.gmtStage2Digis_cfi.gmtStage2Digis.clone(
#    InputLabel = cms.InputTag( 'rawDataCollector', processName=cms.InputTag.skipCurrentProcess())
#)
#
## Create a path for unpacking GMT and add it to the schedule
#process.unpackGMTPath = cms.Path(process.unpackGMT)
#process.schedule.append(process.unpackGMTPath)
#
#process.simGmtStage2Digis.barrelTFInput  = 'unpackGMT:BMTF'
#process.simGmtStage2Digis.overlapTFInput = 'unpackGMT:OMTF'
#process.simGmtStage2Digis.forwardTFInput = 'unpackGMT:EMTF'

# good
#process.simTwinMuxDigis.DTDigi_Source      = "unpackTwinMux:PhIn"
#process.simTwinMuxDigis.DTThetaDigi_Source = "unpackTwinMux:ThIn"

# good
#process.simKBmtfStubs.srcPhi = 'unpackTwinMux:PhOut'

# good
#process.simKBmtfStubs.srcPhi = 'unpackBmtf'
#process.simKBmtfStubs.srcTheta = 'unpackBmtf'

process.options.wantSummary = True

process.l1tGtStage2Digis1 = cms.EDProducer( "L1TRawToDigi",
    FedIds = cms.vint32( 1404 ),
    Setup = cms.string( "stage2::GTSetup" ),
    FWId = cms.uint32( 0 ),
    DmxFWId = cms.uint32( 0 ),
    FWOverride = cms.bool( False ),
    TMTCheck = cms.bool( True ),
    CTP7 = cms.untracked.bool( False ),
    MTF7 = cms.untracked.bool( False ),
    InputLabel = cms.InputTag( "rawDataCollector::@skipCurrentProcess" ),
    lenSlinkHeader = cms.untracked.int32( 8 ),
    lenSlinkTrailer = cms.untracked.int32( 8 ),
    lenAMCHeader = cms.untracked.int32( 8 ),
    lenAMCTrailer = cms.untracked.int32( 0 ),
    lenAMC13Header = cms.untracked.int32( 8 ),
    lenAMC13Trailer = cms.untracked.int32( 8 ),
    debug = cms.untracked.bool( False ),
    MinFeds = cms.uint32( 0 )
)

process.l1tMonitor1 = cms.EDFilter( "TriggerResultsFilter",
    usePathStatus = cms.bool( False ),
    hltResults = cms.InputTag( "" ),
    l1tResults = cms.InputTag( "l1tGtStage2Digis1" ),
    l1tIgnoreMaskAndPrescale = cms.bool( True ),
    throw = cms.bool( True ),
    triggerConditions = cms.vstring( 'L1_SingleMu22_BMTF' )
)

process.L1TMonitorPath1 = cms.Path(
    process.l1tGtStage2Digis1
  + process.l1tMonitor1
)

process.schedule.append( process.L1TMonitorPath1 )

process.l1tGtStage2Digis2 = process.l1tGtStage2Digis1.clone(
    InputLabel = "rawDataCollector::@currentProcess"
)

process.l1tMonitor2 = process.l1tMonitor1.clone(
    l1tResults = "l1tGtStage2Digis2"
)

process.L1TMonitorPath2 = cms.Path(
    process.rawDataCollector
  + process.l1tGtStage2Digis2
  + process.l1tMonitor2
)

process.schedule.append( process.L1TMonitorPath2 )
@EOF

cmsRun l1t_L1REPACK_Full.py &> l1t_L1REPACK_Full.log
grep MonitorPath l1t_L1REPACK_Full.log | head -2
