#!/usr/bin/env python3
import os
import csv
import json

def colored_text(txt, keys=[]):
  _tmp_out = ''
  for _i_tmp in keys:
    _tmp_out += '\033['+_i_tmp+'m'
  _tmp_out += txt
  if len(keys) > 0:
    _tmp_out += '\033[0m'
  return _tmp_out

def renameOwner(owner):
  _tmpReplace = [
    [' (todo)',''],
    [' (to-do)',''],
    [' (toto)',''],
    [' (alca)',''],
    ['DPG (beamspot)','BeamSpot'],
    ['DPG (ECAL)','ECAL'],
    ['DPG (Express)','Express'],
    ['DPG (HCAL)','HCAL'],
    ['DPG (Lumi)','LUM'],
    ['DPG (PPS)','PPS'],
    ['DPG (RPC)','RPC'],
  ]
  ret = owner
  for _tmpOld, _tmpNew in _tmpReplace:
    ret = ret.replace(_tmpOld, _tmpNew)

  return ret

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
        if '_v' in pathName:
          pathName = pathName[:pathName.rfind('_v')+2]
        if pathName:
          ret[pathName] = sorted(list(set([
            renameOwner(f'{labels[idx]} ({row_split[idx]})') for idx in range(1, len(labels)-1) if row_split[idx]
          ])))
          print(pathName, ret[pathName], row_split[len(labels)-1])
#          assert len(ret[pathName]) == int(row_split[len(labels)-1])

  return ret

def main():
  ret = getPathOwnershipDict('owners.csv')
  json.dump(ret, open('owners.json', 'w'), sort_keys=True, indent=4)

if __name__ == '__main__':
  main()
