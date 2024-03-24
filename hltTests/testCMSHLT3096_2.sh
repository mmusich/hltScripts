#!/bin/bash

jobName=hlt_alpaka_test05

hltConfigFromDB --configName /dev/CMSSW_14_0_0/HLT > tmp.py

edmConfigDump tmp.py > "${jobName}"_ref.py

cat <<@EOF >> tmp.py
from HLTrigger.Configuration.customizeHLTforAlpaka import customizeHLTforAlpaka
process = customizeHLTforAlpaka(process)
@EOF

edmConfigDump tmp.py > "${jobName}".py
