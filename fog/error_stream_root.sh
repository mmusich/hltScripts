#!/bin/bash

# help message
showHelpMsg=false
runNumber=-1

helpMessage() {
  cat <<@EOF
Usage:
  This script converts files in FRD format to ROOT formats (repacking).
  It can be executed from any directory with access to CERN EOS.
  Only input files in the EOS directory /eos/cms/store/group/tsg/FOG/error_stream/ are considered.
  One number, N, is required as command-line argument.
  This script will repack available error-stream files of run(s) *N*,
  and place them in the EOS directories /eos/cms/store/group/tsg/FOG/error_stream_root/run*.

  > ./error_stream_root.sh N

Options:
  -h, --help      Show this help message
@EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) showHelpMsg=true; shift;;
    *) runNumber=$1; shift;;
  esac
done

# print help message
if [ ${showHelpMsg} == true ]; then
  helpMessage
  exit 0
fi

if ! [[ ${runNumber} =~ '^[0-9]+$' ]]; then
  printf "%s\n" "ERROR -- Command-line argument is not a valid number: ${runNumber} (specify -h or --help for more info)."
  exit 1 
fi

if [ -z "${CMSSW_BASE}" ]; then
  printf "%s\n" "ERROR -- Environment variable CMSSW_BASE not initialised."
  printf "%s\n" "         Please enable a recent CMSSW release before running this script."
  exit 1
fi

cfgFile=${BASH_SOURCE[0]/.sh/_cfg.py}

if [ ! -f "${cfgFile}" ]; then
  printf "%s\n" "ERROR -- Target configuration file does not exist: ${cfgFile}"
  printf "%s\n" "         This is unexpected. Please contact the FOG conveners."
  exit 1
fi

fileNamesRaw=($(ls /eos/cms/store/group/tsg/FOG/error_stream/*"${runNumber}"*/*raw 2> /dev/null))

rm -rf run000000

for fileNameRaw in "${fileNamesRaw[@]}"; do
  fileNameRoot=${fileNameRaw/error_stream/error_stream_root}
  fileNameRoot=${fileNameRoot/.raw/.root}
  [ ! -f "${fileNameRoot}" ] || continue
  mkdir -p $(dirname "${fileNameRoot}")
  cmsRun "${cfgFile}" "${fileNameRaw}" "${fileNameRoot}"
done
unset fileNameRaw fileNameRoot

rm -rf run000000
