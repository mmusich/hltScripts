#!/usr/bin/env python3
import os

os.system('hltConfigFromDB --configName /dev/CMSSW_14_0_0/HLT > HLT.py')
from HLT import cms,process as hlt

os.system('hltConfigFromDB --configName /dev/CMSSW_14_0_0/GRun > GRun.py')
from GRun import process as grun

os.system('hltConfigFromDB --configName /dev/CMSSW_14_0_0/HIon > HIon.py')
from HIon import process as hion

os.system('hltConfigFromDB --configName /dev/CMSSW_14_0_0/PRef > PRef.py')
from PRef import process as pref

os.system('hltConfigFromDB --configName /dev/CMSSW_14_0_0/PIon > PIon.py')
from PIon import process as pion

os.system('hltConfigFromDB --configName /dev/CMSSW_14_0_0/Special > Spec.py')
from Spec import process as spec

paths = sorted(list(set([foo for foo in hlt.paths_()])))
for foo in paths:
  if foo in grun.paths_(): continue
  if foo in hion.paths_(): continue
  if foo in pref.paths_(): continue
  if foo in pion.paths_(): continue
  if foo in spec.paths_(): continue
  print(foo[:foo.rfind('_v')+2] if '_v' in foo else foo)
