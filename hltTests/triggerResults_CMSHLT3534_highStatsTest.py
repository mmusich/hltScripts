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
    maxRunNumber = -1
    numEventsPerJob = -1

    numThreadsPerJobs = 32
    numStreamsPerJobs = 24

    eosDirs = [f'/eos/cms/store/data/Run2025D/EphemeralHLTPhysics{idx}/RAW/v1/000/394/959/00000/' for idx in range(8)]

    hltMenu = '/users/missirol/test/dev/CMSSW_15_0_0/CMSHLT_3534/Test41/GRun/V3'

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

for foo in ['HLTAnalyzerEndpath', 'dqmOutput']:
    if hasattr(process, foo):
        process.__delattr__(foo)

process.hltOutputMinimal.outputCommands = [
    'drop *',
    'keep edmTriggerResults_*_*_HLTX',
]
@EOF
"""

    hltGetCmd = hltGetCmd(hltMenu, hltLabel)

    print(f'Creating list of EDM input files on EOS ...')
    inputFileBlocks = []
    inputFiles = []
    for eosDir in eosDirs:
        execmd(f'eos ls {eosDir} > tmp.txt')
        inputFilesTmp = [fileName for fileName in open('tmp.txt').read().splitlines() if fileName.endswith('.root')]
        inputFiles += [f'root://eoscms.cern.ch/{eosDir}/{fileName}' for fileName in inputFilesTmp]
        os.remove('tmp.txt')
    inputFiles = sorted(list(set(inputFiles)))

    count = multiprocessing.cpu_count() // numThreadsPerJobs
    nRuns = len(inputFiles)
    print(f'... {nRuns} input files found')

    print(f'Downloading HLT menu ({hltMenu}) from ConfDB ...')
    execmd(hltGetCmd)

    print(f'Creating python configurations for {count} parallel jobs ', end='')
    print(f'({numThreadsPerJobs} threads and {numStreamsPerJobs} streams per job) ...')

    inputFileBlocks = []
    for run_i in range(nRuns):
        if minRunNumber > 0 and run_i < minRunNumber:
            continue
        if maxRunNumber > 0 and run_i > maxRunNumber:
            continue

        if len(inputFileBlocks) == 0 or len(inputFileBlocks[-1]) == count:
            inputFileBlocks += [[]]

        inputFileBlocks[-1] += [run_i]

    for inputFileBlock in inputFileBlocks:

        jobCmds = []
        hltLogs = []

        for run_i in inputFileBlock:

            runLabel = f'run{run_i:05d}'
            print(f'{runLabel} ...')

            fileName = inputFiles[run_i]

            jobLabel = f'{hltLabel}_{runLabel}'        

            hltLogs += [f'{jobLabel}.log']

            with open(f'{jobLabel}.py', 'w') as hltCfgFile:
                hltCfgFile.write(f'from {hltLabel} import cms, process\n')
                hltCfgFile.write(f'process.source.fileNames = ["{fileName}"]\n')
                hltCfgFile.write(f'process.hltOutputMinimal.fileName = "{jobLabel}.root"\n')

            jobCmds += [f'cmsRun {jobLabel}.py &> {hltLogs[-1]}']

        pool = multiprocessing.Pool(processes=len(jobCmds))
        pool.map(execmd, jobCmds)

        for hltLog in hltLogs:
            execmd(f'grep -inrl fatal {hltLog}')
