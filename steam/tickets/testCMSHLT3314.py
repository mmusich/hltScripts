#!/usr/bin/env python3
import os
import sys
import csv
import fnmatch
import copy

runNumber = 384910 # int(sys.argv[1])

defaultColumn = '2p0E34'

magicFactor = 2

# L1T Seeds not to be modified
l1tWhiteList = [
  'L1_FirstBunchAfterTrain',
  'L1_FirstCollisionInOrbit',
  'L1_FirstCollisionInTrain',
  'L1_LastCollisionInTrain',
  'L1_IsolatedBunch',
  'L1_DoubleMu0er1p4_SQ_OS_dEta_Max1p2',
  'L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p5',
  'L1_DoubleMu0er2p0_SQ_OS_dEta_Max1p6',
  'L1_CDC_SingleMu_3_er1p2_TOP120_DPHI2p618_3p142',
  'L1_SingleJet60_FWD2p5',
  'L1_SingleJet90',
  'L1_SingleJet90_FWD2p5',
  'L1_SingleJet120',
  'L1_SingleJet120_FWD2p5',
  'L1_DoubleJet40er2p5',
  'L1_DoubleJet100er2p5',
  'L1_DoubleJet120er2p5',
  'L1_Mu3_Jet60er2p5_dR_Max0p4',
  'L1_Mu3_Jet16er2p5_dR_Max0p4',
  'L1_SingleMu15_DQ',
  'L1_HTT120er',
  'L1_HTT160er',
  'L1_HTT200er',
  'L1_HTT255er',
  'L1_SingleEG8er2p5',
  'L1_SingleEG10er2p5',
  'L1_SingleEG15er2p5',
  'L1_SingleEG26er2p5',
]

hltPathsUsingZeroBias = [
  'AlCa_AK8PFJet40_v',
  'AlCa_EcalEtaEBonly_v',
  'AlCa_EcalEtaEEonly_v',
  'AlCa_EcalPhiSym_v',
  'AlCa_EcalPi0EBonly_v',
  'AlCa_EcalPi0EEonly_v',
  'AlCa_LumiPixelsCounts_ZeroBias_v',
  'AlCa_PFJet40_CPUOnly_v',
  'AlCa_PFJet40_v',
  'DST_PFScouting_ZeroBias_v',
  'DST_ZeroBias_v',
  'HLT_AK8PFJet40_v',
  'HLT_AK8PFJet60_v',
  'HLT_AK8PFJet80_v',
  'HLT_AK8PFJetFwd40_v',
  'HLT_AK8PFJetFwd60_v',
  'HLT_DiPFJetAve100_HFJEC_v',
  'HLT_DiPFJetAve40_v',
  'HLT_DiPFJetAve60_HFJEC_v',
  'HLT_DiPFJetAve60_v',
  'HLT_DiPFJetAve80_HFJEC_v',
  'HLT_DiPFJetAve80_v',
  'HLT_HcalNZS_v',
  'HLT_PFJet40_v',
  'HLT_PFJet60_v',
  'HLT_PFJet80_v',
  'HLT_PFJetFwd40_v',
  'HLT_PFJetFwd60_v',
  'HLT_PPSMaxTracksPerArm1_v',
  'HLT_PPSMaxTracksPerRP4_v',
  'HLT_ZeroBias_Alignment_v',
  'HLT_ZeroBias_Beamspot_v',
  'HLT_ZeroBias_v',
  'HLT_EphemeralZeroBias_v',
]

def getL1TPrescaleDict(filename):
    l1tDict = {}
    with open(filename, newline='') as l1tfile:
        l1tReader = csv.reader(l1tfile, delimiter=',')
        colNames = []
        for row in l1tReader:
            if row[0] == 'Default':
                continue
            if colNames:
                l1tDict[row[1]] = {'b': int(row[0]), 'p': {}}
                for colIdx in range(2, len(row)):
                    l1tDict[row[1]]['p'][colNames[colIdx-2]] = int(row[colIdx])
            else:
                colNames = row[2:]
    return l1tDict

