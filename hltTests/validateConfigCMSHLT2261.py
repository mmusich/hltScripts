import FWCore.ParameterSet.Config as cms

# hltGeConfiguration /users/dmytro/dimuon/HLT/V2 > ref_dima.py
from ref_dima import process as process1
# hltGetConfiguration /users/missirol/test/dev/CMSSW_12_3_0/CMSHLT_2261/IntegTest_v02/HLT/V2 > target.py
from target import process as process2

def updateL1TSeedName(seed):
  ret = seed
  if   seed == "L1_DoubleMuOpen_er1p4_OS_dEta_Max1p6": ret = "L1_DoubleMu0er1p4_OQ_OS_dEta_Max1p6"
  elif seed == "L1_DoubleMu4p5er2p0_SQ_OS_Mass7to18": ret = "L1_DoubleMu4p5er2p0_SQ_OS_Mass_7to18"
  elif seed == "L1_TripleMu_2_1p5_0OQ_Mass_Max_15": ret = "L1_TripleMu_2_1p5_0OQ_Mass_Max15"
  elif seed == "L1_TripleMu_2SQ_1p5SQ_0OQ_Mass_Max_15": ret = "L1_TripleMu_2SQ_1p5SQ_0OQ_Mass_Max15"
  elif seed == "L1_MuShower_OneNominal": ret = "L1_SingleMuShower_Nominal"
  elif seed == "L1_MuShower_OneTight": ret = "L1_SingleMuShower_Tight"
  elif seed == "L1_DoubleMu3_OS_DoubleEG7p5Upsilon": ret = "L1_DoubleMu3_OS_er2p3_Mass_Max14_DoubleEG7p5_er2p1_Mass_Max20"
  elif seed == "L1_DoubleMu5Upsilon_OS_DoubleEG3": ret = "L1_DoubleMu5_OS_er2p3_Mass_8to14_DoubleEG3er2p1_Mass_Max20"
  elif seed == "L1_DoubleIsoTau26er2p1_Jet55_OvRm_dR0p5": ret = "L1_DoubleIsoTau26er2p1_Jet55_RmOvlp_dR0p5"
  elif seed == "L1_QuadJet36er2p5_IsoTau52er2p1": ret = "L1_IsoTau52er2p1_QuadJet36er2p5"
  elif seed == "L1_HTT280er_QuadJet_70_55_40_35_er2p4": ret = "L1_HTT280er_QuadJet_70_55_40_35_er2p5"
  elif seed == "L1_HTT320er_QuadJet_70_55_40_40_er2p4": ret = "L1_HTT320er_QuadJet_70_55_40_40_er2p5"
  elif seed == "L1_ETMHF90_SingleJet60er2p5_ETMHF90_DPHI_MIN2p094": ret = "L1_ETMHF90_SingleJet60er2p5_dPhi_Min2p1"
  elif seed == "L1_ETMHF90_SingleJet60er2p5_ETMHF90_DPHI_MIN2p618": ret = "L1_ETMHF90_SingleJet60er2p5_dPhi_Min2p6"
  elif seed == "L1_ETMHF90_SingleJet80er2p5_ETMHF90_DPHI_MIN2p094": ret = "L1_ETMHF90_SingleJet80er2p5_dPhi_Min2p1"
  elif seed == "L1_ETMHF90_SingleJet80er2p5_ETMHF90_DPHI_MIN2p618": ret = "L1_ETMHF90_SingleJet80er2p5_dPhi_Min2p6"
  elif seed == "L1_DoubleEG5er1p22_dR_0p9": ret = "L1_DoubleEG5_er1p2_dR_Max0p9"
  elif seed == "L1_DoubleEG5p5er1p22_dR_0p8": ret = "L1_DoubleEG5p5_er1p2_dR_Max0p8"
  elif seed == "L1_DoubleEG6er1p22_dR_0p8": ret = "L1_DoubleEG6_er1p2_dR_Max0p8"
  elif seed == "L1_DoubleEG6p5er1p22_dR_0p8": ret = "L1_DoubleEG6p5_er1p2_dR_Max0p8"
  elif seed == "L1_DoubleEG7er1p22_dR_0p8": ret = "L1_DoubleEG7_er1p2_dR_Max0p8"
  elif seed == "L1_DoubleEG7p5er1p22_dR_0p7": ret = "L1_DoubleEG7p5_er1p2_dR_Max0p7"
  elif seed == "L1_DoubleEG8er1p22_dR_0p7": ret = "L1_DoubleEG8_er1p2_dR_Max0p7"
  elif seed == "L1_DoubleEG8p5er1p22_dR_0p7": ret = "L1_DoubleEG8p5_er1p2_dR_Max0p7"
  elif seed == "L1_DoubleEG9er1p22_dR_0p7": ret = "L1_DoubleEG9_er1p2_dR_Max0p7"
  elif seed == "L1_DoubleEG9p5er1p22_dR_0p6": ret = "L1_DoubleEG9p5_er1p2_dR_Max0p6"
  elif seed == "L1_DoubleEG10er1p22_dR_0p6": ret = "L1_DoubleEG10_er1p2_dR_Max0p6"
  elif seed == "L1_DoubleEG10p5er1p22_dR_0p6": ret = "L1_DoubleEG10p5_er1p2_dR_Max0p6"
  elif seed == "L1_DoubleMu0_upt6ip123_upt4": ret = "L1_DoubleMu0_upt6_IP_Min1_upt4"
  elif seed == "L1_DoubleMu18er2p1": ret = "L1_DoubleMu18er2p1_SQ"
  return ret

def getL1TSeedLogicExpr(process, pathName):
  ret = None
  path = getattr(process, pathName)
  for moduleName in path.moduleNames():
    module = getattr(process, moduleName)
    if hasattr(module, 'L1SeedsLogicalExpression'):
      if ret != None:
        raise RuntimeError(pathName)
      ret = module.L1SeedsLogicalExpression.value()
  if ret == None:
    raise RuntimeError(pathName)
  ret = sorted([updateL1TSeedName(foo.replace(' ', '')) for foo in ret.split('OR')])
  return ret

l1tSeedDict1 = {}
l1tSeedDict2 = {}
for pathName in [
  'HLT_DoubleMu4_3_Bs_v15',
  'HLT_DoubleMu4_3_Jpsi_v15',
  'HLT_DoubleMu4_3_LowMass_v1',
  'HLT_DoubleMu4_LowMass_Displaced_v1',
  'HLT_Mu4_L1DoubleMu_v1',
  'HLT_Mu0_L1DoubleMu_v1',
]:
  l1tSeedDict1[pathName] = getL1TSeedLogicExpr(process1, pathName)
  l1tSeedDict2[pathName] = getL1TSeedLogicExpr(process2, pathName)

  if l1tSeedDict1[pathName] != l1tSeedDict2[pathName]:
    print(pathName)
