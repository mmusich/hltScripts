#!/bin/bash -e

merge_files() {
  hltLabel="${1}"
  outFile="${hltLabel}".root
  [ ! -f "${outFile}" ] || exit 1
  ls "${hltLabel}"_run*.root > "${hltLabel}".txt
  edmCopyPickMerge filePrepend=file: outputFile="${outFile}" inputFiles_load="${hltLabel}".txt
  rm -f "${hltLabel}".txt
}

hltLabels=(
  hlt_ecalPFRH_TL235
  hlt_ecalPFRH_TL470_2025moy_x1p0
  hlt_ecalPFRH_TL550_2025eoy_x1p0
  hlt_ecalPFRH_TL550_2025eoy_x0p6
  hlt_ecalPFRH_TL550_2025eoy_x0p4
  hlt_ecalPFRH_TL550_2025eoy_x0p2
)

for hltLabel in "${hltLabels[@]}"; do

  merge_files "${hltLabel}"

done
unset hltLabel
