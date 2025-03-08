#!/bin/bash

# https://cmsdmops.docs.cern.ch/Users/Subscribe%20data/

datasets=(
#  /EphemeralHLTPhysics0/Run2024I-v1/RAW#4912efee-48ec-4a81-841d-bca1d9427c3d
#  /EphemeralHLTPhysics1/Run2024I-v1/RAW#b857a277-4467-4360-bbf5-94bf640c194e
#  /EphemeralHLTPhysics2/Run2024I-v1/RAW#f0a4aa04-15d4-49e9-bbd6-d65d65ba2375
#  /EphemeralHLTPhysics3/Run2024I-v1/RAW#f69cae67-6b54-4361-9dd9-83eae35ba929
#  /EphemeralHLTPhysics4/Run2024I-v1/RAW#a654fd78-0711-4be1-bf5e-53db59a3f8e6
#  /EphemeralHLTPhysics5/Run2024I-v1/RAW#e4a0494d-c4ec-4562-b0cf-b824b373a25a
#  /EphemeralHLTPhysics6/Run2024I-v1/RAW#bccb2fd8-8a2c-45f3-ae2a-d9fe92920052
#  /EphemeralHLTPhysics7/Run2024I-v1/RAW#b538dc10-6715-4e81-92a0-9d1817e5b5c2
)

# rucio list-rules --account $RUCIO_ACCOUNT | grep Run2024 | grep Epheme

export RUCIO_ACCOUNT="t2_ch_cern_local_users"

for dataset in "${datasets[@]}"; do

#  rucio add-rule \
#    cms:"${dataset}" \
#    1 \
#    'rse_type=DISK&cms_type=real\tier=3\tier=0' \
#    --grouping 'ALL' \
#    --lifetime 12960000 \
#    --ask-approval \
#    --activity "User AutoApprove" \
#    --comment "Trigger Studies Group (HLT)"

#  rucio add-rule \
#    cms:"${dataset}" \
#    1 \
#    T2_CH_CERN \
#    --lifetime 12960000 \
#    --ask-approval \
#    --activity "User AutoApprove" \
#    --comment "Trigger Studies Group (HLT)"

done
unset dataset
