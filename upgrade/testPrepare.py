import os
import subprocess
import re

# Define the cmsDriver.py command to create the base configuration
base_cmsdriver_command = (
    "cmsDriver.py step2 -s DIGI:pdigi_valid,L1TrackTrigger,L1,L1P2GT,DIGI2RAW,HLT:75e33_timing "
    "--conditions auto:phase2_realistic_T33 --datatier GEN-SIM-DIGI-RAW -n 1 --eventcontent FEVTDEBUGHLT "
    "--geometry Extended2026D110 --era Phase2C17I13M9 --filein file:step1.root --fileout file:step2.root --no_exec"
)

# The base configuration file and the dumped configuration file
base_config_file = "step2_DIGI_L1TrackTrigger_L1_L1P2GT_DIGI2RAW_HLT.py"
dumped_config_file = "step2_dump.py"

# Directory where all test configurations will be stored
output_dir = "hlt_test_configs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Step 1: Run the cmsDriver.py command to generate the base configuration
print(f"Running cmsDriver.py to generate the base config: {base_config_file}")
subprocess.run(base_cmsdriver_command, shell=True)

# Step 2: Use edmConfigDump to dump the full configuration
print(f"Dumping the full configuration using edmConfigDump to {dumped_config_file}")
with open(dumped_config_file, "w") as dump_file:
    subprocess.run(f"edmConfigDump {base_config_file} > {dumped_config_file}", shell=True, stdout=dump_file)

# Step 3: Extract the list of HLT paths from the dumped configuration
print(f"Extracting HLT paths from {dumped_config_file}...")

# Read the dumped configuration to extract HLT paths
with open(dumped_config_file, "r") as f:
    config_content = f.read()

# Use regex to find all HLT paths defined in process.schedule (Assumes paths start with 'process.')
hlt_paths = re.findall(r"process\.(HLT_[A-Za-z0-9_]+)", config_content)

if not hlt_paths:
    print("No HLT paths found in the schedule!")
    exit(1)

print(f"Found {len(hlt_paths)} HLT paths.")

# Step 4: Debugging: Print a portion of the config to examine the schedule syntax
config_excerpt = config_content[:2000]  # First 2000 characters for inspection
print(f"Configuration excerpt for inspection:\n{config_excerpt}")

# Step 5: Broadened Regex for Matching process.schedule
# We'll allow for extra spaces, newlines, or formatting issues around the schedule assignment
schedule_match = re.search(
    r"(process\.schedule\s*=\s*cms\.Schedule\(\*?\s*\[)([\s\S]+?)(\]\s*\))", 
    config_content
)

if not schedule_match:
    print("No schedule match found after tweaking regex! Exiting...")
    exit(1)
else:
    # Log the matched schedule section
    print(f"Matched schedule section:\n{schedule_match.group(0)}")

# Step 6: Generate N configurations by modifying the dumped config to keep only one path at a time
for path_name in hlt_paths:
    # Create a new configuration file for this path
    config_filename = os.path.join(output_dir, f"step2_{path_name}.py")
    
    # Define regex to find all HLT paths in the cms.Schedule and replace them
    def replace_hlt_paths(match):
        # Get all paths inside the square brackets
        all_paths = match.group(2).split(", ")
        
        # Keep non-HLT paths, and include only the current HLT path
        filtered_paths = [path for path in all_paths if "HLT_" not in path or f"process.{path_name}" in path]

        # Log the filtered paths for debugging
        #print(f"Filtered paths for {path_name}:\n{filtered_paths}")

        # Join the filtered paths back, preserving original formatting
        return match.group(1) + ", ".join(filtered_paths) + match.group(3)

    # Apply the regex to remove all HLT paths except the current one
    modified_content = re.sub(
        r"(process\.schedule\s*=\s*cms\.Schedule\(\*?\s*\[)([\s\S]+?)(\]\s*\))",
        replace_hlt_paths,
        config_content
    )

    # Write the new config to a file
    with open(config_filename, "w") as new_config:
        new_config.write(modified_content)
    
    print(f"Generated config: {config_filename}")

# Optionally, print a success message
print(f"Generated {len(hlt_paths)} configuration files in the {output_dir} directory.")
