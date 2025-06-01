#!/bin/bash

cmsDriver.py bar \
 --no_output --no_exec --dump_python \
 --era Run3_2025 --data --conditions 150X_dataRun3_HLT_v1 \
 -s RAW2DIGI --python_filename l1t_L1TReEmulFromRAW_cfg.py \
 --customise L1Trigger/Configuration/customiseReEmul.L1TReEmulFromRAW

cmsDriver.py foo \
 --no_output --no_exec --dump_python \
 --era Run3_2025 --data --conditions 150X_dataRun3_HLT_v1 \
 -s L1REPACK:Full --python_filename l1t_L1REPACK_Full_cfg_tmp.py

# rename some unpackers in l1t_L1REPACK_Full_cfg_tmp.py
# to match the module labels used in l1t_L1TReEmulFromRAW_cfg.py
sed -i.bak 's/\<unpackEcal\>/ecalDigis/g' l1t_L1REPACK_Full_cfg_tmp.py
sed -i 's/\<unpackHcal\>/hcalDigis/g' l1t_L1REPACK_Full_cfg_tmp.py
sed -i 's/\<unpackDT\>/muonDTDigis/g' l1t_L1REPACK_Full_cfg_tmp.py
sed -i 's/\<unpackCSC\>/muonCSCDigis/g' l1t_L1REPACK_Full_cfg_tmp.py
sed -i 's/\<unpackRPC\>/muonRPCDigis/g' l1t_L1REPACK_Full_cfg_tmp.py
sed -i 's/\<unpackGEM\>/muonGEMDigis/g' l1t_L1REPACK_Full_cfg_tmp.py
sed -i 's/\<unpackOmtf\>/omtfStage2Digis/g' l1t_L1REPACK_Full_cfg_tmp.py
sed -i 's/\<unpackEmtf\>/emtfStage2Digis/g' l1t_L1REPACK_Full_cfg_tmp.py
sed -i 's/\<unpackBmtf\>/bmtfDigis/g' l1t_L1REPACK_Full_cfg_tmp.py
sed -i 's/\<unpackTwinMux\>/twinMuxStage2Digis/g' l1t_L1REPACK_Full_cfg_tmp.py
sed -i 's/\<unpackRPCTwinMux\>/rpcTwinMuxRawToDigi/g' l1t_L1REPACK_Full_cfg_tmp.py
sed -i 's/\<unpackTcds\>/tcdsDigis/g' l1t_L1REPACK_Full_cfg_tmp.py

edmConfigDump l1t_L1REPACK_Full_cfg_tmp.py > l1t_L1REPACK_Full_cfg.py
