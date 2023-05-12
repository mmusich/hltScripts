# hltConfigFromDB --configName --adg /cdaq/test/missirol/test/2023/week18/CMSLITOPS_411/Test02/HLT/V1 > hlt.py
from hlt import cms,process

problematicPaths = []
for pathName,path in process.paths_().items():
  if pathName.startswith('Dataset_'): continue
  hasProblem = False
  for (type_i, label_i) in path.expandAndClone().directDependencies():
    if type_i != 'modules': continue    
    module_i = getattr(process, label_i)
    if not hasProblem:
      if label_i == 'hltGtStage2Digis':
        hasProblem = True
    else:
      if module_i.type_() == 'HLTL1TSeed':
        hasProblem = False
  if hasProblem:
    problematicPaths += [pathName]

for foo in problematicPaths:
  print(foo)
