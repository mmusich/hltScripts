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
    if len(sys.argv) < 3:
      raise Exception('Two cmd-line args required: (a) name of the PSet, and (b) path to python configuration file, or name of a menu in ConfDB')

    psetName = sys.argv[1]

    if os.path.isfile(sys.argv[2]):
      cfgFilePath = sys.argv[2]
    else:
      cfgFilePath = 'tmp.py'
      os.system(f'hltConfigFromDB --configName {sys.argv[2]} > {cfgFilePath}')

    sys.argv = [sys.argv[0]]+sys.argv[2:]
    spec = importlib.util.spec_from_file_location('process', os.path.abspath(cfgFilePath))
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    process = foo.process
    del spec, foo

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

    print('='*60)
    print(f'{psetName}')
    print('='*60)

    print('-'*20)
    print('Modules')
    print('-'*20)
    pathNames = set()
    for moduleName_i in sorted(modulePSetDepDict.keys()):
      if psetName in modulePSetDepDict[moduleName_i]:
        print(f'{moduleName_i}')
        for pathName,path in process.paths_().items():
          if path.contains(getattr(process, moduleName_i)):
            pathNames.add(pathName)

    pathNames = sorted(list(pathNames))
    print('-'*20)
    print('Paths')
    print('-'*20)
    for pathName in pathNames:
      print(f'{pathName}')
