Quick recipe:
```
# check if there are Paths without owners
./listPathsWithoutOwners.py /dev/CMSSW_13_2_0/GRun --meta owners.json

# if there are Paths without owners, update the file owners.json accordingly
#  - modify owners.json manually
#  - use the command below to write a new version of it to tmp.json
#  - check tmp.json: if it is correct, rename it manually to owners.json
import json
json.dump(json.load(open('owners.json')),open('tmp.json','w'),sort_keys=True, indent=2)

# produce the .csv files summarising the content of the HLT menu
./makeHLTMenuTabs.py /dev/CMSSW_13_2_0/GRun --meta owners.json --prescale 2e34
```
