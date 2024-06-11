#!/usr/bin/env python3
import argparse
import json

from omsapi import OMSAPI

def get_omsapi():
    omsapi = OMSAPI('https://cmsoms.cern.ch/agg/api', 'v1', cert_verify=False)
    # Authenticate using kerberos
    omsapi.auth_krb()
    return omsapi

def expand_lumisections_list(lsList):
    lsSet = set()
    for lsMin,lsMax in lsList:
        for lsNum in range(lsMin, lsMax+1):
            lsSet.add(lsNum)
    return sorted(list(lsSet))

def group_lumisections_list(lsList):
    if not lsList: return []
    ret, lsSubList = [], [lsList[0], lsList[0]]
    for lsNum in lsList[1:]:
        if lsSubList[-1] == (lsNum - 1):
            lsSubList[-1] = lsNum
        else:
           ret += [lsSubList]
           lsSubList = [lsNum, lsNum]
    ret += [lsSubList]
    return ret

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Script to remove LSs where any of the Tracker (Tk) DCS bits are set to False')
    parser.add_argument('-i', '--input-json', dest='input_json', default=None, help='Path to input .json file')
    parser.add_argument('-o', '--output-json', dest='output_json', default=None, help='Path to output .json file')
    args = parser.parse_args()

    json_input = json.load(open(args.input_json, 'r'))

    tkDCSLabels = [
      'bpix_ready',
      'fpix_ready',
      'tibtid_ready',
      'tob_ready',
      'tecm_ready',
      'tecp_ready',
    ]

    json_output = {}

    omsapi = get_omsapi()

    stdout_separator = '-'*100

    for runNumber in json_input:
        print(stdout_separator)
        print(f'Run: {runNumber}')
        lsListInp, lsSetOut = expand_lumisections_list(json_input[runNumber]), set()
        q_lumis = omsapi.query('lumisections')
        q_lumis.set_verbose(False)
        q_lumis.filter('run_number', runNumber)
        q_lumis.paginate(page=1, per_page=1)
        data_lumis = q_lumis.data()
        data_lumis_dict = data_lumis.json()
        ntot_lumis = data_lumis_dict['meta']['totalResourceCount']
        npages_lumis = int(1+ntot_lumis/1e5)
        for page_idx in range(1, 1+npages_lumis):
            q_lumis.paginate(page=page_idx, per_page=int(1e5))
            data_lumis_dict = q_lumis.data().json()['data']
            for lumi_entry in data_lumis_dict:
                lumi_attr = lumi_entry['attributes']
                lsNumber = int(lumi_attr['lumisection_number'])
                if lsNumber not in lsListInp:
                    continue
                hasAllTkDCSBitsOn = True
                for dcsLabel in tkDCSLabels:
                    hasAllTkDCSBitsOn *= lumi_attr[dcsLabel]
                if hasAllTkDCSBitsOn:
                    lsSetOut.add(lsNumber)

        lsListOut = sorted(list(lsSetOut))
        lsListOutGrouped = group_lumisections_list(lsListOut)
        if lsListOutGrouped:
            json_output[runNumber] = lsListOutGrouped

        if lsListInp != lsListOut:
            print(f'  {len(lsListInp)-len(lsListOut)} lumisections removed')
            print(f'  input  list: {json_input[runNumber]}')
            print(f'  output list: {lsListOutGrouped}')

    if json_input:
        print(stdout_separator)

    json.dump(json_output, open(args.output_json, 'w'), sort_keys=True)
