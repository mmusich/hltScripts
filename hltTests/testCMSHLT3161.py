#!/usr/bin/env python3
import fnmatch
import os

if not os.path.isfile('tmp.py'):
    os.system('hltConfigFromDB --adg --configName /cdaq/test/sdonato/2024_04/1200b/HLT > tmp.py')

from tmp import cms, process

def pathNameUnversioned(name):
    return name[:name.rfind('_v')]+'_v' if '_v' in name else name

def getPrescaleDict(process, pattern='*'):
  ret = {}
  for pset_i in process.PrescaleService.prescaleTable:
    pathName = pset_i.pathName.value()
    if not fnmatch.fnmatch(pathName, pattern):
      continue
    pathKey = pathNameUnversioned(pathName)
    if pathKey in ret:
      raise RuntimeError('')
    ret[pathKey] = {}
    for colIdx,colName in enumerate(process.PrescaleService.lvl1Labels):
      ret[pathKey][colName] = pset_i.prescales[colIdx]
  for paths in [process.paths_(), process.endpaths_()]:
    for pathName in paths:
      pathKey = pathNameUnversioned(pathName)
      if pathKey not in ret:
        ret[pathKey] = {}
        for colIdx,colName in enumerate(process.PrescaleService.lvl1Labels):
          ret[pathKey][colName] = 1
  return ret

psDict = getPrescaleDict(process, '*')
cols = process.PrescaleService.lvl1Labels

ret = []
for pathName, path in process.paths_().items():
    if not path.contains(process.hltParticleFlowRecHitHBHESoA):
        continue
    pathKey = pathNameUnversioned(pathName)
    if psDict[pathKey]['2p0E34_OnlyMuons'] > 0:
        ret += [pathKey]

ret = sorted(list(set(ret)))

for foo in ret:
    print(foo)
