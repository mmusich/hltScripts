#!/usr/bin/env python3
import os

os.system('hltConfigFromDB --configName /dev/CMSSW_15_0_0/GRun/V57 > GRun.py')
from GRun import cms,process

ret = []

for pathName in process.paths_():
    path = getattr(process, pathName)

    flag1 = False
    flag2 = False
    flag3 = False

    keepPath = False

    for (type_i, label_i) in path.expandAndClone().directDependencies():
        if type_i != 'modules':
            continue

        if label_i == 'hltSiStripRawToClustersFacility':
            flag1 = True

        if label_i == 'hltIter0PFlowTrackSelectionHighPurity':
            flag2 = True

        if label_i == 'hltParticleFlow':
            flag3 = True

    if flag1 and flag2 and (not flag3):
        keepPath = True

    if keepPath:
        ret += [pathName]

ret = sorted(list(set(ret)))

for foo in ret:
    print(foo)
