# for foo in HLT GRun HIon PRef PIon ; do hltConfigFromDB --configName /dev/CMSSW_13_0_0/"${foo}" > "${foo}".py ; done ; unset foo ;
from HLT import cms,process as hlt
from GRun import process as grun
from HIon import process as hion
from PRef import process as pref
from PIon import process as pion

paths = []
for foo in hlt.paths_():
  paths.append(foo)
paths = sorted(list(set(paths)))
for foo in paths:
  if foo in grun.paths_(): continue
  if foo in hion.paths_(): continue
  if foo in pref.paths_(): continue
  if foo in pion.paths_(): continue
  print(foo[:foo.rfind('_v')+2] if '_v' in foo else foo)
