deprecated_bits_file = "deprecatedbits.txt"
hlt_grun_cff_file = "HLT_GRun_cff.py"

# Read lines from deprecated bits file
with open(deprecated_bits_file, 'r') as deprecated_file:
    deprecated_bits = [line.strip() for line in deprecated_file.readlines()]

# Count occurrences in HLT_GRun_cff.py
occurrences_count = {bit: 0 for bit in deprecated_bits}

with open(hlt_grun_cff_file, 'r') as hlt_file:
    for line in hlt_file:
        for bit in deprecated_bits:
            if bit in line:
                occurrences_count[bit] += 1

# Print results for occurrences larger than 0
for bit, count in occurrences_count.items():
    if count > 0:
        print(f"Bit: {bit}, Occurrences in {hlt_grun_cff_file}: {count}")
