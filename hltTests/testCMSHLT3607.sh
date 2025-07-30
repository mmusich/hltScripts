#!/bin/bash -e

merge_files() {
  hltLabel="${1}"
  outFile="${hltLabel}".root
  [ ! -f "${outFile}" ] || return
  ls "${hltLabel}"_run*.root > "${hltLabel}".txt
  edmCopyPickMerge filePrepend=file: outputFile="${outFile}" inputFiles_load="${hltLabel}".txt
  rm -f "${hltLabel}".txt
}

hltLabels=(
  hltc5eb61af_baseline
  hltc5eb61af_XcalRecHits
)

for hltLabel in "${hltLabels[@]}"; do

  merge_files "${hltLabel}"

done
unset hltLabel
