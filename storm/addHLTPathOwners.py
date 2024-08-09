#!/usr/bin/env python3
import os
import json
import fnmatch

pathOwnersDict = json.load(open(f'{os.environ["CMSSW_BASE"]}/src/HLTrigger/Configuration/scripts/utils/hltPathOwners.json'))

groupNames = [
  'AlCa',
]

pathNames = [
]

#paths = []
#for pathName in pathNames:
#    for pathNameKey in pathOwnersDict:
#        if fnmatch.fnmatch(pathNameKey, pathName):
#            paths += [pathNameKey]
#            for groupName in groupNames:
#                pathOwnersDict[pathNameKey]['owners'] += [groupName]

paths = []
for pathNameKey in pathOwnersDict:
    addGroups = 0
    for group in [
      'Tracker',
      'ECAL',
      'HCAL',
      'RPC',
      'GEM',
      'PPS',
      'L1T',
    ]:
      if group in pathOwnersDict[pathNameKey]['owners']:
        addGroups += 1

    if (addGroups > 0 or pathNameKey.startswith('AlCa_')) and (not pathNameKey.startswith('DQM_')):
            paths += [pathNameKey]
#            for groupName in groupNames:
#               pathOwnersDict[pathNameKey]['owners'] += [groupName]

paths = sorted(list(set(paths)))
for path in paths:
    print(path)

for pathNameKey in pathOwnersDict:
    pathOwnersDict[pathNameKey]['owners'] = sorted(list(set(pathOwnersDict[pathNameKey]['owners'])))

#for pathName in pathOwnersDict:
#    if groupName in pathOwnersDict[pathName]['owners'] and pathName not in pathNames:
#        print(f'WARNING -- Path not found: {pathName}')

json.dump(pathOwnersDict, open(f'{os.environ["CMSSW_BASE"]}/src/HLTrigger/Configuration/scripts/utils/hltPathOwners.json', 'w'), sort_keys=True, indent=2)
