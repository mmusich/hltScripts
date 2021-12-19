#!/bin/bash -ex

OUTDIR=tmpTest36666

mkdir -p "${OUTDIR}"
cd "${OUTDIR}"

if [ ! -f hlt.py ] ; then
  hltGetConfiguration /dev/CMSSW_12_3_0/GRun/V12 \
   --input /store/relval/CMSSW_12_3_0_pre2/RelValQQToHToTauTau_14TeV/GEN-SIM-DIGI-RAW/PU_122X_mcRun3_2021_realistic_v5-v1/2580000/ba8a1b61-ba47-4e91-a692-0871bd85c703.root \
   --max-events 20 --no-output --no-prescale --mc --globaltag auto:run3_mc_GRun --eras Run3 --dbproxy \
   > hlt.py
fi

cp -p hlt.py tmp.py
cat <<EOF >> tmp.py
process.options.numberOfThreads = 1

process.hltTausTest0 = process.hltHpsL1JetsHLTPFTauTrackLooseChargedIsolationAgainstMuonMatch.clone()
process.hltTausTest1 = process.hltHpsL1JetsHLTPFTauTrackLooseChargedIsolationAgainstMuonMatch.clone()

from RecoTauTag.RecoTau.pfTauPrimaryVertexProducer_cfi import pfTauPrimaryVertexProducer as _PFTauPrimaryVertexProducer
process.hltTauPVATagsTest0 = _PFTauPrimaryVertexProducer.clone(
  PFTauTag = 'hltTausTest0',
  PVTag = 'hltPixelVertices',
  useBeamSpot = False,
  qualityCuts = dict(primaryVertexSrc = 'hltPixelVertices'),
  discriminators = cms.VPSet(),
)

from RecoTauTag.RecoTau.PFTauSecondaryVertexProducer_cfi import PFTauSecondaryVertexProducer as _PFTauSecondaryVertexProducer
process.hltTauSVATagsTest0 = _PFTauSecondaryVertexProducer.clone(PFTauTag = 'hltTausTest0')

from RecoTauTag.RecoTau.PFTauTransverseImpactParameters_cfi import PFTauTransverseImpactParameters as _PFTauTransverseImpactParameters
process.hltTauIPsTest0 = _PFTauTransverseImpactParameters.clone(
  PFTauTag = 'hltTausTest0',
  PFTauPVATag = 'hltTauPVATagsTest0',
  PFTauSVATag = 'hltTauSVATagsTest0',
)

from RecoTauTag.HLTProducers.hltTauIPFilter_cfi import hltTauIPFilter as _hltTauIPFilter
process.hltTestTauIPFilterCorrect = _hltTauIPFilter.clone(
  Taus = 'hltTausTest0',
  TausIP = 'hltTauIPsTest0',
  MinN = -1,
)

process.hltTestTauIPFilterIncorrect = _hltTauIPFilter.clone(
  Taus = 'hltTausTest1',
  TausIP = 'hltTauIPsTest0',
  MinN = -1,
)

process.HLTTestTauSeq = cms.Sequence(
    process.hltTausTest0
  + process.hltTausTest1
  + process.hltTauPVATagsTest0
  + process.hltTauSVATagsTest0
  + process.hltTauIPsTest0
  + process.hltTestTauIPFilterCorrect
  + process.hltTestTauIPFilterIncorrect
)

_pathName = 'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v4'
_path = getattr(process, _pathName)
_path.insert(_path.index(process.HLTEndSequence), process.HLTTestTauSeq)
process.setSchedule_(cms.Schedule(_path))
EOF

python3 tmp.py
cmsRun tmp.py &> tmp.log
