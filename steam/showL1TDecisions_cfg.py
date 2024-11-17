import FWCore.ParameterSet.Config as cms

process = cms.Process('TEST')

process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
process.options.wantSummary = True
process.maxEvents.input = -1

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100 # only report every 100th event start
process.MessageLogger.cerr.enableStatistics = False # enable "MessageLogger Summary" message
process.MessageLogger.cerr.threshold = 'INFO' # change to 'WARNING' not to show INFO-level messages
## enable reporting of INFO-level messages (default is limit=0, i.e. no messages reported)
#process.MessageLogger.cerr.INFO = cms.untracked.PSet(
#    reportEvery = cms.untracked.int32(1), # every event!
#    limit = cms.untracked.int32(-1)       # no limit!
#)
process.MessageLogger.L1TGlobalSummary = cms.untracked.PSet()

# read back the trigger decisions
process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring('file:tmp.root')
)

# Global Tag
from Configuration.AlCa.GlobalTag import GlobalTag
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag = GlobalTag(process.GlobalTag, '141X_dataRun3_HLT_v1', '')

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

process.l1tResultsFilter = cms.EDFilter("TriggerResultsFilter",
    usePathStatus = cms.bool( False ),
    hltResults = cms.InputTag( "" ),
    l1tResults = cms.InputTag( "gtStage2Digis" ),
    l1tIgnoreMaskAndPrescale = cms.bool( False ),
    throw = cms.bool( True ),
    triggerConditions = cms.vstring( 'NOT L1_ZDC1n_OR_MinimumBiasHF1_AND_BptxAND' )
)

process.l1tGlobalSummary = cms.EDAnalyzer( "L1TGlobalSummary",
    AlgInputTag = cms.InputTag( "gtStage2Digis" ),
    ExtInputTag = cms.InputTag( "gtStage2Digis" ),
    MinBx = cms.int32( 0 ),
    MaxBx = cms.int32( 0 ),
    DumpTrigResults = cms.bool( False ),
    DumpRecord = cms.bool( False ),
    DumpTrigSummary = cms.bool( True ),
    ReadPrescalesFromFile = cms.bool( False ),
    psFileName = cms.string( "prescale_L1TGlobal.csv" ),
    psColumn = cms.int32( 0 )
)

process.path = cms.Path(
    process.gtStage2Digis
  + process.l1tResultsFilter
  + process.l1tGlobalSummary
)
