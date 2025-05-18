#!/usr/bin/env python3
from a1 import cms,process

ret = []
for pp in process.paths_():
    if not pp.startswith('Dataset_'): continue
    ret += [pp.replace('Dataset_','')]

ret = sorted(list(set(ret)))

for ff in ret:
    print(ff)
