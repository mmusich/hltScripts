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
  hltTestCMSHLT3534_target_GTv6
)

for hltLabel in "${hltLabels[@]}"; do

  diff_files hltTestCMSHLT3534_baseline_GTv6 "${hltLabel}"

done
unset hltLabel
