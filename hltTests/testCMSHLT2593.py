from hlt import cms,process as hlt
from grun import process as grun
from hion import process as hion
from pref import process as pref
from pion import process as pion

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
