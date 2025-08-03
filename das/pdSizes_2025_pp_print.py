#!/usr/bin/env python3
import json

tmp = json.load(open('tmp.json'))


prompt = 0
parking = 0
scouting = 0

for group in tmp:
    for pd_stats in tmp[group]:
        if group.startswith('Physics'): prompt += pd_stats[1]
        if group.startswith('Parking'): parking += pd_stats[1]
        if group.startswith('HLT-Scouting'): scouting += pd_stats[1]

prompt /= 1e15
parking /= 1e15
scouting /= 1e15

prompt_exp = 2.8 * 1.2 * 6.5
parking_exp = 6.0 * 1.1 * 6.5
scouting_exp = 30 * 0.012 * 6.5

prompt_exp *= 37./120.
parking_exp *= 37./120.
scouting_exp *= 37./120.

print(f'prompt   : {prompt:>5.2f} vs {prompt_exp:>5.2f}')
print(f'parking  : {parking:>5.2f} vs {parking_exp:>5.2f}')
print(f'scouting : {scouting:>5.2f} vs {scouting_exp:>5.2f}')
