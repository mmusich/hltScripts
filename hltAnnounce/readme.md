./makeHLTMenuTabs.py /dev/CMSSW_13_0_0/GRun --meta owners.json

import json
json.dump(json.load(open('owners.json')),open('tmp.json','w'),sort_keys=True, indent=2)
