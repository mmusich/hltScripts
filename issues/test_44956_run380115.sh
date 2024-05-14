#!/bin/bash -ex

cd CMSSW_14_0_5_patch1/src
eval `scramv1 runtime -sh`

export MALLOC_CONF=junk:true

https_proxy=http://cmsproxy.cms:3128 hltConfigFromDB --runNumber 380115 > hlt_run380115.py
cat <<@EOF >> hlt_run380115.py
from EventFilter.Utilities.EvFDaqDirector_cfi import EvFDaqDirector as _EvFDaqDirector
process.EvFDaqDirector = _EvFDaqDirector.clone(
  buBaseDir = '/eos/cms/store/group/tsg/FOG/error_stream/',
  runNumber = 380115
)
from EventFilter.Utilities.FedRawDataInputSource_cfi import source as _source
process.source = _source.clone(
  fileListMode = True,
  fileNames = (
  '/eos/cms/store/group/tsg/FOG/error_stream/run380115/run380115_ls0338_index000079_fu-c2b03-28-01_pid1451372.raw',
  '/eos/cms/store/group/tsg/FOG/error_stream/run380115/run380115_ls0338_index000104_fu-c2b03-28-01_pid1451372.raw'
  )
)
process.options.wantSummary = True

process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
@EOF

mkdir run380115
cmsRun hlt_run380115.py &> crash_run380115.log
