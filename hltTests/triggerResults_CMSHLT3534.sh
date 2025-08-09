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
  hltTestCMSHLT3534_250808_hlt1_mod
  hltTestCMSHLT3534_250808_hlt2_mod
  hltTestCMSHLT3534_250808_hlt3_mod
)

for hltLabel in "${hltLabels[@]}"; do

  merge_files "${hltLabel}"

done
unset hltLabel
