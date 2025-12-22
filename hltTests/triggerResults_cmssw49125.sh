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
  hlt251209_ref6ea595b1a76_pixDigMorph0_cpu
  hlt251209_ref6ea595b1a76_pixDigMorph0_gpu
  hlt251209_ref6ea595b1a76_pixDigMorph1_cpu
  hlt251209_ref6ea595b1a76_pixDigMorph1_gpu
  hlt251209_tar91e814d4912_pixDigMorph0_cpu
  hlt251209_tar91e814d4912_pixDigMorph0_gpu
  hlt251209_tar91e814d4912_pixDigMorph1_cpu
  hlt251209_tar91e814d4912_pixDigMorph1_gpu
)

for hltLabel in "${hltLabels[@]}"; do

  merge_files "${hltLabel}"

done
unset hltLabel
