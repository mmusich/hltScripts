import FWCore.ParameterSet.Config as cms
import os
import sys
import glob

if sys.argv[0] == 'cmsRun':
  INPUTS = [sys.argv[2]]
  outputFilePath = sys.argv[3]
else:
  INPUTS = [sys.argv[1]]
  outputFilePath = sys.argv[2]

process = cms.Process('TEST')
process.options.wantSummary = False
process.maxEvents.input = -1

inputFilePaths = []
for inp_i in INPUTS:
  for inp_j in glob.glob(inp_i):
    inp_j2 = 'file:'+inp_j if os.path.isfile(inp_j) else inp_j
    inputFilePaths.append(inp_j2)
inputFilePaths = sorted(list(set(inputFilePaths)))
print(inputFilePaths)

process.EvFDaqDirector = cms.Service('EvFDaqDirector')

process.source = cms.Source('FedRawDataInputSource',
  fileListMode = cms.untracked.bool(True),
  fileNames = cms.untracked.vstring(inputFilePaths)
)

process.edmOutput = cms.OutputModule('PoolOutputModule',
  dataset = cms.untracked.PSet(
    dataTier = cms.untracked.string('RAW')
  ),
  fileName = cms.untracked.string('file:'+outputFilePath)
)

process.outputPath = cms.EndPath(process.edmOutput)
