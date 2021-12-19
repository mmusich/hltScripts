#!/bin/bash

#HLTMENU=/dev/CMSSW_12_3_0/HLT/V72
#PATHS=(
#  HLT_AK8PFJet230_SoftDropMass40_v1
#  HLT_AK8PFJet230_SoftDropMass40_PFAK8ParticleNetBB0p35_v1
#  HLT_AK8PFJet250_SoftDropMass40_PFAK8ParticleNetBB0p35_v1
#  HLT_AK8PFJet275_SoftDropMass40_PFAK8ParticleNetBB0p35_v1
#  HLT_AK8PFJet400_SoftDropMass40_v1
#  HLT_AK8PFJet425_SoftDropMass40_v1
#  HLT_AK8PFJet450_SoftDropMass40_v1
#)
#MAXEVENTS=200
#EDMFILE=/store/mc/Run3Summer21DRPremix/GluGluToHHTo4B_node_cHHH1_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/120X_mcRun3_2021_realistic_v6-v2/30000/69255d81-b9ef-4a9b-8d32-55541b9f9295.root

HLTMENU=/users/rgerosa/boostedHtt/HLT/V5
PATHS=(
  HLT_AK8PFJet230_SoftDropMass40_PFAK8ParticleNetTauTau0p30_v1
  HLT_AK8PFJet250_SoftDropMass40_PFAK8ParticleNetTauTau0p30_v1
  HLT_AK8PFJet275_SoftDropMass40_PFAK8ParticleNetTauTau0p30_v1
)
MAXEVENTS=800
EDMFILE=/store/mc/Run3Winter21DRMiniAOD/GluGluToHHTo2B2Tau_node_cHHH1_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/FlatPU30to80FEVT_112X_mcRun3_2021_realistic_v16-v2/250000/d1a7fb05-6746-4fa8-82fd-9d52d236eac8.root

([ $# -ge 1 ] && [ ! -d $1 ]) || exit 1

OUTDIR="${1}"
mkdir -p "${OUTDIR}"
cd "${OUTDIR}"

for iPath in "${PATHS[@]}"; do

  hltGetConfiguration "${HLTMENU}" --dbproxy --max-events "${MAXEVENTS}" \
   --mc --globaltag auto:phase1_2021_realistic --l1 L1Menu_Collisions2018_v2_1_0-d1_xml \
   --process HLTX --full --offline --output none --prescale none \
   --paths HLTriggerFirstPath,HLTriggerFinalPath,"${iPath}" \
   --input "${EDMFILE}" > hlt_"${iPath}".py

  printf "\n%s %s\n" "`date +%T`" "cmsRun hlt_${iPath}.py &> hlt_${iPath}.log"
  cmsRun hlt_${iPath}.py &> hlt_${iPath}.log; iStatus=$?;
  printf "%s %s\n" "`date +%T`" "`grep -inr TrigReport hlt_${iPath}.log | grep ${iPath} | head -1`"
  printf "%s %s\n" "`date +%T`" "exit status: ${iStatus}"
  unset iStatus
done
unset iPath

cd "${OLDPWD}"

unset HLTMENU PATHS MAXEVENTS EDMFILE OUTDIR
