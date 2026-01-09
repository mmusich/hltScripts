#!/usr/bin/env python3
import sys
import subprocess

def colored_text(txt, keys=[]):
    _tmp_out = ''
    for _i_tmp in keys:
        _tmp_out += '\033['+_i_tmp+'m'
    _tmp_out += txt
    if len(keys) > 0: _tmp_out += '\033[0m'

    return _tmp_out

def KILL(log):
    raise RuntimeError('\n '+colored_text('@@@ FATAL', ['1','91'])+' -- '+log+'\n')

def WARNING(log):
    print('\n '+colored_text('@@@ WARNING', ['1','93'])+' -- '+log+'\n')

def get_output(cmd, permissive=False):
    prc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf8')

    out, err = prc.communicate()

    if (not permissive) and prc.returncode:
       KILL('get_output -- shell command failed (execute command to reproduce the error):\n'+' '*14+'> '+cmd)

    return (out, err)

def command_output_lines(cmd, stdout=True, stderr=False, permissive=False):
    _tmp_out_ls = []

    if not (stdout or stderr):
       WARNING('command_output_lines -- options "stdout" and "stderr" both set to FALSE, returning empty list')
       return _tmp_out_ls

    _tmp_out = get_output(cmd, permissive=permissive)

    if stdout: _tmp_out_ls += _tmp_out[0].split('\n')
    if stderr: _tmp_out_ls += _tmp_out[1].split('\n')

    return _tmp_out_ls

if __name__ == '__main__':

  rles = [
    '379765:680:1480598569',
    '379866:528:591086643',
    '380564:97:82621912',
    '380963:312:555226512',
    '381544:57:115517957',
    '382792:11:21651220',
    '383155:723:1778413076',
    '383162:1179:2742138641',
    '383537:21:49431336',
    '383629:135:282848790',
    '384202:1700:3885126867',
    '384265:224:535357942',
    '385168:1793:4010777559',
    '385415:316:631661023',
    '385437:233:432347306',
    '385515:939:2165172387',
    '385620:242:548366206',
    '385713:456:1031543538',
    '385764:2126:4693786018',
    '386025:129:186487855',
  ]

  for rle in rles:
    print(rle)

    rle_split = rle.split(':')
    run = rle_split[0]
    lumi = rle_split[1]

    datasets = command_output_lines(f'dasgoclient -query "dataset run={run} dataset=/Muon*/Run202*/RAW"')
    for dataset in datasets:
      if not (dataset.startswith('/Muon0/') or dataset.startswith('/Muon1/')):
        continue
      fileAndLumis = command_output_lines(f'dasgoclient -query "file,lumi run={run} dataset={dataset}" | grep {lumi}')
      for fileAndLumi in fileAndLumis:
        if not fileAndLumi:
          continue
        fileAndLumi_split = fileAndLumi.split()
        lumis = fileAndLumi_split[1][1:-1].split(',')
        if lumi not in lumis:
          continue
        print(f'  {fileAndLumi_split[0]}')
