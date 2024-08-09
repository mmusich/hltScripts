#!/usr/bin/env python3
import os

def get_entries(filenames):
    entries = []
    for filename_tmp in filenames:
        filename = f'{os.environ["CMSSW_BASE"]}/src/HLTrigger/Configuration/tables/{filename_tmp}'
        with open(filename) as ifile:
            lines = ifile.read().splitlines()
            for line in lines:
                if '#' in line:
                    line = line[:line.find('#')]
                line_blocks = line.split()
                for foo in line_blocks:
                    if foo:
                        entries += [foo]
                        break
    return sorted(list(set(entries)))

l1 = get_entries([
    'online_Special.txt'
])

l2 = get_entries([
    'online_Circulating.txt', 'online_Cosmics.txt', 'online_ECALTiming.txt',
    'online_FirstCollisions.txt', 'online_LumiScan.txt', 'online_PPS.txt',
    'online_Splashes.txt', 'online_TrackerVR.txt',
])

for foo in l1:
    if foo not in l2:
        print(f'NOT ONLINE: {foo}')

for foo in l2:
    if foo not in l1:
        print(f'NOT SPECIAL: {foo}')
