from grun import cms,process
import fnmatch
import os
import json

def getPrescaleDict(process, pattern='*'):
  ret = {}
  for pset_i in process.PrescaleService.prescaleTable:
    pathName = pset_i.pathName.value()
    if not fnmatch.fnmatch(pathName, pattern):
      continue
    pathKey = pathName.split('_v')[0]
    if pathKey in ret:
      raise RuntimeError('')
    ret[pathKey] = {}
    for colIdx,colName in enumerate(process.PrescaleService.lvl1Labels):
      ret[pathKey][colName] = pset_i.prescales[colIdx]
  for paths in [process.paths_(), process.endpaths_()]:
    for pathName in paths:
      pathKey = pathName.split('_v')[0]
      if pathKey not in ret:
        ret[pathKey] = {}
        for colIdx,colName in enumerate(process.PrescaleService.lvl1Labels):
          ret[pathKey][colName] = 1
  return ret

psDict = getPrescaleDict(process, '*')
cols = process.PrescaleService.lvl1Labels

os.system('rm -f tmp.log')

pathNames = set()
for pathName in psDict:
  if pathName.startswith('MC_'): continue

#  ## 1
#  cols_ps0 = set()
#  for col in psDict[pathName]:
#    if psDict[pathName][col] == 0:
#      cols_ps0.add(col)
#  if len(cols_ps0) > 0.5 * len(cols):
#    print(pathName)

  ## 3
  cols_psSum = 0
  for col in psDict[pathName]:
    if col.startswith('0p') or col.startswith('1p') or col.startswith('2p'):
      cols_psSum += psDict[pathName][col]
  if cols_psSum == 0:
    pathNames.add(pathName)
    os.system('grep "'+pathName+'_v*" HLTrigger/Configuration/tables/GRun.txt >> tmp.log')

os.system('awk \'{ print "  -", $3, ":", $1 }\' tmp.log | sed \'s|,||g\' -- | sed \'s|v\*|v|g\' -- | sort -u')

#  ## 2
#  if psDict[pathName]['2p2E34'] == 0 and psDict[pathName]['0p8E34'] == 0:
#    if 'HI'
#    print(pathName)

ownersDict = json.load(open('owners.json'))

outDict = {}
for pathName0 in pathNames:
  pathName = pathName0+'_v'
  groupNames = ownersDict[pathName]['owners']
  for gname in groupNames:
    if gname not in outDict:
      outDict[gname] = []
    outDict[gname] += [pathName]

pathNames2 = []
for foo in outDict:
  pathNames2 += outDict[foo]
pathNames2 = sorted(list(set(pathNames2)))

pathNames0 = [foo+'_v' for foo in pathNames]

for foo in pathNames0:
  if foo not in pathNames2:
    raise RuntimeError('XXX', foo)

for foo in pathNames2:
  if foo not in pathNames0:
    raise RuntimeError('YYY', foo)

for gname in sorted(outDict.keys()):
  print('')
  print('Group:', gname)
  print('{code}')
  for foo in sorted(list(set(outDict[gname]))): print(foo)
  print('{code}')
