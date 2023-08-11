#!/bin/bash

hltGetConfiguration /dev/CMSSW_13_0_0/GRun/V150 \
  --globaltag 126X_mcRun3_2023_forPU65_v5 \
  --mc \
  --no-prescale \
  --output minimal \
  --max-events 100 \
  --input /store/mc/Run3Winter23Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/GTv4BTagDigi_126X_mcRun3_2023_forPU65_forBTag_v1_ext2-v2/60000/ae2ab9cc-64d7-40ff-a73f-bae4a7a17cf4.root \
  --eras Run3 --l1-emulator FullMC --l1 L1Menu_Collisions2023_v1_3_0_xml \
  > hlt0.py
edmConfigDump hlt0.py > hlt0_dump.py
cmsRun hlt0.py &> hlt0.log
mv output.root hlt0.root
grep 'TrigReport     1' hlt0.log | grep '0 HLT_' > hlt0_res.txt

hltGetConfiguration /dev/CMSSW_13_0_0/GRun/V150 \
  --globaltag 126X_mcRun3_2023_forPU65_v5 \
  --mc \
  --no-prescale \
  --output minimal \
  --max-events 100 \
  --input /store/mc/Run3Winter23Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/GTv4BTagDigi_126X_mcRun3_2023_forPU65_forBTag_v1_ext2-v2/60000/ae2ab9cc-64d7-40ff-a73f-bae4a7a17cf4.root \
  --eras Run3 --l1-emulator FullMC --l1 L1Menu_Collisions2023_v1_3_0_xml \
  --customise HLTrigger/Configuration/customizeHLTforCMSSW.customizeHLTfor41632 \
  > hlt1.py
edmConfigDump hlt1.py > hlt1_dump.py
cmsRun hlt1.py &> hlt1.log
mv output.root hlt1.root
grep 'TrigReport     1' hlt1.log | grep '0 HLT_' > hlt1_res.txt
