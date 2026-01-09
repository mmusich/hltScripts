#!/bin/bash -e

diff_files() {
  hltDiff -j -c \
    -o "${1}".root \
    -n "${2}".root \
    -F "${3}" \
     > "${3}".txt
}

diff_files hlt251209_ref6ea595b1a76_pixDigMorph0_cpu hlt251209_tar91e814d4912_pixDigMorph0_cpu hlt251209_ref6ea595b1a76_vs_tar91e814d4912_pixDigMorph0_cpu
diff_files hlt251209_ref6ea595b1a76_pixDigMorph0_gpu hlt251209_tar91e814d4912_pixDigMorph0_gpu hlt251209_ref6ea595b1a76_vs_tar91e814d4912_pixDigMorph0_gpu
diff_files hlt251209_ref6ea595b1a76_pixDigMorph1_cpu hlt251209_tar91e814d4912_pixDigMorph1_cpu hlt251209_ref6ea595b1a76_vs_tar91e814d4912_pixDigMorph1_cpu
diff_files hlt251209_ref6ea595b1a76_pixDigMorph1_gpu hlt251209_tar91e814d4912_pixDigMorph1_gpu hlt251209_ref6ea595b1a76_vs_tar91e814d4912_pixDigMorph1_gpu
