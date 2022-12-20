#!/bin/bash

INPUTFILE=root://eoscms.cern.ch//eos/cms/store/group/dpg_trigger/comm_trigger/TriggerStudiesGroup/STORM/RAW/Run2022F_EphemeralHLTPhysics0_run361468/26ce1488-8c46-436b-becd-6b41535dda79.root

HLTMENU=/users/missirol/test/dev/CMSSW_13_0_0/tmp/test01/cmssw40334/HLT/V3

[ -d run361468 ] || (convertToRaw -f 100 -l 100 -r 361468:172 -o . -- "${INPUTFILE}")

if [ ! -f hlt.py ]; then
  tmpfile=$(mktemp)
  hltConfigFromDB --configName "${HLTMENU}" > "${tmpfile}"
  cat <<EOF >> "${tmpfile}"

process.load('run361468_cff')

process.hltOnlineBeamSpotESProducer.timeThreshold = int(1e6)

#del process.FastTimerService

from HLTrigger.Configuration.common import producers_by_type
for producer in producers_by_type(process, 'PSMonitor'):
  if hasattr(producer, 'FolderName'):
    if not hasattr(producer, 'folderName'):
      producer.folderName = producer.FolderName
    del producer.FolderName
EOF
  edmConfigDump "${tmpfile}" > hlt.py
fi

cmsRun hlt.py &> hlt.log

# diff --git a/DQM/Integration/python/clients/hlt_dqm_clientPB-live_cfg.py b/DQM/Integration/python/clients/hlt_dqm_clientPB-live_cfg.py
# index 4cf721d4f13..968750c68e9 100644
# --- a/DQM/Integration/python/clients/hlt_dqm_clientPB-live_cfg.py
# +++ b/DQM/Integration/python/clients/hlt_dqm_clientPB-live_cfg.py
# @@ -83,5 +83,8 @@ process.psColumnVsLumi = process.dqmCorrelationClient.clone(
#     ),
#  )
#  
# +process.source.datafnPosition = cms.untracked.uint32(4)
#  print("Final Source settings:", process.source)
#  process.p = cms.EndPath( process.fastTimerServiceClient + process.throughputServiceClient + process.psColumnVsLumi + process.dqmEnv + process.dqmSaver + process.dqmSaverPB )
# +
# +open('tmp.py', 'w').write(process.dumpPython())
# 
# cmsRun DQM/Integration/python/clients/hlt_dqm_clientPB-live_cfg.py runInputDir=. runNumber=361468 runkey=pp_run scanOnce=True
