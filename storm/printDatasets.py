#!/usr/bin/env python3
from GRun import cms,process

if __name__ == '__main__':

  datasetNames = []
  for pathName in process.paths_():
    if pathName.startswith('Dataset_'):
      datasetNames += [pathName[len('Dataset_'):]]
  datasetNames = sorted(list(set(datasetNames)))

  for datasetName in datasetNames:
    print(datasetName)
