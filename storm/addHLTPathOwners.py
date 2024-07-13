#!/usr/bin/env python3
import os
import json

pathOwnersDict = json.load(open(f'{os.environ["CMSSW_BASE"]}/src/HLTrigger/Configuration/scripts/utils/hltPathOwners.json'))

pathNames = [
  'HLT_DoubleMu3_DZ_PFMET50_PFMHT60_v',
  'HLT_DoubleMu3_DZ_PFMET70_PFMHT70_v',
  'HLT_DoubleMu3_DZ_PFMET90_PFMHT90_v',
  'HLT_DoubleMu4_Mass3p8_DZ_PFHT350_v',
  'HLT_Mu3er1p5_PFJet100er2p5_PFMET100_PFMHT100_IDTight_v',
  'HLT_Mu3er1p5_PFJet100er2p5_PFMET80_PFMHT80_IDTight_v',
  'HLT_Mu3er1p5_PFJet100er2p5_PFMET90_PFMHT90_IDTight_v',
  'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu100_PFMHTNoMu100_IDTight_v',
  'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu80_PFMHTNoMu80_IDTight_v',
  'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu90_PFMHTNoMu90_IDTight_v',
  'HLT_TripleMu_5_3_3_Mass3p8_DCA_v',
  'HLT_DoubleMu3_DCA_PFMET50_PFMHT60_Mass2p0_noDCA_v',
  'HLT_DoubleMu3_DCA_PFMET50_PFMHT60_Mass2p0_v',
  'HLT_DoubleMu3_DCA_PFMET50_PFMHT60_v',
]

for pathName in pathNames:
    if pathName not in pathOwnersDict:
        print(f'WARNING -- Path not found: {pathName}')
    pathOwnersDict[pathName]['owners'] += ['EXO']
    pathOwnersDict[pathName]['owners'] = sorted(list(set(pathOwnersDict[pathName]['owners'])))

#for pathName in pathOwnersDict:
#    if 'EXO' in pathOwnersDict[pathName]['owners'] and pathName not in pathNames:
#        print(f'WARNING -- Path not found: {pathName}')

json.dump(pathOwnersDict, open(f'{os.environ["CMSSW_BASE"]}/src/HLTrigger/Configuration/scripts/utils/hltPathOwners.json', 'w'), sort_keys=True, indent=2)
