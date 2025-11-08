#!/bin/bash -ex

# cmsrel CMSSW_15_0_15_patch4
# cd CMSSW_15_0_15_patch4/src
# cmsenv

LOCALPATH='/eos/cms/store/data/Run2025G/EphemeralHLTPhysics0/RAW/v1/000/398/183/00000/'
echo "Input source: |${LOCALPATH}|"
LOCALFILES=$(ls -1 ${LOCALPATH})
ALL_FILES=""
for f in ${LOCALFILES[@]}; do
    ALL_FILES+="file:${LOCALPATH}/${f},"
done
# Remove the last character
ALL_FILES="${ALL_FILES%?}"
echo "Discovered files: $ALL_FILES"

cmsDriver.py step2 -s HLT:GRun,DQM:sistripMonitorHLTsequence+sipixelMonitorHLTsequence+trackingMonitorHLT \
	     --conditions 150X_dataRun3_HLT_Candidate_2025_10_27_10_07_21 \
	     --datatier DQMIO \
	     -n 10000 \
	     --eventcontent DQMIO \
	     --geometry DB:Extended \
	     --era Run3_2025 \
	     --filein file:$ALL_FILES \
	     --fileout file:step2.root \
	     --nThreads 24 \
	     --process HLTX \
	     --python_filename hlt_BPix1OFF.py \
	     --inputCommands='keep *, drop *_hlt*_*_HLT, drop triggerTriggerFilterObjectWithRefs_l1t*_*_HLT' \
	     --no_exec

cat <<@EOF >> hlt_BPix1OFF.py
#### print TriggerResults
process.options.wantSummary = True

#### recipe to kill BPix 1
process.hltSiPixelClustersSoA.UseQualityInfo = cms.bool( True )
process.hltSiPixelClustersSoASerialSync.UseQualityInfo = cms.bool( True )
process.hltSiPixelDigisRegForDisplaced.UseQualityInfo = cms.bool( True )
process.hltESPSiPixelCablingSoA.UseQualityInfo = cms.bool( True )
process.siPixelROCsStatusAndMappingWrapperESProducer.UseQualityInfo = cms.bool( True )

### changes in DQM to run in the same step as HLT
process.hltTrackRefitterForPixelDQM.Fitter = cms.string('hltESPFlexibleKFFittingSmoother')
process.hltTrackRefitterForPixelDQM.MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEvent")
process.hltTrackRefitterForPixelDQM.MeasurementTracker = cms.string('hltESPMeasurementTracker')

process.hltTrackRefitterForSiStripMonitorTrack.Fitter = cms.string('hltESPKFFittingSmootherWithOutliersRejectionAndRK')
process.hltTrackRefitterForSiStripMonitorTrack.MeasurementTracker = cms.string('hltESPMeasurementTracker')
process.hltTrackRefitterForSiStripMonitorTrack.MeasurementTrackerEvent = cms.InputTag("hltMeasurementTrackerEvent")
@EOF

cmsRun hlt_BPix1OFF.py &> hlt_BPix1OFF.log

cmsDriver.py step3 -s HARVESTING:@standardDQM \
	     --conditions 150X_dataRun3_HLT_Candidate_2025_10_27_10_07_21  \
	     --data \
	     --geometry DB:Extended \
	     --scenario pp \
	     --filetype DQM \
	     --era Run3_2025 \
	     -n 1000 \
	     --filein file:step2.root \
	     --fileout file:step3.root \
	     --no_exec

cmsRun step3_HARVESTING.py >& harvesting.log
