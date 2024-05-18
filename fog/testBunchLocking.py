#!/usr/bin/env python3
import sys

nBunches = int(sys.argv[1])
prescale = float(sys.argv[2])

m_singlestep = 100
trigger_counter = 0

prescale_count = round(prescale * m_singlestep)

nEvents = 10000 * nBunches

l1aCounts = [0] * nBunches

# https://github.com/cms-sw/cmssw/blob/d376eb350a3e9af9f0ce3618fbac6afc36ce56d8/L1Trigger/L1TGlobal/src/GlobalBoard.cc#L1241
def accept():
    global trigger_counter
    trigger_counter += m_singlestep
    if prescale_count == 0 or trigger_counter < prescale_count:
        return False
    trigger_counter -= prescale_count
    return True

for event_i in range(nEvents):
    l1aCounts[event_i % nBunches] += int(accept())

for bunch_i in range(nBunches):
    print(f' {bunch_i: >5d} {l1aCounts[bunch_i]: >8d}')
