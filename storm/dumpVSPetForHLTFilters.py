filters = []

with open("filters_with_saveTags.log") as f:
    for line in f:
        line = line.strip()
        if line.startswith("fullname:"):
            # Extract the substring after "name:"
            parts = line.split(":")
            if len(parts) == 2:
                name = parts[1].strip()
                filters.append(name)

print("filters = cms.VPSet(")
for name in filters:
    print(f"  cms.PSet(")
    print(f"        name = cms.string('{name}'),")
    print(f"        type = cms.uint32(0),")
    print(f"        ptMin = cms.untracked.double(0),")
    print(f"        ptMax = cms.untracked.double(200)")
    print(f"      ),")
print(")")
