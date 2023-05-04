Copy/paste bin contents from JSON data of L1T histogram in online-DQM, e.g.

L1T/L1TStage2uGT/algoBits_before_bxmask_bx_global

The following returns the list of BXs with data in LHC convention (L1T convention = LHC+2, HLT/CMSSW convention = LHC+1)

```
#!/usr/bin/env python3
import sys

aa = open(sys.argv[1]).read().splitlines()
bxs = [int(foo) for foo in aa[0].replace('\t',' ').split()[1:-1]]
ind = [idx for idx,foo in enumerate(bxs) if foo > 0]
print(f'Number of BXs: {len(ind)}')
print(f'List of BX IDs (LHC convention): {ind}')
```
