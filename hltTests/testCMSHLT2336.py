from hlt2336 import cms,process as process1
from hlt2336_2 import process as process2

pathNames = process1.paths_().keys()[:]

pathsToBeDisabledRaw = [
  'HLT_TrkMu17_DoubleTrkMu8NoFiltersNoVtx_v',
  'HLT_TrkMu16_DoubleTrkMu6NoFiltersNoVtx_v',
  'HLT_TripleMu_5_3_3_Mass3p8_DCA_v',
  'HLT_Mu23_Mu12_v',
  'HLT_Mu23_Mu12_SameSign_v',
  'HLT_Mu23_Mu12_SameSign_DZ_v',
  'HLT_Mu23_Mu12_DZ_v',
  'HLT_Mu20_Mu10_v',
  'HLT_Mu20_Mu10_SameSign_v',
  'HLT_Mu20_Mu10_SameSign_DZ_v',
  'HLT_Mu20_Mu10_DZ_v',
  'HLT_Mu18_Mu9_v',
  'HLT_Mu18_Mu9_SameSign_DZ_v',
  'HLT_Mu18_Mu9_DZ_v',
  'HLT_DoubleMu40NoFiltersNoVtxDisplaced_v',
  'HLT_DoubleL2Mu50_v',
  'HLT_DoubleL2Mu25NoVtx_2Cha_NoL2Matched_v',
  'HLT_DoubleL2Mu25NoVtx_2Cha_CosmicSeed_NoL2Matched_v',
  'HLT_DoubleL2Mu23NoVtx_2Cha_NoL2Matched_v',
  'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched_v',
  'HLT_Photon90_CaloIdL_PFHT700_v',
  'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ600DEta3_v',
  'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_CaloMJJ400_PFJetsMJJ600DEta3_v',
  'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_CaloMJJ300_PFJetsMJJ400DEta3_v',
  'HLT_Photon60_R9Id90_CaloIdL_IsoL_v',
  'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_v',
  'HLT_Photon50_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_PFMET50_v',
  'HLT_Photon120EB_TightID_TightIso_v',
  'HLT_Photon100EEHE10_v',
  'HLT_Photon100EE_TightID_TightIso_v',
  'HLT_Photon100EB_TightID_TightIso_v',
  'HLT_Ele300_CaloIdVT_GsfTrkIdT_v',
  'HLT_Ele27_Ele37_CaloIdL_MW_v',
  'HLT_Ele250_CaloIdVT_GsfTrkIdT_v',
  'HLT_Ele200_CaloIdVT_GsfTrkIdT_v',
  'HLT_Ele20_WPTight_Gsf_v',
  'HLT_Ele20_eta2p1_WPLoose_Gsf_v',
  'HLT_Ele17_WPLoose_Gsf_v',
  'HLT_Ele15_Ele8_CaloIdL_TrackIdL_IsoVL_v',
  'HLT_Ele15_CaloIdL_TrackIdL_IsoVL_PFJet30_v',
  'HLT_Ele145_CaloIdVT_GsfTrkIdT_v',
  'HLT_Diphoton30PV_18PV_R9Id_AND_IsoCaloId_AND_HE_R9Id_Mass55_v',
  'HLT_L1UnpairedBunchBptxPlus_v',
  'HLT_L1UnpairedBunchBptxMinus_v',
  'HLT_L1NotBptxOR_v',
  'HLT_DiPFJet25_NoCaloMatched_v',
  'HLT_DiPFJet15_NoCaloMatched_v',
  'HLT_DiPFJetAve35_HFJEC_v',
  'HLT_DiPFJetAve25_HFJEC_v',
  'HLT_DiPFJetAve15_HFJEC_v',
  'HLT_DiPFJet25_FBEta3_NoCaloMatched_v',
  'HLT_DiPFJet15_FBEta3_NoCaloMatched_v',
  'HLT_SinglePhoton20_Eta3p1ForPPRef_v',
  'HLT_SinglePhoton10_Eta3p1ForPPRef_v',
  'HLT_SinglePhoton30_Eta3p1ForPPRef_v',
  'HLT_RsqMR320_Rsq0p09_MR200_v',
  'HLT_RsqMR320_Rsq0p09_MR200_4jet_v',
  'HLT_RsqMR300_Rsq0p09_MR200_v',
  'HLT_RsqMR300_Rsq0p09_MR200_4jet_v',
  'HLT_Rsq0p40_v',
  'HLT_Rsq0p35_v',
  'HLT_PFJet25_v',
  'HLT_PFJet15_v',
  'HLT_PFHT800_PFMET85_PFMHT85_IDTight_v',
  'HLT_PFHT700_PFMET95_PFMHT95_IDTight_v',
  'HLT_PFHT350MinPFJet15_v',
  'HLT_AK8PFJet25_v',
  'HLT_AK8PFJet15_v',
  'HLT_PFMET140_PFMHT140_IDTight_CaloBTagDeepCSV_3p1_v',
  'HLT_PFMET130_PFMHT130_IDTight_CaloBTagDeepCSV_3p1_v',
  'HLT_PFMET120_PFMHT120_IDTight_CaloBTagDeepCSV_3p1_v',
  'HLT_PFMET110_PFMHT110_IDTight_CaloBTagDeepCSV_3p1_v',
  'HLT_PFMET100_PFMHT100_IDTight_CaloBTagDeepCSV_3p1_v',
  'HLT_MonoCentralPFJet80_PFMETNoMu140_PFMHTNoMu140_IDTight_v',
  'HLT_MonoCentralPFJet80_PFMETNoMu130_PFMHTNoMu130_IDTight_v',
  'HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight_v',
  'HLT_MonoCentralPFJet80_PFMETNoMu110_PFMHTNoMu110_IDTight_v',
  'HLT_CaloMET80_NotCleaned_v',
  'HLT_CaloMET300_NotCleaned_v',
  'HLT_CaloMET250_NotCleaned_v',
  'HLT_CaloMET110_NotCleaned_v',
  'HLT_CaloMET100_NotCleaned_v',
  'HLT_Mu12_DoublePhoton20_v',
  'HLT_DoubleMu20_7_Mass0to30_Photon23_v',
  'HLT_DoubleMu20_7_Mass0to30_L1_DM4EG_v',
  'HLT_DoubleMu20_7_Mass0to30_L1_DM4_v',
  'HLT_DiMu4_Ele9_CaloIdL_TrackIdL_DZ_Mass3p8_v',
  'HLT_Mu9_IP6_ToCSCS_v',
  'HLT_Mu9_IP5_ToCSCS_v',
  'HLT_Mu9_IP4_ToCSCS_v',
  'HLT_Mu8_IP6_ToCSCS_v',
  'HLT_Mu8_IP5_ToCSCS_v',
  'HLT_Mu8_IP3_ToCSCS_v',
  'HLT_Mu7_IP4_ToCSCS_v',
  'HLT_Mu12_IP6_ToCSCS_v',
  'HLT_L2Mu50_v',
  'HLT_L2Mu10_v',
  'HLT_L1SingleMu25_v',
  'HLT_L1SingleMu18_v',
  'HLT_IsoMu30_v',
  'HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_v',
  'HLT_TrkMu6NoFiltersNoVtx_v1',
  'HLT_TrkMu16NoFiltersNoVtx_v1',
  'HLT_DoubleTrkMu_16_6_NoFiltersNoVtx_v1',
  'HLT_IsoMu27_MET90_v3',
  'HLT_IsoMu27_LooseChargedIsoPFTau20_Trk1_eta2p1_SingleL1_v5',
]

