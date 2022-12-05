#!/bin/bash -ex

# This script updates the file "${CMSSW_BASE}"/src/HLTrigger/Configuration/test/testAccessToEDMInputs_filelist.txt
# with the list of EDM files potentially used by HLT tests in the main release cycles of CMSSW (i.e. branches named CMSSW_\d_\d_X).

# path to directory hosting this script
TESTDIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)

# ensure that directory hosting this script corresponds to ${CMSSW_BASE}/src/HLTrigger/Configuration/test
if [ "${TESTDIR}" != "${CMSSW_BASE}"/src/HLTrigger/Configuration/test ]; then
  printf "\n%s\n" "ERROR -- the directory hosting testAccessToHLTTestInputs.sh [1] does not correspond to \${CMSSW_BASE}/src/HLTrigger/Configuration/test [2]"
  printf "%s\n"   "         [1] ${TESTDIR}"
  printf "%s\n\n" "         [2] ${CMSSW_BASE}/src/HLTrigger/Configuration/test"
  exit 1
fi

# files in CMSSW using EDM inputs for HLT tests
cmsswFiles=(
  HLTrigger/Configuration/test/cmsDriver.csh
  Configuration/HLT/python/addOnTestsHLT.py
  Utilities/ReleaseScripts/scripts/addOnTests.py
)

# list of CMSSW branches to be checked
# official-cmssw is the default name of the remote corresponding to the central CMSSW repository
cmsswBranches=$(git branch -a | grep 'remotes/official-cmssw/CMSSW_[0-9]*_[0-9]*_X$')
cmsswBranches+=("HEAD") # add HEAD to include updates committed locally

# path to output file
outputFile="${CMSSW_BASE}"/src/HLTrigger/Configuration/test/testAccessToEDMInputs_filelist.txt

# loop over CMSSW branches to be grep-d
for cmsswBranch in "${cmsswBranches[@]}"; do
  inputEDMFiles+=$(git grep -h --full-name "[='\" ]/store/.*.root" ${cmsswBranch[*]} -- ${cmsswFiles[*]} |
    sed 's|=/store/| /store/|g' | sed "s|'| |g" | sed 's|"| |g' | \
    awk '{ for(i=1;i<=NF;i++) if ($i ~ /\/store\/.*.root/) print $i }')
done; unset cmsswBranch

echo "${inputEDMFiles}" | sort -u > "${outputFile}"
