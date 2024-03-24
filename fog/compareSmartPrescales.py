#!/usr/bin/env python3
import os
import sys

from HLTrigger.Configuration.common in producers_by_type

os.system(f'hltConfigFromDB --configName {sys.argv[1]} > hlt0.py')
from hlt0 import cms,process as hlt0

os.system(f'hltConfigFromDB --configName {sys.argv[2]} > hlt1.py')
from hlt1 import process as hlt1

def smartPrescaleMap(process):



    ret = {}
    for prod in producers_by_type(process, 'TriggerResultsFilter'):
        if not prod.label().startswith('hltDataset'):
            continue
        datasetName = prod.label()[len('hltDataset'):]
        ret[datasetName] = []
        for trigCond in prod.triggerConditions:
            trigCond_split = trigCond.split(' / ')

            pathName = trigCond_split[0] if len(trigCond_split) > 0

            ret[datasetName] += [[pathNameUnv, smartPrescaleStr]]


paths = sorted(list(set([foo for foo in hlt.paths_()])))
for foo in paths:
  if foo in grun.paths_(): continue
  if foo in hion.paths_(): continue
  if foo in pref.paths_(): continue
  if foo in pion.paths_(): continue
  if foo in spec.paths_(): continue
  print(foo[:foo.rfind('_v')+2] if '_v' in foo else foo)
