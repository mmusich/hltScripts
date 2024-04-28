#!/bin/bash

# https://cmsdmops.docs.cern.ch/Users/Subscribe%20data/

datasets=(
#  /EphemeralHLTPhysics0/Run2023C-v1/RAW#698ffdd0-c383-4c12-b439-bdc72ebe0cdd
#  /EphemeralHLTPhysics1/Run2023C-v1/RAW#b0622783-8f45-4b27-b32f-65fea2002c60
  /EphemeralHLTPhysics2/Run2023C-v1/RAW#a62d1a3a-ca7b-4eca-bfeb-7eda24989f41
#  /EphemeralHLTPhysics3/Run2023C-v1/RAW#9da02aaf-cf46-4b71-8017-de8147ca7fc0
#  /EphemeralHLTPhysics4/Run2023C-v1/RAW#ca36d6b8-3eef-4848-8059-90b5c4c061a3
#  /EphemeralHLTPhysics5/Run2023C-v1/RAW#7218b852-cfec-472e-a62d-980f5fb5c8a2
#  /EphemeralHLTPhysics6/Run2023C-v1/RAW#b03e14a2-7699-443e-8264-9fab5e82594c
#  /EphemeralHLTPhysics7/Run2023C-v1/RAW#bf611e0b-6767-49f3-b4e3-1a70616aee9a
)

#    'rse_type=DISK&cms_type=real\tier=3\tier=0' \
#    --grouping 'ALL' \

# rucio list-rules --account $RUCIO_ACCOUNT | grep Run2023 | grep Epheme

export RUCIO_ACCOUNT="t2_ch_cern_local_users"

for dataset in "${datasets[@]}"; do
  rucio add-rule \
    cms:"${dataset}" \
    1 \
    T2_CH_CERN \
    --lifetime 1592000 \
    --activity "User AutoApprove" \
    --ask-approval \
    --comment "Trigger Studies Group (HLT)"
done
unset dataset
