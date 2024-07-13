#!/bin/bash -ex
https_proxy=http://cmsproxy.cms:3128 hltConfigFromDB --runNumber 380466 > hlt_run380466.py
export MALLOC_CONF=junk:true
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
    )
)
process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
process.options.wantSummary = True
process.hltOnlineBeamSpotESProducer.timeThreshold = int(1e6)
del process.MessageLogger
process.load('FWCore.MessageService.MessageLogger_cfi')
@EOF

DIR="run380466"

# Check if directory exists
if [ -d "$DIR" ]; then
  echo "Directory $DIR exists. Removing it..."
  rm -rf "$DIR"  # Remove the directory and its contents
  echo "Directory $DIR removed."
else
  echo "Directory $DIR does not exist."
fi

# Create the directory
mkdir "$DIR"
echo "Directory $DIR created."

cmsRun hlt_run380466.py &> crash_run380466.log
