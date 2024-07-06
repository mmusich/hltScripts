#!/usr/bin/env python3
import os
import math
import multiprocessing

def execmd(cmd):
    return os.system(cmd)

if __name__ == '__main__':

    ###
    ### parameters
    ###
    maxNumRuns = -1
    numEventsPerJob = -1

    numThreadsPerJobs = 32
    numStreamsPerJobs = 24

    eosDirs = [f'/eos/cms/store/data/Run2024F/EphemeralHLTPhysics{foo}/RAW/v1/000/382/250/00000' for foo in range(7)]

    hltMenu = '/dev/CMSSW_14_0_0/GRun/V153'

    hltGetCmd = f"""
https_proxy=http://cmsproxy.cms:3128/ \
hltGetConfiguration {hltMenu} \
  --globaltag 140X_dataRun3_HLT_v3 \
  --data \
  --no-prescale \
  --no-output \
  --max-events {numEventsPerJob} \
  --customise HLTrigger/Configuration/customizeHLTforAlpaka.customizeHLTforAlpaka \
  > hlt.py && \
cat <<@EOF >> hlt.py
process.options.numberOfThreads = {numThreadsPerJobs}
process.options.numberOfStreams = {numStreamsPerJobs}
process.options.wantSummary = False

for foo in ['HLTAnalyzerEndpath', 'dqmOutput', 'MessageLogger']:
    if hasattr(process, foo):
        process.__delattr__(foo)

process.load('FWCore.MessageLogger.MessageLogger_cfi')
@EOF
"""

    print(f'Creating list of EDM input files on EOS ...')
    inputFileBlocks = []
    inputFiles = []
    for eosDir in eosDirs:
        execmd(f'eos ls {eosDir} > tmp.txt')
        inputFilesTmp = [fileName for fileName in open('tmp.txt').read().splitlines() if fileName.endswith('.root')]
        inputFiles += [f'root://eoscms.cern.ch/{eosDir}/{fileName}' for fileName in inputFilesTmp]
        os.remove('tmp.txt')
    inputFiles = sorted(list(set(inputFiles)))

    count = multiprocessing.cpu_count() * 2 // numThreadsPerJobs
    nRuns = math.ceil(len(inputFiles) / count)

    for run_i in range(nRuns):
        inputFileBlocks.append(inputFiles[count*run_i:count*(run_i+1)])

    print(f'Downloading HLT menu ({hltMenu}) from ConfDB ...')
    execmd(hltGetCmd)

    print(f'Creating python configurations for {count} parallel jobs ', end='')
    print(f'({numThreadsPerJobs} threads and {numStreamsPerJobs} streams per job) ...')

    for run_i in range(nRuns):
        if maxNumRuns >= 0 and run_i >= maxNumRuns:
            continue

        runLabel = f'run{run_i:03d}'
        print(f'{runLabel} ...')

        jobCmds = []
        for job_i,fileName in enumerate(inputFileBlocks[run_i]):
            hltLog = f'hlt_{runLabel}_job{job_i}.log'
            jobCmds += [f'cmsRun hlt.py inputFiles={fileName} &> {hltLog}']

        pool = multiprocessing.Pool(processes=count)
        pool.map(execmd, jobCmds)
