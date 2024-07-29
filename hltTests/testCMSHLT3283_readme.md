GPU-vs-CPU comparisons after the integrations of CMSHLT-3281.
 - ~225k events of EphemeralHLTPhysics data from run-383631 (PU ~64).
 - Running 2 jobs with 32 threads and 24 streams each (full machine).
 - No HLT prescales applied.
 - Scripts used to run jobs and harvest outputs can be found in this directory.

Case "CMSSW_14_0_12".
 - Release: `CMSSW_14_0_12`.
 - Node: `gpu-c2a02-39-02`.

Case "CMSSW_14_0_12_MULTIARCHS".
 - Release: `CMSSW_14_0_12_MULTIARCHS`.
 - Node: `gpu-c2a02-39-03`.

Commands to produce hltDiff outputs.
```
hltDiff -j -c \
  -o /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/output_CMSSW_14_0_12/hlt240728_AlpakaSerialSync.root \
  -n /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/output_CMSSW_14_0_12_MULTIARCHS/hlt240728_AlpakaSerialSync.root \
  -F /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/hltDiff_AlpakaSerialSync_x8664v2_vs_x8664v3 \
   > /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/hltDiff_AlpakaSerialSync_x8664v2_vs_x8664v3.txt

hltDiff -j -c \
  -o /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/output_CMSSW_14_0_12/hlt240728_AlpakaGPU.root \
  -n /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/output_CMSSW_14_0_12_MULTIARCHS/hlt240728_AlpakaGPU.root \
  -F /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/hltDiff_AlpakaGPU_x8664v2_vs_x8664v3 \
   > /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/hltDiff_AlpakaGPU_x8664v2_vs_x8664v3.txt

hltDiff -j -c \
  -o /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/output_CMSSW_14_0_12/hlt240728_AlpakaSerialSync.root \
  -n /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/output_CMSSW_14_0_12/hlt240728_AlpakaGPU.root \
  -F /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/hltDiff_x8664v2_AlpakaSerialSync_vs_AlpakaGPU \
   > /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/hltDiff_x8664v2_AlpakaSerialSync_vs_AlpakaGPU.txt

hltDiff -j -c \
  -o /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/output_CMSSW_14_0_12_MULTIARCHS/hlt240728_AlpakaSerialSync.root \
  -n /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/output_CMSSW_14_0_12_MULTIARCHS/hlt240728_AlpakaGPU.root \
  -F /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/hltDiff_x8664v3_AlpakaSerialSync_vs_AlpakaGPU \
   > /eos/cms/store/group/tsg/STEAM/validations/CMSHLT-3281/check03/hltDiff_x8664v3_AlpakaSerialSync_vs_AlpakaGPU.txt
