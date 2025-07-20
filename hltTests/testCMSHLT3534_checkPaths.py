#!/usr/bin/env python3
import os

os.system('hltConfigFromDB --configName /dev/CMSSW_15_0_0/GRun/V98 > GRun.py')
from GRun import cms,process

ret = []

for pathName in process.paths_():
    path = getattr(process, pathName)

    hasTracks = path.contains(process.hltMergedTracks)

    hasSeq = False
    hasSeq |= path.contains(process.HLTTrackReconstructionForPF)
    hasSeq |= path.contains(process.HLTTrackReconstructionForPFDispl)
    hasSeq |= path.contains(process.HLTTrackReconstructionForPFNoMu)
    hasSeq |= path.contains(process.HLTTrackReconstructionForPFSerialSync)
    hasSeq |= path.contains(process.HLTTrackerMuonSequenceLowPt)

    if hasTracks and not hasSeq:
        print(pathName)

#    flag1 = False
#    flag2 = False
#    flag3 = False
#
#    keepPath = False
#
#    for (type_i, label_i) in path.expandAndClone().directDependencies():
#        if type_i != 'sequences':
#            continue
#        print(type_i)
#        continue
#
#        if label_i == 'hltSiStripRawToClustersFacility':
#            flag1 = True
#
#        if label_i == 'hltIter0PFlowTrackSelectionHighPurity':
#            flag2 = True
#
#        if label_i == 'hltParticleFlow':
#            flag3 = True
#
#    if flag1 and flag2 and (not flag3):
#        keepPath = True
#
#    if keepPath:
#        ret += [pathName]
#
#ret = sorted(list(set(ret)))
#
#for foo in ret:
#    print(foo)