def writeL1TPrescaleCSV(psDict, filename):
    l1tDict = {}
    with open(filename, 'w') as l1tFile:
        colNames = []
        for foo in psDict:
            colNames = list(psDict[foo]['p'].keys())
            break

        lines = []
        lines += [f'Default,{defaultColumn}'+','*len(colNames)]
        lines += ['Bit,Algo Name,'+','.join(colNames)]

        l1tSeeds = [foo[0] for foo in sorted(psDict.items(), key=lambda x:x[1]['b'])]

        for l1tSeed in l1tSeeds:
            bit = psDict[l1tSeed]['b']
            line = f'{bit},{l1tSeed}'
            for colName in psDict[l1tSeed]['p']:
                line += f',{psDict[l1tSeed]["p"][colName]}'
            lines += [line]

        for line in lines:
            l1tFile.write(f'{line}\n')
    return True

def writeHLTPrescaleCSV(psDict, filename):
    hltDict = {}
    with open(filename, 'w') as hltFile:
        colNames = []
        for foo in psDict:
            colNames = list(psDict[foo].keys())
            break

        lines = []
        lines += ['HLTPath,'+','.join(colNames)]

        hltPaths = sorted(list(psDict.keys()))

        for hltPath in hltPaths:
            line = hltPath+'1' if hltPath.endswith('_v') else hltPath
            for colName in psDict[hltPath]:
                line += f',{psDict[hltPath][colName]}'
            lines += [line]

        for line in lines:
            hltFile.write(f'{line}\n')
    return True

def pathNameUnversioned(name):
    return name[:name.rfind('_v')]+'_v' if '_v' in name else name

def getL1TSeedsPerHLTPath(process):
    retDict = {}
    for pathName in process.paths_():
        pathNameUnv = pathName[:pathName.rfind('_v')+2] if '_v' in pathName else pathName
        retDict[pathNameUnv] = []
        path = getattr(process, pathName)
        for moduleName in path.moduleNames():
            module = getattr(process, moduleName)
            if module.type_() == 'HLTL1TSeed' and hasattr(module, 'L1SeedsLogicalExpression'):
                strippedL1TSeedStr = module.L1SeedsLogicalExpression.value()
                for specialStr in ['(', ')', ' OR', ' AND', ' NOT', 'OR ', 'AND ', 'NOT ']:
                    strippedL1TSeedStr = strippedL1TSeedStr.replace(specialStr, ' ')
                retDict[pathNameUnv] += sorted(list(set([foo for foo in strippedL1TSeedStr.split() if foo != 'L1GlobalDecision'])))
    return retDict

def getHLTPrescaleDict(runNumber, pattern='*'):
    tmpfile = 'tmp.py'
    if not os.path.isfile(f'{tmpfile}'):
        tmpstr = 'https_proxy=http://cmsproxy.cms:3128/'
        tmpstr += f'  hltGetConfiguration run:{runNumber} > {tmpfile}'
        os.system(tmpstr)
    from tmp import cms, process

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

    ret2 = getL1TSeedsPerHLTPath(process)

    return ret, ret2

l1tPS = getL1TPrescaleDict('l1ps.csv')
l1tColNames = list(l1tPS['L1_AlwaysTrue']['p'].keys())

hltPS, hltSeeds = getHLTPrescaleDict(runNumber)
hltColNames = list(hltPS['HLTriggerFirstPath'].keys())

l1tPS_new = copy.deepcopy(l1tPS)
hltPS_new = copy.deepcopy(hltPS)

if l1tColNames != hltColNames:
    raise RuntimeError('column names')

l1tSeedsChanged = []

