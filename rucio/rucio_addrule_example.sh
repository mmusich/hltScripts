#!/bin/bash

# https://cmsdmops.docs.cern.ch/Users/Subscribe%20data/

datasets=(
#  /EphemeralHLTPhysics0/Run2023C-v1/RAW#698ffdd0-c383-4c12-b439-bdc72ebe0cdd
#  /EphemeralHLTPhysics1/Run2023C-v1/RAW#b0622783-8f45-4b27-b32f-65fea2002c60
#  /EphemeralHLTPhysics2/Run2023C-v1/RAW#a62d1a3a-ca7b-4eca-bfeb-7eda24989f41
#  /EphemeralHLTPhysics3/Run2023C-v1/RAW#9da02aaf-cf46-4b71-8017-de8147ca7fc0
#  /EphemeralHLTPhysics4/Run2023C-v1/RAW#ca36d6b8-3eef-4848-8059-90b5c4c061a3
#  /EphemeralHLTPhysics5/Run2023C-v1/RAW#7218b852-cfec-472e-a62d-980f5fb5c8a2
#  /EphemeralHLTPhysics6/Run2023C-v1/RAW#b03e14a2-7699-443e-8264-9fab5e82594c
#  /EphemeralHLTPhysics7/Run2023C-v1/RAW#bf611e0b-6767-49f3-b4e3-1a70616aee9a

# /store/data/Run2024D/EphemeralHLTPhysics0/RAW/v1/000/380/647/00000/273a88ce-097e-4cb7-9e27-f22772a70010.root
# /store/data/Run2024D/EphemeralHLTPhysics1/RAW/v1/000/380/647/00000/5f622fbb-55ea-4d5b-ab19-6f99a5301ded.root
# /store/data/Run2024D/EphemeralHLTPhysics2/RAW/v1/000/380/647/00000/6d9b89cd-2318-488a-ba70-b5f07a1c9cb6.root
# /store/data/Run2024D/EphemeralHLTPhysics3/RAW/v1/000/380/647/00000/eb0d2b80-b588-4cba-9512-9cf49da11c22.root
# /store/data/Run2024D/EphemeralHLTPhysics4/RAW/v1/000/380/647/00000/fafb42a9-3ac7-4690-bcba-af12028b3d95.root
# /store/data/Run2024D/EphemeralHLTPhysics5/RAW/v1/000/380/647/00000/5e66c7cd-e9f8-4f5c-825a-8264e24859a7.root
# /store/data/Run2024D/EphemeralHLTPhysics6/RAW/v1/000/380/647/00000/cbbfb353-738c-4200-a1fa-49d08ac6e875.root
# /store/data/Run2024D/EphemeralHLTPhysics7/RAW/v1/000/380/647/00000/d93e0e4f-263f-458a-81ed-51f90c3e0d7e.root
# /store/data/Run2024D/EphemeralHLTPhysics0/RAW/v1/000/380/647/00000/273a88ce-097e-4cb7-9e27-f22772a70010.root
# /store/data/Run2024D/EphemeralHLTPhysics1/RAW/v1/000/380/647/00000/5f622fbb-55ea-4d5b-ab19-6f99a5301ded.root
# /store/data/Run2024D/EphemeralHLTPhysics2/RAW/v1/000/380/647/00000/6d9b89cd-2318-488a-ba70-b5f07a1c9cb6.root
# /store/data/Run2024D/EphemeralHLTPhysics3/RAW/v1/000/380/647/00000/eb0d2b80-b588-4cba-9512-9cf49da11c22.root
# /store/data/Run2024D/EphemeralHLTPhysics4/RAW/v1/000/380/647/00000/fafb42a9-3ac7-4690-bcba-af12028b3d95.root
# /store/data/Run2024D/EphemeralHLTPhysics5/RAW/v1/000/380/647/00000/5e66c7cd-e9f8-4f5c-825a-8264e24859a7.root
# /store/data/Run2024D/EphemeralHLTPhysics6/RAW/v1/000/380/647/00000/cbbfb353-738c-4200-a1fa-49d08ac6e875.root
# /store/data/Run2024D/EphemeralHLTPhysics7/RAW/v1/000/380/647/00000/d93e0e4f-263f-458a-81ed-51f90c3e0d7e.root
# /store/data/Run2024D/EphemeralHLTPhysics0/RAW/v1/000/380/647/00000/b83d2da3-8f07-4c2c-9fdf-9f86461c1271.root
# /store/data/Run2024D/EphemeralHLTPhysics1/RAW/v1/000/380/647/00000/391596c3-d86e-4b5c-bc0d-587bc4a328b6.root
# /store/data/Run2024D/EphemeralHLTPhysics2/RAW/v1/000/380/647/00000/32e528ba-c6d9-4469-93b0-89f357c83846.root
# /store/data/Run2024D/EphemeralHLTPhysics3/RAW/v1/000/380/647/00000/e6fc96d2-4b3b-4a18-9cee-530aebbb3261.root
# /store/data/Run2024D/EphemeralHLTPhysics4/RAW/v1/000/380/647/00000/9936fde6-2eef-4a06-9484-6f2f8305106a.root
# /store/data/Run2024D/EphemeralHLTPhysics5/RAW/v1/000/380/647/00000/ff576c03-27c7-4ab9-85bb-f0a04df7a23b.root
# /store/data/Run2024D/EphemeralHLTPhysics6/RAW/v1/000/380/647/00000/b7d8d958-9a75-49fd-be6b-613653be07d7.root
# /store/data/Run2024D/EphemeralHLTPhysics7/RAW/v1/000/380/647/00000/5bd9819a-f38b-4129-b598-035aa2dd8d3e.root
# /store/data/Run2024D/EphemeralHLTPhysics0/RAW/v1/000/380/647/00000/b83d2da3-8f07-4c2c-9fdf-9f86461c1271.root
# /store/data/Run2024D/EphemeralHLTPhysics1/RAW/v1/000/380/647/00000/391596c3-d86e-4b5c-bc0d-587bc4a328b6.root
# /store/data/Run2024D/EphemeralHLTPhysics2/RAW/v1/000/380/647/00000/32e528ba-c6d9-4469-93b0-89f357c83846.root
# /store/data/Run2024D/EphemeralHLTPhysics3/RAW/v1/000/380/647/00000/e6fc96d2-4b3b-4a18-9cee-530aebbb3261.root
# /store/data/Run2024D/EphemeralHLTPhysics4/RAW/v1/000/380/647/00000/9936fde6-2eef-4a06-9484-6f2f8305106a.root
# /store/data/Run2024D/EphemeralHLTPhysics5/RAW/v1/000/380/647/00000/ff576c03-27c7-4ab9-85bb-f0a04df7a23b.root
# /store/data/Run2024D/EphemeralHLTPhysics6/RAW/v1/000/380/647/00000/b7d8d958-9a75-49fd-be6b-613653be07d7.root
# /store/data/Run2024D/EphemeralHLTPhysics7/RAW/v1/000/380/647/00000/5bd9819a-f38b-4129-b598-035aa2dd8d3e.root

# /store/data/Run2024A/Cosmics/RAW/v1/000/378/483/00000/e51ad2ec-686a-4246-b879-0ff3add6bc29.root

 /store/data/Run2024E/ParkingSingleMuon4/RAW/v1/000/381/443/00000/95d48fcb-0633-415c-a5cf-f2caeebab628.root
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
    --lifetime 15552000 \
    --activity "User AutoApprove" \
    --ask-approval \
    --comment "Trigger Studies Group (HLT)"
done
unset dataset
