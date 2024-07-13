#!/bin/bash -e

cmsDriver.py step3 -s RAW2DIGI,L1Reco,RECO,DQM:@HLTMon \
  --conditions 140X_dataRun3_Prompt_v4 --datatier DQMIO -n -1 \
  --eventcontent DQM --geometry DB:Extended --era Run3 --no_exec \
  --filein file:/eos/cms/tier0/store/backfill/1/express/Tier0_REPLAY_2024/HLTMonitor/FEVTHLTALL/Express-v8154816/000/382/686/00000/01dd398e-3eb8-4410-90a2-023f836f34a3.root \
  --processName RECO2 \
  --python_filename tmp.py

cat <<@EOF >> tmp.py

#process.source.inputCommands = cms.untracked.vstring([
#    'drop *',
#    'keep *_hltDeepBLifetimeTagInfosPF_*_*',
#    'keep *_hltDeepCombinedSecondaryVertexBJetTagsCalo_*_*',
#    'keep *_hltDeepCombinedSecondaryVertexBJetTagsInfosCalo_*_*',
#    'keep *_hltDeepCombinedSecondaryVertexBJetTagsInfos_*_*',
#    'keep *_hltDeepCombinedSecondaryVertexBJetTagsPF_*_*',
#    'keep *_hltDeepSecondaryVertexTagInfosPF_*_*',
#    'keep *_hltDisplacedhltIter4PFlowTrackSelectionHighPurity_*_*',
#    'keep *_hltDoubletRecoveryPFlowTrackSelectionHighPurity_*_*',
#    'keep *_hltEcalRecHit_*_*',
#    'keep *_hltEgammaGsfTracks_*_*',
#    'keep *_hltFastPixelBLifetimeL3Associator_*_*',
#    'keep *_hltFastPrimaryVertex_*_*',
#    'keep *_hltHbhereco_*_*',
#    'keep *_hltHfreco_*_*',
#    'keep *_hltHoreco_*_*',
#    'keep *_hltImpactParameterTagInfos_*_*',
#    'keep *_hltInclusiveSecondaryVertexFinderTagInfos_*_*',
#    'keep *_hltIter2MergedForDisplaced_*_*',
#    'keep *_hltMergedTracksForBTag_*_*',
#    'keep *_hltMergedTracks_*_*',
#    'keep *_hltOnlineBeamSpot_*_*',
#    'keep *_hltPFJetForBtag_*_*',
#    'keep *_hltPFJetForPNetAK8_*_*',
#    'keep *_hltPFMuonMerging_*_*',
#    'keep *_hltParticleNetDiscriminatorsJetTagsAK8_*_*',
#    'keep *_hltParticleNetDiscriminatorsJetTags_*_*',
#    'keep *_hltParticleNetJetTagInfos_*_*',
#    'keep *_hltPixelTracks_*_*',
#    'keep *_hltPixelVertices_*_*',
#    'keep *_hltSelector8CentralJetsL1FastJet_*_*',
#    'keep *_hltSiPixelClustersCache_*_*',
#    'keep *_hltSiPixelClusters_*_*',
#    'keep *_hltSiStripRawToClustersFacility_*_*',
#    'keep *_hltVerticesL3_*_*',
#    'keep *_hltVerticesPFFilter_*_*',
#    'keep *_hltVerticesPFSelector_*_*',
#    'keep FEDRawDataCollection_rawDataCollector_*_*',
#    'keep FEDRawDataCollection_source_*_*',
#    'keep GlobalObjectMapRecord_hltGtStage2ObjectMap_*_*',
#    'keep edmTriggerResults_*_*_*',
#    'keep triggerTriggerEvent_*_*_*'
#])
@EOF

cmsRun tmp.py > tmp.log
