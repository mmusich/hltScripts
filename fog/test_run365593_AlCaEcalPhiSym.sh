#!/bin/bash

# hlt1: reproduce 365593
hltGetConfiguration run:365593 --globaltag 130X_dataRun3_HLT_v2 \
 --no-output --no-prescale --max-events 2200 --paths AlCa_EcalPhiSym_v* \
 --input file:/eos/cms/store/t0streamer/Data/PhysicsZeroBias0/000/365/593/run365593_ls0035_streamPhysicsZeroBias0_StorageManager.dat \
 > hlt1.py

cat <<@EOF >> hlt1.py
process.source = cms.Source("NewEventStreamFileReader",
  fileNames = cms.untracked.vstring(process.source.fileNames)
)
@EOF
cmsRun hlt1.py &> hlt1.log
echo "input data: run365593 | ECAL pedestals: those used in 365593"
echo "                           Input     Accepted    Rejected"
grep '0 AlCa_EcalPhiSym_v11' hlt1.log | head -1
echo "---"

# hlt2: rerun on 365593 with ECAL pedestals used in 365568
cp hlt1.py hlt2.py
cat <<@EOF >> hlt2.py
process.GlobalTag.globaltag = '130X_dataRun3_HLT_Candidate_2023_04_03_20_00_07'
@EOF
cmsRun hlt2.py &> hlt2.log
echo "input data: run365593 | ECAL pedestals: those used in 365568"
echo "                           Input     Accepted    Rejected"
grep '0 AlCa_EcalPhiSym_v11' hlt2.log | head -1
