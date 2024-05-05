#!/bin/bash

hltGetConfiguration /dev/CMSSW_14_0_0/GRun \
   --globaltag 140X_dataRun3_HLT_JEC_2024_v1 \
   --data \
   --unprescale \
   --output full \
   --max-events 300 \
   --eras Run3 --l1-emulator uGT --l1 L1Menu_Collisions2024_v1_2_0_xml \
   --input file:/eos/cms/tier0/store/data/Run2024D/EphemeralHLTPhysics0/RAW/v1/000/380/346/00000/898b6217-0c2f-4cd8-9af3-14f255b3efb1.root \
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
process.GlobalTag.globaltag = '140X_dataRun3_HLT_HCALRespCorr_2024_v1'
EOF
cmsRun hlt1.py &> hlt1.log
mv output.root hlt1.root
