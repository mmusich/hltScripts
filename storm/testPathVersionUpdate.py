#!/usr/bin/env python3
import os
import sys

# cp ../../../hltScripts/storm/testPathVersionUpdate.py .
# hltConfigFromDB --configName /dev/CMSSW_13_0_0/HLT/V75 > hlt0.py
# hltConfigFromDB --configName /dev/CMSSW_13_0_0/HLT/V76 > hlt1.py
# rm -f hlt0_new.py hlt1_new.py
# ./testPathVersionUpdate.py hlt0.py hlt0_new.py
# ./testPathVersionUpdate.py hlt1.py hlt1_new.py
# rm ./testPathVersionUpdate.py

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
