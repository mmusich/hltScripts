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
  hltTestCMSHLT3529_target_JECs2025v2
)

for hltLabel in "${hltLabels[@]}"; do

  diff_files hltTestCMSHLT3529_baseline_JECs2025v2 "${hltLabel}"

done
unset hltLabel
