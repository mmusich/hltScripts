import FWCore.ParameterSet.Config as cms

import argparse
import sys
import math
import glob

parser = argparse.ArgumentParser(prog=sys.argv[0], description='Test of the L1-uGT emulator')
parser.add_argument('-n', '--maxEvents', type=int, help='Value of process.maxEvents.input', default=-1)
parser.add_argument('-f', '--fileNames', nargs='+', help='List of EDM input files (to be used in process.source.fileNames)', default=[])
parser.add_argument('-t', '--threads', type=int, help='Value of process.options.numberOfThreads', default=1)
parser.add_argument('-s', '--streams', type=int, help='Value of process.options.numberOfStreams', default=0)
parser.add_argument('-l', '--rawDataLabel', type=str, help='Label for the FEDRawDataCollection input product', default='rawDataCollector')
parser.add_argument('-d', '--dumpTriggerResults', action = 'store_true', default = False, help = 'Value of (L1TGlobalSummary).dumpTriggerResults (trigger results per event)')
group = parser.add_mutually_exclusive_group()
group.add_argument('--mc', dest = 'useMC', action = 'store_true', default = False, help = 'Use MC as input')
group.add_argument('--data', dest = 'useMC', action = 'store_false', default = False, help = 'Use real data as input')
args = parser.parse_args()

process = cms.Process('TEST')

process.options.numberOfThreads = args.threads
process.options.numberOfStreams = args.streams
process.options.wantSummary = False

process.maxEvents.input = args.maxEvents

# MessageLogger
process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1 #int(math.pow(10, max(0, int(math.log10(args.maxEvents)) - 2)) if args.maxEvents > 0 else 100)
process.MessageLogger.L1TGlobalSummary = cms.untracked.PSet()

# Global Tag
from Configuration.AlCa.GlobalTag import GlobalTag
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag = GlobalTag(process.GlobalTag, '150X_dataRun3_HLT_v1')

# Input source
process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        [f'file:{file_i}' for file_i in sorted(list(set(glob.glob('/eos/cms/store/data/Run2025F/HLTPhysics/RAW/*/*/397/638/*/*.root'))))]
    )
)

process.GlobalParametersRcdSource = cms.ESSource('EmptyESSource',
    recordName = cms.string('L1TGlobalParametersRcd'),
    iovIsRunNotTime = cms.bool(True),
    firstValid = cms.vuint32(1)
)

process.GlobalParameters = cms.ESProducer('StableParametersTrivialProducer',
    NumberPhysTriggers = cms.uint32(512),
    NumberL1Muon = cms.uint32(8),
    NumberL1EGamma = cms.uint32(12),
    NumberL1Jet = cms.uint32(12),
    NumberL1Tau = cms.uint32(12),
    NumberChips = cms.uint32(1),
    PinsOnChip = cms.uint32(512),
    OrderOfChip = cms.vint32(1)
)

process.gtStage2Digis = cms.EDProducer('L1TRawToDigi',
    FedIds = cms.vint32(1404),
    Setup = cms.string('stage2::GTSetup'),
    FWId = cms.uint32(0),
    DmxFWId = cms.uint32(0),
    FWOverride = cms.bool(False),
    TMTCheck = cms.bool(True),
    CTP7 = cms.untracked.bool(False),
    MTF7 = cms.untracked.bool(False),
    InputLabel = cms.InputTag(args.rawDataLabel),
    lenSlinkHeader = cms.untracked.int32(8),
    lenSlinkTrailer = cms.untracked.int32(8),
    lenAMCHeader = cms.untracked.int32(8),
    lenAMCTrailer = cms.untracked.int32(0),
    lenAMC13Header = cms.untracked.int32(8),
    lenAMC13Trailer = cms.untracked.int32(8),
    debug = cms.untracked.bool(False),
    MinFeds = cms.uint32(0)
)

process.gtStage2Digis2 = cms.EDProducer('L1TGlobalProducer',
    MuonInputTag = cms.InputTag('gtStage2Digis:Muon'),
    MuonShowerInputTag = cms.InputTag('gtStage2Digis:MuonShower'),
    EGammaInputTag = cms.InputTag('gtStage2Digis:EGamma'),
    TauInputTag = cms.InputTag('gtStage2Digis:Tau'),
    JetInputTag = cms.InputTag('gtStage2Digis:Jet'),
    EtSumInputTag = cms.InputTag('gtStage2Digis:EtSum'),
    EtSumZdcInputTag = cms.InputTag('gtStage2Digis:EtSumZDC'),
    CICADAInputTag = cms.InputTag('gtStage2Digis:CICADAScore'),
    ExtInputTag = cms.InputTag('gtStage2Digis'),
    AlgoBlkInputTag = cms.InputTag('gtStage2Digis'),
    GetPrescaleColumnFromData = cms.bool(False),
    AlgorithmTriggersUnprescaled = cms.bool(True),
    RequireMenuToMatchAlgoBlkInput = cms.bool(True),
    AlgorithmTriggersUnmasked = cms.bool(True),
    useMuonShowers = cms.bool(True),
    produceAXOL1TLScore = cms.bool(False),
    resetPSCountersEachLumiSec = cms.bool(False),
    semiRandomInitialPSCounters = cms.bool(False),
    ProduceL1GtDaqRecord = cms.bool(True),
    ProduceL1GtObjectMapRecord = cms.bool(True),
    EmulateBxInEvent = cms.int32(1),
    L1DataBxInEvent = cms.int32(5),
    AlternativeNrBxBoardDaq = cms.uint32(0),
    BstLengthBytes = cms.int32(-1),
    PrescaleSet = cms.uint32(1),
    Verbosity = cms.untracked.int32(0),
    PrintL1Menu = cms.untracked.bool(False),
    TriggerMenuLuminosity = cms.string('startup')
)

