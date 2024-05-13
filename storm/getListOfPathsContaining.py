#!/usr/bin/env python3
import os
import sys
import importlib.util
import FWCore.ParameterSet.Config as cms

if __name__ == '__main__':
    if len(sys.argv) < 3:
      raise Exception('Two cmd-line args required: (a) name of the Module, and (b) path to python configuration file, or name of a menu in ConfDB')

    moduleName = sys.argv[1]

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

    pathNames = set()
    for pathName,path in process.paths_().items():
        if path.contains(getattr(process, moduleName)):
            pathNames.add(pathName)

    pathNames = sorted(list(pathNames))
    print('-'*20)
    print('Paths')
    print('-'*20)
    for pathName in pathNames:
      print(f'{pathName}')
    
