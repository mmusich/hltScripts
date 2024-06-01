#!/bin/bash

# testCMSHLT3195.sh

runHLT(){
  rm -rf $1
  mkdir -p $1
  cd $1
  hltGetConfiguration $2 \
    --globaltag 140X_dataRun3_HLT_v3 \
    --unprescale \
    --output all \
    --max-events 5000 \
    --paths *RPC* \
    --input /store/data/Run2024E/EphemeralHLTPhysics0/RAW/v1/000/381/150/00000/9bfcd9a7-0a04-42d8-9579-4f8bc71d9c1b.root \
    > hlt.py
  cat <<EOF >> hlt.py
# remove paths containing OutputModules
streamPaths = [pathName for pathName in process.finalpaths_()]
for foo in streamPaths:
    if 'RPCMON' not in foo:
        process.__delattr__(foo)
EOF
  cmsRun hlt.py &> hlt.log
  cd -
}

runHLT out_ref  /dev/CMSSW_14_0_0/GRun/V127
runHLT out_tar1 /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3195/Test01/GRun/V2
runHLT out_tar2 /users/missirol/test/dev/CMSSW_14_0_0/CMSHLT_3195/Test02/GRun/V2
