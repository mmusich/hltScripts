#!/usr/bin/env python3
import sys

def getProcess(filepath):
  foo = {'process': None}
  exec(open(filepath, 'r').read(), foo)
  return foo['process']

if __name__ == '__main__':

  process = getProcess(sys.argv[1])

  streams_whitelist = [
    'ReleaseValidation',
  ]

  print('# datasets')

  emptyDatasets = []

  for dsetKey, dsetVal in process.datasets.parameters_().items():
    if len(dsetVal) > 0: continue
    emptyDatasets.append(dsetKey)

  for dsetKey in emptyDatasets:
    print(dsetKey)

  print('\n# streams')

  emptyStreams = []

  for streamKey, streamVal in process.streams.parameters_().items():
    dsetList = [dset for dset in streamVal if dset not in emptyDatasets]
    if len(dsetList) > 0 or streamKey in streams_whitelist: continue
    emptyStreams.append(streamKey)

  for streamKey in emptyStreams:
    print(streamKey)
