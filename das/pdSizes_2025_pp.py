#!/usr/bin/env python3
import os
import sys
import subprocess
import json
import re

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

    ret = {}

    pd_dict = {
        'PhysicsMuon': [
            ['/Muon*/Run2025*/RAW','/Muon[0-9]+/Run2025[B-Z]-v[0-9]+/RAW'],
        ],
        'PhysicsEGamma': [
            ['/EGamma*/Run2025*/RAW', '/EGamma[0-9]+/Run2025[B-Z]-v[0-9]+/RAW'],
        ],
        'PhysicsJetMET': [
            ['/JetMET*/Run2025*/RAW', '/JetMET[0-9]+/Run2025[B-Z]-v[0-9]+/RAW'],
        ],
        'PhysicsOthers': [
            ['/BTagMu/Run2025*/RAW', '/BTagMu/Run2025[B-Z]-v[0-9]+/RAW'],
            ['/Commissioning/Run2025*/RAW','/Commissioning/Run2025[B-Z]-v[0-9]+/RAW'],
            ['/DisplacedJet/Run2025*/RAW','/DisplacedJet/Run2025[B-Z]-v[0-9]+/RAW'],
            ['/HLTPhysics/Run2025*/RAW','/HLTPhysics/Run2025[B-Z]-v[0-9]+/RAW'],
            ['/HcalNZS/Run2025*/RAW','/HcalNZS/Run2025[B-Z]-v[0-9]+/RAW'],
            ['/NoBPTX/Run2025*/RAW','/NoBPTX/Run2025[B-Z]-v[0-9]+/RAW'],
            ['/ZeroBias/Run2025*/RAW','/ZeroBias/Run2025[B-Z]-v[0-9]+/RAW'],
            ['/Tau/Run2025*/RAW','/Tau/Run2025[B-Z]-v[0-9]+/RAW'],
            ['/ScoutingPFMonitor/Run2025*/RAW','/ScoutingPFMonitor/Run2025[B-Z]-v[0-9]+/RAW'],
        ],

        'ParkingSingleMuon': [
            ['/ParkingSingleMuon*/Run2025*/RAW', '/ParkingSingleMuon[0-9]+/Run2025[B-Z]-v[0-9]+/RAW'],
        ],
        'ParkingDoubleMuonLowMass': [
            ['/ParkingDoubleMuonLowMass*/Run2025*/RAW', '/ParkingDoubleMuonLowMass[0-9]+/Run2025[B-Z]-v[0-9]+/RAW'],
        ],
        'ParkingVBF': [
            ['/ParkingVBF*/Run2025*/RAW', '/ParkingVBF[0-9]+/Run2025[B-Z]-v[0-9]+/RAW'],
        ],
        'ParkingHH': [
            ['/ParkingHH/Run2025*/RAW', '/ParkingHH/Run2025[B-Z]-v[0-9]+/RAW'],
        ],
        'ParkingLLP': [
            ['/ParkingLLP*/Run2025*/RAW', '/ParkingLLP[0-9]+/Run2025[B-Z]-v[0-9]+/RAW'],
        ],

        'HLT-Scouting': [
            ['/ScoutingPFRun3/Run2025*/HLTSCOUT', '/ScoutingPFRun3/Run2025[B-Z]-v[0-9]+/HLTSCOUT'],
        ],
    }

    pd_keys = sorted(pd_dict.keys())
    for pd_key in pd_keys:
        ret[pd_key] = []
        pd_exprs = pd_dict[pd_key]
        for pd_wildcard, pd_regex in pd_exprs:
            datasets = command_output_lines(f'dasgoclient -query "{pd_wildcard}" status=VALID')
            datasets = sorted(list(set([foo for foo in datasets if re.match(pd_regex, foo)])))
            for dataset in datasets:
                print(f'{pd_key: <30} {dataset: <50}')
                das_query = f'dasgoclient -query "file dataset={dataset} | sum(file.size)"'
                dataset_size_lines = [foo for foo in command_output_lines(das_query) if foo]
                if len(dataset_size_lines) != 1:
                    raise RuntimeError(f'invalid output for DAS query "{das_query}": {dataset_size_lines}')
                dataset_size = int(dataset_size_lines[0].replace('sum(file.size): ', ''))
                ret[pd_key] += [(dataset, dataset_size)]
        ret[pd_key].sort(key=lambda x : x[0])
        print('-'*100)

    json.dump(ret, open('tmp.json', 'w'), sort_keys=True, indent=4)

    print('\n'+'='*100+'\n')

    for foo in ret:
        print(foo)
        for bar in ret[foo]:
            print(f'    {bar[0]: <50} {bar[1]: >30d}')

#    str_separator = '-'*200
#    print(str_separator)
#    for dataset in datasets:
#        if dataset in datasetMap:
#            continue
#        parent_dataset = command_output_lines(f'dasgoclient -query "parent dataset={dataset}"')[0]
#        print(parent_dataset)
#        configs = command_output_lines(f'dasgoclient -query "config dataset={parent_dataset}"')
#        config = None
#        config_label = None
#        for config in configs:
#            for config_piece in config.split('_'):
#                if campaign_name in config_piece and 'GS' in config_piece:
#                    print(config)
#                    config_label = config_piece
#                    break
#        fragment_url = f'https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/{config_label}/0'
#        EXE(f'wget -O {config_label}.py {fragment_url} &> /dev/null')
#        objs = {'externalLHEProducer': None}
#        exec(open(f'{config_label}.py').read(), globals(), objs)
#        tarball_name = objs['externalLHEProducer'].args.value() if objs['externalLHEProducer'] != None else 'None'
#        print(tarball_name)
#        print(str_separator)
#        datasetMap[dataset] = tarball_name
#        json.dump(datasetMap, open(output_file, 'w'), sort_keys=True, indent=4)
