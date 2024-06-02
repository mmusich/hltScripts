#!/bin/bash -e

runNumber=380379
inputFile=/eos/cms/tier0/store/data/Run2024D/Cosmics/RAW/v1/000/380/379/00000/fd8cc58c-3ca3-47d6-ac1e-2eb019f45292.root
[ -f run"${runNumber}"_cff.py ] || convertToRaw -f 1000 -l 1000 -r "${runNumber}":75-"${runNumber}":75 "${inputFile}"

hltMenu=/cdaq/test/missirol/test/2024/240602_HLTTest_cosmics/Test02/HLT/V3
hltConfigFromDB --configName --adg "${hltMenu}" > hlt.py

# prescale HLT_L1SingleMuCosmics_ppTracking_v by 2
cat <<@EOF >> hlt.py

process.load("run${runNumber}_cff")

process.hltOnlineBeamSpotESProducer.timeThreshold = int(1e6)

process.options.wantSummary = True
process.options.numberOfThreads = 4
process.options.numberOfStreams = 0

process.PrescaleService.forceDefault = True
psIdx = process.PrescaleService.lvl1Labels.index( process.PrescaleService.lvl1DefaultLabel )
for pathPSet in process.PrescaleService.prescaleTable:
    if pathPSet.pathName.value().startswith('HLT_L1SingleMuCosmics_ppTracking_v'):
        pathPSet.prescales[psIdx] = 2
        break
@EOF

## run on CPU for half of the events, and on GPU for the other half
cp hlt.py test_cmssw44643_hlt_cpu.py
cp hlt.py test_cmssw44643_hlt_gpu.py
rm -f hlt.py

cat <<@EOF >> test_cmssw44643_hlt_cpu.py

process.hltPreL1SingleMuCosmicsppTracking.offset = 0
@EOF

cat <<@EOF >> test_cmssw44643_hlt_gpu.py

process.hltPreL1SingleMuCosmicsppTracking.offset = 1
@EOF

# GPU case (a 50% of input events)
unset CUDA_VISIBLE_DEVICES
cmsRun test_cmssw44643_hlt_gpu.py &> test_cmssw44643_hlt_gpu.log
cat run"${runNumber}"/*streamHLTMonitor*.ini run"${runNumber}"/*streamHLTMonitor*.dat > streamHLTMonitor_tmp.dat
rm -rf run"${runNumber}"/*{mon,open,processing,BoLS,output,pid}*

# CPU case (the other 50% of input events)
CUDA_VISIBLE_DEVICES= \
cmsRun test_cmssw44643_hlt_cpu.py &> test_cmssw44643_hlt_cpu.log
cat streamHLTMonitor_tmp.dat run"${runNumber}"/*streamHLTMonitor*.dat > streamHLTMonitor.dat
rm -rf run"${runNumber}"/*{mon,open,processing,BoLS,output,pid}*
rm -f streamHLTMonitor_tmp.dat

cat <<EOF > test_cmssw44643_repack_cfg.py
import FWCore.ParameterSet.Config as cms

process = cms.Process('TEST')
process.options.wantSummary = False
process.maxEvents.input = -1

process.EvFDaqDirector = cms.Service('EvFDaqDirector')

process.source = cms.Source('NewEventStreamFileReader',
  fileNames = cms.untracked.vstring(
    'file:streamHLTMonitor.dat',
  )
)

process.edmOutput = cms.OutputModule('PoolOutputModule',
  dataset = cms.untracked.PSet(
    dataTier = cms.untracked.string('RAW')
  ),
  fileName = cms.untracked.string('file:streamHLTMonitor.root')
)

process.outputPath = cms.EndPath(process.edmOutput)
EOF

rm -rf run000000
cmsRun test_cmssw44643_repack_cfg.py &> test_cmssw44643_repack_cfg.log
rm -rf run000000
rm -f streamHLTMonitor.dat

cmsDriver.py step3 -s RAW2DIGI,RECO,DQM:@HLTMon \
 --conditions 140X_dataRun3_Prompt_v2 --datatier DQMIO -n -1 \
 --eventcontent DQM --geometry DB:Extended --era Run3 \
 --filein file:streamHLTMonitor.root \
 &> test_cmssw44643_recodqm.log

rm -rf __pycache__
