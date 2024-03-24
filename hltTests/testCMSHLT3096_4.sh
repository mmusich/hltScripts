#!/bin/bash

# V82 + customizeHLTforAlpaka
hltConfigFromDB --configName /dev/CMSSW_14_0_0/HLT/V82 > tmp.py

cat <<@EOF >> tmp.py
from HLTrigger.Configuration.customizeHLTforAlpaka import customizeHLTforAlpaka
process = customizeHLTforAlpaka(process)
@EOF

edmConfigDump --prune tmp.py > hlt0.py

# latest + customizeHLTforAlpaka
hltConfigFromDB --configName /dev/CMSSW_14_0_0/HLT/V83 > tmp.py

cat <<@EOF >> tmp.py
from HLTrigger.Configuration.customizeHLTforAlpaka import customizeHLTforAlpaka
process = customizeHLTforAlpaka(process)
@EOF

edmConfigDump --prune tmp.py > hlt1.py
