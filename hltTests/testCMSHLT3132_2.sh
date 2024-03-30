#!/bin/bash

# V1 is a copy of /dev/CMSSW_14_0_0/HLT/V93
hltConfigFromDB --configName /users/missirol/test/dev/CMSSW_14_0_0/tmp/240303_firstAlpakaMenu/Test11/HLT/V1 > a1.py
cat <<@EOF >> a1.py
from HLTrigger.Configuration.customizeHLTforAlpaka import customizeHLTforAlpaka
process = customizeHLTforAlpaka(process)
@EOF
edmConfigDump a1.py > a1_dump.py

# V2 includes the renaming, done via ConfDB
hltConfigFromDB --configName /users/missirol/test/dev/CMSSW_14_0_0/tmp/240303_firstAlpakaMenu/Test11/HLT/V2 > a2.py
edmConfigDump a2.py > a2_dump.py

# This diff will not be empty,
# because of the name of the configuration in ConfDB (process.HLTConfigVersion)
# and because the order of Sequences and Tasks in the configuration will not be exactly the same.
# Modulo these spurious differences, the configurations should be identical.
diff -q a1_dump.py a2_dump.py
