import FWCore.ParameterSet.Config as cms

process = cms.Process('TEST')

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing('analysis')
options.setDefault('inputFiles', [
    'root://eoscms.cern.ch//eos/cms/store/data/Run2024F/EphemeralHLTPhysics0/RAW/v1/000/382/250/00000/d69c0220-8282-496c-8e88-2fb663a43ea5.root'
])
options.setDefault('maxEvents', 100)
options.parseArguments()

# set max number of input events
process.maxEvents.input = options.maxEvents

# initialize MessageLogger and output report
process.options.wantSummary = False
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100 # only report every 100th event start
process.MessageLogger.cerr.enableStatistics = False # enable "MessageLogger Summary" message
process.MessageLogger.cerr.threshold = 'INFO' # change to 'WARNING' not to show INFO-level messages
## enable reporting of INFO-level messages (default is limit=0, i.e. no messages reported)
#process.MessageLogger.cerr.INFO = cms.untracked.PSet(
#    reportEvery = cms.untracked.int32(1), # every event!
#    limit = cms.untracked.int32(-1)       # no limit!
#)

###
### Source (input file)
###
process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(options.inputFiles)
)
print('process.source.fileNames =', process.source.fileNames)

###
### Path (FEDRAWData producers)
###
_siPixelFEDs = [foo for foo in range(1200, 1349)]
_siStripFEDs = [foo for foo in range(50, 489)]

from EventFilter.Utilities.EvFFEDExcluder_cfi import EvFFEDExcluder as _EvFFEDExcluder
process.rawDataNOTracker = _EvFFEDExcluder.clone(
    src = 'rawDataCollector',
    fedsToExclude = _siPixelFEDs+_siStripFEDs,
)

process.rawDataSelectionPath = cms.Path(
    process.rawDataNOTracker
)

###
### EndPath (output file)
###
process.rawDataOutputModule = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string('file:tmp.root'),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep FEDRawDataCollection_rawDataNOTracker_*_*',
        'keep FEDRawDataCollection_rawDataCollector_*_*',
        'keep edmTriggerResults_*_*_*',
        'keep GlobalObjectMapRecord_hltGtStage2ObjectMap_*_*',
        'keep triggerTriggerEvent_*_*_*',
    )
)

process.outputEndPath = cms.EndPath( process.rawDataOutputModule )
