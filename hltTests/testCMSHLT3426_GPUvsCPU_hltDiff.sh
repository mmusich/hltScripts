#!/bin/bash -e

diff_files() {
  hltOldTag=$1
  hltNewTag=$2
  hltDiff -j -c \
    -o hlt"${hltOldTag}".root \
    -n hlt"${hltNewTag}".root \
    -F hlt_"${hltOldTag}"_vs_"${hltNewTag}" \
     > hlt_"${hltOldTag}"_vs_"${hltNewTag}".txt
}

diff_files 1500p2_try0 1500p2_try1
diff_files 1500p3_try0 1500p3_try1
diff_files 1500p2_try0 1500p3_try0
