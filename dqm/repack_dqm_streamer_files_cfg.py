# run as e.g.: 
# cmsRun repack_dqm_streamer_files_cfg.py runInputDir=/eos/user/d/dpapagia/data/ outputBaseDir=. runNumber=392700 scanOnce=True

import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
from DQM.Integration.config.dqmPythonTypes import *

options = VarParsing.VarParsing('analysis')

options.register('runNumber',
                 111,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Run number.")

options.register('datafnPosition',
                 3, # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Data filename position in the positional arguments array 'data' in json file.")

options.register('runInputDir',
                 '/tmp',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Directory where the DQM files will appear.")

options.register('scanOnce',
                 False, # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "Don't repeat file scans: use what was found during the initial scan. EOR file is ignored and the state is set to 'past end of run'.")

options.register('skipFirstLumis',
                 False, # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "Skip (and ignore the minEventsPerLumi parameter) for the files which have been available at the beginning of the processing.")

options.register('noDB',
                 True, # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "Don't upload the BeamSpot conditions to the DB")

options.register('BeamSplashRun',
                 False, # default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "Set client source settings for beam SPLASH run")

# Parameters for runType

options.register('runkey',
                 'pp_run',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Run Keys of CMS")

# Parameter for frontierKey

options.register('runUniqueKey',
                 'InValid',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Unique run key from RCMS for Frontier")

# Parameter for output directory of the event display clients
# visualization-live and visualization-live-secondInstance
# this additional input argument was added in the hltd framework
# only for the visualization clients 
# Note, the other clients do not use this input parameter

options.register('outputBaseDir',
                 '.',
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Directory where the visualization output files will appear.")

options.parseArguments()

process = cms.Process( 'REPACK' )

runType = RunType()
if not options.runkey.strip():
    options.runkey = 'pp_run'

runType.setRunType(options.runkey.strip())

if not options.inputFiles:
    # Input source
    nextLumiTimeoutMillis = 240000
    endOfRunKills = True

    if options.scanOnce:
        endOfRunKills = False
        nextLumiTimeoutMillis = 0

    # stream label
    if runType.getRunType() == runType.hi_run:
        streamLabel = 'streamHIDQM'
    else:
        streamLabel = 'streamDQM'

    process.source = cms.Source("DQMStreamerReader",
                                runNumber = cms.untracked.uint32(options.runNumber),
                                runInputDir = cms.untracked.string(options.runInputDir),
                                SelectEvents = cms.untracked.vstring('*'),
                                streamLabel = cms.untracked.string(streamLabel),
                                scanOnce = cms.untracked.bool(options.scanOnce),
                                datafnPosition = cms.untracked.uint32(options.datafnPosition),
                                minEventsPerLumi = cms.untracked.int32(-1),
                                delayMillis = cms.untracked.uint32(500),
                                nextLumiTimeoutMillis = cms.untracked.int32(nextLumiTimeoutMillis),
                                skipFirstLumis = cms.untracked.bool(options.skipFirstLumis),
                                deleteDatFiles = cms.untracked.bool(False),
                                endOfRunKills  = cms.untracked.bool(endOfRunKills),
                                inputFileTransitionsEachEvent = cms.untracked.bool(False)
                                )

process.output = cms.OutputModule( 'PoolOutputModule',
                                   fileName = cms.untracked.string( 'repacked.root' ),
                                   outputCommands = cms.untracked.vstring( 'keep *' )
                                  )

process.endPath = cms.EndPath( process.output )
