#!/usr/bin/env python3
import os
import json

pathOwnersDict = json.load(open(f'{os.environ["CMSSW_BASE"]}/src/HLTrigger/Configuration/scripts/utils/hltPathOwners.json'))

pathNames = [
'DST_PFScouting_DoubleMuon_v4',
'DST_PFScouting_DoubleEG_v4',
'DST_PFScouting_JetHT_v4',
'DST_PFScouting_DatasetMuon_v4',
'DST_PFScouting_AXOVLoose_v2',
'DST_PFScouting_AXOLoose_v2',
'DST_PFScouting_AXONominal_v4',
'DST_PFScouting_AXOTight_v4',
'DST_PFScouting_AXOVTight_v2',
'DST_PFScouting_SingleMuon_v4',
'DST_PFScouting_SinglePhotonEB_v1',
'DST_PFScouting_ZeroBias_v2',
'MC_PFScouting_v4',
'HLT_IsoMu20_v25',
'HLT_IsoMu24_v23',
'HLT_IsoMu24_TwoProngs35_v11',
'HLT_IsoMu24_OneProng32_v7',
'HLT_IsoMu24_eta2p1_v25',
'HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS20_eta2p1_SingleL1_v10',
'HLT_IsoMu24_eta2p1_PNetTauhPFJet20_eta2p2_SingleL1_v4',
'HLT_IsoMu24_eta2p1_PFHT250_v4',
'HLT_IsoMu24_eta2p1_PFHT250_QuadPFJet25_v4',
'HLT_IsoMu24_eta2p1_PFHT250_QuadPFJet25_PNet1Tauh0p50_v4',
'HLT_IsoMu24_eta2p1_SinglePFJet25_PNet1Tauh0p50_v4',
'HLT_IsoMu27_v26',
'HLT_IsoMu27_MediumChargedIsoDisplacedPFTauHPS24_eta2p1_SingleL1_v6',
'HLT_DoubleIsoMu20_eta2p1_v17',
'HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1_v11',
'HLT_IsoMu24_eta2p1_LooseDeepTauPFTauHPS30_eta2p1_CrossL1_v11',
'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Tight_eta2p3_CrossL1_ETau_Monitoring_v4',
'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Medium_eta2p3_CrossL1_ETau_Monitoring_v4',
'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Loose_eta2p3_CrossL1_ETau_Monitoring_v4',
'HLT_IsoMu20_eta2p1_PNetTauhPFJet27_Tight_eta2p3_CrossL1_v4',
'HLT_IsoMu20_eta2p1_PNetTauhPFJet27_Medium_eta2p3_CrossL1_v4',
'HLT_IsoMu20_eta2p1_PNetTauhPFJet27_Loose_eta2p3_CrossL1_v4',
'HLT_IsoMu24_eta2p1_LooseDeepTauPFTauHPS180_eta2p1_v11',
'HLT_IsoMu24_eta2p1_PNetTauhPFJet130_Loose_L2NN_eta2p3_CrossL1_v4',
'HLT_IsoMu24_eta2p1_PNetTauhPFJet130_Medium_L2NN_eta2p3_CrossL1_v4',
'HLT_IsoMu24_eta2p1_PNetTauhPFJet130_Tight_L2NN_eta2p3_CrossL1_v4',
'HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS35_L2NN_eta2p1_CrossL1_v11',
'HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS45_L2NN_eta2p1_CrossL1_v10',
'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Medium_L2NN_eta2p3_CrossL1_v4',
'HLT_IsoMu24_eta2p1_PNetTauhPFJet30_Tight_L2NN_eta2p3_CrossL1_v4',
'HLT_IsoMu24_eta2p1_PNetTauhPFJet45_L2NN_eta2p3_CrossL1_v4',
'HLT_IsoMu50_AK8PFJet220_SoftDropMass40_v10',
'HLT_IsoMu50_AK8PFJet220_SoftDropMass40_PNetBB0p06_v7',
'HLT_IsoMu50_AK8PFJet230_SoftDropMass40_v10',
'HLT_IsoMu50_AK8PFJet230_SoftDropMass40_PNetBB0p06_v7',
'HLT_IsoMu50_AK8PFJet230_SoftDropMass40_PNetBB0p10_v7',
'HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_CrossL1_v10',
'HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_PFJet60_CrossL1_v10',
'HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_PFJet75_CrossL1_v10',
'HLT_IsoMu24_eta2p1_PNetTauhPFJet26_L2NN_eta2p3_CrossL1_v4',
'HLT_IsoMu24_eta2p1_PNetTauhPFJet26_L2NN_eta2p3_CrossL1_PFJet60_v4',
'HLT_IsoMu24_eta2p1_PNetTauhPFJet26_L2NN_eta2p3_CrossL1_PFJet75_v4',
'HLT_IsoMu24_eta2p1_MediumDeepTauPFTauHPS30_L2NN_eta2p1_OneProng_CrossL1_v6',
'MC_IsoMu_v25',
]

pathNames = sorted([pathName if '_v' not in pathName else pathName[:pathName.rfind('_v')]+'_v' for pathName in pathNames if not pathName.startswith('Dataset_')])

groups = set()
for path in pathOwnersDict:
    if path not in pathNames:
        continue
    for group in pathOwnersDict[path]['owners']:
        groups.add(group)
groups = sorted(list(set(groups)))

for group in groups:
    print(group)
