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

# git checkout -b HLTdevelopment130X_for131X && git commit -m 'HLT menu development for 13_0_X (branch: 13_1_X)' --allow-empty
# git checkout -b HLTdevelopment130X && git commit -m 'HLT menu development for 13_0_X' --allow-empty

if [ "${branch}" = HLTdevelopment130X_for131X ]; then
  sshkey_enable
  cimsg='HLT menu development for 13_0_X (branch: 13_1_X)'
  cd "${CMSSW_BASE}"/src/HLTrigger/Configuration/tables
  echo cms100kHz | ./makeSubTables
  cd "${CMSSW_BASE}"/src/HLTrigger/Configuration/test
  ./getHLT.sh
  git add -u :/
  git commit --amend --reset-author -m "${cimsg}"
  git push cms-tsg-storm "${branch}" -f
  cd "${CMSSW_BASE}"/src

elif [ "${branch}" = HLTdevelopment130X ]; then
  [ $# -eq 1 ] || return 1
  sshkey_enable
  cimsg='HLT menu development for 13_0_X'
  hash=$1
  cd "${CMSSW_BASE}"/src
  stormCherryPick
  cd "${CMSSW_BASE}"/src
fi
