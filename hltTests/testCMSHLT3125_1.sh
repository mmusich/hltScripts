#!/bin/bash

hltGetConfiguration /users/missirol/test/dev/CMSSW_14_0_0/tmp/240303_firstAlpakaMenu/Test03/GRun \
   --globaltag auto:phase1_2024_realistic \
   --mc \
   --no-prescale \
   --max-events 100 \
   --input /store/mc/Run3Winter24Digi/TT_TuneCP5_13p6TeV_powheg-pythia8/GEN-SIM-RAW/133X_mcRun3_2024_realistic_v8-v2/80000/dc984f7f-2e54-48c4-8950-5daa848b6db9.root \
   --eras Run3 --l1-emulator uGT --l1 L1Menu_Collisions2024_v1_0_0_xml \
   > hlt1.py

#   --customise HLTrigger/Configuration/customizeHLTforAlpaka.customizeHLTforAlpaka \

cat <<@EOF >> hlt1.py
for out_mod_label, out_mod in process.outputModules_().items():
  try: out_mod.SelectEvents.SelectEvents = ['HLTriggerFirstPath']
  except: pass

#process.hltHbheRecHitSoA.src = cms.InputTag( process.hltHbheRecHitSoA.src.value() )
#process.hltHbheRecHitSoACPUSerial = process.hltHbheRecHitSoA.clone(
#    alpaka = dict(backend = 'serial_sync'),
#)
#
#process.hltParticleFlowRecHitHBHESoA.topology = cms.ESInputTag( process.hltParticleFlowRecHitHBHESoA.topology.value() )
#
#process.hltParticleFlowRecHitHBHESoA.producers = cms.VPSet(
#    cms.PSet(
#        src = cms.InputTag("hltHbheRecHitSoA"),
#        params = cms.ESInputTag("hltESPPFRecHitHCALParams:"),
#    )
#)
#
#process.hltParticleFlowRecHitHBHE.src = cms.InputTag( process.hltParticleFlowRecHitHBHE.src.value() )
#process.hltParticleFlowRecHitHBHECPUOnly = process.hltParticleFlowRecHitHBHE.clone(
#    src = 'hltParticleFlowRecHitHBHESoACPUSerial',
#)
#
#process.hltParticleFlowRecHitHBHESoACPUSerial = process.hltParticleFlowRecHitHBHESoA.clone(alpaka = dict(backend = 'serial_sync'))
#process.hltParticleFlowRecHitHBHESoACPUSerial.producers[0].src = 'hltHbheRecHitSoACPUSerial'
#
#process.hltParticleFlowClusterHBHESoA = cms.EDProducer("PFClusterSoAProducer@alpaka",
#    pfRecHits = cms.InputTag("hltParticleFlowRecHitHBHESoA"),
#    topology = cms.ESInputTag("hltESPPFRecHitHCALTopology:"),
#    pfClusterParams = cms.ESInputTag("hltESPPFClusterParams:"),
#    synchronise = cms.bool(False),
#    alpaka = cms.untracked.PSet(
#        backend = cms.untracked.string('')
#    )
#)
#
#process.hltParticleFlowClusterHBHESoACPUSerial = process.hltParticleFlowClusterHBHESoA.clone(
#    pfRecHits = 'hltParticleFlowRecHitHBHESoACPUSerial',
#    alpaka = dict(backend = 'serial_sync'),
#)
@EOF

edmConfigDump hlt1.py > hlt1_dump.py

cmsRun hlt1.py &> hlt1.log
