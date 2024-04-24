#!/bin/bash -ex

scram p CMSSW CMSSW_14_0_5_patch1
cd CMSSW_14_0_5_patch1/src
eval `scramv1 runtime -sh`

https_proxy=http://cmsproxy.cms:3128 hltConfigFromDB --runNumber 379731 > hlt_run379731.py
cat <<@EOF >> hlt_run379731.py
from EventFilter.Utilities.EvFDaqDirector_cfi import EvFDaqDirector as _EvFDaqDirector
process.EvFDaqDirector = _EvFDaqDirector.clone(
    buBaseDir = '/eos/cms/store/group/tsg/FOG/error_stream/',
    runNumber = 379731
)
from EventFilter.Utilities.FedRawDataInputSource_cfi import source as _source
process.source = _source.clone(
    fileListMode = True,
    fileNames = (
        '/eos/cms/store/group/tsg/FOG/error_stream/run379731/run379731_ls0181_index000232_fu-c2b05-18-01_pid3467502.raw',
	'/eos/cms/store/group/tsg/FOG/error_stream/run379731/run379731_ls0181_index000233_fu-c2b05-18-01_pid3467502.raw'
    )
)
process.options.wantSummary = True

process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
@EOF

mkdir run379731
cmsRun hlt_run379731.py &> crash_run379731.log
