#!/bin/bash

# V2 already includes the renaming, done via ConfDB
hltConfigFromDB --configName /users/missirol/test/dev/CMSSW_14_0_0/tmp/240303_firstAlpakaMenu/Test11/HLT/V2 > a2.py
edmConfigDump a2.py > a2_dump.py

cat <<@EOF >> a2.py
from HLTrigger.Configuration.customizeHLTforAlpaka import customizeHLTforAlpaka
process = customizeHLTforAlpaka(process)
@EOF
edmConfigDump a2.py > a3_dump.py

# This diff must be empty
diff -q a2_dump.py a3_dump.py
