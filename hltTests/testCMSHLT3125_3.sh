#!/bin/bash

jobName=hlt_CMSHLT3125

hltConfigFromDB --configName /dev/CMSSW_14_0_0/HLT > tmp.py

edmConfigDump tmp.py > "${jobName}"_ref.py

for nnn in {1..3}; do

  cat <<@EOF >> tmp.py
from HLTrigger.Configuration.customizeHLTforAlpaka import customizeHLTforAlpaka
process = customizeHLTforAlpaka(process)
@EOF

  edmConfigDump tmp.py > "${jobName}"_tar"${nnn}".py

done; unset nnn
