#!/usr/bin/env python3
import os
import sys
import importlib.util
import FWCore.ParameterSet.Config as cms

def getPSetDependencies(module, process):
    ret = []
    for parName in module.parameterNames_():
      param = getattr(module, parName)

      if isinstance(param, cms.VPSet):
        for pset in param:
          ret += getPSetDependencies(pset, process)

      elif isinstance(param, cms.PSet):
        ret += getPSetDependencies(param, process)

      elif parName == 'refToPSet_':
        ret += [param.value()]
        if not hasattr(process, param.value()):
          raise Exception('PSet missing in the cms.Process:', param.value())
        ret += getPSetDependencies(getattr(process, param.value()), process)

    return ret

if __name__ == '__main__':
    verbosity = 0

    if len(sys.argv) < 2:
      raise Exception('one cmd-line arg required: path to python configuration file')
    elif not os.path.isfile(sys.argv[1]):
      raise Exception('invalid path to python configuration file: '+sys.argv[1])

    cfgFilePath = os.path.abspath(sys.argv[1])
    sys.argv = [sys.argv[0]]+sys.argv[2:]

    spec = importlib.util.spec_from_file_location('process', cfgFilePath)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    process = foo.process
    del spec, foo

    psetWhiteList = [
      'HLTConfigVersion',
      'transferSystem',
      'streams',
      'datasets',
      'options',
      'maxEvents',
      'maxLuminosityBlocks',
      'nanoDQMIO_perLSoutput',
    ]

    modulePSetDepDict = {}

    for moduleDict in [
      process.analyzers_(),
      process.es_prefers_(),
      process.es_producers_(),
      process.es_sources_(),
      process.filters_(),
      process.outputModules_(),
      process.producers_(),
      process.switchProducers_(),
    ]:
      for moduleName_i in moduleDict:
        if moduleName_i in modulePSetDepDict:
          raise Exception('attempt to redefine existing dictionary entry (key = "'+moduleName_i+'")')
        modulePSetDepDict[moduleName_i] = getPSetDependencies(getattr(process, moduleName_i), process)

    if verbosity > 0:
      for moduleName_i in sorted(modulePSetDepDict.keys()):
        print(moduleName_i)
        for dep_i in modulePSetDepDict[moduleName_i]:
          print('   '+dep_i)
      print('-'*25)

    requiredPSets = []
    for moduleName_i in sorted(modulePSetDepDict.keys()):
      for dep_i in modulePSetDepDict[moduleName_i]:
        requiredPSets.append(dep_i)
    requiredPSets = sorted(list(set(requiredPSets)))

    for psetName in sorted(process.psets_().keys()):
      if psetName in psetWhiteList:
        continue
      if psetName in requiredPSets:
        continue
      print(psetName)
