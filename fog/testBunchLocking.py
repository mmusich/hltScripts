#!/usr/bin/env python3
import sys

m_singlestep = 100
trigger_counter = 0

# https://github.com/cms-sw/cmssw/blob/d376eb350a3e9af9f0ce3618fbac6afc36ce56d8/L1Trigger/L1TGlobal/src/GlobalBoard.cc#L1241
def accept():
    global trigger_counter
    trigger_counter += m_singlestep
    if prescale_count == 0 or trigger_counter < prescale_count:
        return False
    trigger_counter -= prescale_count
    return True

if __name__ == '__main__':

    nBunches = int(sys.argv[1])
    l1aCounts = [0] * nBunches

    prescale = float(sys.argv[2])
    prescale_count = round(prescale * m_singlestep)

    nEventsPerBunch = int(sys.argv[3]) if len(sys.argv) > 3 else 10000
    nEvents = nBunches * nEventsPerBunch

    for event_i in range(nEvents):
        l1aCounts[event_i % nBunches] += int(accept())

    for bunch_i in range(nBunches):
        print(f' {bunch_i: >5d} {l1aCounts[bunch_i]: >8d}')
