import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Function to run a shell command and handle errors
def run_command(command, workdir=None):
    try:
        print(f"Running command: {command}")
        subprocess.run(command, shell=True, check=True, cwd=workdir)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")

# Step 1: Run cmsDriver.py for TTbar GEN,SIM steps
ttbar_command = (
    "cmsDriver.py TTbar_14TeV_TuneCP5_cfi -s GEN,SIM -n 1 "
    "--conditions auto:phase2_realistic_T33 --beamspot DBrealisticHLLHC --datatier GEN-SIM "
    "--eventcontent FEVTDEBUG --geometry Extended2026D110 --era Phase2C17I13M9 "
    "--relval 9000,100 --fileout file:step1.root"
)

print("Running TTbar GEN,SIM step...")
run_command(ttbar_command)

# Directory containing HLT test configurations
hlt_configs_dir = "hlt_test_configs"

# Check if the directory exists
if not os.path.exists(hlt_configs_dir):
    print(f"Directory {hlt_configs_dir} not found! Exiting...")
    exit(1)

# Step 2: Function to run cmsRun on a given HLT config file
def run_cmsrun(config_file):
    cmsrun_command = f"cmsRun {config_file}"
    run_command(cmsrun_command)

# Step 3: Loop through all files in hlt_test_configs and run cmsRun on each in parallel
config_files = [f for f in os.listdir(hlt_configs_dir) if f.endswith(".py")]
print(f"Found {len(config_files)} configuration files in {hlt_configs_dir}.")

# Set the number of parallel jobs (e.g., 4)
num_parallel_jobs = 4

# Run cmsRun on all config files in parallel
with ThreadPoolExecutor(max_workers=num_parallel_jobs) as executor:
    for config_file in config_files:
        config_path = os.path.join(hlt_configs_dir, config_file)
        executor.submit(run_cmsrun, config_path)

print("All cmsRun jobs submitted.")
