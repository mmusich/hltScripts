from hion_tsg import cms,process as tsg
from hion_pag import process as hin

####################################################

paths1 = sorted(list(tsg.paths_().keys()))
paths2 = sorted(list(hin.paths_().keys()))

for foo2 in paths2:
  foo1 = foo2.replace('HIDataRawPrime','HITestRawPrime')
  foo1 = foo1.replace('HIData','HITestRaw')

#  if foo.startswith('Dataset_'):
#    continue
  if foo1 not in paths1:
    print('path missing: '+foo1)
    continue

  if foo2.startswith('Dataset_'):
    tsg_pd = sorted([bar for bar in getattr(tsg, 'hltDataset'+foo1[8:]).triggerConditions if hasattr(hin, bar.split(' / ')[0])])
    hin_pd = sorted([bar for bar in getattr(hin, 'hltDataset'+foo2[8:]).triggerConditions])
    if tsg_pd != hin_pd:
      print('dataset differs: '+foo2)
      print(tsg_pd)
      print(hin_pd)
      continue

####################################################

fpaths1 = sorted(list(tsg.finalpaths_().keys()))
fpaths2 = sorted(list(hin.finalpaths_().keys()))

for foo2 in fpaths2:
  foo1 = foo2.replace('HIDataRawPrime','HITestRawPrime')
  foo1 = foo1.replace('HIData','HITestRaw')

  if foo1 not in fpaths1:
    print('finalpath missing: '+foo1)
    continue

  ec1 = getattr(tsg, 'hltOutput'+foo1[:-6]).outputCommands
  ec2 = getattr(hin, 'hltOutput'+foo2[:-6]).outputCommands
  if ec1 != ec2:
    print('eventcontent differs: '+foo1)
