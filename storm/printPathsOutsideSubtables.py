#!/usr/bin/env python3
import os

for foo in [
  'HLT', 'GRun', 'HIon', 'PRef', 'PIon', 'Special'
]:
  if not os.path.isfile(f'{foo}.py'):
    os.system(f'hltConfigFromDB --configName /dev/CMSSW_14_0_0/{foo} > {foo}.py')

from HLT import cms,process as hlt
from GRun import process as grun
from HIon import process as hion
from PRef import process as pref
from PIon import process as pion
from Special import process as special

paths = []
for foo in hlt.paths_():
  paths.append(foo)
paths = sorted(list(set(paths)))
for foo in paths:
  if foo in grun.paths_(): continue
  if foo in hion.paths_(): continue
  if foo in pref.paths_(): continue
  if foo in pion.paths_(): continue
  if foo in special.paths_(): continue
  print(foo[:foo.rfind('_v')+2] if '_v' in foo else foo)
