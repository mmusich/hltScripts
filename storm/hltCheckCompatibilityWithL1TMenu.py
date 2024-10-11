#!/usr/bin/env python3
import argparse
import os
import subprocess
import tempfile

from HLTrigger.Configuration.common import filters_by_type

def get_output(cmd, permissive = False):
    prc = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True)
    out, err = prc.communicate()
    if (not permissive) and prc.returncode:
       raise RuntimeError('get_output -- shell command failed (execute command to reproduce the error):\n'+' '*14+'> '+cmd)
    return (out, err)

def command_output_lines(cmd, stdout = True, stderr = False, permissive = False):
    if not (stdout or stderr):
       print('command_output_lines -- options "stdout" and "stderr" both set to FALSE, returning empty list')
       return []

    _tmp_out, _tmp_out_ls = get_output(cmd, permissive=permissive), []
    if stdout: _tmp_out_ls += _tmp_out[0].split('\n')
    if stderr: _tmp_out_ls += _tmp_out[1].split('\n')

    return _tmp_out_ls

def conddb_exe(database):
    ret = 'conddb'+(database != None)*f' --db "{database}"'
    return ret

def getXMLFileFromL1TMenuTag(tag_name, run_number, database = None):
    # find hash of payload for the selected IOV of the L1T-menu tag (last IOV up the snapshot time, if available)
    conddb_cmd = f'{conddb_exe(database)} list {tag_name} | grep L1TUtmTriggerMenu'
    out_lines = [foo for foo in command_output_lines(conddb_cmd) if len(foo) > 0]
    payload = None
    for tag_iov_line in reversed(out_lines):
        tag_iov_info = tag_iov_line.split()
        if tag_iov_info[4] != 'L1TUtmTriggerMenu':
            continue
        try:
            if run_number >= int(tag_iov_info[0]):
                payload = tag_iov_info[3]
                break
        except:
            continue

    if payload == None:
        raise RuntimeError('failed to find L1T-menu payload for IOV corresponding to run={run_number}: cmd="{conddb_cmd}"\n{out_lines}')

    xml_outfile_path = None
    with tempfile.NamedTemporaryFile() as tmp:
        xml_outfile_path = tmp.name

    get_output(f'{conddb_exe(database)} dump {payload} > {xml_outfile_path}')

    print(f'L1T menu taken from conditions-db tag "{tag_name}" (payload = {payload})')

    return xml_outfile_path

def getL1TMenuTagFromGlobalTag(globaltag, database = None):
    conddb_cmd = f'{conddb_exe(database)} list {globaltag} | grep L1TUtmTriggerMenuRcd | sed "s/ *$//g" | sed "s/^.* //g"'
    out_lines = [foo for foo in command_output_lines(conddb_cmd) if len(foo) > 0]
    if len(out_lines) != 1:
        raise RuntimeError('failed parsing output of conddb (failed to find tag of L1T menu in GlobalTag): cmd="{conddb_cmd}"\n{out_lines}')
    return out_lines[0]

def getL1TSeedsFromXMLFile(xml_file_path):
    # first check the .xml format returned by conddb;
    # if no match, check the other .xml format, the one used by the L1T DPG
    # (one could add a flag to decide which .xml format to check,
    #  but here we simply check the other one when the first returns 0 matches,
    #  as we don't expect any .xml to return one or more matches for both formats;
    #  in other words, the two formats are 'orthogonal')
    for grep_cmd in [
        # .xml format returned by conddb
        f"grep '<first>' {xml_file_path} | sed 's/^.*<first>\(.*\)<\/first>*$/\\1/g' | sed '/--/d'",
        # .xml format used by L1T DPG
        f"grep '<algorithm>' -A 1 {xml_file_path} | grep -v '<algorithm>' | sed 's/^.*<name>\(.*\)<\/name>*$/\\1/g' | sed '/--/d'",
    ]:
        ret = [foo for foo in command_output_lines(grep_cmd) if len(foo) > 0 and foo.startswith('L1_')]
        if len(ret) > 0:
            break
    return ret

def getL1TSeedsFromGlobalTag(globaltag, run_number, database = None):
    l1tMenu_tag = getL1TMenuTagFromGlobalTag(globaltag, database)
    return getL1TSeedsFromL1TMenuTag(l1tMenu_tag, run_number, database)

def getL1TSeedsFromL1TMenuTag(tag_name, run_number, database = None):
    xml_file_path = getXMLFileFromL1TMenuTag(tag_name, run_number, database)
    return getL1TSeedsFromXMLFile(xml_file_path)