process.l1tGlobalSummary1 = cms.EDAnalyzer('L1TGlobalSummary',
    AlgInputTag = cms.InputTag('gtStage2Digis'),
    ExtInputTag = cms.InputTag('gtStage2Digis'),
    MinBx = cms.int32(0),
    MaxBx = cms.int32(0),
    DumpTrigResults = cms.bool(args.dumpTriggerResults),
    DumpRecord = cms.bool(False),
    DumpTrigSummary = cms.bool(True),
    ReadPrescalesFromFile = cms.bool(False),
    psFileName = cms.string('prescale_L1TGlobal.csv'),
    psColumn = cms.int32(0)
)

process.l1tGlobalSummary2 = process.l1tGlobalSummary1.clone(
    AlgInputTag = 'gtStage2Digis2',
    ExtInputTag = 'gtStage2Digis2'
)

# Path definition
process.Path = cms.Path(
    process.gtStage2Digis
  + process.gtStage2Digis2
  + process.l1tGlobalSummary1
  + process.l1tGlobalSummary2
)

if args.useMC:
    process.GlobalTag.globaltag = '140X_mcRun3_2024_realistic_v26'

    process.source.fileNames = [
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/7a90945a-ce3d-4060-927c-a36d5b50eaad.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/894cf03a-3842-4e0b-a428-a9c8c5e92009.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/f2deb12b-eda6-4e72-89fc-3d54a1d42d63.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/64fff95b-ed12-4787-924f-5556325711be.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/f1d182c4-a1cf-439c-b767-5d642e308770.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/d5df5792-4f27-41fa-8462-67b161968965.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/b1b2291d-379c-4bfa-94e0-0551c12f73b0.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/d4742769-bd5d-42d6-a640-bd36c5c98177.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/00b885d1-1749-4688-9e94-ae9ace024eb5.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/9db35cea-80f9-4706-ace4-d795e628c16e.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/f2519a6b-67f4-41bd-b838-026a367a1535.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/ce9bdc65-369d-4dc9-aa53-ea1dd1ea89e3.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/a3727a49-0242-4d63-84a5-3170f150cf52.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/4aae6e8c-a3c5-4945-903c-a82a2ba8d39a.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/d118521d-df84-4c5e-b578-6a09da9d816e.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/57d82dfe-c932-4770-a801-c230ed5ca3d4.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/c6fced16-0419-4c86-8059-7e092dd0308a.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/57f3b18f-9623-4ae3-8005-a67de238538a.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/b808e6c7-3e23-4b40-bb2f-75852d5ec4f5.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/121d1b31-75e2-493a-bbad-adf36b9ba539.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/b032030a-6200-4ec5-a06a-ce5c6ba23db1.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/5d61b834-3101-445d-8045-80a1695d5c5a.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/6a514b05-2921-49e0-8569-b1a1abb7fe0e.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/8c44469e-182c-441c-ba2d-763e20cb5eb1.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/0ae4fe11-0c78-42d3-93d9-39cff350c9ae.root',
        '/store/mc/RunIII2024Summer24MiniAOD/VBFH-Hto2G_Par-M-1000-W-5p6_TuneCP5_13p6TeV_powheg-pythia8/MINIAODSIM/140X_mcRun3_2024_realistic_v26-v2/2530000/ca1fd686-3af8-4822-b179-9afb1dfd2ec3.root',
    ]

process.gtStage2Digis2.MuonInputTag = 'gmtStage2Digis:Muon'
process.gtStage2Digis2.MuonShowerInputTag = ''
process.gtStage2Digis2.EGammaInputTag = 'caloStage2Digis:EGamma'
process.gtStage2Digis2.TauInputTag = 'caloStage2Digis:Tau'
process.gtStage2Digis2.JetInputTag = 'caloStage2Digis:Jet'
process.gtStage2Digis2.EtSumInputTag = 'caloStage2Digis:EtSum'
process.gtStage2Digis2.EtSumZdcInputTag = ''
process.gtStage2Digis2.CICADAInputTag = ''

process.Path.remove(process.gtStage2Digis)

if args.fileNames:
    process.source.fileNames = args.fileNames
