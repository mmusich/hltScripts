#!/bin/bash -ex

[ $# -eq 1 ] || (exit 1)

outDir="${1}"

mkdir -p "${outDir}"
cd "${outDir}"

inputFileDATA=/store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/2E066536-5CF2-B340-A73B-209640F29FF6.root

hltMenu=/dev/CMSSW_12_3_0/GRun/V4
hltMenuTag=hlt_GRun_V04_test1
hltGetConfiguration ${hltMenu} \
 --dbproxy \
 --max-events 10 --no-output --unprescale \
 --input "${inputFileDATA}" --data --globaltag auto:run3_hlt \
 --eras Run2_2018 \
 --customise \
HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input,\
HLTrigger/Configuration/customizeHLTforPatatrack.customizeHLTforPatatrackTriplets \
 > "${hltMenuTag}"_DATA.py
(edmConfigDump "${hltMenuTag}"_DATA.py > "${hltMenuTag}"_DATA_dump.py) || true
(python3 "${hltMenuTag}"_DATA_dump.py) || true

hltMenu=/dev/CMSSW_12_3_0/GRun/V4
hltMenuTag=hlt_GRun_V04_test2
hltGetConfiguration ${hltMenu} \
 --dbproxy \
 --max-events 10 --no-output --unprescale \
 --input "${inputFileDATA}" --data --globaltag auto:run3_hlt \
 --eras Run2_2018 \
 --customise \
HLTrigger/Configuration/customizeHLTforPatatrack.customizeHLTforPatatrackTriplets,\
HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input \
 > "${hltMenuTag}"_DATA.py
(edmConfigDump "${hltMenuTag}"_DATA.py > "${hltMenuTag}"_DATA_dump.py) || true
(python3 "${hltMenuTag}"_DATA_dump.py) || true

hltMenu=/dev/CMSSW_12_3_0/GRun/V10
hltMenuTag=hlt_GRun_V10_test1
hltGetConfiguration ${hltMenu} \
 --dbproxy \
 --max-events 10 --no-output --unprescale \
 --input "${inputFileDATA}" --data --globaltag auto:run3_hlt \
 --eras Run2_2018 \
 --customise \
HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input,\
HLTrigger/Configuration/customizeHLTforPatatrack.customizeHLTforPatatrackTriplets \
 > "${hltMenuTag}"_DATA.py
(edmConfigDump "${hltMenuTag}"_DATA.py > "${hltMenuTag}"_DATA_dump.py) || true
(python3 "${hltMenuTag}"_DATA_dump.py) || true

hltMenu=/dev/CMSSW_12_3_0/GRun/V10
hltMenuTag=hlt_GRun_V10_test2
hltGetConfiguration ${hltMenu} \
 --dbproxy \
 --max-events 10 --no-output --unprescale \
 --input "${inputFileDATA}" --data --globaltag auto:run3_hlt \
 --eras Run2_2018 \
 --customise \
HLTrigger/Configuration/customizeHLTforPatatrack.customizeHLTforPatatrackTriplets,\
HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input \
 > "${hltMenuTag}"_DATA.py
(edmConfigDump "${hltMenuTag}"_DATA.py > "${hltMenuTag}"_DATA_dump.py) || true
(python3 "${hltMenuTag}"_DATA_dump.py) || true

hltMenu=/dev/CMSSW_12_3_0/GRun/V10
hltMenuTag=hlt_GRun_V10_test3
hltGetConfiguration ${hltMenu} \
 --dbproxy \
 --max-events 10 --no-output --unprescale \
 --input "${inputFileDATA}" --data --globaltag auto:run3_hlt \
 --eras Run2_2018 \
 --customise \
HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input \
 > "${hltMenuTag}"_DATA.py
(edmConfigDump "${hltMenuTag}"_DATA.py > "${hltMenuTag}"_DATA_dump.py) || true
(python3 "${hltMenuTag}"_DATA_dump.py) || true

unset outDir inputFileDATA hltMenu hltMenuTag