def getL1TSeedUsedInHLTMenu(hltConfig_file_path):
    try:
        foo = {'process': None}
        exec(open(hltConfig_file_path).read(), foo)
        process = foo['process']
    except:
        # if first attempt fails, try again with the fully-expanded version of the configuration file
        try:
            with tempfile.NamedTemporaryFile() as tmp:
                get_output(f'edmConfigDump {hltConfig_file_path} > {tmp.name}')
                foo = {'process': None}
                exec(open(tmp.name).read(), foo)
                process = foo['process']
        except:
            raise RuntimeError(f'failed to parse HLT configuration: {hltConfig_file_path}')

    ret = []
    for mod in filters_by_type(process, 'HLTL1TSeed'):
        tmplist = [foo.replace('(','').replace(')','') for foo in mod.L1SeedsLogicalExpression.value().split()]
        ret += [foo for foo in tmplist if foo.startswith('L1_')]
    for mod in filters_by_type(process, 'TriggerResultsFilter'):
        tmplist = [bar.replace('(','').replace(')','') for foo in mod.triggerConditions for bar in foo.split()]
        ret += [foo for foo in tmplist if foo.startswith('L1_') and (('*' not in foo) and ('?' not in foo))]

    try:
        hltConfigVersionStr = f' (HLTConfigVersion.tableName = "{process.HLTConfigVersion.tableName.value()}")'
    except:
        hltConfigVersionStr = ''

    print(f'HLT menu taken from configuration file: {hltConfig_file_path}{hltConfigVersionStr}')

    return sorted(list(set(ret)))

###
### main
###
def main():
    ### args
    parser = argparse.ArgumentParser(
        prog = './'+os.path.basename(__file__),
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = __doc__
    )

    parser.add_argument('hltConfig_file_path', type = str,
                        help = 'Path to cmsRun configuration file for HLT jobs')

    parser.add_argument('-r', '--run-number', dest = 'run_number', action = 'store', type = int, default = None,
                        help = 'Run number (necessary to choose IOV of L1T-menu tag, if options "-g" or "-t" are used)')

    parser.add_argument('-d', '--db', dest = 'db', action = 'store', default = None,
                        help = 'Database to run the command on (this string is passed to the --db argument of conddb)')

    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-g', '--globaltag', dest = 'globaltag', type = str, default = None,
                       help = 'Name of GlobalTag')

    group.add_argument('-t', '--l1t-menu-tag-name', dest = 'l1t_menu_tag_name', type = str, default = None,
                       help = 'Name of L1T-menu tag in the conditions database')

    group.add_argument('-x', '--l1t-menu-xml-file', dest = 'l1t_menu_xml_file_path', type = str, default = None,
                       help = 'Path to .xml file containing the L1T menu')

    args, args_unknown = parser.parse_known_args()
    ### ----

    if len(args_unknown) > 0:
        raise RuntimeError('unsupported command-line arguments: '+str(args_unknown))

    l1tMenuAlgos = None
    if args.l1t_menu_xml_file_path != None:
        print(f'L1T menu taken from .xml file: {args.l1t_menu_xml_file_path}')
        l1tMenuAlgos = getL1TSeedsFromXMLFile(args.l1t_menu_xml_file_path)
    else:
        if args.run_number == None:
            raise RuntimeError('failed to specify run number [-r] (necessary to choose IOV of L1T-menu tag)')
        if args.globaltag != None:
            l1tMenuAlgos = getL1TSeedsFromGlobalTag(args.globaltag, args.run_number, args.db)
        elif args.l1t_menu_tag_name != None:
            l1tMenuAlgos = getL1TSeedsFromL1TMenuTag(args.l1t_menu_tag_name, args.run_number, args.db)

    if l1tMenuAlgos == None:
        raise RuntimeError('failed to specify a L1T menu (see options "-g", "-t" and "-x" with "--help")')

    if not os.path.isfile(args.hltConfig_file_path):
        raise RuntimeError(f'invalid path to cmsRun configuration file for HLT jobs: "{args.hltConfig_file_path}"')

    hltMenuSeeds = getL1TSeedUsedInHLTMenu(args.hltConfig_file_path)
    print('='*30)
    print(f'L1T Seeds in HLT menu = {len(hltMenuSeeds)}')
    print(f'L1T Algos in L1T menu = {len(l1tMenuAlgos)}')
    print('='*30)

    l1tAlgosMissing = []
    for hltSeed in hltMenuSeeds:
        if hltSeed not in l1tMenuAlgos:
            l1tAlgosMissing += [hltSeed]
    l1tAlgosMissing = sorted(list(set(l1tAlgosMissing)))

    if l1tAlgosMissing:
        print(f'\033[31m\033[1mERROR: -- The following {len(l1tAlgosMissing)} L1T algos are required in the HLT menu, but missing in the L1T menu.\033[0m')
        for l1tAlgo in l1tAlgosMissing:
            print(f' \033[31m\033[1m{l1tAlgo}\033[0m')
        raise SystemExit(1)

    print('These L1T and HLT menus are compatible.')

if __name__ == '__main__':
    main()
