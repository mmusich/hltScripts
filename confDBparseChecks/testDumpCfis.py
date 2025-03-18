import os
import subprocess

# ANSI escape codes for color formatting
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Define the directories and corresponding module paths
directories = {
    "HLTrigger/Configuration/python/HLT_75e33/modules/": "HLTrigger.Configuration.HLT_75e33.modules",
    "HLTrigger/Configuration/python/HLT_75e33/eventsetup/": "HLTrigger.Configuration.HLT_75e33.eventsetup"
}

# Iterate over both directories
for dir_path, module_base in directories.items():
    if not os.path.exists(dir_path):
        print(f"Warning: Directory {dir_path} not found! Skipping...")
        continue

    # Get all Python files in the directory
    module_files = [f for f in os.listdir(dir_path) if f.endswith(".py")]

    print(f"\nFound {len(module_files)} module files in {dir_path}. Testing each one...\n")

    # Iterate over each module file
    for module_file in module_files:
        module_name = module_file.replace(".py", "")  # Remove .py extension

        # Define the interactive Python script to test the module
        test_script = f"""
import FWCore.ParameterSet.Config as cms
process = cms.Process("TEST")
try:
    process.load("{module_base}.{module_name}")
    process.dumpPython()
    print("[SUCCESS] {module_base}.{module_name}")
except Exception as e:
    print("[CRASH] {module_base}.{module_name} ->", str(e))
"""

        print(f"Testing {module_base}.{module_name}...")

        # Run the test script in a subprocess
        result = subprocess.run(
            ["python3", "-c", test_script],
            capture_output=True,
            text=True
        )

         # Process the output
        if "[CRASH]" in result.stdout:
            print(f"{RED}{result.stdout.strip()}{RESET}")  # Print in red
        elif result.returncode != 0:
            print(f"{RED}[CRASH] {module_base}.{module_name} -> Non-zero exit code{RESET}")
        else:
            pass
            #print(f"{GREEN}[SUCCESS] {module_base}.{module_name}{RESET}")
        
print("\nTesting complete!")
