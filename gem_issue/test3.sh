
cmsDriver.py --python_filename L1REPACK_FullMC_cmsDriver.py -s L1REPACK:FullMC --mc -n 10 --conditions auto:run3_mc_GRun --customise=HLTrigger/Configuration/CustomConfigs.L1T \
 --era Run3 --filein /store/relval/CMSSW_12_2_0_pre2/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/122X_mcRun3_2021_realistic_v1-v1/2580000/5541adab-cc2d-4401-b069-8140c90078c8.root
# --customise_commands=\'if hasattr(process,"simMuonGEMPadTask"): setattr(process,"simMuonGEMPadTask",cms.Task())\'',

#hltGetConfiguration /dev/CMSSW_12_2_0/GRun --dbproxy \
# --input /store/relval/CMSSW_12_2_0_pre2/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/122X_mcRun3_2021_realistic_v1-v1/2580000/5541adab-cc2d-4401-b069-8140c90078c8.root \
# --mc --globaltag auto:run3_mc_GRun --unprescale --output none --paths HLTriggerFirstPath,HLTriggerFinalPath --l1-emulator FullMC > L1REPACK_FullMC_hltGetConf.py
