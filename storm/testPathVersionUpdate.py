#!/usr/bin/env python3
import os
import sys

if len(sys.argv) < 3:
  raise RuntimeError('missing args')

oldFile = sys.argv[1]
newFile = sys.argv[2]

if not os.path.isfile(oldFile):
  raise RuntimeError('not a file: '+oldFile)

if os.path.exists(newFile):
  raise RuntimeError('exists: '+newFile)

dirname = os.path.dirname(os.path.abspath(__file__))
tmpFile = dirname+'/tmp.py'

# hltConfigFromDB --configName XXX > hlt.py
os.system('cp -p '+oldFile+' '+tmpFile)
from tmp import cms,process
with open(oldFile, 'rt') as fin:
  data = fin.read()
  for pathNameOld in process.paths_():
    if '_v' not in pathNameOld: continue
    pathNameNew = pathNameOld[:pathNameOld.rfind('_v')]+'_v1'
    data = data.replace(pathNameOld, pathNameNew)
    print(pathNameNew)
  with open(newFile, 'wt') as fou:
    fou.write(data)
os.remove(tmpFile)
