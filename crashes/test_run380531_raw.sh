#!/bin/bash -ex

scram p CMSSW CMSSW_14_0_6_MULTIARCHS
cd CMSSW_14_0_6_MULTIARCHS/src
eval `scramv1 runtime -sh`

https_proxy=http://cmsproxy.cms:3128 hltConfigFromDB --runNumber 380531 > hlt_run380531.py
cat <<@EOF >> hlt_run380531.py
from EventFilter.Utilities.EvFDaqDirector_cfi import EvFDaqDirector as _EvFDaqDirector
process.EvFDaqDirector = _EvFDaqDirector.clone(
   buBaseDir = '/eos/cms/store/group/tsg/FOG/error_stream/',
   runNumber = 380531
)
from EventFilter.Utilities.FedRawDataInputSource_cfi import source as _source
process.source = _source.clone(
   fileListMode = True,
   fileNames = (
       '/eos/cms/store/group/tsg/FOG/error_stream/run380531/run380531_ls0683_index000414_fu-c2b04-03-01_pid312890.raw',
       '/eos/cms/store/group/tsg/FOG/error_stream/run380531/run380531_ls0683_index000446_fu-c2b04-03-01_pid312890.raw',
       '/eos/cms/store/group/tsg/FOG/error_stream/run380531/run380531_ls0683_index000473_fu-c2b04-03-01_pid312890.raw' 
   )
)
process.options.wantSummary = True

process.options.numberOfThreads = 32
process.options.numberOfStreams = 24
@EOF

mkdir run380531
cmsRun hlt_run380531.py &> crash_run380531.log
