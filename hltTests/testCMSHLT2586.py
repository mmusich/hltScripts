#!/usr/bin/env python3
import FWCore.ParameterSet.Config as cms
import os
import json

def getESModuleDict(process):
  ret1 = {key:val.dumpPython() for key,val in process.es_producers_().items()}
  ret2 = {key:val.dumpPython() for key,val in process.es_sources_().items()}
  ret1.update(ret2)
  return ret1

def writeJSON(output_file):
  ###
  ### HLT
  ###
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
  os.system('''\
  cmsDriver.py RelVal -s RAW2DIGI,L1Reco,RECO --data --scenario=pp -n 10 --conditions auto:run3_data_GRun --relval 9000,50 \
    --datatier "RAW-HLT-RECO" --eventcontent FEVTDEBUGHLT --customise=HLTrigger/Configuration/CustomConfigs.L1THLT \
    --customise=HLTrigger/Configuration/CustomConfigs.HLTRECO --customise=HLTrigger/Configuration/CustomConfigs.customiseGlobalTagForOnlineBeamSpot \
    --era Run3 --processName=HLTRECO --filein file:RelVal_Raw_GRun_DATA.root --fileout file:RelVal_Raw_GRun_DATA_HLT_RECO.root \
    --python_filename recoData_cfg.py --dump_python --no_exec &> /dev/null
  ''')
  from recoData_cfg import cms,process as recoData
  reco_data = getESModuleDict(recoData)
  
  ###
  ### RECO (MC)
  ###
  os.system('''\
  cmsDriver.py RelVal -s RAW2DIGI,L1Reco,RECO --mc --scenario=pp -n 10 --conditions auto:run3_mc_GRun --relval 9000,50 \
    --datatier "RAW-HLT-RECO" --eventcontent FEVTDEBUGHLT --customise=HLTrigger/Configuration/CustomConfigs.L1THLT \
    --customise=HLTrigger/Configuration/CustomConfigs.HLTRECO \
    --era Run3 --processName=HLTRECO --filein file:RelVal_Raw_GRun_MC.root --fileout file:RelVal_Raw_GRun_MC_HLT_RECO.root \
    --python_filename recoMC_cfg.py --dump_python --no_exec &> /dev/null
  ''')
  from recoMC_cfg import cms,process as recoMC
  reco_mc = getESModuleDict(recoMC)
  
  json.dump({'HLT': hlt, 'RECO_Data': reco_data, 'RECO_MC': reco_mc},
    open(output_file,'w'), sort_keys=True, indent=2)

###
### main
###
if __name__ == '__main__':

  jsonOutFile = 'testCMSHLT2586.json'

  if not os.path.isfile(jsonOutFile):
    writeJSON(jsonOutFile)

  out = json.load(open(jsonOutFile))

  # check RECO
  for recoMC_mod in out['RECO_MC']:
    if recoMC_mod in out['RECO_Data']:
      if out['RECO_MC'][recoMC_mod] != out['RECO_Data'][recoMC_mod]:
        print('RECO diff:', recoMC_mod)
        print(out['RECO_Data'][recoMC_mod])
        print(out['RECO_MC'][recoMC_mod])
        print('---')
