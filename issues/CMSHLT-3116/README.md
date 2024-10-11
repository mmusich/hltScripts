# CMSHLT-3284

Instructions for the investigations in `CMSSW_14_0_16/src` (on `lxplus8-gpu`):
```
./git.sh     
mkdir ref
mkdir base
cp hlt_git_full_3.root ref
cp hlt_git_full_4.root base/hlt_git_full_3.root
cd comparisons
python3 validateJR.py --base ../base/ --ref ../ref/
```

this will create a folder `CMSSW_14_0_16/src/all_HLTX_hlt1` with all the plots in it.