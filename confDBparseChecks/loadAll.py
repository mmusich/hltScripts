import os
import importlib.util
import re
from collections import defaultdict
from pprint import pprint

# Specify the base directory
base_directory = os.path.join(os.environ['CMSSW_RELEASE_BASE'], 'cfipython/el9_amd64_gcc12/')

# Dictionary to store the loaded modules
loaded_modules = defaultdict(list)

# Define regular expression patterns to match cms.EDProducer and cms.EDFilter definitions
edproducer_pattern = re.compile(r"cms\.EDProducer\(['\"]([^'\"]+)['\"]")
edfilter_pattern = re.compile(r"cms\.EDFilter\(['\"]([^'\"]+)['\"]")

# Traverse through all folders and subfolders
for root, dirs, files in os.walk(base_directory):
    for file in files:
        # Check if the file has a .py extension
        if file.endswith('.py'):
            # Construct the full path to the file
            file_path = os.path.join(root, file)

            # Read the content of the file
            with open(file_path, 'r') as f:
                content = f.read()

            # Find matches using the regular expression patterns
            edproducer_matches = edproducer_pattern.findall(content)
            edfilter_matches = edfilter_pattern.findall(content)

            # Append the matches to the loaded_modules dictionary
            loaded_modules[file].extend(edproducer_matches)
            loaded_modules[file].extend(edfilter_matches)

# Create the reverse dictionary
reverse_loaded_modules = defaultdict(list)
for file, classes in loaded_modules.items():
    for cls in classes:
        reverse_loaded_modules[cls].append(file)

# Print the reverse loaded modules
pprint(dict(reverse_loaded_modules))
