#!/bin/bash

#[ -f hlt.py ] || (wget https://raw.githubusercontent.com/cms-sw/cmssw/master/HLTrigger/Configuration/python/HLT_FULL_cff.py -O hlt.py)
[ -f hlt.py ] || (hltConfigFromDB --adg --configName /cdaq/circulating/2022/v1.1/HLT/V1 > hlt.py)
#[ -f hlt.py ] || (hltConfigFromDB --adg --configName /cdaq/cosmic/commissioning2022/CRAFT/v2.2/HLT/V1 > hlt.py)

python3 <<EOF
from hlt import cms, fragment as process

def selectPaths(pathName):
  return True

retDict = {}
for pathName in process.paths_():
  if not selectPaths(pathName):
    continue
  retDict[pathName] = []
  path = getattr(process, pathName)
  for moduleName in path.moduleNames():
    module = getattr(process, moduleName)
    if module.type_() == 'HLTL1TSeed' and hasattr(module, 'L1SeedsLogicalExpression'):
      strippedL1TSeedStr = module.L1SeedsLogicalExpression.value()
      for specialStr in ['(', ')', ' OR', ' AND', ' NOT', 'OR ', 'AND ', 'NOT ']:
        strippedL1TSeedStr = strippedL1TSeedStr.replace(specialStr, ' ')
      retDict[pathName] += sorted(list(set(strippedL1TSeedStr.split())))

for pathName in sorted(retDict.keys()):
  l1tSeeds = retDict[pathName]
  if l1tSeeds:
    print(pathName)
    for l1tSeed in retDict[pathName]:
      if l1tSeed.startswith('L1_'):
        print('  ', l1tSeed)
      else:
        raise Exception(l1tSeed)
EOF