for l1tSeed in l1tPS:
    if l1tSeed in l1tWhiteList:
        continue

    l1t_ps = l1tPS[l1tSeed]['p'][defaultColumn]
    if l1t_ps == 0:
        continue

    if l1t_ps == 1:
        continue

    l1tPS_new[l1tSeed]['p'][defaultColumn] *= magicFactor

    l1tSeedsChanged += [l1tSeed]

    if l1tSeed not in ['L1_ZeroBias', 'L1_ZeroBias_copy']:
        continue

    for colName in l1tPS[l1tSeed]['p']:
        if colName == defaultColumn or not colName.startswith('1p'):
            continue

        l1tPS_new[l1tSeed]['p'][colName] /= magicFactor

l1tSeedsChanged = sorted(list(set(l1tSeedsChanged)))

hltPathsChanged = []
hltPathsAffected = []

for hltPath in hltPS:
    if hltPath not in hltSeeds:
        continue

    if len([foo for foo in hltSeeds[hltPath] if l1tPS[foo]['p'][defaultColumn] == 1]) > 0:
        continue

    hltChangePS = len([foo for foo in hltSeeds[hltPath] if l1tPS[foo]['p'][defaultColumn] > 1 and foo in l1tSeedsChanged]) > 0

    if not hltChangePS:
        continue

    hlt_ps = hltPS[hltPath][defaultColumn]

    if hlt_ps == 0:
        pass
    elif hlt_ps == 1:
        hltPathsAffected += [hltPath]
    else:
        hltPS_new[hltPath][defaultColumn] = round(hlt_ps / magicFactor)
        hltPathsChanged += [hltPath]

    if hltPath not in hltPathsUsingZeroBias:
        continue

    if hltPath in hltPathsAffected:
        continue

    for colName in hltPS[hltPath]:
        if colName == defaultColumn or not colName.startswith('1p'):
            continue
        hltPS_new[hltPath][colName] *= magicFactor

hltPathsChanged = sorted(list(set(hltPathsChanged)))
hltPathsAffected = sorted(list(set(hltPathsAffected)))

print(f'\n------ L1T Seeds with reduced rate in {defaultColumn} ------')
for l1tSeed in l1tSeedsChanged:
    print(l1tSeed)

print(f'\n------ HLT Paths with reduced rate in {defaultColumn} ------')
for hltPath in hltPathsAffected:
    print(hltPath)

print(f'\n------ HLT Paths with ~same rate in {defaultColumn} (after changing HLT PS) ------')
for hltPath in hltPathsChanged:
    print(hltPath)

### New L1T Prescale Table
for l1tSeed in l1tPS:
    for colName in l1tPS[l1tSeed]['p']:
        if colName == defaultColumn:
            continue
        # update columns derived from the default column
        if not colName.startswith(defaultColumn):
            continue

        if l1tPS_new[l1tSeed]['p'][colName] == 0:
            continue

        psDef_new = l1tPS_new[l1tSeed]['p'][defaultColumn]
        psDef_old = l1tPS[l1tSeed]['p'][defaultColumn]

        if psDef_new != psDef_old:
            l1tPS_new[l1tSeed]['p'][colName] = psDef_new

writeL1TPrescaleCSV(l1tPS, 'l1tPS_old.csv')
writeL1TPrescaleCSV(l1tPS_new, 'l1tPS_new.csv')

### New HLT Prescale Table
for hltPath in hltPS:
    for colName in hltPS[hltPath]:
        if colName == defaultColumn:
            continue
        # update columns derived from the default column
        if not colName.startswith(defaultColumn):
            continue

        if hltPS_new[hltPath][colName] == 0:
            continue

        psDef_new = hltPS_new[hltPath][defaultColumn]
        psDef_old = hltPS[hltPath][defaultColumn]
        if psDef_new != psDef_old:
            hltPS_new[hltPath][colName] = psDef_new

writeHLTPrescaleCSV(hltPS, 'hltPS_old.csv')
writeHLTPrescaleCSV(hltPS_new, 'hltPS_new.csv')
