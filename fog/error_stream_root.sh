#!/bin/bash

[ ! -z "${CMSSW_BASE}" ] || exit 1

cfgFile=${BASH_SOURCE[0]/.sh/_cfg.py}
[ -f "${cfgFile}" ] || exit 1

[ $# -eq 1 ] || exit 1
fileNamesRaw=($(ls /eos/cms/store/group/tsg/FOG/error_stream/*"${1}"*/*raw 2> /dev/null))

for fileNameRaw in "${fileNamesRaw[@]}"; do
  fileNameRoot=${fileNameRaw/error_stream/error_stream_root}
  fileNameRoot=${fileNameRoot/.raw/.root}
  [ ! -f "${fileNameRoot}" ] || continue
  mkdir -p $(dirname "${fileNameRoot}")
  cmsRun "${cfgFile}" "${fileNameRaw}" "${fileNameRoot}"
done
unset fileNameRaw fileNameRoot
