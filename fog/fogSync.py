#!/usr/bin/env python3
import FWCore.ParameterSet.Config as cms
import sys

def getProcess(configFile):
  try:
    foo = {'process': None}
    exec(open(configFile).read(), foo)
    process = foo['process']
  except:
    raise Exception(f'python file is invalid:\n "{configFile}"')

  if not isinstance(process, cms.Process):
    raise Exception(f'HLT menu is invalid:\n "{configFile}"')

  return process

def compareGroup(process1, process2, group, options):
  obj1 = getattr(process1, group)
  obj2 = getattr(process2, group)
  names = set(list(obj1) + list(obj2))
  for foo in names:
    if foo in obj1 and foo in obj2:
      if obj1[foo].dumpPython() != obj2[foo].dumpPython():
        print('DIFFER |', group, ':', foo)
    elif foo not in obj1:
      if not options.only1:
        print('MISSING IN 1 |', group, ':', foo)
    elif foo not in obj2:
      if not options.only2:
        print('MISSING IN 2 |', group, ':', foo)

def compareModule(process1, process2, module, options):
  if not hasattr(process1, module):
    if not options.only1:
      print('MISSING IN 1 |', module)
  elif not hasattr(process2, module):
    if not options.only2:
      print('MISSING IN 2 |', module)
  else:
    obj1 = getattr(process1, module)
    obj2 = getattr(process2, module)
    if obj1.dumpPython() != obj2.dumpPython():
      print('DIFFER |', module)

if __name__ == '__main__':

  file1 = sys.argv[1]
  file2 = sys.argv[2]

  proc1 = getProcess(file1)
  proc2 = getProcess(file2)

  class Options:
    def __init__(self):
      self.only1 = False
      self.only2 = False

  opts = Options()
  opts.only1 = False
  opts.only2 = False

  for groupName in [
    'paths',
    'endpaths',
    'finalpaths',
    'sequences',
    'tasks',
    'outputModules',
    'analyzers',
    'filters',
    'producers',
    'aliases',
    'switchProducers',
    'es_producers',
    'es_prefers',
    'es_sources',
    'services',
    'psets',
    'vpsets',
  ]:
    compareGroup(process1=proc1, process2=proc2, group=groupName, options=opts)

  for moduleName in [
    'source',
    'schedule',
  ]:
    compareModule(process1=proc1, process2=proc2, module=moduleName, options=opts)

  #def count(process1, process2, key):
  #  obj1 = getattr(process1, key)
  #  obj2 = getattr(process2, key)
  #  print(key, len(obj1), len(obj2))
  #
  #count(process1, process2, 'aliases')
  #count(process1, process2, 'analyzers')
  #count(process1, process2, 'filters')
  #count(process1, process2, 'producers')
  #count(process1, process2, 'switchProducers')
  #count(process1, process2, 'es_producers')
  #count(process1, process2, 'es_prefers')
  #count(process1, process2, 'es_sources')
  #count(process1, process2, 'services')
  #count(process1, process2, 'psets')
  #count(process1, process2, 'vpsets')
