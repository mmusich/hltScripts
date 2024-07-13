#!/bin/bash -e

hltGetConfiguration run:381147 \
  --globaltag 140X_dataRun3_HLT_v3 \
  --no-prescale \
  --output minimal \
  --max-events 1 \
  --paths HLT_CDC_L2cosmic_10_er1p0_v* \
  --input root://eoscms.cern.ch//eos/cms/store/group/tsg/FOG/error_stream_root/run381147/run381147_ls0202_index000187_fu-c2b05-29-01_pid2159904.root \
  > hlt0.py

cat <<@EOF >> hlt0.py
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0

process.source.skipEvents = cms.untracked.uint32( 56 )

del process.MessageLogger
process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.hltOutputMinimal.outputCommands += [
  'keep *_hltL1sCDC_*_*',
  'keep *_hltL1fL1sCDCL1Filtered0_*_*',
  'keep *_hltL2fL1sCDCL2CosmicMuL2Filtered3er2stations5p5er1p0_*_*',
]
@EOF
cmsRun hlt0.py &> hlt0.log
mv output.root hlt0.root

cp hlt0.py hlt1.py
cat <<@EOF >> hlt1.py

process.hltL1fL1sCDCL1Filtered0.CentralBxOnly = True
@EOF
cmsRun hlt1.py &> hlt1.log
mv output.root hlt1.root

cp hlt0.py hlt2.py
cat <<@EOF >> hlt2.py

process.hltGtStage2ObjectMap.L1DataBxInEvent = 1
@EOF
cmsRun hlt2.py &> hlt2.log
mv output.root hlt2.root
