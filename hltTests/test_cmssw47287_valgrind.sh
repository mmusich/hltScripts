#!/bin/bash

https_proxy=http://cmsproxy.cms:3128/ \
hltConfigFromDB --configName /dev/CMSSW_14_2_0/GRun/V11 > tmp.py

cp /gpu_data/store/data/Run2024I/EphemeralHLTPhysics/FED/run386593_cff.py .

cat <<@EOF >> tmp.py

process.load('run386593_cff')

from HLTrigger.Configuration.customizeHLTforCMSSW import customizeHLTforCMSSW
process = customizeHLTforCMSSW(process)

process.GlobalTag.globaltag = '150X_dataRun3_HLT_v1'

#del process.PrescaleService
process.PrescaleService.lvl1DefaultLabel = '2p0E34'
process.PrescaleService.forceDefault = True

process.hltPixelTracksSoA.CAThetaCutBarrel = 0.00111685053
process.hltPixelTracksSoA.CAThetaCutForward = 0.00249872683
process.hltPixelTracksSoA.hardCurvCut = 0.695091509
process.hltPixelTracksSoA.dcaCutInnerTriplet = 0.0419242041
process.hltPixelTracksSoA.dcaCutOuterTriplet = 0.293522194
process.hltPixelTracksSoA.phiCuts = [
    832, 379, 481, 765, 1136,
    706, 656, 407, 1212, 404,
    699, 470, 652, 621, 1017,
    616, 450, 555, 572
]

process.options.numberOfThreads = 4
process.options.numberOfStreams = 0
process.maxEvents.input = 4
@EOF

edmConfigDump tmp.py > hlt_dump.py

for outn in {00..00}; do
  rm -rf output"${outn}"
  mkdir -p output"${outn}"
  cd output"${outn}"
  valgrind \
   --tool=memcheck --suppressions="${CMSSW_RELEASE_BASE}"/src/Utilities/ReleaseScripts/data/cms-valgrind-memcheck.supp \
   --log-file=memcheck.log --soname-synonyms=somalloc=libjemalloc* \
   --fullpath-after="${CMSSW_RELEASE_BASE}"/src/ --fullpath-after="${CMSSW_BASE}"/src/ \
  cmsRun ../hlt_dump.py &> test_"${outn}".log
  cd ..
done
unset outn

rm -rf run386593_cff.py
rm -rf __pycache__
rm -rf tmp.py
