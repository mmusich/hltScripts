#!/usr/bin/env python3
import os
import json

fileName = f'{os.environ["CMSSW_BASE"]}/src/HLTrigger/Configuration/scripts/utils/hltPathOwners.json'

pathOwnersDict = json.load(open(fileName))

for pathName in pathOwnersDict:
    pathOwnersDict[pathName]['owners'] = sorted(list(set(pathOwnersDict[pathName]['owners'])))

json.dump(pathOwnersDict, open(fileName, 'w'), sort_keys=True, indent=2)
