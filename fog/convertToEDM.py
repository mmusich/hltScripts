import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing('analysis')
options.parseArguments()

process = cms.Process( 'REPACK' )

process.source = cms.Source( 'FedRawDataInputSource',
    eventChunkSize = cms.untracked.uint32( 200 ),
    eventChunkBlock = cms.untracked.uint32( 200 ),
    numBuffers = cms.untracked.uint32( 4 ),
    maxBufferedFiles = cms.untracked.uint32( 2 ),
    alwaysStartFromfirstLS = cms.untracked.uint32( 0 ),
    verifyChecksum = cms.untracked.bool( True ),
    useL1EventID = cms.untracked.bool( False ),
    testTCDSFEDRange = cms.untracked.vuint32(  ),
    fileListMode = cms.untracked.bool( True ),
    fileNames = cms.untracked.vstring( options.inputFiles )
)

from EventFilter.Utilities.EvFDaqDirector_cfi import EvFDaqDirector as _EvFDaqDirector
process.EvFDaqDirector = _EvFDaqDirector.clone( buBaseDir = '.', runNumber = 0 )

process.output = cms.OutputModule( 'PoolOutputModule',
    fileName = cms.untracked.string( 'repacked.root' ),
    outputCommands = cms.untracked.vstring( 'keep *' )
)

process.endPath = cms.EndPath( process.output )
