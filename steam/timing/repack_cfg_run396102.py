import FWCore.ParameterSet.Config as cms
import sys
import glob

output = sys.argv[1]

process = cms.Process("REPACK")

fileNames = []

lumiSections = [295, 296, 297, 298]

for lsId in lumiSections:
    fileNames += glob.glob(f'/eos/cms/store/t0streamer/Data/PhysicsHLTPhysics*/000/396/102/run396102_ls{lsId:04d}_streamPhysicsHLTPhysics*_StorageManager.dat')

fileNames = sorted(list(set([f'root://eoscms.cern.ch//eos/cms{fileName}' for fileName in fileNames])))

process.source = cms.Source("NewEventStreamFileReader",
    fileNames = cms.untracked.vstring(fileNames)
)

print(process.source)

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
