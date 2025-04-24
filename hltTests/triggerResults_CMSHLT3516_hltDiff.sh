#!/bin/bash -e

diff_files() {
  hltOldTag=$1
  hltNewTag=$2
  hltDiff -j -c \
    -o "${hltOldTag}".root \
    -n "${hltNewTag}".root \
    -F "${hltOldTag}"_vs_"${hltNewTag}" \
     > "${hltOldTag}"_vs_"${hltNewTag}".txt
}

hltLabels=(
  hltTestCMSHLT3516_JECs2025v2
)

for hltLabel in "${hltLabels[@]}"; do

  diff_files hltTestCMSHLT3516_JECs2025v1 "${hltLabel}"

done
unset hltLabel
