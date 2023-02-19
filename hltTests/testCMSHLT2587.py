#!/usr/bin/env python3
import FWCore.ParameterSet.Config as cms
import os
import sys
import json

def getESModuleDict(process):
  ret1 = {key:val.dumpPython() for key,val in process.es_producers_().items()}
  ret2 = {key:val.dumpPython() for key,val in process.es_sources_().items()}
  ret1.update(ret2)
  ret3 = {key:val.dumpPython() for key,val in process.psets_().items()}
  ret1.update(ret3)
  return ret1

def writeJSON(output_file):
  ###
  ### HLT
  ###
  print('Loading HLT configuration...', file=sys.stderr)
  hltESModules = {}
  for menu in [
    'FULL',
  #  'GRun',
  #  'HIon',
  #  'PIon',
  #  'PRef',
  ]:
    proc = cms.Process("TEST")
    proc.load('HLTrigger.Configuration.HLT_'+menu+'_cff')
    hltESModules[menu] = getESModuleDict(proc)
    del proc
  for key in hltESModules:
    if hltESModules['FULL'] != hltESModules[key]:
      raise RuntimeError('HLT menu "'+key+'" has different EventSetup modules compared to HLT menu "FULL"')
  hlt = hltESModules['FULL']

  ###
  ### RECO (Data)
  ###
  print('Loading RECO (Data) configuration...', file=sys.stderr)
  os.system('''\
  cmsDriver.py RelVal -s RAW2DIGI,L1Reco,RECO --data --scenario=pp -n 10 --conditions auto:run3_data_GRun --relval 9000,50 \
    --datatier "RAW-HLT-RECO" --eventcontent FEVTDEBUGHLT --customise=HLTrigger/Configuration/CustomConfigs.L1THLT \
    --customise=HLTrigger/Configuration/CustomConfigs.HLTRECO --customise=HLTrigger/Configuration/CustomConfigs.customiseGlobalTagForOnlineBeamSpot \
    --era Run3 --processName=HLTRECO --filein file:RelVal_Raw_GRun_DATA.root --fileout file:RelVal_Raw_GRun_DATA_HLT_RECO.root \
    --python_filename testCMSHLT2587_recoData_cfg.py --dump_python --no_exec &> /dev/null
  ''')
  from testCMSHLT2587_recoData_cfg import process as recoData
  reco_data = getESModuleDict(recoData)

  ###
  ### RECO (MC)
  ###
  print('Loading RECO (MC) configuration...', file=sys.stderr)
  os.system('''\
  cmsDriver.py RelVal -s RAW2DIGI,L1Reco,RECO --mc --scenario=pp -n 10 --conditions auto:run3_mc_GRun --relval 9000,50 \
    --datatier "RAW-HLT-RECO" --eventcontent FEVTDEBUGHLT --customise=HLTrigger/Configuration/CustomConfigs.L1THLT \
    --customise=HLTrigger/Configuration/CustomConfigs.HLTRECO \
    --era Run3 --processName=HLTRECO --filein file:RelVal_Raw_GRun_MC.root --fileout file:RelVal_Raw_GRun_MC_HLT_RECO.root \
    --python_filename testCMSHLT2587_recoMC_cfg.py --dump_python --no_exec &> /dev/null
  ''')
  from testCMSHLT2587_recoMC_cfg import process as recoMC
  reco_mc = getESModuleDict(recoMC)

  # create output file in JSON format
  json.dump({'HLT': hlt, 'RECO_Data': reco_data, 'RECO_MC': reco_mc},
    open(output_file,'w'), sort_keys=True, indent=2)

###
### main
###
if __name__ == '__main__':

  jsonOutFile = 'testCMSHLT2587.json'

  if not os.path.isfile(jsonOutFile):
    writeJSON(jsonOutFile)

  out = json.load(open(jsonOutFile))

  checkRECO = False
  checkHLT = True

  # check RECO
  if checkRECO:
    for mod in out['RECO_MC']:
      if mod in out['RECO_Data']:
        if out['RECO_MC'][mod] != out['RECO_Data'][mod]:
          print('RECO diff:', mod)
          print(out['RECO_Data'][mod])
          print(out['RECO_MC'][mod])
          print('---')

  # check HLT
  if checkHLT:

    for inputType in ['MC', 'Data']:
      mods = []
      for mod in out['HLT']:
        if mod in out['RECO_'+inputType]:
          if out['HLT'][mod] != out['RECO_'+inputType][mod]:
            mods += [mod]

      with open('testCMSHLT2587_diff_HLT.txt', 'w') as ofile:
        for mod in mods:
          ofile.write(mod+' = '+out['HLT'][mod]+'\n')

      with open('testCMSHLT2587_diff_'+inputType+'.txt', 'w') as ofile:
        for mod in mods:
          ofile.write(mod+' = '+out['RECO_'+inputType][mod]+'\n')
