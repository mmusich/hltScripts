#!/usr/bin/env python3

# hltConfigFromDB --configName /dev/CMSSW_12_4_0/HLT/V201 > offl_new.py
from offl_new import cms, process as offl
from onli import process as onli
import fnmatch

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
  return ret

psDict_offl = getPrescaleDict(offl, '*')
psDict_onli = getPrescaleDict(onli, '*')

#colName_offl = '2.0e34+ZB+HLTPhysics'
#colName_onli = '2p00E+34+ZeroBias+HLTPhysics'

#colName_offl = 'Emergency'
#colName_onli = 'Emergency'

cols_offl = offl.PrescaleService.lvl1Labels
cols_onli = onli.PrescaleService.lvl1Labels

pathNames = sorted(list(set(list(psDict_offl.keys()) + list(psDict_onli.keys()))))

# common paths
pathBlacklist = [
  'HLT_Mu12eta2p3',
  'HLT_DoublePFJets350_PFBTagDeepJet_p71',
  'AlCa_AK8PFJet40',
  'AlCa_PFJet40',
  'AlCa_PFJet40_CPUOnly',
  'HLT_HT200_L1SingleLLPJet_DelayedJet40_SingleDelay1nsTrackless',
  'HLT_HT200_L1SingleLLPJet_DelayedJet40_DoubleDelay0p5nsTrackless',
]
for col in cols_offl:
  if col not in cols_onli: continue
  print('---'+col)
  for pathName in psDict_onli:
    if pathName in pathBlacklist: continue
    if pathName not in psDict_offl: continue
    psval_offl = psDict_offl[pathName][col]
    psval_onli = psDict_onli[pathName][col]
    if psval_offl != psval_onli:
      print(f'{pathName:70} {psval_offl: 5d} {psval_onli: 5d}')



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
