#!/usr/bin/env python3
import os
import sys
import subprocess
import json

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

def MKDIRP(dirpath, verbose=False, dry_run=False):
    if verbose:
        print('\033[1m'+'>'+'\033[0m'+' os.mkdirs("'+dirpath+'")')
    if dry_run:
        return
    try:
      os.makedirs(dirpath)
    except OSError:
      if not os.path.isdir(dirpath):
        raise
    return

def EXE(cmd, suspend=True, verbose=False, dry_run=False):
    if verbose:
        print('\033[1m'+'>'+'\033[0m'+' '+cmd)
    if dry_run:
        return

    _exitcode = os.system(cmd)
    _exitcode = min(255, _exitcode)

    if _exitcode and suspend:
       WARNING(cmd)
       raise RuntimeError(_exitcode)

    return _exitcode

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
    campaign_name = sys.argv[1]
    output_file = sys.argv[2]

    datasetMap = dict()
    if os.path.isfile(output_file):
        datasetMap = json.load(open(output_file, 'r'))

    datasets = command_output_lines(f'dasgoclient -query "/*/*{campaign_name}*/*RAW*" status=*')
    datasets = sorted(list(set([foo for foo in datasets if foo])))

    str_separator = '-'*200
    print(str_separator)
    for dataset in datasets:
        if dataset in datasetMap:
            continue
        parent_dataset = command_output_lines(f'dasgoclient -query "parent dataset={dataset}"')[0]
        print(parent_dataset)
        configs = command_output_lines(f'dasgoclient -query "config dataset={parent_dataset}"')
        config = None
        config_label = None
        for config in configs:
            for config_piece in config.split('_'):
                if campaign_name in config_piece and 'GS' in config_piece:
                    print(config)
                    config_label = config_piece
                    break
        fragment_url = f'https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/{config_label}/0'
        EXE(f'wget -O {config_label}.py {fragment_url} &> /dev/null')
        objs = {'externalLHEProducer': None}
        exec(open(f'{config_label}.py').read(), globals(), objs)
        tarball_name = objs['externalLHEProducer'].args.value() if objs['externalLHEProducer'] != None else 'None'
        print(tarball_name)
        print(str_separator)
        datasetMap[dataset] = tarball_name
        json.dump(datasetMap, open(output_file, 'w'), sort_keys=True, indent=4)
