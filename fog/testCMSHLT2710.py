#!/usr/bin/env python3

# hltConfigFromDB --configName /dev/CMSSW_12_6_0/HLT > offl.py
# hltConfigFromDB --adg --configName /cdaq/physics/Run2022/2e34/v1.5.0/HLT/V13 > onli.py
from onli2 import process as onli
import fnmatch

def getOnlineColumn(columnName):
  return columnName
#  return 'CosmicsHighExpress' if columnName in ['CRUZET','CRAFT'] else columnName

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

psDict_offl = {} #getPrescaleDict(offl, '*')
psDict_onli = getPrescaleDict(onli, '*')

#colName_offl = '2.0e34+ZB+HLTPhysics'
#colName_onli = '2p00E+34+ZeroBias+HLTPhysics'

#colName_offl = 'Emergency'
#colName_onli = 'Emergency'

cols_offl = [] #offl.PrescaleService.lvl1Labels
cols_onli = onli.PrescaleService.lvl1Labels

pathNames = sorted(list(set(list(psDict_offl.keys()) + list(psDict_onli.keys()))))

# common paths
pathBlacklist = [
#  'HLT_Mu12eta2p3',
#  'HLT_DoublePFJets350_PFBTagDeepJet_p71',
#  'AlCa_AK8PFJet40',
#  'AlCa_PFJet40',
#  'AlCa_PFJet40_CPUOnly',
#  'HLT_HT200_L1SingleLLPJet_DelayedJet40_SingleDelay1nsTrackless',
#  'HLT_HT200_L1SingleLLPJet_DelayedJet40_DoubleDelay0p5nsTrackless',
]

for col1,col2 in [
  ['Emergency', 'HLTPhysics+ZeroBias'],
  ['2p2E34', '2p3E34'],
  ['0p6E34', '0p7E34'],
  ['0p7E34', '0p8E34'],
  ['0p8E34', '0p9E34'],
  ['0p9E34', '1p0E34'],
  ['1p0E34', '1p1E34'],
  ['1p1E34', '1p2E34'],
  ['1p2E34', '1p3E34'],
]:
  print('-'*10, col1, 'VS', col2)
  for pathName in psDict_onli:
    ps1 = psDict_onli[pathName][col1]
    ps2 = psDict_onli[pathName][col2]
    if ps1 != ps2:
      print(pathName, ps2, f'[ {ps1} ]')


#for col in cols_offl:
#  col_onli = getOnlineColumn(col)
#  if col_onli not in cols_onli: continue
#  print('---', col)
#  for pathName in psDict_onli:
#    if pathName in pathBlacklist: continue
#    if pathName not in psDict_offl: continue
#    psval_offl = psDict_offl[pathName][col]
#    psval_onli = psDict_onli[pathName][col_onli]
#    if psval_offl != psval_onli:
#      print(f'{pathName:70} {psval_offl: 5d} {psval_onli: 5d}')
#  print('---')






#for pathName in pathNames:
#  psval_offl = psDict_offl[pathName][colName_offl] if pathName in psDict_offl else -1
#  psval_onli = psDict_onli[pathName][colName_onli] if pathName in psDict_onli else -1
#  if psval_offl != psval_onli:
#    print(f'{pathName:70} {psval_offl: 5d} {psval_onli: 5d}')
#
##
#for pathName in psDict_onli:
#  val = None
#  for colName in psDict_onli[pathName]:
#    if 'E+' not in colName: continue
#    val2 = psDict_onli[pathName][colName]
#    if val == None: val = val2
#    elif val != val2:
##      print(pathName)
#      break

#print('HLTPath,CRUZET,CRAFT')
#for pathName in psDict_offl:
#  psvals = []
#  for col in ['CRUZET', 'CRAFT']:
#    if pathName not in psDict_onli:
#      psval = psDict_offl[pathName][col] if pathName.startswith('Dataset_') else (1 if ('_' not in pathName) else 0)
#    else:
#      psval = psDict_onli[pathName]['CosmicsHighExpress']
#    psvals.append(psval)
#  if len(psvals) != 2: raise RuntimeError('AAA')
#  if psvals[0] != psvals[1]: raise RuntimeError('BBB')
#  print(f'{pathName},{psvals[0]},{psvals[1]}')
