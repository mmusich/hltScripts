#!/bin/bash -e

diff_files() {
  hltDiff -j -c \
    -o "${1}".root \
    -n "${2}".root \
    -F "${3}" \
     > "${3}".txt
}

diff_files hltTestCMSHLT3534_250808_hlt1_mod hltTestCMSHLT3534_250808_hlt3_mod hltTestCMSHLT3534_250808_hlt1_vs_hlt3
diff_files hltTestCMSHLT3534_250808_hlt2_mod hltTestCMSHLT3534_250808_hlt3_mod hltTestCMSHLT3534_250808_hlt2_vs_hlt3
