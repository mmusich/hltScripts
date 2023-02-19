#!/usr/bin/env python3
from dump_RelVal_HLT_Reco_GRun_DATA import cms,process as hltPlusReco
from dump_RelVal_HLT_GRun_DATA import process as hlt

###
### Add the following two lines to a cfg to apply customiseForCMSHLT2587
###
### from customiseForCMSHLT2587 import customiseForCMSHLT2587
### process = customiseForCMSHLT2587(process)
###

outName = 'customiseForCMSHLT2587'

removePathsStr = """
  process.options.numberOfThreads = 1
  process.options.numberOfStreams = 0

  pathWhiteList = [
    'AlCa_EcalPi0EBonly_v15',
#    'raw2digi_step',
#    'L1Reco_step',
#    'reconstruction_step',
  ]
  
  pathNames = set()
  for pathName in process.paths_():
    if pathName not in pathWhiteList:
      pathNames.add(pathName)
  
  for pathName in pathNames:
    process.__delattr__(pathName)
"""

moduleBlackList = [
  'options',
  'GlobalTag', # this changes the GT to Prompt for the HLT-only cfg
]

with open(outName+'.py', 'w') as ofile:
  ofile.write('import FWCore.ParameterSet.Config as cms\n')
  ofile.write('\ndef '+outName+'(process):\n')
  ofile.write(removePathsStr+'\n')
  ofile.write('  process.SiStripClusterChargeCutNone = process.HLTSiStripClusterChargeCutNone.clone()\n\n')
  for mod_type in ['psets', 'es_sources', 'es_producers']:
    ofile.write('  ### '+mod_type+'\n\n')
    modulesDict = getattr(hltPlusReco, mod_type+'_')()
    for modName in sorted(modulesDict.keys()):
      if modName in moduleBlackList: continue
      if not hasattr(hlt, modName): continue
      modStr = modulesDict[modName].dumpPython()
      if modStr == getattr(hlt, modName).dumpPython(): continue
      modStr = modStr.replace('\n', '\n  ')
      ofile.write('  process.'+modName+' = '+modStr+'\n')
  ofile.write('\n')
  ofile.write('  return process\n')
#from customiseForCMSHLT2587 import customiseForCMSHLT2587
#process = customiseForCMSHLT2587(process)
