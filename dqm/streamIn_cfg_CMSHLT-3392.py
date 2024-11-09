import FWCore.ParameterSet.Config as cms

process = cms.Process("TRANSFER")

import FWCore.Framework.test.cmsExceptionsFatal_cff
process.options = FWCore.Framework.test.cmsExceptionsFatal_cff.options

process.load("FWCore.MessageLogger.MessageLogger_cfi")


process.source  = cms.Source("DQMStreamerReader",
                             SelectEvents = cms.untracked.vstring('*'),
                             datafnPosition = cms.untracked.uint32(3),
                             delayMillis = cms.untracked.uint32(500),
                             deleteDatFiles = cms.untracked.bool(False),
                             endOfRunKills = cms.untracked.bool(False),
                             inputFileTransitionsEachEvent = cms.untracked.bool(False),
                             minEventsPerLumi = cms.untracked.int32(10000000),
                             nextLumiTimeoutMillis = cms.untracked.int32(0),
                             runInputDir = cms.untracked.string('.'),
                             runNumber = cms.untracked.uint32(387968),
                             scanOnce = cms.untracked.bool(True),
                             skipFirstLumis = cms.untracked.bool(False),
                             streamLabel = cms.untracked.string('streamHIDQM')
                             )

process.json = cms.EDAnalyzer("DQMStreamerWriteJsonAnalyzer",
                              eventsPerLumi = cms.untracked.uint32(100000),
                              runNumber = cms.untracked.uint32(1),
                              streamName = cms.untracked.string("streamHIDQM"),
                              dataFileForEachLumi = cms.untracked.vstring(),
                              pathToWriteJson = cms.untracked.string(".")
)

#process.a1 = cms.EDAnalyzer("StreamThingAnalyzer",
#    product_to_get = cms.string('m1')
#)

process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('myout.root')
)

process.end = cms.EndPath(process.out*process.json)
