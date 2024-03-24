#!/bin/bash

jobName=hlt_alpaka_test14

hltConfigFromDB --configName /dev/CMSSW_14_0_0/HLT > tmp.py

edmConfigDump tmp.py > "${jobName}"_ref.py

cat <<@EOF >> tmp.py
from HLTrigger.Configuration.customizeHLTforAlpaka import customizeHLTforAlpaka
process = customizeHLTforAlpaka(process)
@EOF

edmConfigDump tmp.py > "${jobName}".py

cat <<@EOF >> tmp.py
from HLTrigger.Configuration.customizeHLTforAlpaka import customizeHLTforAlpaka
process = customizeHLTforAlpaka(process)
@EOF

edmConfigDump tmp.py > "${jobName}"_2.py

cat <<@EOF >> tmp.py
from HLTrigger.Configuration.customizeHLTforAlpaka import customizeHLTforAlpaka
process = customizeHLTforAlpaka(process)
@EOF

edmConfigDump tmp.py > "${jobName}"_3.py
