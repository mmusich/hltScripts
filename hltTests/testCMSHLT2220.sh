opts="--dbproxy --eras Run3 --mc --globaltag auto:phase1_2021_realistic --unprescale --input /store/mc/Run3Summer21DRPremix/WprimeToMuNu_M-5000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/120X_mcRun3_2021_realistic_v6-v2/2550000/026722bd-ccc5-4da2-9295-13896532d7ab.root --max-events 100 --full --offline --no-output"

#hltGetConfiguration /dev/CMSSW_12_3_0/HLT \
# --customise \
#HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForPatatrackWithIsoAndTriplets,\
#HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForPatatrackTkMu,\
#HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForPatatrackNoVtx,\
#HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForPatatrackOpenMu,\
#HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeIOSeedingPatatrack\
# ${opts} > hlt_muon.py
#edmConfigDump hlt_muon.py > hlt_muon_dump.py
#edmConfigDump --prune hlt_muon.py > hlt_muon_dumpPruned.py
##cmsRun hlt_muon_dump.py &> hlt_muon_dump.log
#
#hltGetConfiguration /users/missirol/test/dev/CMSSW_12_3_0/CMSHLT_2220/IntegTest_v03/HLT/V2 \
# ${opts} > hlt_tsgTest1.py
#edmConfigDump hlt_tsgTest1.py > hlt_tsgTest1_dump.py
#edmConfigDump --prune hlt_tsgTest1.py > hlt_tsgTest1_dumpPruned.py
##cmsRun hlt_tsgTest1_dump.py &> hlt_tsgTest1_dump.log

#hltGetConfiguration /users/missirol/test/dev/CMSSW_12_3_0/CMSHLT_2220/IntegTest_v03/HLT/V2 \
# --paths HLTriggerFirstPath,HLT_IsoMu24_v*,HLT_Mu50_v*,\
#HLT_PFMET120_PFMHT120_IDTight_v*,HLT_TrimuonOpen_5_3p5_2_Upsilon_Muon_v*,\
#DST_Run3_PFScoutingPixelTracking_v*,HLTriggerFinalPath,HLTAnalyzerEndpath\
# ${opts} > hlt_tsgTest2.py
##edmConfigDump hlt_tsgTest2.py > hlt_tsgTest2_dump.py
##edmConfigDump --prune hlt_tsgTest2.py > hlt_tsgTest2_dumpPruned.py
#cmsRun hlt_tsgTest2.py &> hlt_tsgTest2.log

hltGetConfiguration /dev/CMSSW_12_3_0/GRun \
 ${opts} > hlt_tsgTest3.py
edmConfigDump hlt_tsgTest3.py > hlt_tsgTest3_dump.py
edmConfigDump --prune hlt_tsgTest3.py > hlt_tsgTest3_dumpPruned.py
cmsRun hlt_tsgTest3.py &> hlt_tsgTest3.log
