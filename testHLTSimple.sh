#!/bin/bash -ex

outDir=tmp_testHLTTracks"${1}"

for inputType in mc ; do

  for hltMenu in GRun ; do

    hltGetConfOpts="--output minimal --unprescale"

    if [ "${inputType}" = "mc" ]; then
      hltGetConfOpts+=" --max-events 100"
    elif [ "${inputType}" = "data" ]; then
      hltGetConfOpts+=" --max-events 200"
    fi

    hltGetConfOpts+=" ${2}"

    if [ "${inputType}" = "mc" ] && [ "${hltMenu}" = "GRun" ]; then
      hltGetConfOpts+=" --input /store/relval/CMSSW_12_2_0_pre2/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/122X_mcRun3_2021_realistic_v1-v1/2580000/5541adab-cc2d-4401-b069-8140c90078c8.root --mc --globaltag auto:run3_mc_GRun --eras Run3"
    elif [ "${inputType}" = "mc" ] && [ "${hltMenu}" = "HIon" ]; then
      hltGetConfOpts+=" --input file:/work/missiroli_m/test/tsg/storm/test_36459/CMSSW_12_3_X_2021-12-30-1100/src/addOnTests/hlt_mc_HIon/RelVal_Raw_HIon_MC.root --mc --globaltag auto:run3_mc_HIon --eras Run3"
    elif [ "${inputType}" = "data" ] && [ "${hltMenu}" = "GRun" ]; then
      hltGetConfOpts+=" --input /store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/2E066536-5CF2-B340-A73B-209640F29FF6.root --data --globaltag auto:run3_hlt_GRun --eras Run2_2018 --customise HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input"
    elif [ "${inputType}" = "data" ] && [ "${hltMenu}" = "HIon" ]; then
      continue
    fi

    jobTag="${inputType}"_"${hltMenu}"

    outSubDir="${outDir}"/"${jobTag}"
    rm -rf "${outSubDir}"
    mkdir -p "${outSubDir}"
    pushd "${outSubDir}"

    hltGetConfiguration --dbproxy /dev/CMSSW_12_3_0/"${hltMenu}" ${hltGetConfOpts} > hlt_"${inputType}"_"${hltMenu}"_cfg.py

    for idx in {0..0}; do

      cp -p hlt_"${inputType}"_"${hltMenu}"_cfg.py hlt_"${inputType}"_"${hltMenu}"_cfg"${idx}".py

      cat <<EOF >> hlt_"${inputType}"_"${hltMenu}"_cfg"${idx}".py
process.options.numberOfThreads = 1
process.hltOutputMinimal.fileName = 'hlt_${inputType}_${hltMenu}_output${idx}.root'
EOF
      python3 hlt_"${inputType}"_"${hltMenu}"_cfg"${idx}".py
      edmConfigDump hlt_"${inputType}"_"${hltMenu}"_cfg"${idx}".py > hlt_"${inputType}"_"${hltMenu}"_cfg"${idx}"_dump.py
      cmsRun hlt_"${inputType}"_"${hltMenu}"_cfg"${idx}".py &> hlt_"${inputType}"_"${hltMenu}"_cfg"${idx}".log

      /work/missiroli_m/test/tsg/storm/scripts/hltTests/hltFWLite_exa03.py -v 10 \
        -i hlt_"${inputType}"_"${hltMenu}"_output"${idx}".root \
         > hlt_"${inputType}"_"${hltMenu}"_output"${idx}".txt
    done; unset idx

    popd

    unset hltGetConfOpts jobTag outSubDir
  done; unset inputType

done; unset hltMenu

unset outDir
