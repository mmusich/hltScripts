#!/usr/bin/env python3
import os

for hltCmd in [
    'hltConfigFromDB --configName /dev/CMSSW_15_0_0/HLT > HLT.py',
    'hltConfigFromDB --configName /dev/CMSSW_15_0_0/GRun > GRun.py',
    'hltConfigFromDB --configName /dev/CMSSW_15_0_0/HIon > HIon.py',
    'hltConfigFromDB --configName /dev/CMSSW_15_0_0/PRef > PRef.py',
    'hltConfigFromDB --configName /dev/CMSSW_15_0_0/PIon > PIon.py',
    'hltConfigFromDB --configName /dev/CMSSW_15_0_0/Special > Spec.py',
]:
    print(hltCmd)
    os.system(f'{hltCmd}')

from HLT import cms,process as hlt
from GRun import process as grun
from HIon import process as hion
from PRef import process as pref
from PIon import process as pion
from Spec import process as spec

paths = []
for pathlist in [hlt.paths_(), hlt.endpaths_()]:
  for foo in pathlist:
    paths.append(foo)
paths = sorted(list(set(paths)))

for foo in paths:
  if foo in grun.paths_(): continue
  if foo in hion.paths_(): continue
  if foo in pref.paths_(): continue
  if foo in pion.paths_(): continue
  if foo in spec.paths_(): continue
  if foo in grun.endpaths_(): continue
  if foo in hion.endpaths_(): continue
  if foo in pref.endpaths_(): continue
  if foo in pion.endpaths_(): continue
  if foo in spec.endpaths_(): continue
  print(foo[:foo.rfind('_v')+2] if '_v' in foo else foo)
