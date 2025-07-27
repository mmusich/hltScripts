#!/bin/bash

hltMenu=/dev/CMSSW_15_0_0/GRun/V100
numEventsPerJob=500
hltLabel0=testCMSHLT3606_hlt0
hltLabel1=testCMSHLT3606_hlt1
hltLabel2=testCMSHLT3606_hlt2

hltGetConfiguration "${hltMenu}" \
  --process HLTX \
  --globaltag 150X_dataRun3_HLT_v1 \
  --data \
  --no-prescale \
  --no-output \
  --input /store/data/Run2025C/Muon0/RAW/v1/000/393/376/00000/9a3663a2-f22c-462d-b4b1-8338be2cebcf.root \
  --max-events "${numEventsPerJob}" \
  --paths "HLT_IsoMu24_*Loose*_ETau_Monitoring*" \
  > "${hltLabel0}".py

cat <<@EOF >> "${hltLabel0}".py

process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
process.options.wantSummary = True

process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.options.accelerators = ['cpu']

del process.dqmOutput
@EOF

cmsRun "${hltLabel0}".py &> "${hltLabel0}".log

# hltLabel1
cp "${hltLabel0}".py "${hltLabel1}".py
cat <<@EOF >> "${hltLabel1}".py

process.hltIsoMu24FilterEle24Tau30Monitoring = cms.EDFilter( "HLTMuonL3SimplePreFilter",
    saveTags = cms.bool( True ),
    BeamSpotTag = cms.InputTag( "hltOnlineBeamSpot" ),
    CandTag = cms.InputTag( "hltIterL3MuonCandidates" ),
    PreviousCandTag = cms.InputTag( "hltL3crIsoBigORMu18erTauXXer2p1L1f0L2f10QL3f20QL3trkIsoFiltered" ),
    MatchToPreviousCand = cms.bool( True ),
    MinN = cms.int32( 1 ),
    MaxEta = cms.double( 2.1 ),
    MinPt = cms.double( 24.0 ),
    NSigmaPt = cms.double( 0.0 ),
    MinTrackPt = cms.double( 0.0 ),
    MaxPtDifference = cms.double( 9999.0 ),
    MinNhits = cms.int32( 0 ),
    MinNmuonHits = cms.int32( 0 ),
    MaxDz = cms.double( 9999.0 ),
    MinDxySig = cms.double( -1.0 ),
    MaxNormalizedChi2 = cms.double( 9999.0 ),
    MinDXYBeamSpot = cms.double( -1.0 ),
    MaxDXYBeamSpot = cms.double( 9999.0 )
)
@EOF

cmsRun "${hltLabel1}".py &> "${hltLabel1}".log

# hltLabel2
cp "${hltLabel1}".py "${hltLabel2}".py
cat <<@EOF >> "${hltLabel2}".py

for moduleLabel in [
  'hltHpsOverlapFilterIsoMu24LooseETauWPPNetTauhTagJet30L1Seeded',
  'hltHpsOverlapFilterIsoMu24MediumETauWPPNetTauhTagJet30L1Seeded',
  'hltHpsOverlapFilterIsoMu24TightETauWPPNetTauhTagJet30L1Seeded',
]:
    if hasattr(process, moduleLabel):
        mod = getattr(process, moduleLabel)
        mod.inputTag1 = 'hltL3crIsoBigORMu18erTauXXer2p1L1f0L2f10QL3f20QL3trkIsoFiltered'
@EOF

cmsRun "${hltLabel2}".py &> "${hltLabel2}".log
