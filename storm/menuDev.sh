#!/bin/bash -e

stormCherryPick(){
  git fetch --all
  git branch -D tmp
  git checkout -b tmp
  git branch -D "${branch}"
  git checkout -b "${branch}" "${CMSSW_VERSION}"
  git cherry-pick "${hash}" --no-commit
  git commit -m "${cimsg}"
  git push cms-tsg-storm "${branch}" -f
}

branch=$(git rev-parse --abbrev-ref HEAD)

# git checkout -b HLTdevelopment126X_for130X && git commit -m 'HLT menu development for 12_6_X (branch: 13_0_X)' --allow-empty
# git checkout -b HLTdevelopment126X && git commit -m 'HLT menu development for 12_6_X' --allow-empty

if [ "${branch}" = HLTdevelopment126X_for130X ]; then
  sshkey_enable
  cimsg='HLT menu development for 12_6_X (branch: 13_0_X)'
  cd "${CMSSW_BASE}"/src/HLTrigger/Configuration/tables
  echo cms100kHz | ./makeSubTables
  cd "${CMSSW_BASE}"/src/HLTrigger/Configuration/test
  ./getHLT.sh
  git add -u :/
  git commit --amend --reset-author -m "${cimsg}"
  git push cms-tsg-storm "${branch}" -f
  cd "${CMSSW_BASE}"/src

elif [ "${branch}" = HLTdevelopment126X ]; then
  sshkey_enable
  cimsg='HLT menu development for 12_6_X'
  hash=$1
  cd "${CMSSW_BASE}"/src
  stormCherryPick
  cd "${CMSSW_BASE}"/src
fi
