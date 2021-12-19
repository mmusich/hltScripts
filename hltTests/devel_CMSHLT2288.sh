#!/bin/bash -ex

HLTVER=V98

hltConfigFromDB --configName /dev/CMSSW_12_3_0/HLT/"${HLTVER}" > tmp.py

sed -i "s|process = cms.Process( \"HLT\" )|from Configuration.Eras.Era_Run3_cff import Run3\nprocess = cms.Process( \"HLT\" , Run3 )|g" tmp.py

edmConfigDump tmp.py > "${HLTVER}"_pre.py

cat <<EOF >> tmp.py

from HLTrigger.Configuration.customizeHLTforPatatrack import customizeHLTforPatatrackTriplets
process = customizeHLTforPatatrackTriplets(process)
EOF

edmConfigDump tmp.py > "${HLTVER}"_post.py
rm -f tmp.py

mkdir -p "${HOME}"/private/cmshlt2288
mv "${HLTVER}"_*.py "${HOME}"/private/cmshlt2288
rm -rf "${HOME}"/private/cmshlt2288/*{class,pyc}
