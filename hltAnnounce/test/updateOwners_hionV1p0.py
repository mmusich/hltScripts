#!/usr/bin/env python3
import json

from hi_offl import cms, process as offl
from hi_onli import process as onli

dict0 = json.load(open('owners.json'))

def getUnvPathList(process):
  return [(foo[:foo.rfind('_v')]+'_v' if '_v' in foo else foo) for foo in process.paths_() if not foo.startswith('Dataset_')]

offl_paths = getUnvPathList(offl)
onli_paths = getUnvPathList(onli)

for pathName in offl_paths:

  if pathName in dict0:
    continue

  isOnline = pathName in onli_paths

  owners = []
  if 'DQM_HI' in pathName:
    owners = ['TSG (DQM)']
  elif 'HI' in pathName:
    if 'AlCa_Ecal' in pathName: owners = ['AlCa','ECAL']
    elif 'AlCa_RPCMuonNor' in pathName: owners = ['AlCa','RPC']
    elif 'Beamspot' in pathName: owners = ['AlCa','BeamSpot','HIon']
    else: owners = ['HIon']

  dict0[pathName] = { 'online?': isOnline, 'owners': owners }

  if not owners:
    print(pathName)
    print('  ', dict0[pathName]['owners'])

json.dump(dict0, open('tmp.json','w'), sort_keys=True, indent=2)
