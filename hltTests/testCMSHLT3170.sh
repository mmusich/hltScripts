#!/bin/bash -e

hltMenu="--runNumber 379617"
runNumber=379660

inpFile=root://eoscms.cern.ch//eos/cms/store/data/Run2024C/EphemeralHLTPhysics0/RAW/v1/000/379/660/00000/57e67aa5-63fe-440f-908f-c66c967680de.root

outDir=run"${runNumber}"

maxEvents=1000

jobLabel=testCMSHLT3170

cmsswDirHLT=../../CMSSW_14_0_MULTIARCHS_X_2024-04-21-2300
cmsswDirREP=../../CMSSW_14_0_X_2024-04-21-2300 

###
### HLT
###

cd "${cmsswDirHLT}"/src
cmsenv
cd "${OLDPWD}"

echo "----------------------------------"
echo "HLT running in ${CMSSW_BASE}"
echo "----------------------------------"

https_proxy=http://cmsproxy.cms:3128/ \
hltConfigFromDB ${hltMenu} > "${jobLabel}"_hlt.py

cat <<@EOF >> "${jobLabel}"_hlt.py

process.setName_("HLTX")

process.maxEvents.input = ${maxEvents}

del process.PrescaleService

process.source = cms.Source( "PoolSource",
    fileNames = cms.untracked.vstring( "${inpFile}" )
)

from EventFilter.Utilities.EvFDaqDirector_cfi import EvFDaqDirector as _EvFDaqDirector
process.EvFDaqDirector = _EvFDaqDirector.clone(
    buBaseDir = '.',
    runNumber = ${runNumber}
)
@EOF

rm -rf "${outDir}"
mkdir -p "${outDir}"

cmsRun "${jobLabel}"_hlt.py &> "${jobLabel}"_hlt.log

###
### REPACK
###

cd "${cmsswDirREP}"/src
cmsenv
cd "${OLDPWD}"

echo "----------------------------------"
echo "REPACK running in ${CMSSW_BASE}"
echo "----------------------------------"

cat <<@EOF > "${jobLabel}"_repack_cfg.py
import FWCore.ParameterSet.Config as cms
from sys import argv

input = argv[1]
stream = input.rsplit('/',1)[-1].rstrip('.dat')
output = argv[2]

process = cms.Process("REPACK")

process.source = cms.Source("NewEventStreamFileReader",
    fileNames = cms.untracked.vstring("file:"+input)
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.write = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('RAW')
    ),
    fileName = cms.untracked.string(output)
)

process.outputPath = cms.EndPath(process.write)
@EOF

streamNames=($(ls -l "${outDir}"/*dat | awk '{split($0,a,"_"); print a[3]}' | sort -u))

rm -rf "${outDir}"/testRepack/{input,output}
mkdir -p "${outDir}"/testRepack/{input,output}

for streamName in "${streamNames[@]}"; do

  stream=$(basename $streamName)

  if [[ ${stream} == streamDQMHistograms ]] ||
     [[ ${stream} == streamHLTRates ]] ||
     [[ ${stream} == streamL1Rates ]]; then
    continue
  fi

  inpfiles=$(find "${outDir}" -name "*_${streamName}_*" -type f | grep -E "ini|dat" | grep -v initemp | sort)

  if ! [ "${inpfiles}" ]; then continue; fi;

  newfile="${outDir}"/testRepack/input/${stream}.dat

  cat ${inpfiles} > ${newfile}

  cmsRun "${jobLabel}"_repack_cfg.py ${newfile} ${outDir}/testRepack/output/${stream}.root
done

rm -rf "${jobLabel}"_hlt.{py,log}
rm -rf "${jobLabel}"_repack_cfg.py
