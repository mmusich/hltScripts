#!/usr/bin/env python3

errors = []

with open('f3mon_logtable_2023-04-30T09 25 51.685Z.txt') as ifile:
  lines = ifile.read().splitlines()
  errorIdx = -1
  for line in lines:
    if line.startswith('msgtime:'):
      errorIdx += 1
      errors.append([])
    if errorIdx >= 0:
      errors[errorIdx] += [line]

nL1RegionData = 0
nOthers = 0

for errorLines in errors:

  badLines = []

  check = -1
  hasL1RegionData = False

  for line in errorLines:
    if check >= 10:
      break

    if 'sig_dostack_then_abort' in line:
      if check >= 0:
        raise RuntimeError(f'double sig_dostack_then_abort: {line}')
      else:
        check = 0

    if check >= 0:
      check += 1
      if 'HLTRecHitInAllL1RegionsProducer' in line:
        hasL1RegionData = True
      badLines += [line]

  if hasL1RegionData:
    nL1RegionData += 1
  else:
    for line in badLines:
      print(line)
    if len(badLines) > 0:
      print('-'*100)

  if check < 0:
    nOthers += 1
    for line in errorLines:
      print(line)
    if len(errorLines) > 0:
      print('-'*100)

print(f'Number of Errors: {errorIdx+1} (L1RegionData = {nL1RegionData}, Others = {nOthers})')
