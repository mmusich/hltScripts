#!/usr/bin/env python3
import json

dd = json.load(open('legacy_vs_AlpakaSericalSync.json'))

for ev in dd['events']:
    for tt in ev['t']:
        if tt['t'] != 481:
            continue
        if tt['o']['s'] != tt['n']['s']:
            print(ev['r'], ev['l'], ev['e'])
