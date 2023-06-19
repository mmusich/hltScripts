#!/usr/bin/env python3
import os

# hltGetConfiguration /dev/CMSSW_13_0_0/HLT/V79 > hlt.py
from hlt import cms, process as hlt

from HLTrigger.Configuration.common import filters_by_type

'''
diff --git a/HLTrigger/btau/plugins/HLTJetTag.cc b/HLTrigger/btau/plugins/HLTJetTag.cc
index 61f15b886dc..556a7acd578 100644
--- a/HLTrigger/btau/plugins/HLTJetTag.cc
+++ b/HLTrigger/btau/plugins/HLTJetTag.cc
@@ -101,6 +101,9 @@ bool HLTJetTag<T>::hltFilter(edm::Event& event,
           << dependent_provenance.branchName() << ", which has been dropped";
   }
 
+edm::LogPrint("HLTJetTag") << moduleDescription().moduleLabel() << " : dep.isNonNull = " << dependent.isNonnull() << ", makesSense = "
+  << (dependent.isNonnull() and dependent.id() == h_Jets.id()) << " (" << h_Jets->size() << ", " << h_JetTags->size() << ")";
+
   TRef jetRef;
 
   // Look at all jets in decreasing order of Et.
'''

def getModuleLabels(process):
  modLabels = []
  for mod in filters_by_type(process, 'HLTCaloJetTag'):
    modLabels += [mod.label()]
  for mod in filters_by_type(process, 'HLTPFJetTag'):
    modLabels += [mod.label()]
  return sorted(list(set(modLabels)))

def main():
  modDict = {}
  logFilePath = 'testHLT1.log'
  if os.path.isfile(logFilePath):
    with open(logFilePath, 'r') as logFile:
      lines = logFile.read().splitlines()
      for line in lines:
        if line.endswith(' (0, 0)'):
          continue
        if 'makesSense' in line:
          if 'makesSense = 0' in line:
            makesSense = 0
          elif 'makesSense = 1' in line:
            makesSense = 1
          else:
            raise RuntimeError('X1 '+line)
          modName = line.split()[0]
          if modName in modDict and modDict[modName] != makesSense:
            raise RuntimeError('X2 '+line)
          else:
            modDict[modName] = makesSense

  modLabels_missing = [modLabel for modLabel in getModuleLabels(hlt) if modLabel not in modDict]
  if len(modLabels_missing) > 0:
    print('MISSING MODULES')
    for modLabel in modLabels_missing:
      print(' ', modLabel)
  else:
    for modLabel in modDict:
      if modDict[modLabel] == 0:
        print(modLabel)

if __name__ == '__main__':
  main()
