./makeHLTMenuTabs.py /dev/CMSSW_13_0_0/GRun --meta owners.json

# modify owners.json, then use the following command to write its new version to tmp.json,
# and, if tmp.json is correct, rename it to owners.json
import json
json.dump(json.load(open('owners.json')),open('tmp.json','w'),sort_keys=True, indent=2)

./checkOwners.py /dev/CMSSW_13_0_0/GRun
