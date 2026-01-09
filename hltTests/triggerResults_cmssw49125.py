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
    maxRunNumber = 99
    numEventsPerJob = -1

    numThreadsPerJobs = 32
    numStreamsPerJobs = 24

    eosDirs = [f'/eos/cms/store/data/Run2025G/EphemeralHLTPhysics0/RAW/v1/000/398/183/00000/']

    hltMenu = 'run:398802'

    hltLabel = sys.argv[1]

    def hltGetCmd(hltMenu, hltLabel):
        return f"""
https_proxy=http://cmsproxy.cms:3128/ \
hltGetConfiguration {hltMenu} \
  --process HLTX \
  --globaltag 150X_dataRun3_HLT_v1 \
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
@EOF
"""

    hltGetCmd = hltGetCmd(hltMenu, hltLabel)

    config_hlt1 = f"from {hltLabel} import cms, process"

    config_hlt2 = f"from {hltLabel} import cms, process"
    config_hlt2 += """
process.hltSiPixelClustersSoA.DoDigiMorphing = False
process.hltSiPixelClustersSoASerialSync.DoDigiMorphing = False
"""

    config_hlt3 = f"from {hltLabel} import cms, process"
    config_hlt3 += """
process.options.accelerators = ['cpu']
"""

    config_hlt4 = f"from {hltLabel} import cms, process"
    config_hlt4 += """
process.hltSiPixelClustersSoA.DoDigiMorphing = False
process.hltSiPixelClustersSoASerialSync.DoDigiMorphing = False

process.options.accelerators = ['cpu']
"""

    hltCfgTypes = {
        f'{hltLabel}_pixDigMorph1_gpu': config_hlt1,
        f'{hltLabel}_pixDigMorph0_gpu': config_hlt2,
        f'{hltLabel}_pixDigMorph1_cpu': config_hlt3,
        f'{hltLabel}_pixDigMorph0_cpu': config_hlt4,
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

    print(f'Downloading HLT menu ({hltMenu}) from ConfDB ...')
    execmd(hltGetCmd)

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
