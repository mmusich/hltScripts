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
    nReps = 100

    maxNumRuns = -1
    numEventsPerJob = -1

    numThreadsPerJobs = 32
    numStreamsPerJobs = 24

    hltMenu = 'run:383669'

    # List of run numbers
    runs = [
#        380399,
#        380624,
#        381067,
#        381190,
#        381286,
#        381443,
#        381479,
#        381417,
#        381543,
#        381544,
        383669,
    ]

    hltLabel = 'hlt'
    eosDirs = [f'/eos/cms/store/group/tsg/FOG/error_stream_root/run{runNum}' for runNum in runs]
    globalTag = '140X_dataRun3_HLT_v3'

    hltGetCmd = f"""
https_proxy=http://cmsproxy.cms:3128/ \
hltGetConfiguration {hltMenu} \
  --globaltag {globalTag} \
  --data \
  --no-prescale \
  --no-output \
  --max-events {numEventsPerJob} \
  > {hltLabel}.py && \
cat <<@EOF >> {hltLabel}.py
process.options.numberOfThreads = {numThreadsPerJobs}
process.options.numberOfStreams = {numStreamsPerJobs}
process.options.wantSummary = False

for foo in ['HLTAnalyzerEndpath', 'dqmOutput', 'MessageLogger']:
    if hasattr(process, foo):
        process.__delattr__(foo)

process.load('FWCore.MessageLogger.MessageLogger_cfi')

#process.options.accelerators = ['cpu']
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
    inputFiles = sorted(list(set([foo for foo in inputFiles if foo.endswith('.root')])))
    inputFilesStr = ','.join(inputFiles)

    nRuns = multiprocessing.cpu_count() // numThreadsPerJobs

    print(f'Downloading HLT menu ({hltMenu}) from ConfDB ...')
    execmd(hltGetCmd)

    print(f'Creating python configurations for {nRuns} parallel jobs ', end='')
    print(f'({numThreadsPerJobs} threads and {numStreamsPerJobs} streams per job) ...')

    for rep_i in range(nReps):
      repLabel = f'rep{rep_i:03d}'
      print(f'{repLabel} ...')

      jobCmds = []
      hltLogs = []
      for run_i in range(nRuns):
        runLabel = f'run{run_i:03d}'
        hltLogs += [f'{hltLabel}_{repLabel}_{runLabel}.log']
        jobCmds += [f'cmsRun {hltLabel}.py inputFiles={inputFilesStr} &> {hltLogs[-1]}']

      pool = multiprocessing.Pool(processes=nRuns)
      pool.map(execmd, jobCmds)

      for hltLog in hltLogs:
          execmd(f'grep -inrl fatal {hltLog}')
