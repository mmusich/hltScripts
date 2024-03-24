#!/bin/bash

[ $# -eq 1 ] || exit 1

block="cms:${1}"
shift

source /cvmfs/cms.cern.ch/cmsset_default.sh
source /cvmfs/cms.cern.ch/rucio/setup-py3.sh
export RUCIO_ACCOUNT="t2_ch_cern_local_users"

[ -f "${X509_USER_PROXY}" ] || voms-proxy-init -voms cms -rfc -valid 192:00

account="${RUCIO_ACCOUNT}"
lifetime=$((86400 * 150)) # Lifetime in seconds. Multiplication factor is days. 
comment="Studies of Trigger Studies Group (HLT)"
#block="cms:/store/data/Run2022A/MinimumBias0/RAW/v1/000/352/568/00000/d4dcc6b1-0c5d-4b89-a117-d82fbceec7d1.root" # file name
#block="cms:/MinimumBias0/Run2022A-v1/RAW#fc8a2c55-b525-4052-b234-dcf48b9ec0f7" # block name
copies=1
rse_expression="T2_CH_CERN"

echo "Are you sure you want to create the following rule?"
echo "====="
echo "Account: $account"
echo "Comment: $comment"
echo "RSE: $rse_expression"
echo "Block: $block"
echo "Copies $copies"
echo "Lifetime: $lifetime seconds ($(expr $lifetime / 86400) days)"
echo "====="

select yn in "Yes" "No"; do
  case $yn in
    Yes ) rucio add-rule --account $account --lifetime $lifetime --comment "$comment" $block $copies $rse_expression ; break;;
    No ) echo "Aborting"; break;;
  esac
done
