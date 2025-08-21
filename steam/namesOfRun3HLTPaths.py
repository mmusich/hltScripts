#!/usr/bin/env python3
import os
import csv
import json
import argparse
import subprocess

import FWCore.ParameterSet.Config as cms
import HLTrigger.Configuration.Tools.options as options
from HLTrigger.Configuration.extend_argparse import *

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

def colored_text(txt, keys=[]):
  _tmp_out = ''
  for _i_tmp in keys:
    _tmp_out += '\033['+_i_tmp+'m'
  _tmp_out += txt
  if len(keys) > 0:
    _tmp_out += '\033[0m'
  return _tmp_out

def getHLTProcess(menu, config):
  if menu.run:
    configline = f'--runNumber {menu.run}'
  else:
    configline = f'--{menu.database} --{menu.version} --configName {menu.name}'

  # cmd to download HLT configuration
  cmdline = f'hltConfigFromDB {configline} --noedsources --noes --nooutput'
  if config.proxy:
    cmdline += f' --dbproxy --dbproxyhost {config.proxy_host} --dbproxyport {config.proxy_port}'

  # download HLT configuration
  proc = subprocess.Popen(cmdline, shell = True, stdin = None, stdout = subprocess.PIPE, stderr = None)
  (out, err) = proc.communicate()

  # load HLT configuration
  try:
    foo = {'process': None}
    exec(out, foo)
    process = foo['process']
  except:
    raise Exception(f'query did not return a valid python file:\n query="{cmdline}"')

  if not isinstance(process, cms.Process):
    raise Exception(f'query did not return a valid HLT menu:\n query="{cmdline}"')

  return process

def getPathNames(menu, config):
  process = getHLTProcess(menu, config)
  ret = [pathName[:pathName.rfind('_v')] if '_v' in pathName else pathName for pathName in process.paths_().keys()]
  return sorted(list(set(ret)))

def create_csv(outputFilePath, delimiter, lines):
  # create output directory
  MKDIRP(os.path.dirname(outputFilePath))
  # write .csv file
  with open(outputFilePath, 'w') as csvfile:
    outf = csv.writer(csvfile, delimiter=delimiter)
    for line_i in lines:
      outf.writerow(line_i)
  print(colored_text(outputFilePath, ['1']))

def main():
  # define an argparse parser to parse our options
  textwidth = int( 80 )
  try:
    textwidth = int( os.popen("stty size", "r").read().split()[1] )
  except:
    pass
  formatter = FixedWidthFormatter( HelpFormatterRespectNewlines, width = textwidth )

  # read defaults
  defaults = options.HLTProcessOptions()

  parser = argparse.ArgumentParser(
    description       = 'List the HLT Paths used during selected 2022-25 runs. For the 4 HLT menus to be specified, supported formats are:\n  - /path/to/configuration[/Vn]\n  - [[{v1|v2|v3}/]{run3|run2|online|adg}:]/path/to/configuration[/Vn]\n  - run:runnumber\nThe possible converters are "v1", "v2, and "v3" (default).\nThe possible databases are "run3" (default, used for offline development), "run2" (used for accessing run2 offline development menus), "online" (used to extract online menus within Point 5) and "adg" (used to extract the online menus outside Point 5).\nIf no menu version is specified, the latest one is automatically used.\nIf "run:" is used instead, the HLT menu used for the given run number is looked up and used.\nNote other converters and databases exist as options but they are only for expert/special use.',
    argument_default  = argparse.SUPPRESS,
    formatter_class   = formatter,
    add_help          = False )

  # required arguments
  parser.add_argument('--menu-2022',
                      dest    = 'menu_2022',
                      action  = 'store',
                      type    = options.ConnectionHLTMenu,
                      metavar = 'MENU_2022',
                      help    = f'2022 HLT menu to dump from the database.' )

  parser.add_argument('--menu-2023',
                      dest    = 'menu_2023',
                      action  = 'store',
                      type    = options.ConnectionHLTMenu,
                      metavar = 'MENU_2023',
                      help    = f'2023 HLT menu to dump from the database.' )

  parser.add_argument('--menu-2024',
                      dest    = 'menu_2024',
                      action  = 'store',
                      type    = options.ConnectionHLTMenu,
                      metavar = 'MENU_2024',
                      help    = f'2024 HLT menu to dump from the database.' )

  parser.add_argument('--menu-2025',
                      dest    = 'menu_2025',
                      action  = 'store',
                      type    = options.ConnectionHLTMenu,
                      metavar = 'MENU_2025',
                      help    = f'2025 HLT menu to dump from the database.' )

  # options
  parser.add_argument('--dbproxy',
                      dest    = 'proxy',
                      action  = 'store_true',
                      default = defaults.proxy,
                      help    = 'Use a socks proxy to connect outside CERN network (default: False)' )
  parser.add_argument('--dbproxyport',
                      dest    = 'proxy_port',
                      action  = 'store',
                      metavar = 'PROXYPORT',
                      default = defaults.proxy_port,
                      help    = 'Port of the socks proxy (default: 8080)' )
  parser.add_argument('--dbproxyhost',
                      dest    = 'proxy_host',
                      action  = 'store',
                      metavar = 'PROXYHOST',
                      default = defaults.proxy_host,
                      help    = 'Host of the socks proxy (default: "localhost")' )

  parser.add_argument('--csv-delimiter',
                      dest    = 'csv_delimiter',
                      action  = 'store',
                      default = '|',
                      help    = 'Delimiter used in the .csv output files (default: "|")' )

  parser.add_argument('-o', '--output-filename',
                      dest    = 'output_filename',
                      action  = 'store',
                      default = 'namesOfRun3HLTPaths.csv',
                      help    = 'Path to the output file' )

  # redefine "--help" to be the last option, and use a customized message 
  parser.add_argument('-h', '--help', 
                      action  = 'help', 
                      help    = 'Show this help message and exit' )

  # parse command line arguments and options
  config = parser.parse_args()

  pathNames = []

  print('Downloading a 2022 trigger menu..')
  pathNames2022 = getPathNames(config.menu_2022, config)
  pathNames += pathNames2022

  print('Downloading a 2023 trigger menu..')
  pathNames2023 = getPathNames(config.menu_2023, config)
  pathNames += pathNames2023

  print('Downloading a 2024 trigger menu..')
  pathNames2024 = getPathNames(config.menu_2024, config)
  pathNames += pathNames2024

  print('Downloading a 2025 trigger menu..')
  pathNames2025 = getPathNames(config.menu_2025, config)
  pathNames += pathNames2025

  pathNames = sorted(list(set(foo for foo in pathNames if not foo.startswith('Dataset_'))))

  lines = [['Trigger Name', 'Code', '2022', '2023', '2024', '2025']]
  for pathName in pathNames:
      is2022 = pathName in pathNames2022
      is2023 = pathName in pathNames2023
      is2024 = pathName in pathNames2024
      is2025 = pathName in pathNames2025
      pathCode = 1*is2022 + 2*is2023 + 4*is2024 + 8*is2025
      lines += [[pathName, pathCode, is2022, is2023, is2024, is2025]]

  create_csv(
    outputFilePath = config.output_filename,
    delimiter = config.csv_delimiter,
    lines = lines,
  )

###
### main
###
if __name__ == '__main__':
  main()
