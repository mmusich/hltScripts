#!/usr/bin/env python3

if __name__ == '__main__':

  dsetDict = {}

  for hltMenuType in [
    'GRun',
    'HIon',
    'PIon',
    'PRef',
    'Fake',
    'Fake1',
    'Fake2',
  ]:
    if hltMenuType == 'GRun':
      from HLTrigger.Configuration.HLT_GRun_cff import cms,fragment

    elif hltMenuType == 'HIon':
      from HLTrigger.Configuration.HLT_HIon_cff import cms,fragment

    elif hltMenuType == 'PIon':
      from HLTrigger.Configuration.HLT_PIon_cff import cms,fragment

    elif hltMenuType == 'PRef':
      from HLTrigger.Configuration.HLT_PRef_cff import cms,fragment

    elif hltMenuType == 'Fake':
      from HLTrigger.Configuration.HLT_Fake_cff import cms,fragment

    elif hltMenuType == 'Fake1':
      from HLTrigger.Configuration.HLT_Fake1_cff import cms,fragment

    elif hltMenuType == 'Fake2':
      from HLTrigger.Configuration.HLT_Fake2_cff import cms,fragment

    else:
      raise Exception('invalid type of HLT menu (must be "GRun", "HIon", "PIon", or "PRef")')

    foo = {'process': None}
    exec(open('tmp_'+hltMenuType+'.py', 'r'), foo)
    process = foo['process']

    dsetDict[hltMenuType] = []
    for dsetName in process.datasets.parameterNames_():
      dsetDict[hltMenuType].append(dsetName)

  for hltMenuType in dsetDict:
    print('-'*50, hltMenuType, '-'*50)
    dsets = sorted(list(set(dsetDict[hltMenuType])))
    dsetStrFormat = 'Dataset_{: <'+str(max([len(tmp) for tmp in dsets]))+'} # CMSHLT-2245'
    for dsetName in dsets:
      print(dsetStrFormat.format(dsetName))

#for ttt in GRun HIon PIon PRef; do
#  echo "" >> "${ttt}".txt
#  ./printDatasets.py "${ttt}" >> "${ttt}".txt
#  echo "" >> online_"${ttt,,}".txt
#  ./printDatasets.py "${ttt}" >> online_"${ttt,,}".txt
#done
#unset ttt
