#!/usr/bin/env python3
import os
import sys

import FWCore.ParameterSet.Config as cms

def getPathsDict(fileName):
  if not os.path.isfile(fileName):
    raise RuntimeError('not a file: '+fileName)

  # load HLT configuration
  try:
    foo = {'process': None}
    exec(open(fileName, 'r').read(), foo)
    process = foo['process']
  except:
    raise Exception(f'query did not return a valid python file:\n file="{fileName}"')

  if not isinstance(process, cms.Process):
    raise Exception(f'query did not return a valid HLT menu:\n file="{fileName}"')

  pathsDict = {}
  for pathName in process.paths_():
    pathName_unv = pathName[:pathName.rfind('_v')] if '_v' in pathName else pathName
    pathsDict[pathName_unv] = pathName

  return pathsDict

if len(sys.argv) < 3:
  raise RuntimeError('missing args')

file1 = sys.argv[1]
file2 = sys.argv[2]

paths1 = getPathsDict(file1)
paths2 = getPathsDict(file2)

for p2 in sorted(paths2.keys()):
  if p2 not in paths1 and not paths2[p2].endswith('_v1'):
    print(p2)
