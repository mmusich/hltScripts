import FWCore.ParameterSet.Config as cms
from sys import argv

output = argv[1]

process = cms.Process("REPACK")

process.source = cms.Source("NewEventStreamFileReader",
    fileNames = cms.untracked.vstring(
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics3/000/383/363/run383363_ls0193_streamPhysicsHLTPhysics3_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics0/000/383/363/run383363_ls0193_streamPhysicsHLTPhysics0_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics2/000/383/363/run383363_ls0193_streamPhysicsHLTPhysics2_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics1/000/383/363/run383363_ls0193_streamPhysicsHLTPhysics1_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics0/000/383/363/run383363_ls0194_streamPhysicsHLTPhysics0_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics1/000/383/363/run383363_ls0194_streamPhysicsHLTPhysics1_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics2/000/383/363/run383363_ls0194_streamPhysicsHLTPhysics2_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics3/000/383/363/run383363_ls0194_streamPhysicsHLTPhysics3_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics0/000/383/363/run383363_ls0195_streamPhysicsHLTPhysics0_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics1/000/383/363/run383363_ls0195_streamPhysicsHLTPhysics1_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics2/000/383/363/run383363_ls0195_streamPhysicsHLTPhysics2_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics3/000/383/363/run383363_ls0195_streamPhysicsHLTPhysics3_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics0/000/383/363/run383363_ls0196_streamPhysicsHLTPhysics0_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics1/000/383/363/run383363_ls0196_streamPhysicsHLTPhysics1_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics2/000/383/363/run383363_ls0196_streamPhysicsHLTPhysics2_StorageManager.dat',
'root://eoscms.cern.ch//eos/cms/store/t0streamer/Data/PhysicsHLTPhysics3/000/383/363/run383363_ls0196_streamPhysicsHLTPhysics3_StorageManager.dat',
    )
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.write = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('RAW')
    ),
    fileName = cms.untracked.string(output)
)

process.outputPath = cms.EndPath(process.write)
