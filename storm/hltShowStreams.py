#!/usr/bin/env python3
import FWCore.ParameterSet.Config as cms

import HLTrigger.Configuration.Tools.options as _options
import HLTrigger.Configuration.Tools.confdb as _confdb

import sys

def _build_options(**args):
    options = _options.HLTProcessOptions()
    for key, val in args.items():
        setattr(options, key, val)
    return options

def getHltConfiguration(menu, **args):
    args['menu'] = menu
    args['fragment'] = False
    options = _build_options(**args)

    try:
        foo = {'process': None}
        exec(_confdb.HLTProcess(options).dump(), globals(), foo)
        process = foo['process']
    except:
        raise Exception(f'query to ConfDB failed (output is not a valid python file)\n  args={args}')

    if not isinstance(process, cms.Process):
        raise Exception(f'query to ConfDB did not return a valid HLT menu (cms.Process not found)\n  args={args}')

    return process

process = getHltConfiguration('/dev/CMSSW_13_2_0/HIon')

for streamName in process.streams.parameterNames_():
    outputModuleName = f'hltOutput{streamName}'
    if not hasattr(process, outputModuleName):
        continue
    outputModule = getattr(process, outputModuleName)
    print(f'\nStream: {streamName}')
    print('  Datasets:')
    for foo in outputModule.SelectEvents.SelectEvents:
        print(f'    {foo[len("Dataset_"):]}')
    print('  EventContent:')
    for foo in outputModule.outputCommands:
        print(f'    {foo}')
