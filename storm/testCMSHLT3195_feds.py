#!/usr/bin/env python3

detFeds = {
    'DT': [
        [770, 779,],
        [780, 780,],
        [823, 823,],
        [1369, 1371,],
    ],
    'RPC': [
        [790, 795,],
        [821, 821,],
    ],
    'CSC': [
        [750, 757,],
        [760, 760,],
        [822, 822,],
        [830, 869,],
        [880, 887,],
        [890, 901,],
    ],
    'GEM': [
        [1467, 1478,],
    ],
}

for det in detFeds:
    print(det)
    fedList = []
    for minFed,maxFed in detFeds[det]:
        fedList += list(range(minFed, maxFed+1))
    fedList = sorted(list(set(fedList)))
    print(fedList)
    print('-'*50)
