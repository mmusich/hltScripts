#!/bin/bash

https_proxy=http://cmsproxy.cms:3128/ \
hltConfigFromDB --runNumber 379617 > hlt.py

rm -rf run379617
mkdir -p run379617

cat <<@EOF >> hlt.py

import os
import glob

for out_mod_label, out_mod in process.outputModules_().items():
  try: out_mod.SelectEvents.SelectEvents = ['HLTriggerFirstPath']
  except: pass

del process.MessageLogger
process.load('FWCore.MessageLogger.MessageLogger_cfi')

process.options.numberOfThreads = 32
process.options.numberOfStreams = 24

fileList = sorted(list(set([file_i for file_i in glob.glob("/store/error_stream/run379617/*raw") if os.stat(file_i).st_size > 0])))

from EventFilter.Utilities.FedRawDataInputSource_cfi import source as _source
process.source = _source.clone(
    eventChunkSize = 200,   # MB
    eventChunkBlock = 200,  # MB
    numBuffers = 4,
    maxBufferedFiles = 4,
    fileListMode = True,
    fileNames = fileList
)

from EventFilter.Utilities.EvFDaqDirector_cfi import EvFDaqDirector as _EvFDaqDirector
process.EvFDaqDirector = _EvFDaqDirector.clone(
    buBaseDir = '.',
    runNumber = 379617
)

from EventFilter.Utilities.FastMonitoringService_cfi import FastMonitoringService as _FastMonitoringService
process.FastMonitoringService = _FastMonitoringService.clone()
@EOF

cmsRun hlt.py &> hlt.log
