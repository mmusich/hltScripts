import FWCore.ParameterSet.Config as cms
import glob

#runNumber = 392732
runNumber = 392733

inputFiles = [f'file:{foo}' for foo in glob.glob(f'/eos/cms/store/group/tsg/FOG/debug/250531_run392733/run{runNumber}_*.dat')]
outputFile = f'/eos/cms/store/group/tsg/FOG/debug/250531_run392733/run{runNumber}_dstPhysics.root'

process = cms.Process('TEST')

process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
process.options.wantSummary = False
process.maxEvents.input = -1

# MessageLogger
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100000

# Global Tag
from Configuration.AlCa.GlobalTag import GlobalTag
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag = GlobalTag(process.GlobalTag, '150X_dataRun3_HLT_v1', '')

# Input source
process.source = cms.Source("NewEventStreamFileReader",
  fileNames = cms.untracked.vstring(sorted(list(set((inputFiles)))))
)

process.dstPhysicsFilter = cms.EDFilter( "TriggerResultsFilter",
    usePathStatus = cms.bool( False ),
    hltResults = cms.InputTag( "TriggerResults::HLT" ),
    l1tResults = cms.InputTag( "" ),
    l1tIgnoreMaskAndPrescale = cms.bool( False ),
    throw = cms.bool( True ),
    triggerConditions = cms.vstring( 'DST_Physics_v*' )
)

process.gtStage2Digis = cms.EDProducer( "L1TRawToDigi",
    FedIds = cms.vint32( 1404 ),
    Setup = cms.string( "stage2::GTSetup" ),
    FWId = cms.uint32( 0 ),
    DmxFWId = cms.uint32( 0 ),
    FWOverride = cms.bool( False ),
    TMTCheck = cms.bool( True ),
    CTP7 = cms.untracked.bool( False ),
    MTF7 = cms.untracked.bool( False ),
    InputLabel = cms.InputTag( "hltFEDSelectorL1" ),
    lenSlinkHeader = cms.untracked.int32( 8 ),
    lenSlinkTrailer = cms.untracked.int32( 8 ),
    lenAMCHeader = cms.untracked.int32( 8 ),
    lenAMCTrailer = cms.untracked.int32( 0 ),
    lenAMC13Header = cms.untracked.int32( 8 ),
    lenAMC13Trailer = cms.untracked.int32( 8 ),
    debug = cms.untracked.bool( False ),
    MinFeds = cms.uint32( 0 )
)

# Path definition
process.l1tPath = cms.Path(
    process.dstPhysicsFilter
  + process.gtStage2Digis
)

process.l1tOutput = cms.OutputModule( "PoolOutputModule",
    fileName = cms.untracked.string( outputFile ),
    compressionAlgorithm = cms.untracked.string( "ZSTD" ),
    compressionLevel = cms.untracked.int32( 3 ),
    fastCloning = cms.untracked.bool( False ),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string( "" ),
        dataTier = cms.untracked.string( "RAW" )
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring( 'l1tPath' )
    ),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *GlobalAlgBlk*_gtStage2Digis_*_*',
    )
)

# EndPath definition
process.l1tEndPath = cms.EndPath( process.l1tOutput )
