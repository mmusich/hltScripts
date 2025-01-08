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

def load_modules(directory):
    # Specify the base directory
    base_directory = os.path.join(os.environ['CMSSW_RELEASE_BASE'], directory)

    # Dictionary to store the loaded modules
    loaded_modules = defaultdict(list)

    # Define regular expression patterns to match cms.EDProducer and cms.EDFilter definitions
    edproducer_pattern = re.compile(r"cms\.EDProducer\(['\"]([^'\"]+)['\"]")
    edfilter_pattern = re.compile(r"cms\.EDFilter\(['\"]([^'\"]+)['\"]")
    edanalyzer_pattern = re.compile(r"cms\.EDAnalyzer\(['\"]([^'\"]+)['\"]")

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

                    # Append the matches to the loaded_modules dictionary
                    loaded_modules[file].extend(edproducer_matches)
                    loaded_modules[file].extend(edfilter_matches)
                    loaded_modules[file].extend(edanalyzer_matches)

    # Create the reverse dictionary
    reverse_loaded_modules = defaultdict(list)
    for file, classes in loaded_modules.items():
        for cls in classes:
            reverse_loaded_modules[cls].append(file)

    return dict(reverse_loaded_modules)

# Assuming you are in the 'test' directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the python directory
python_directory = os.path.join(current_directory, '..', 'python')

# Construct the path to the file
file_path = os.path.join(python_directory, 'HLT_FULL_cff.py')

# Check if the file exists
if os.path.exists(file_path):
    # Load the module dynamically
    spec = importlib.util.spec_from_file_location('HLT_FULL_cff', file_path)
    hlt_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hlt_module)

    # Check if 'fragment' attribute exists in the module
    if hasattr(hlt_module, 'fragment'):
        fragment = getattr(hlt_module, 'fragment')

        # Get all members of the 'fragment'
        fragment_members = inspect.getmembers(fragment)

        # Extract names of objects that are instances of cms.EDFilter or cms.EDProducer
        ed_objects = [
            name
            for name, obj in fragment_members
            if isinstance(obj, (hlt_module.cms.EDFilter, hlt_module.cms.EDProducer, hlt_module.cms.EDAnalyzer))
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
        for class_name in unique_class_names:
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
