# CMSHLT-3284

Instructions for the investigations in `CMSSW_14_0_X_2024-08-26-230/src` (on `lxplus8-gpu`):
```
./testMenu.sh     
mkdir ref
mkdir base
cp hlt1.root ref
cp hlt2.root base/hlt1.root
cd comparisons
python3 validateJR.py --base ../base/ --ref ../ref/
```

this will create a folder `CMSSW_14_0_X_2024-08-26-230/src/all_HLTX_hlt1` with all the plots in it.