import json
json.dump(json.load(open('owners.json')),open('tmp.json','w'),sort_keys=True, indent=2)
