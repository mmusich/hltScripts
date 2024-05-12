#!/bin/bash -ex

runNumber=380624

https_proxy=http://cmsproxy.cms:3128 \
hltConfigFromDB --runNumber "${runNumber}" > tmp.py

cat <<@EOF >> tmp.py

process.hltOnlineBeamSpotESProducer.timeThreshold = int(1e6)

from EventFilter.Utilities.EvFDaqDirector_cfi import EvFDaqDirector as _EvFDaqDirector
process.EvFDaqDirector = _EvFDaqDirector.clone(
    buBaseDir = '.',
    runNumber = ${runNumber}
)

from EventFilter.Utilities.FedRawDataInputSource_cfi import source as _source
process.source = _source.clone(
    fileListMode = True,
    fileNames = []
)

process.options.numberOfThreads = 16
process.options.numberOfStreams = 8
#process.options.wantSummary = True
@EOF

fileNames=(
  run380624_ls0411_index000136_fu-c2b01-12-01_pid2375140
  run380624_ls0411_index000145_fu-c2b01-12-01_pid2375140
  run380624_ls0411_index000164_fu-c2b01-12-01_pid2375140
)

for fileName in "${fileNames[@]}"; do
  echo "${fileName}"
  cp tmp.py "${fileName}".py
  cat <<@EOF >> "${fileName}".py
process.source.fileNames = ['/eos/cms/store/group/tsg/FOG/error_stream/run${runNumber}/${fileName}.raw']
@EOF

  rm -rf run"${runNumber}"
  mkdir -p run"${runNumber}"
  CUDA_LAUNCH_BLOCKING=1 \
  cmsRun "${fileName}".py &> "${fileName}".log
done
unset fileName

rm -rf tmp.py run"${runNumber}"
