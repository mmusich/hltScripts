#!/bin/bash -ex

runNumber=380360

https_proxy=http://cmsproxy.cms:3128 \
hltConfigFromDB --runNumber "${runNumber}" > tmp.py

cat <<@EOF >> tmp.py
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

process.options.numberOfThreads = 1
process.options.numberOfStreams = 0
process.options.wantSummary = True
@EOF

fileNames=(
  run380360_ls0497_index000285_fu-c2b05-24-01_pid2354912
  run380360_ls0497_index000302_fu-c2b05-24-01_pid2354912
  run380360_ls0497_index000351_fu-c2b05-24-01_pid2354912
  run380360_ls0497_index000384_fu-c2b05-24-01_pid2354912
  run380360_ls1228_index000205_fu-c2b03-06-01_pid2086739
  run380360_ls1228_index000210_fu-c2b03-06-01_pid2086739
)

for fileName in "${fileNames[@]}"; do
  echo "${fileName}"
  cp tmp.py "${fileName}".py
  cat <<@EOF >> "${fileName}".py
process.source.fileNames = ['/store/error_stream/run380360/${fileName}.raw']
@EOF

  rm -rf run"${runNumber}"
  mkdir -p run"${runNumber}"
  CUDA_LAUNCH_BLOCKING=1 \
  cmsRun "${fileName}".py &> "${fileName}".log
done
unset fileName

rm -rf tmp.py run"${runNumber}"
