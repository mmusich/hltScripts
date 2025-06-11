import FWCore.ParameterSet.Config as cms
import sys

output = sys.argv[1]

process = cms.Process("REPACK")

process.source = cms.Source("NewEventStreamFileReader",
    fileNames = cms.untracked.vstring(
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics0/000/392/642/run392642_ls0178_streamPhysicsHLTPhysics0_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics0/000/392/642/run392642_ls0179_streamPhysicsHLTPhysics0_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics0/000/392/642/run392642_ls0180_streamPhysicsHLTPhysics0_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics1/000/392/642/run392642_ls0178_streamPhysicsHLTPhysics1_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics1/000/392/642/run392642_ls0179_streamPhysicsHLTPhysics1_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics1/000/392/642/run392642_ls0180_streamPhysicsHLTPhysics1_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics2/000/392/642/run392642_ls0178_streamPhysicsHLTPhysics2_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics2/000/392/642/run392642_ls0179_streamPhysicsHLTPhysics2_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics2/000/392/642/run392642_ls0180_streamPhysicsHLTPhysics2_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics3/000/392/642/run392642_ls0178_streamPhysicsHLTPhysics3_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics3/000/392/642/run392642_ls0179_streamPhysicsHLTPhysics3_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics3/000/392/642/run392642_ls0180_streamPhysicsHLTPhysics3_StorageManager.dat',
    )
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.write = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('RAW')
    ),
    fileName = cms.untracked.string(output),
    splitLevel = cms.untracked.int32(0),
#    compressionAlgorithm = cms.untracked.string("LZMA"),
#    compressionLevel = cms.untracked.int32(4),
)

process.outputPath = cms.EndPath(process.write)
