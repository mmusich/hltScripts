#!/bin/bash

#[ -f hlt.py ] || (wget https://raw.githubusercontent.com/cms-sw/cmssw/master/HLTrigger/Configuration/python/HLT_FULL_cff.py -O hlt.py)

python3 <<@EOF
from hlt import cms, fragment as process

def selectPaths(pathName):
  return True

retDict = {}
for pathName in process.paths_():
  if not selectPaths(pathName):
    continue
  pathNameUnv = pathName[:pathName.rfind('_v')+2] if '_v' in pathName else pathName
  retDict[pathNameUnv] = []
  path = getattr(process, pathName)
  for moduleName in path.moduleNames():
    module = getattr(process, moduleName)
    if module.type_() == 'HLTL1TSeed' and hasattr(module, 'L1SeedsLogicalExpression'):
      strippedL1TSeedStr = module.L1SeedsLogicalExpression.value()
      for specialStr in ['(', ')', ' OR', ' AND', ' NOT', 'OR ', 'AND ', 'NOT ']:
        strippedL1TSeedStr = strippedL1TSeedStr.replace(specialStr, ' ')
      retDict[pathNameUnv] += sorted(list(set(strippedL1TSeedStr.split())))

for pathName in sorted(retDict.keys()):
  l1tSeeds = retDict[pathName]
  if l1tSeeds:
    print('\n', pathName)
    for l1tSeed in retDict[pathName]:
      if l1tSeed.startswith('L1_'):
        print('  ', l1tSeed)
      else:
        print('  ', l1tSeed)
#        raise Exception(l1tSeed)

#retDict2 = {}
#for foo in retDict:
#  for bar in retDict[foo]:
#      if bar not in retDict2: retDict2[bar] = []
#      retDict2[bar] += [foo]
#
#for seedName in sorted(retDict2.keys()):
#  hltSeeds = sorted(list(set(retDict2[seedName])))
#  if hltSeeds:
#    print('\n', seedName)
#    for hltSeed in hltSeeds:
#      print('  ', hltSeed)
@EOF
