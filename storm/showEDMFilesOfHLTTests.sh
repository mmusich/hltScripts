#!/bin/bash -e

cmsswBranches=(
  official-cmssw/CMSSW_5_3_X
  official-cmssw/CMSSW_8_0_X
  official-cmssw/CMSSW_9_4_X
  official-cmssw/CMSSW_10_2_X
  official-cmssw/CMSSW_10_3_X
  official-cmssw/CMSSW_10_6_X
  official-cmssw/CMSSW_11_0_X
  official-cmssw/CMSSW_11_1_X
  official-cmssw/CMSSW_11_2_X
  official-cmssw/CMSSW_11_3_X
  official-cmssw/CMSSW_12_0_X
  official-cmssw/CMSSW_12_1_X
  official-cmssw/CMSSW_12_4_X
  official-cmssw/CMSSW_12_5_X
  official-cmssw/CMSSW_12_6_X
  official-cmssw/CMSSW_13_0_X
)

cmsswFiles=(
  HLTrigger/Configuration/test/cmsDriver.csh
  Configuration/HLT/python/addOnTestsHLT.py
  Utilities/ReleaseScripts/scripts/addOnTests.py
)

cd "${CMSSW_BASE}"/src
rm -f .tmp.txt

for cmsswBranch in "${cmsswBranches[@]}"; do
  for cmsswFile in "${cmsswFiles[@]}"; do
    git grep -h '[= ]/store/.*.root' "${cmsswBranch}" -- "${cmsswFile}" |
     sed 's|=/store/| /store/|g' | sed "s|'| |g" | sed 's|"| |g' | \
     awk '{ for(i=1;i<=NF;i++) if ($i ~ /\/store\/.*.root/) print $i }' >> .tmp.txt
  done
  unset cmsswFile
done
unset cmsswBranch

cat .tmp.txt | sort -u
rm -f .tmp.txt
