#!/usr/bin/env python3
import sys

# not sure why i wrote this..

aa = open(sys.argv[1]).read().splitlines()
bxs = [int(foo) for foo in aa[0].replace('\t',' ').split()[1:-1]]
ind = [idx for idx,foo in enumerate(bxs) if foo > 0]
print(f'Number of BXs: {len(ind)}')
print(f'List of BX IDs (LHC convention): {ind}')
