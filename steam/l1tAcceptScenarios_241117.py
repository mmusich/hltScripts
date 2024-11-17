import FWCore.ParameterSet.Config as cms

process = cms.Process('TEST')

process.maxEvents.input = 2125000

process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
process.options.wantSummary = True

process.MessageLogger.cerr.FwkReport.reportEvery = int(max(1, process.maxEvents.input.value() / 10))

process.source = cms.Source('PoolSource',
    lumisToProcess = cms.untracked.VLuminosityBlockRange('386924:108-386924:116'),
    fileNames = cms.untracked.vstring(
        'root://eoscms.cern.ch//eos/cms/store/group/tsg/STEAM/test/241116_L1Accept_run386924/c41f7eb7-cc3e-4b27-b58d-87e297fdf6e0.root',
    ),
)

l1tBit = {
  'L1_SingleMu11_SQ14_BMTF': 24,
  'L1_DoubleIsoTau34er2p1': 270,
  'L1_DoubleIsoTau26er2p1_Jet55_RmOvlp_dR0p5': 283,
  'L1_DoubleIsoTau26er2p1_Jet70_RmOvlp_dR0p5': 284,
  'L1_DoubleEG11_er1p2_dR_Max0p6': 214,
  'L1_DoubleEG_LooseIso20_LooseIso12_er1p5': 227,

  'L1_DoubleJet_110_35_DoubleJet35_Mass_Min800': 357,
  'L1_DoubleJet_65_35_DoubleJet35_Mass_Min600_DoubleJetCentral50': 364,
  'L1_DoubleJet_70_35_DoubleJet35_Mass_Min500_ETMHF65': 370,
  'L1_DoubleJet45_Mass_Min550_LooseIsoEG20er2p1_RmOvlp_dR0p2': 366,
  'L1_DoubleJet_85_35_DoubleJet35_Mass_Min600_Mu3OQ': 368,
  'L1_DoubleJet45_Mass_Min550_IsoTau45er2p1_RmOvlp_dR0p5': 362,
  'L1_QuadJet_95_75_65_20_DoubleJet_75_65_er2p5_Jet20_FWD3p0': 386,

  'L1_SingleMuShower_Nominal': 111,

  'L1_ETMHF90': 420,
  'L1_ETMHF90_HTT60er': 429,
  'L1_ETMHF90_SingleJet60er2p5_dPhi_Min2p1': 336,
  'L1_ETMHF90_SingleJet60er2p5_dPhi_Min2p6': 337,

  'L1_SingleIsoEG30er2p5': 192,
  'L1_SingleEG36er2p5': 168,
}

scenarios = [
  ('0', {
  }),
  ('1p0', {
    'L1_SingleMu11_SQ14_BMTF': 1.5,
  }),
  ('1p1', {
    'L1_DoubleIsoTau26er2p1_Jet55_RmOvlp_dR0p5': 0,
  }),
  ('1p2', {
    'L1_DoubleEG11_er1p2_dR_Max0p6': 0,
  }),
  ('1p3', {
    'L1_DoubleEG_LooseIso20_LooseIso12_er1p5': 0,
  }),
  ('2p0', {
    'L1_SingleMu11_SQ14_BMTF': 0,
  }),
  ('2p1', {
    'L1_DoubleIsoTau34er2p1': 0,
  }),
  ('3p0', {
    'L1_SingleMuShower_Nominal': 0,
  }),
  ('3p1', {
    'L1_DoubleJet_110_35_DoubleJet35_Mass_Min800': 0,
    'L1_DoubleJet_85_35_DoubleJet35_Mass_Min600_Mu3OQ': 0,
    'L1_DoubleJet_70_35_DoubleJet35_Mass_Min500_ETMHF65': 0,
    'L1_DoubleJet_65_35_DoubleJet35_Mass_Min600_DoubleJetCentral50': 0,
    'L1_DoubleJet45_Mass_Min550_LooseIsoEG20er2p1_RmOvlp_dR0p2': 0,
    'L1_DoubleJet45_Mass_Min550_IsoTau45er2p1_RmOvlp_dR0p5': 0,
  }),
  ('3p2', {
    'L1_QuadJet_95_75_65_20_DoubleJet_75_65_er2p5_Jet20_FWD3p0': 0,
  }),
  ('3p3', {
    'L1_ETMHF90': 0,
    'L1_ETMHF90_HTT60er': 0,
    'L1_ETMHF90_SingleJet60er2p5_dPhi_Min2p1': 0,
    'L1_ETMHF90_SingleJet60er2p5_dPhi_Min2p6': 0,
  }),
  ('3p4', {
    'L1_SingleIsoEG30er2p5': 0,
  }),
  ('3p5', {
    'L1_SingleEG36er2p5': 0,
  }),
]

process.dstPhysicsTrigger = cms.EDFilter('TriggerResultsFilter',
    usePathStatus = cms.bool( False ),
    hltResults = cms.InputTag( 'TriggerResults::HLT' ),
    l1tResults = cms.InputTag( '' ),
    l1tIgnoreMaskAndPrescale = cms.bool( False ),
    throw = cms.bool( True ),
    triggerConditions = cms.vstring( 'DST_Physics_v*' )
)

from EventFilter.L1TRawToDigi.l1tRawToDigi_cfi import l1tRawToDigi as _l1tRawToDigi
process.l1tGTStage2Digis = _l1tRawToDigi.clone(
    InputLabel = 'hltFEDSelectorL1',
    Setup = 'stage2::GTSetup',
    FedIds = [ 1404 ],
)

from L1Trigger.L1TGlobal.l1tGlobalPrescaler_cfi import l1tGlobalPrescaler as _l1tGlobalPrescaler
process.l1tPrescaler = _l1tGlobalPrescaler.clone(
    l1tResults = 'l1tGTStage2Digis',
)

process.path_dstPhysicsTrigger = cms.Path(
    process.dstPhysicsTrigger
)

for scenario_idx,scenario in enumerate(scenarios):
    prescale_mod_label = f'l1tPrescalerScenario{scenario[0]}'
    setattr(process, prescale_mod_label, process.l1tPrescaler.clone())
    prescaler_mod = getattr(process, prescale_mod_label)
    for scenario_idx2 in range(scenario_idx+1):
        for l1tSeed,l1tPrescale in scenarios[scenario_idx2][1].items():
            prescaler_mod.l1tPrescales[l1tBit[l1tSeed]] = l1tPrescale
    setattr(process, f'path_Scenario{scenario[0]}', cms.Path(
        process.dstPhysicsTrigger
      + process.l1tGTStage2Digis
      + prescaler_mod
    ))
