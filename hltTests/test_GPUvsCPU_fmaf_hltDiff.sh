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

diff_files 478cdcdaf03_AlpakaSerialSync 478cdcdaf03_AlpakaGPU
diff_files 478cdcdaf03_AlpakaSerialSync e40866a8667_AlpakaSerialSync
diff_files e40866a8667_AlpakaSerialSync e40866a8667_AlpakaGPU
