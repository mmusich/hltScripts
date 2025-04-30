#!/usr/bin/env python3
import os
import sys
import multiprocessing

def execmd(cmd):
    return os.system(cmd)

if __name__ == '__main__':

    ###
    ### parameters
    ###
    minRunNumber = 0
    maxRunNumber = 50
    numEventsPerJob = -1

    numThreadsPerJobs = 32
    numStreamsPerJobs = 24

    eosDirs = [f'/eos/cms/store/data/Run2024I/EphemeralHLTPhysics{foo}/RAW/v1/000/386/593/00000' for foo in range(7)]

    hltMenu1 = '/users/missirol/test/dev/CMSSW_15_0_0/CMSHLT_3529/Test01/GRun/V4'
    hltMenu2 = '/users/missirol/test/dev/CMSSW_15_0_0/CMSHLT_3529/Test01/GRun/V6'

    hltLabel1 = sys.argv[1]+'_baseline'
    hltLabel2 = sys.argv[1]+'_target'

    def hltGetCmd(hltMenu, hltLabel):
        return f"""
https_proxy=http://cmsproxy.cms:3128/ \
hltGetConfiguration {hltMenu} \
  --process HLTX \
  --globaltag 150X_dataRun3_HLT_forTriggerStudies_v5 \
  --data \
  --prescale "2p0E34" \
  --output minimal \
  --max-events {numEventsPerJob} \
  > {hltLabel}.py && \
cat <<@EOF >> {hltLabel}.py
process.options.numberOfThreads = {numThreadsPerJobs}
process.options.numberOfStreams = {numStreamsPerJobs}
process.options.wantSummary = False

for foo in ['HLTAnalyzerEndpath', 'dqmOutput']: #, 'MessageLogger']:
    if hasattr(process, foo):
        process.__delattr__(foo)

#process.load('FWCore.MessageLogger.MessageLogger_cfi')

process.hltOutputMinimal.outputCommands = [
    'drop *',
    'keep edmTriggerResults_*_*_HLTX',
]

process.options.accelerators = ['cpu']
@EOF
"""

    hltGetCmd1 = hltGetCmd(hltMenu1, hltLabel1)
    hltGetCmd2 = hltGetCmd(hltMenu2, hltLabel2)

    customizeHLTfor2024L1TMenu = """
def customizeHLTfor2024L1TMenu(process):
    seed_replacements = {

        'L1_SingleMu5_BMTF' : 'L1_AlwaysTrue',
        'L1_SingleMu13_SQ14_BMTF': 'L1_AlwaysTrue',

        'L1_AXO_Medium' : 'L1_AXO_Nominal',
        'L1_AXO_VVTight': 'L1_AlwaysTrue',
        'L1_AXO_VVVTight': 'L1_AlwaysTrue',

        'L1_CICADA_VVTight': 'L1_AlwaysTrue',
        'L1_CICADA_VVVTight': 'L1_AlwaysTrue',
        'L1_CICADA_VVVVTight': 'L1_AlwaysTrue',

        'L1_DoubleTau_Iso34_Iso26_er2p1_Jet55_RmOvlp_dR0p5': 'L1_DoubleIsoTau26er2p1_Jet55_RmOvlp_dR0p5 OR L1_DoubleIsoTau26er2p1_Jet70_RmOvlp_dR0p5',
        'L1_DoubleTau_Iso38_Iso26_er2p1_Jet55_RmOvlp_dR0p5': 'L1_DoubleIsoTau26er2p1_Jet55_RmOvlp_dR0p5 OR L1_DoubleIsoTau26er2p1_Jet70_RmOvlp_dR0p5',
        'L1_DoubleTau_Iso40_Iso26_er2p1_Jet55_RmOvlp_dR0p5': 'L1_DoubleIsoTau26er2p1_Jet55_RmOvlp_dR0p5 OR L1_DoubleIsoTau26er2p1_Jet70_RmOvlp_dR0p5',

        'L1_DoubleEG15_11_er1p2_dR_Max0p6': 'L1_DoubleEG11_er1p2_dR_Max0p6',
        'L1_DoubleEG16_11_er1p2_dR_Max0p6': 'L1_DoubleEG11_er1p2_dR_Max0p6',
        'L1_DoubleEG17_11_er1p2_dR_Max0p6': 'L1_DoubleEG11_er1p2_dR_Max0p6',

        'L1_DoubleEG15_er1p5_dEta_Max1p5': 'L1_AlwaysTrue',
        'L1_DoubleEG16_er1p5_dEta_Max1p5': 'L1_AlwaysTrue',
        'L1_DoubleEG17_er1p5_dEta_Max1p5': 'L1_AlwaysTrue',

        'L1_DoubleJet_110_35_DoubleJet35_Mass_Min1000': 'L1_AlwaysTrue',
        'L1_DoubleJet_110_35_DoubleJet35_Mass_Min1100': 'L1_AlwaysTrue',
        'L1_DoubleJet_110_35_DoubleJet35_Mass_Min1200': 'L1_AlwaysTrue',
        'L1_DoubleJet45_Mass_Min700_IsoTau45er2p1_RmOvlp_dR0p5': 'L1_AlwaysTrue',
        'L1_DoubleJet45_Mass_Min800_IsoTau45er2p1_RmOvlp_dR0p5': 'L1_AlwaysTrue',
        'L1_DoubleJet_65_35_DoubleJet35_Mass_Min750_DoubleJetCentral50': 'L1_AlwaysTrue',
        'L1_DoubleJet_65_35_DoubleJet35_Mass_Min850_DoubleJetCentral50': 'L1_AlwaysTrue',
        'L1_DoubleJet_65_35_DoubleJet35_Mass_Min950_DoubleJetCentral50': 'L1_AlwaysTrue',
        'L1_DoubleJet45_Mass_Min700_LooseIsoEG20er2p1_RmOvlp_dR0p2': 'L1_AlwaysTrue',
        'L1_DoubleJet45_Mass_Min800_LooseIsoEG20er2p1_RmOvlp_dR0p2': 'L1_AlwaysTrue',
        'L1_DoubleJet_85_35_DoubleJet35_Mass_Min700_Mu3OQ': 'L1_AlwaysTrue',
        'L1_DoubleJet_85_35_DoubleJet35_Mass_Min800_Mu3OQ': 'L1_AlwaysTrue',
        'L1_DoubleJet_85_35_DoubleJet35_Mass_Min900_Mu3OQ': 'L1_AlwaysTrue',
        'L1_DoubleJet_70_35_DoubleJet35_Mass_Min600_ETMHF65': 'L1_AlwaysTrue',
        'L1_DoubleJet_70_35_DoubleJet35_Mass_Min700_ETMHF65': 'L1_AlwaysTrue',
        'L1_DoubleJet_70_35_DoubleJet35_Mass_Min800_ETMHF65': 'L1_AlwaysTrue',
    }

    for module in filters_by_type(process, 'HLTL1TSeed'):
        l1Seed = module.L1SeedsLogicalExpression.value()
        if any(old_seed in l1Seed for old_seed in seed_replacements):
            for old_seed, new_seed in seed_replacements.items():
                l1Seed = l1Seed.replace(old_seed, new_seed)
            module.L1SeedsLogicalExpression = cms.string(l1Seed)

    return process
"""

    customizeHLTfor2025JECs = """
def customizeHLTfor2025JECs(process):
    jecTagsDict = {
        'AK4CaloHLT': 'JetCorrectorParametersCollection_Run3Winter25Digi_AK4CaloHLT_v2',
        'AK8CaloHLT': 'JetCorrectorParametersCollection_Run3Winter25Digi_AK8CaloHLT_v2',
        'AK4PFHLT': 'JetCorrectorParametersCollection_Run3Winter25Digi_AK4PFHLT_v2',
        'AK8PFHLT': 'JetCorrectorParametersCollection_Run3Winter25Digi_AK8PFHLT_v2',
    }

    try:
        for (labelName, tagName) in jecTagsDict.items():
            process.GlobalTag.toGet += [
                cms.PSet(
                    record = cms.string("JetCorrectionsRecord"),
                    label = cms.untracked.string(labelName),
                    tag = cms.string(tagName),
                ),
            ]
    except:
        raise RuntimeError("customizeHLTfor2025JECs -- GlobalTag ESSource could not be customized !")

    return process
"""

    config_customisation = f"""
from HLTrigger.Configuration.common import *

process.GlobalTag.globaltag = '150X_dataRun3_HLT_forTriggerStudies_v5'

{customizeHLTfor2024L1TMenu}

process = customizeHLTfor2024L1TMenu(process)

{customizeHLTfor2025JECs}

process = customizeHLTfor2025JECs(process)

for prod in producers_by_type(process, 'CaloTowersCreator'):
    prod.EcalRecHitThresh = True
"""

    config_baseline = f"from {hltLabel1} import cms, process"
    config_baseline += config_customisation

    config_target = f"from {hltLabel2} import cms, process"
    config_target += config_customisation

    hltCfgTypes = {
        f'{hltLabel1}_JECs2025v2': config_baseline,
        f'{hltLabel2}_JECs2025v2': config_target,
    }

    print(f'Creating list of EDM input files on EOS ...')
    inputFileBlocks = []
    inputFiles = []
    for eosDir in eosDirs:
        execmd(f'eos ls {eosDir} > tmp.txt')
        inputFilesTmp = [fileName for fileName in open('tmp.txt').read().splitlines() if fileName.endswith('.root')]
        inputFiles += [f'root://eoscms.cern.ch/{eosDir}/{fileName}' for fileName in inputFilesTmp]
        os.remove('tmp.txt')
    inputFiles = sorted(list(set(inputFiles)))

    count = len(hltCfgTypes.keys())
    nRuns = len(inputFiles)
    print(f'... {nRuns} input files found')

    print(f'Downloading HLT menu ({hltMenu1}) from ConfDB ...')
    execmd(hltGetCmd1)

    print(f'Downloading HLT menu ({hltMenu2}) from ConfDB ...')
    execmd(hltGetCmd2)

    print(f'Creating python configurations for {count} parallel jobs ', end='')
    print(f'({numThreadsPerJobs} threads and {numStreamsPerJobs} streams per job) ...')

    for hltCfgLabel in hltCfgTypes:
        with open(f'{hltCfgLabel}.py', 'w') as hltCfgFile:
            hltCfgFile.write(f'{hltCfgTypes[hltCfgLabel]}\n')

    for run_i in range(nRuns):
        if minRunNumber != None and run_i < minRunNumber:
            continue
        if maxRunNumber != None and run_i > maxRunNumber:
            continue

        runLabel = f'run{run_i:04d}'
        print(f'{runLabel} ...')

        jobCmds = []
        fileName = inputFiles[run_i]

        for hltCfgLabel in hltCfgTypes:
            hltLog = f'{hltCfgLabel}_{runLabel}.log'
            with open(f'{hltCfgLabel}.py', 'a') as hltCfgFile:
                hltCfgFile.write(f'process.hltOutputMinimal.fileName = "{hltCfgLabel}_{runLabel}.root"\n')
            jobCmds += [f'cmsRun {hltCfgLabel}.py inputFiles={fileName} &> {hltLog}']

        pool = multiprocessing.Pool(processes=count)
        pool.map(execmd, jobCmds)
