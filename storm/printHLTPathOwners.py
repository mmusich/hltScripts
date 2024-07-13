#!/usr/bin/env python3
import os
import json

pathOwnersDict = json.load(open(f'{os.environ["CMSSW_BASE"]}/src/HLTrigger/Configuration/scripts/utils/hltPathOwners.json'))

knownGroups = [
    'TRK','EGM','MUO','JME','BTV','TAU','LUM',
    'BPH','EXO','HIG','B2G','SUS','SMP','TOP','HIN',
    'L1T','ECAL','HCAL','RPC','PPS',
    'TSG (Scouting)', 'AlCa/DPGs'
]

os.system('hltConfigFromDB --configName /dev/CMSSW_14_0_0/HLT > tmp.py')
from tmp import cms,process
pathNames = sorted([pathName if '_v' not in pathName else pathName[:pathName.rfind('_v')]+'_v' for pathName, path in process.paths_().items() if not pathName.startswith('Dataset_')])

def updateLabel(groupLabel):
    ret = groupLabel

    if ret == 'Scouting':
        ret = 'TSG (Scouting)'

    if ret == 'DPG':
        ret = 'AlCa'

    if ret.startswith('AlCa'):
        ret = 'AlCa/DPGs'

    if ret == 'BTV (MC)':
        ret = 'BTV'

    if ret not in knownGroups:
        ret = 'Others'

    return ret

groupsDict = {}
for path in pathOwnersDict:
    if path not in pathNames:
        continue
    for group in pathOwnersDict[path]['owners']:
        groupMod = updateLabel(group)
        if groupMod not in groupsDict:
            groupsDict[groupMod] = []
        groupsDict[groupMod] += [path]

for group in groupsDict:
    groupsDict[group] = sorted(list(set(groupsDict[group])))

groupsList = list(groupsDict.keys())
groupsList.remove('Others')
groupsList = sorted(list(set(groupsList)))
groupsList += ['Others']

pathsOfOthers = []
for path in groupsDict['Others']:
    hasOwners = False
    for group in groupsDict:
        if group == 'Others':
            continue
        if path in groupsDict[group]:
            hasOwners = True
            break
    if not hasOwners:
        pathsOfOthers += [path]
groupsDict['Others'] = sorted(list(set(pathsOfOthers)))

json.dump(groupsDict, open('hltPathOwnersDict.json','w'), sort_keys=True, indent=True)

for group in groupsList:
    print()
    print('='*50)
    print(group)
    print('='*50)
    paths = sorted(list(set(groupsDict[group])))
    for path in paths:
        print(f'  {path}')
