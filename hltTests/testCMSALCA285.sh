#!/bin/bash

hltGetConfiguration /dev/CMSSW_14_0_0/GRun \
  --globaltag 140X_dataRun3_HLT_v3 \
  --data \
  --unprescale \
  --output full \
  --max-events 300 \
  --eras Run3 --l1-emulator uGT --l1 L1Menu_Collisions2024_v1_2_0_xml \
  --input file:/eos/cms/store/data/Run2024E/EphemeralHLTPhysics0/RAW/v1/000/381/150/00000/8ee26707-07a7-4bd4-ba09-595a5169ea9b.root \
  > hlt0.py
cat <<EOF >> hlt0.py
process.hltOutputFull.outputCommands = [
    'drop *',
    'keep *_hlt*Jet*_*_*',
    'keep *_hlt*Fixed*_*_*',
    'drop *_hltHbherecoLegacy_*_*',
    'drop *_hlt*Pixel*SoA*_*_*',
]
EOF
cmsRun hlt0.py &> hlt0.log
mv output.root hlt0.root

cp hlt0.py hlt1.py
cat <<EOF >> hlt1.py
process.GlobalTag.globaltag = '140X_dataRun3_HLT_HCALRespCorrs_w23_v1'
EOF
cmsRun hlt1.py &> hlt1.log
mv output.root hlt1.root