pathsToBeDisabled = []
for dp in pathsToBeDisabledRaw:
  dp_unv = dp[:dp.rfind('_v')+2]
  len1 = len(pathsToBeDisabled)
  for pn in pathNames:
    if pn.startswith(dp_unv):
      pathsToBeDisabled += [pn]
  if len1 == len(pathsToBeDisabled):
    print('!!!', dp)

pathsToBeDisabled = sorted(list(set(pathsToBeDisabled)))

#for aa in pathsToBeDisabled:
#  print(aa)

print(len(pathsToBeDisabledRaw), len(pathsToBeDisabled))

col1 = process1.PrescaleService.lvl1Labels
col2 = process2.PrescaleService.lvl1Labels

if col1 != col2:
  print('COLUMNS DIFFER')
else:
  ps1 = {}
  for pset_i in process1.PrescaleService.prescaleTable:
    ps1[pset_i.pathName.value()] = pset_i.prescales.value()

  ps2 = {}
  for pset_i in process2.PrescaleService.prescaleTable:
    ps2[pset_i.pathName.value()] = pset_i.prescales.value()

  hltPaths = list(ps1.keys())
  hltPaths += list(ps2.keys())
  hltPaths = sorted(list(set(hltPaths)))

  for hltp in hltPaths:
    if hltp not in ps1:
      print(f'{hltp} : ERROR , MISSING IN MENU 1')
    elif hltp not in ps2:
      print(f'{hltp} : ERROR , MISSING IN MENU 2')
    else:
      if hltp in pathsToBeDisabled:
        if ps2[hltp] == len(col2)*[0]:
          pass
        else:
          print(f'{hltp} : ERROR , PRESCALES ARE NOT ZERO FOR PATH TO BE DISABLED')
      else:
        if ps1[hltp] != ps2[hltp]:
          print(f'{hltp} : ERROR , PRESCALES DIFFER for NON-DISABLED PATH')
          str1 = ' '*10+'old - '
          for psv1 in ps1[hltp]:
            str1 += ' {: >5d}'.format(psv1)
          print(str1)
          str2 = ' '*10+'new - '
          for psv2 in ps2[hltp]:
            str2 += ' {: >3d}'.format(psv2)
          print(str2)
