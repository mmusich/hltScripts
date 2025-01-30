#!/bin/bash -e

diff_files() {
  hltOldTag=$1
  hltNewTag=$2
  hltDiff -j -c \
    -o hlt_"${hltOldTag}".root \
    -n hlt_"${hltNewTag}".root \
    -F hlt_"${hltOldTag}"_vs_"${hltNewTag}" \
     > hlt_"${hltOldTag}"_vs_"${hltNewTag}".txt
}

hltLabels=(
#  ecalPFRH_TL235
  ecalPFRH_TL470_2025moy_x1p0
  ecalPFRH_TL550_2025eoy_x1p0
  ecalPFRH_TL550_2025eoy_x0p6
  ecalPFRH_TL550_2025eoy_x0p4
  ecalPFRH_TL550_2025eoy_x0p2
)

for hltLabel in "${hltLabels[@]}"; do

  diff_files ecalPFRH_TL235 "${hltLabel}"

done
unset hltLabel
