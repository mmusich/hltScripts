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

#/EphemeralHLTPhysics1/Run2024D-v1/RAW#7c0c2110-10a3-46f4-ad0d-3705acce70e0
#/EphemeralHLTPhysics1/Run2024D-v1/RAW#9e2b1a27-c4f9-433a-b4cd-f5e778a7c006

#/store/data/Run2024B/SpecialZeroBias0/RAW/v1/000/379/060/00000/5a0ee560-07e6-482e-bc67-89ca1ac8f73e.root

#/store/data/Run2024D/AlCaLumiPixelsCountsPrompt1/RAW/v1/000/380/895/00000/c27ff3c5-8ad9-4cf2-b359-2abfd7bc1b1d.root

  /store/data/Run2024C/Muon0/RAW/v1/000/379/765/00000/fc8626a1-85be-4edb-84ca-00b557c6cd89.root
  /store/data/Run2024C/Muon1/RAW/v1/000/379/765/00000/1e95c5c9-e255-4a36-998f-2faa1d17a121.root

  /store/data/Run2024C/Muon0/RAW/v1/000/379/866/00000/1c4e1376-70da-48df-977b-f0deb5832234.root
  /store/data/Run2024C/Muon1/RAW/v1/000/379/866/00000/67294cf3-6b00-43be-be30-fe42fe220d51.root

  /store/data/Run2024D/Muon0/RAW/v1/000/380/564/00000/ea4b77cc-356b-4b3d-be4d-97e1f8ebf4df.root
  /store/data/Run2024D/Muon1/RAW/v1/000/380/564/00000/d6a57896-0d75-4c16-856c-26fc2830b08a.root

  /store/data/Run2024E/Muon0/RAW/v1/000/380/963/00000/5aab2247-647d-45dc-9cc9-a3c6adbbd118.root
  /store/data/Run2024E/Muon1/RAW/v1/000/380/963/00000/d80703ca-b2b0-4904-aa8b-9cd465b28f6c.root

  /store/data/Run2024E/Muon0/RAW/v1/000/381/544/00000/84243c08-3bd6-49ef-b218-b94623fe2979.root
  /store/data/Run2024E/Muon1/RAW/v1/000/381/544/00000/2df26581-4caf-48a3-9eaf-cb0d42c2a86a.root

  /store/data/Run2024F/Muon0/RAW/v1/000/382/792/00000/0e4a830e-a8c2-400c-8b64-bedd7ee04f65.root
  /store/data/Run2024F/Muon1/RAW/v1/000/382/792/00000/dccc863b-df0c-4009-8b8d-51ef3b8ec09d.root

  /store/data/Run2024F/Muon0/RAW/v1/000/383/155/00000/7a4dd504-f4ba-45b0-8a0f-d4c4e6f12448.root
  /store/data/Run2024F/Muon1/RAW/v1/000/383/155/00000/1dbd637a-5b57-4a24-bf44-a0adf839c80c.root

  /store/data/Run2024F/Muon0/RAW/v1/000/383/162/00001/8daa533d-3007-494e-a080-c31be27b4c3b.root
  /store/data/Run2024F/Muon1/RAW/v1/000/383/162/00001/579c28a6-02fb-4357-b8c5-51137bba805c.root

  /store/data/Run2024F/Muon0/RAW/v1/000/383/537/00000/90bd9b6c-2af5-4934-b273-93a8fe755fea.root
  /store/data/Run2024F/Muon1/RAW/v1/000/383/537/00000/d641ce6e-bb6e-4d10-8ad5-9487a3c8d8c6.root

  /store/data/Run2024F/Muon0/RAW/v1/000/383/629/00000/4dea9467-b3a9-4988-98a9-d1e6be0c51ce.root
  /store/data/Run2024F/Muon1/RAW/v1/000/383/629/00000/6d2a1a50-5693-47fb-81f5-6befc075f413.root

  /store/data/Run2024G/Muon0/RAW/v1/000/384/202/00001/c9cfab1a-b5b3-4d7f-b3ce-b8de61d1ba77.root
  /store/data/Run2024G/Muon1/RAW/v1/000/384/202/00001/95a2b675-3d34-4744-b0e3-de3c8ae5fac8.root

  /store/data/Run2024G/Muon0/RAW/v1/000/384/265/00000/39f20f93-5309-477b-ad00-3769a170554e.root
  /store/data/Run2024G/Muon1/RAW/v1/000/384/265/00000/b16f2483-7190-4407-ba1b-5524a2dd69e5.root

  /store/data/Run2024G/Muon0/RAW/v1/000/385/168/00001/3532ba78-ae10-4908-ac27-041546809f01.root
  /store/data/Run2024G/Muon1/RAW/v1/000/385/168/00001/8fc7770f-1ac5-4894-b3ed-45f766f73c10.root

  /store/data/Run2024G/Muon0/RAW/v1/000/385/415/00000/45cba3b3-9e18-434f-a825-900e1180459c.root
  /store/data/Run2024G/Muon1/RAW/v1/000/385/415/00000/67bef556-0463-4d3b-8624-5c1736680b33.root

  /store/data/Run2024G/Muon0/RAW/v1/000/385/437/00000/5f15f315-07b0-4e23-9118-fabb136f9504.root
  /store/data/Run2024G/Muon1/RAW/v1/000/385/437/00000/21ff7e0c-563a-4753-b723-94a8ef954c2a.root

  /store/data/Run2024G/Muon0/RAW/v1/000/385/515/00000/0fdb5c99-9e56-462d-97fd-6908d136ac26.root
  /store/data/Run2024G/Muon1/RAW/v1/000/385/515/00000/3c1250ad-cb11-4168-a138-79fb64d00f87.root

  /store/data/Run2024G/Muon0/RAW/v1/000/385/620/00000/7ffb64b4-f134-41f2-a327-a90611abf651.root
  /store/data/Run2024G/Muon1/RAW/v1/000/385/620/00000/1994b11f-a358-4962-a495-532541ebb71e.root

  /store/data/Run2024G/Muon0/RAW/v1/000/385/713/00000/cd0ce192-f5e2-48bc-aa3b-c352672c1974.root
  /store/data/Run2024G/Muon1/RAW/v1/000/385/713/00000/9e56672f-7621-4045-8e49-2f98fac5ae55.root

  /store/data/Run2024G/Muon0/RAW/v1/000/385/764/00001/32d08ae1-f841-4d3d-98eb-d6c90bae1899.root
  /store/data/Run2024G/Muon1/RAW/v1/000/385/764/00001/96ce8ebd-63ed-4c0c-a132-b302e7fd9f3d.root

  /store/data/Run2024H/Muon0/RAW/v1/000/386/025/00000/36880fb9-e361-416a-bf01-41bd93cca7d3.root
  /store/data/Run2024H/Muon1/RAW/v1/000/386/025/00000/b086d54f-84ed-43cb-adb7-65265ab182ed.root

)

# rucio list-rules --account $RUCIO_ACCOUNT | grep Run2024 | grep Epheme

for dataset in "${datasets[@]}"; do

  rucio add-rule \
    cms:"${dataset}" \
    1 \
    'rse_type=DISK&cms_type=real\tier=3\tier=0' \
    --grouping 'ALL' \
    --lifetime 1592000 \
    --ask-approval \
    --activity "User AutoApprove" \
    --comment "Trigger Studies Group (HLT)"

#  rucio add-rule \
#    cms:"${dataset}" \
#    1 \
#    T2_CH_CERN \
#    --lifetime 400000 \
#    --ask-approval \
#    --activity "User AutoApprove" \
#    --comment "Trigger Studies Group (TSG, HLT)"

done
unset dataset
