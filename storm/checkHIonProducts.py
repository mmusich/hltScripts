#hltConfigFromDB --configName /dev/CMSSW_14_1_0/HIon > hion.py
from hion import cms,process

pdMap = {
  'rawDataRepacker': [],
  'rawPrimeDataRepacker': [],
  'hltSiStripRawToDigi': [],
  'hltSiStripClusters2ApproxClusters': [],
}

for coll in pdMap:
  for foo in process.streams.parameterNames_():
    outMod = getattr(process, f'hltOutput{foo}')
    hasColl = False
    for bar in outMod.outputCommands:
      if f'_{coll}_' in bar:
        hasColl = True
        break
    if hasColl:
      for pdName in getattr(process.streams, foo):
        for pathName in getattr(process.datasets, pdName):
          pdMap[coll] += [pathName]
  pdMap[coll] = sorted(list(set(pdMap[coll])))

for coll in pdMap:
  pathNames = pdMap[coll]
  for pathName in pathNames:
    path = getattr(process, pathName)
    pathIsOkay = False
    for (type_i, label_i) in path.expandAndClone().directDependencies():
      if type_i != 'modules':
        continue
      if label_i == coll:
        pathIsOkay = True
    if not pathIsOkay:
      print(f'PROBLEM: {coll} missing in {pathName}')
    else:
      print(f'path: {path}')
    
