#!/bin/bash

jsonFilePaths=(
  /eos/user/c/cmsdqm/www/CAF/certification/Collisions22/Cert_Collisions2022_355100_362760_Golden.json
  /eos/user/c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json
  /eos/user/c/cmsdqm/www/CAF/certification/Collisions24/Cert_Collisions2024_378981_381152_Golden.json
#  /eos/user/c/cmsdqm/www/CAF/certification/Collisions24/DCSOnly_JSONS/Collisions24_13p6TeV_eraC_379415_380238_DCSOnly_TkPx.json
)

source /cvmfs/cms-bril.cern.ch/cms-lumi-pog/brilws-docker/brilws-env
export PYTHONPATH="${HOME}"/.local/lib/python3.6/site-packages/:${PYTHONPATH}

for jsonFilePath in "${jsonFilePaths[@]}"; do
  echo "================================================="
  echo "${jsonFilePath}"
  echo "================================================="
  cp "${jsonFilePath}" .
  jsonFileBasename1=$(basename "${jsonFilePath}")
  brilcalc lumi -c web -u /fb --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json --without-checkjson -i "${jsonFileBasename1}"
  jsonFileBasename2=${jsonFileBasename1/.json/_TkDCSOn.json}
  brilcalc lumi -c web -u /fb --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json --without-checkjson -i "${jsonFileBasename2}"
done
