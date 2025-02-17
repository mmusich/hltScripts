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
    maxRunNumber = 24
    numEventsPerJob = -1

    numThreadsPerJobs = 32
    numStreamsPerJobs = 24

    eosDirs = [f'/eos/cms/store/data/Run2024I/EphemeralHLTPhysics{foo}/RAW/v1/000/386/593/00000' for foo in range(8)]

    hltLabel = sys.argv[1]

    hltMenu = '/dev/CMSSW_14_2_0/GRun/V11'

    hltGetCmd = f"""
https_proxy=http://cmsproxy.cms:3128/ \
hltGetConfiguration {hltMenu} \
  --process HLTX \
  --globaltag 141X_dataRun3_HLT_v2 \
  --data \
  --no-prescale \
  --output minimal \
  --max-events {numEventsPerJob} \
  > {hltLabel}.py && \
cat <<@EOF >> {hltLabel}.py
process.options.numberOfThreads = {numThreadsPerJobs}
process.options.numberOfStreams = {numStreamsPerJobs}
#process.options.wantSummary = False

for foo in ['HLTAnalyzerEndpath', 'dqmOutput', 'MessageLogger']:
    if hasattr(process, foo):
        process.__delattr__(foo)

process.load('FWCore.MessageLogger.MessageLogger_cfi')

process.hltOutputMinimal.outputCommands = [
    'drop *',
    'keep edmTriggerResults_*_*_HLTX',
]
@EOF
"""

    hltCfgTypes = {
        f'{hltLabel}_AlpakaSerialSync': f"""from {hltLabel} import cms, process
process.options.accelerators = ['cpu']
""",
        f'{hltLabel}_AlpakaGPU': f"""from {hltLabel} import cms, process
process.options.accelerators = ['*']
""",
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

    count = 2
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
