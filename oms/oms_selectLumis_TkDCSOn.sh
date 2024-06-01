#!/bin/bash

jsonFilePaths=(
  /eos/user/c/cmsdqm/www/CAF/certification/Collisions22/Cert_Collisions2022_355100_362760_Golden.json
  /eos/user/c/cmsdqm/www/CAF/certification/Collisions23/Cert_Collisions2023_366442_370790_Golden.json
  /eos/user/c/cmsdqm/www/CAF/certification/Collisions24/Cert_Collisions2024_378981_380649_Golden.json
#  /eos/user/c/cmsdqm/www/CAF/certification/Collisions24/DCSOnly_JSONS/Collisions24_13p6TeV_eraC_379415_380238_DCSOnly_TkPx.json
)

pyScript=./${BASH_SOURCE[0]/.sh/.py}
[ -f "${pyScript}" ] || exit 1

for jsonFilePath in "${jsonFilePaths[@]}"; do
  echo "================================================="
  echo "${jsonFilePath}"
  echo "================================================="
  jsonFileBasename=$(basename "${jsonFilePath}")
  outputFilePath=${jsonFileBasename/.json/_TkDCSOn.json}
  ${pyScript} -i "${jsonFilePath}" -o "${outputFilePath}"
done
