#!/bin/bash

hltLabel="${1}"

outFile="${hltLabel}".root

[ ! -f "${outFile}" ] || exit 1

ls "${hltLabel}"_run*.root > "${hltLabel}".txt
edmCopyPickMerge filePrepend=file: outputFile="${outFile}" inputFiles_load="${hltLabel}".txt
