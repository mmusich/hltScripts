# ANSI escape code for text color
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'  # Reset color to default

import os
import importlib.util
import re
import inspect
from collections import defaultdict
from pprint import pprint
import subprocess

def create_cmssw_config():
    # Define the folder and filenames
    folder_name = "hlt_test_configs"
    config_filename = os.path.join(folder_name, "phase2_cfg.py")
    dump_filename = os.path.join(folder_name, "Phase2_dump.py")

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created folder: {folder_name}")

    # Write the CMSSW configuration file
    config_content = """
import FWCore.ParameterSet.Config as cms
process = cms.Process("HLT")
process.load("HLTrigger.Configuration.HLT_75e33_cff")
    """

    with open(config_filename, "w") as config_file:
        config_file.write(config_content)

    print(f"Configuration file created: {config_filename}")

    # Run edmConfigDump and save the output
    try:
        with open(dump_filename, "w") as dump_file:
            subprocess.run(
                ["edmConfigDump", config_filename],
                stdout=dump_file,
                check=True
            )
        print(f"Configuration dump saved to: {dump_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running edmConfigDump: {e}")
    except FileNotFoundError:
        print("The edmConfigDump command was not found. Ensure CMSSW is set up correctly.")

def run_hlt_phase2_upgrade():
    try:
        # Execute the command and capture the output
        result = subprocess.run(
            ["hltPhase2UpgradeIntegrationTests", "--dryRun"],
            check=True,  # Raises an exception if the command fails
            text=True,   # Ensures the output is captured as a string
            capture_output=True  # Captures both stdout and stderr
        )
        
        # Print the command output
        print("Command Output:")
        print(result.stdout)
        
    except subprocess.CalledProcessError as e:
        # Print the error message if the command fails
        print("Command failed with error:")
        print(e.stderr)

def load_modules(directory):
    # Specify the base directory
    base_directory = os.path.join(os.environ['CMSSW_RELEASE_BASE'], directory)

    # Dictionary to store the loaded modules
    loaded_modules = defaultdict(list)

    # Define regular expression patterns to match cms.EDProducer and cms.EDFilter definitions
    edproducer_pattern = re.compile(r"cms\.EDProducer\(['\"]([^'\"]+)['\"]")
    edfilter_pattern = re.compile(r"cms\.EDFilter\(['\"]([^'\"]+)['\"]")
    edanalyzer_pattern = re.compile(r"cms\.EDAnalyzer\(['\"]([^'\"]+)['\"]")
    esproducer_pattern = re.compile(r"cms\.ESProducer\(['\"]([^'\"]+)['\"]")
    essource_pattern = re.compile(r"cms\.ESSource\(['\"]([^'\"]+)['\"]")

    # Traverse through all folders and subfolders
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            # Check if the file has a .py extension
            if file.endswith('_cfi.py'):
                # Construct the full path to the file
                file_path = os.path.join(root, file)

                # Read the content of the _cfi.py file
                with open(file_path, 'r') as f:
                    content = f.read()

                # Look for the `from .<module> import <class>` pattern
                match = re.search(r"from \.(\w+) import", content)
                if match:
                    included_file = match.group(1) + ".py"  # Get the included file name
                    included_file_path = os.path.join(root, included_file)  # Construct its path

                    # Check if the included file exists
                    if os.path.exists(included_file_path):
                        with open(included_file_path, 'r') as included_file_obj:
                            included_content = included_file_obj.read()
                            #print(included_file_path, '\n', included_content)
                    else:
                        print(f"Included file {included_file} not found for {file_path}")

                    # Find matches using the regular expression patterns
                    edproducer_matches = edproducer_pattern.findall(included_content)
                    edfilter_matches = edfilter_pattern.findall(included_content)
                    edanalyzer_matches = edanalyzer_pattern.findall(included_content)
                    esproducer_matches = esproducer_pattern.findall(included_content)
                    essource_matches = essource_pattern.findall(included_content)

                    # Append the matches to the loaded_modules dictionary
                    loaded_modules[file].extend(edproducer_matches)
                    loaded_modules[file].extend(edfilter_matches)
                    loaded_modules[file].extend(edanalyzer_matches)
                    loaded_modules[file].extend(esproducer_matches)
                    loaded_modules[file].extend(essource_matches)

    # Create the reverse dictionary
    reverse_loaded_modules = defaultdict(list)
    for file, classes in loaded_modules.items():
        for cls in classes:
            reverse_loaded_modules[cls].append(file)

    return dict(reverse_loaded_modules)

# prepare the area
create_cmssw_config()
#run_hlt_phase2_upgrade()

# Assuming you are in the 'test' directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the python directory
python_directory = os.path.join(current_directory, 'hlt_test_configs')

# Construct the path to the file
file_path = os.path.join(python_directory, 'Phase2_dump.py')

# Check if the file exists
if os.path.exists(file_path):
    # Load the module dynamically
    spec = importlib.util.spec_from_file_location('Phase2_dump', file_path)
    hlt_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hlt_module)

    # Check if 'fragment' attribute exists in the module
    if hasattr(hlt_module, 'process'):
        fragment = getattr(hlt_module, 'process')

        # Get all members of the 'fragment'
        fragment_members = inspect.getmembers(fragment)

        # Extract names of objects that are instances of cms.EDFilter or cms.EDProducer
        ed_objects = [
            name
            for name, obj in fragment_members
            if isinstance(obj, (hlt_module.cms.EDFilter, hlt_module.cms.EDProducer, hlt_module.cms.EDAnalyzer, hlt_module.cms.ESProducer, hlt_module.cms.ESSource))
        ]

        # Extract the class names from the repr of the objects
        #class_names = [
        #    repr(getattr(fragment, obj)).split('(')[1].split(' ')[0]
        #    for obj in ed_objects
        #]

        # Extract the class names from the repr of the objects and clean them up
        class_names = [
            repr(getattr(fragment, obj)).split('(')[1].split(' ')[0].strip().replace(',', '').replace('"','')
            for obj in ed_objects
        ]
    
        # Remove duplicates and blanks using set
        unique_class_names = set(filter(None, class_names))
        sorted_class_names = sorted(unique_class_names)
        
        # Print the list of unique cms.EDFilter and cms.EDProducer class names
        #print("List of unique cms.EDFilter, cms.EDProducer and cms.EDAnalyzer class names in 'fragment':")
        #for class_name in unique_class_names:
        #    print(f"- {class_name}")

        # Load modules and create the reverse dictionary
        reverse_loaded_modules = load_modules('cfipython/el9_amd64_gcc12/')

        #pprint(dict(reverse_loaded_modules))

        keys_list = list(reverse_loaded_modules.keys())
        #print(keys_list)

        #print(keys_list)
        #print(unique_class_names)
        
        # Check if each unique class name is in any key of the reverse dictionary
        for class_name in sorted_class_names:
            if(class_name in  keys_list):
                pass
                #print(GREEN + f"{class_name} is found in the loaded modules." + RESET)
            else:
                #pass
                print(RED + f"{class_name} is NOT found in the loaded modules." + RESET)
    else:
        print("Error: 'fragment' attribute not found in the module.")

else:
    print(f"Error: File '{file_path}' not found.")
