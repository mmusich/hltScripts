#!/bin/bash -ex

hltConfigFromDB --configName /users/missirol/test/dev/CMSSW_12_3_0/CMSHLT_2288/IntegTest_v01/HLT > tmp.py

edmConfigDump --prune tmp.py > pre.py

sed -i "s|process = cms.Process( \"HLT\" )|from Configuration.Eras.Era_Run3_cff import Run3\nprocess = cms.Process( \"HLT\" , Run3 )|g" tmp.py

cat <<EOF >> tmp.py

from HLTrigger.Configuration.customizeHLTforPatatrack import customizeHLTforPatatrackTriplets
process = customizeHLTforPatatrackTriplets(process)
EOF

edmConfigDump --prune tmp.py > post.py
rm -f tmp.py
