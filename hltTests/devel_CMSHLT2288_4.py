#!/usr/bin/env python3
import FWCore.ParameterSet.Config as cms

#from pre import process as process1
#from post import process as process2

def compare(process1, process2, key):
  obj1 = getattr(process1, key)
  obj2 = getattr(process2, key)
  names = set(list(obj1) + list(obj2))
  for foo in names:
    if obj1[foo].dumpPython() != obj2[foo].dumpPython():
      print(key, ':', foo)

def compare1(process1, process2, key):
  obj1 = getattr(process1, key)
  obj2 = getattr(process2, key)
  if obj1.dumpPython() != obj2.dumpPython():
    print(key)

#compare(process1, process2, 'paths')
#compare(process1, process2, 'endpaths')
#compare(process1, process2, 'finalpaths')
#compare(process1, process2, 'sequences')
#compare(process1, process2, 'tasks')
#compare(process1, process2, 'outputModules')
#
#compare(process1, process2, 'analyzers')
#compare(process1, process2, 'filters')
#compare(process1, process2, 'producers')
#compare(process1, process2, 'switchProducers')
#compare(process1, process2, 'es_producers')
#compare(process1, process2, 'es_prefers')
#compare(process1, process2, 'es_sources')
#compare(process1, process2, 'services')
#compare(process1, process2, 'psets')
#compare(process1, process2, 'vpsets')
#
#compare1(process1, process2, 'source')
#compare1(process1, process2, 'schedule')

from ref import process as process1
from tar import process as process2

def count(process1, process2, key):
  obj1 = getattr(process1, key)
  obj2 = getattr(process2, key)
  print(key, len(obj1), len(obj2))

count(process1, process2, 'aliases')
count(process1, process2, 'analyzers')
count(process1, process2, 'filters')
count(process1, process2, 'producers')
count(process1, process2, 'switchProducers')
count(process1, process2, 'es_producers')
count(process1, process2, 'es_prefers')
count(process1, process2, 'es_sources')
count(process1, process2, 'services')
count(process1, process2, 'psets')
count(process1, process2, 'vpsets')
