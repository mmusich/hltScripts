#!/usr/bin/env python3
import os

# V1 is a copy of /dev/CMSSW_14_0_0/HLT/V93
os.system("hltConfigFromDB --configName /users/missirol/test/dev/CMSSW_14_0_0/tmp/240303_firstAlpakaMenu/Test11/HLT/V1 > r1.py")
from r1 import cms,process

oldNames = [foo for foo in process.producers_()]
oldNames += [foo for foo in process.filters_()]
oldNames += [foo for foo in process.analyzers_()]
oldNames += [foo for foo in process.sequences_()]
oldNames += [foo for foo in process.tasks_()]
oldNames += [foo for foo in process.conditionaltasks_()]

os.system('cp r1.py r1_new.py')

for oldName in oldNames:
    newName = oldName

    if 'Portable' in newName:
        newName = newName.replace('Portable', '')

    if 'SerialSync' in newName:
        newName = newName.replace('SerialSync', '') + 'SerialSync'

    if 'CPUOnly' in newName:
        newName = newName.replace('CPUOnly', '') + 'SerialSync'

    if 'CPUSerial' in newName:
        newName = newName.replace('CPUSerial', '') + 'SerialSync'

    if newName != oldName:
        # The 1st replacement requires an exact match using \<foo\>,
        # otherwise one renaming can get in the way of other ones.
        # The 2nd replacement covers EventContent statements.
        sed_cmd = f'sed -i -e "s|\<{oldName}\>|{newName}|g" -e "s|_{oldName}_|_{newName}_|g" r1_new.py'
        os.system(sed_cmd)

# V2 includes the renamings, applied via ConfDB
os.system("hltConfigFromDB --configName /users/missirol/test/dev/CMSSW_14_0_0/tmp/240303_firstAlpakaMenu/Test11/HLT/V2 > r2.py")

# This diff is expected to be empty,
# modulo the name of the configuration in ConfDB
# (process.HLTConfigVersion)
os.system('diff r1_new.py r2.py')
