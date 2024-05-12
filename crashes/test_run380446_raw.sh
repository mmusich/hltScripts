#!/bin/bash -ex

scram p CMSSW CMSSW_14_0_6_MULTIARCHS
cd CMSSW_14_0_6_MULTIARCHS/src
eval `scramv1 runtime -sh`

https_proxy=http://cmsproxy.cms:3128 hltConfigFromDB --runNumber 380466 > hlt_run380466.py
cat <<@EOF >> hlt_run380466.py
from EventFilter.Utilities.EvFDaqDirector_cfi import EvFDaqDirector as _EvFDaqDirector
process.EvFDaqDirector = _EvFDaqDirector.clone(
    buBaseDir = '/eos/cms/store/group/tsg/FOG/error_stream/',
    runNumber = 380466
)
from EventFilter.Utilities.FedRawDataInputSource_cfi import source as _source
process.source = _source.clone(
    fileListMode = True,
    fileNames = (
	'/eos/cms/store/group/tsg/FOG/error_stream/run380466/run380466_ls0276_index000212_fu-c2b03-09-01_pid672001.raw',
	'/eos/cms/store/group/tsg/FOG/error_stream/run380466/run380466_ls0276_index000232_fu-c2b03-09-01_pid672001.raw',
	'/eos/cms/store/group/tsg/FOG/error_stream/run380466/run380466_ls0276_index000246_fu-c2b03-09-01_pid672001.raw'
    )
)
process.options.wantSummary = True

process.options.numberOfThreads = 32
process.options.numberOfStreams = 24
@EOF

mkdir run380466
cmsRun hlt_run380466.py &> crash_run380466.log
