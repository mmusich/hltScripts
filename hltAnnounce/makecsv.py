#!/usr/bin/env python3
import os
import csv
import json

from frozen_ofOnline import cms,process

def colored_text(txt, keys=[]):
  _tmp_out = ''
  for _i_tmp in keys:
    _tmp_out += '\033['+_i_tmp+'m'
  _tmp_out += txt
  if len(keys) > 0:
    _tmp_out += '\033[0m'
  return _tmp_out

def getPathOwnershipDict(filepath):
  ret = {}
  with open(filepath, mode='r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    line_i = -1
    labels = []
    for row_split in lines:
      line_i += 1
      if line_i == 0:
        labels = row_split[:row_split.index('Owners')+1]
        assert row_split[0] == 'path'
      else:
        pathName = row_split[0]
        if pathName:
          ret[pathName] = sorted(list(set([
            renameOwner(f'{labels[idx]} ({row_split[idx]})') for idx in range(1, len(labels)-1) if row_split[idx]
          ])))
          print(pathName, ret[pathName], row_split[len(labels)-1])
#          assert len(ret[pathName]) == int(row_split[len(labels)-1])
  return ret

def getPrescaleTableLines(process, pathNames):
  ret = []
  if hasattr(process, 'PrescaleService'):
    ret += [['Path']+process.PrescaleService.lvl1Labels]
    ncols = len(process.PrescaleService.lvl1Labels)
    psDict = {pset_i.pathName.value():pset_i.prescales for pset_i in process.PrescaleService.prescaleTable}
    for pathName in pathNames:
      if pathName not in process.paths_():
        raise SystemExit(f'getPrescaleTableLines: {pathName}')
      psvals = psDict[pathName] if pathName in psDict else [1]*ncols
      ret += [[pathName]+[str(psval_i) for psval_i in psvals]]
  return ret

def getPrescale(process, pathName, psColumnName):
  ret = ''
  if not hasattr(process, 'PrescaleService'):
    return ret
  psColIndex = -1
  for psColIdx_i, psColName_i in enumerate(process.PrescaleService.lvl1Labels):
    if psColName_i == psColumnName:
      psColIndex = psColIdx_i
  if psColIndex < 0:
    return ret
  ret = '1'
  for pset_i in process.PrescaleService.prescaleTable:
    if pathName == pset_i.pathName:
      ret = f'{pset_i.prescales[psColIndex]}'
      break
  return ret

def getDatasets(process, pathName):
  # format: "PD1 (smartPSinPD1), PD2 (smartPSinPD2), .."
  ret = []
  datasets = [dataset_i for dataset_i in process.datasets.parameterNames_() \
    if pathName in process.datasets.getParameter(dataset_i)]
  for dataset_i in datasets:
    datasetLabel = dataset_i
    # if the DatasetPath exists, add value of smart-prescale
    if hasattr(process, 'Dataset_'+dataset_i):
      datasetPath_i = getattr(process, 'Dataset_'+dataset_i)
      if isinstance(datasetPath_i, cms.Path):
        for modName in datasetPath_i.moduleNames():
          module = getattr(process, modName)
          if module.type_() == 'TriggerResultsFilter':
            if hasattr(module, 'triggerConditions'):
              for trigCond_j in module.triggerConditions:
                trigCond_j_split = trigCond_j.split(' / ')
                if trigCond_j_split[0] == pathName and len(trigCond_j_split) > 1:
                  datasetLabel += f'({trigCond_j_split[1]})'
    ret += [datasetLabel]
  return ', '.join(ret)

def getStreams(process, pathName):
  # format: "Stream1, Stream2, .."
  datasets = [dataset_i for dataset_i in process.datasets.parameterNames_() \
    if pathName in process.datasets.getParameter(dataset_i)]
  streams = [stream_i for stream_i in process.streams.parameterNames_() \
    for dataset_i in datasets if dataset_i in process.streams.getParameter(stream_i)]
  return ', '.join(streams)

def getL1TSeed(process, pathName):
  ret = ''
  path = process.paths_()[pathName]
  for modName in path.moduleNames():
    module = getattr(process, modName)
    if module.type_() == 'HLTL1TSeed':
      if hasattr(module, 'L1SeedsLogicalExpression'):
        ret = module.L1SeedsLogicalExpression.value()
        break
  return ret

def main():

  pathNames = [pathName for pathName, path in process.paths_().items()] # if process.schedule_().contains(path)]

  ownersDict = json.load(open('owners.json'))

  pathAttributes = {}
  for pathName in pathNames:
    pathNameUnv = pathName[:pathName.rfind('_v')+2] if '_v' in pathName else pathName
    pathOwners = ', '.join(ownersDict[pathNameUnv]) if pathNameUnv in ownersDict else ''
    path = process.paths_()[pathName]
    pathAttributes[pathName] = {
      'Online?': 'Yes',
      'Owners': pathOwners,
      'PS (2.0E34)': getPrescale(process, pathName, '2.0e34+ZB+HLTPhysics'),
      'Datasets (SmartPS)': getDatasets(process, pathName),
      'Streams': getStreams(process, pathName),
      'L1T Seed': getL1TSeed(process, pathName),
    }

  lines1 = []

  lines1 += [[
    'Path',
    'Online?',
    'Owners',
    'PS (2.0E34)',
    'Datasets (SmartPS)',
    'Streams',
    'L1T Seed',
  ]]

  for pathName in pathNames:
    if pathName.startswith('Dataset_'):
      continue

    pathDict = pathAttributes[pathName]
    lines1 += [[
      pathName,
      pathDict[lines1[0][1]],
      pathDict[lines1[0][2]],
      pathDict[lines1[0][3]],
      pathDict[lines1[0][4]],
      pathDict[lines1[0][5]],
      pathDict[lines1[0][6]],
    ]]

  lines2 = getPrescaleTableLines(process, pathNames)

  def makecsv(outputFilePath, lines, delimiter):
    with open(outputFilePath, 'w') as csvfile:
      outf = csv.writer(csvfile, delimiter=delimiter)
      for line_i in lines:
        outf.writerow(line_i)

  makecsv(outputFilePath='outputcsv1.csv', lines=lines1, delimiter='|')
  makecsv(outputFilePath='outputcsv2.csv', lines=lines2, delimiter='|')

if __name__ == '__main__':
  main()
