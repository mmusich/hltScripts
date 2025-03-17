import os
import re
import sys
import pprint
from collections import defaultdict

import FWCore.ParameterSet.Config as cms

# Load modules as you already have
def load_modules(directory):
    # Base directories for CMSSW release and user area
    release_base_directory = os.path.join(os.environ['CMSSW_RELEASE_BASE'], directory)
    base_directory = os.path.join(os.environ['CMSSW_BASE'], directory)

    loaded_modules = defaultdict(list)

    patterns = {
        "EDProducer": re.compile(r"cms\.EDProducer\(['\"]([^'\"]+)['\"]"),
        "EDFilter": re.compile(r"cms\.EDFilter\(['\"]([^'\"]+)['\"]"),
        "EDAnalyzer": re.compile(r"cms\.EDAnalyzer\(['\"]([^'\"]+)['\"]"),
        "ESProducer": re.compile(r"cms\.ESProducer\(['\"]([^'\"]+)['\"]"),
        "ESSource": re.compile(r"cms\.ESSource\(['\"]([^'\"]+)['\"]")
    }

    def process_directory(base_directory):
        for root, _, files in os.walk(base_directory):
            for file in files:
                if file.endswith('_cfi.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        content = f.read()

                    # Check for direct definitions
                    for key, pattern in patterns.items():
                        matches = pattern.findall(content)
                        for match in matches:
                            loaded_modules[match].append((file, file_path))

                    # Handle indirect imports (from .something import ...)
                    include_match = re.search(r"from \.(\w+) import", content)
                    if include_match:
                        included_file = include_match.group(1) + ".py"
                        included_file_path = os.path.join(root, included_file)
                        if os.path.exists(included_file_path):
                            with open(included_file_path, 'r') as included_file_obj:
                                included_content = included_file_obj.read()
                                for key, pattern in patterns.items():
                                    matches = pattern.findall(included_content)
                                    for match in matches:
                                        loaded_modules[match].append((file, file_path))
                        else:
                            print(f"Included file {included_file} not found for {file_path}")

    process_directory(release_base_directory)
    process_directory(base_directory)

    reverse_loaded_modules = defaultdict(list)
    for module_name, files in loaded_modules.items():
        for file_name, file_path in files:
            reverse_loaded_modules[module_name].append((file_name, file_path))

    print(f"Found {len(reverse_loaded_modules)} modules.")
    return dict(reverse_loaded_modules)

def get_param_differences(auto_params, current_params):
    differences = {}

    for param, value in current_params.items():
        if param not in auto_params:
            differences[param] = value
        elif isinstance(value, dict) and isinstance(auto_params[param], dict):
            # If both are PSet, recursively find differences
            nested_differences = get_param_differences(auto_params[param], value)
            if nested_differences:  # Only add if something changed inside
                differences[param] = f"cms.PSet({', '.join(f'{k} = {v}' for k, v in nested_differences.items())})"
        elif auto_params[param] != value:
            differences[param] = value

    return differences

import re

# Recursively parse nested cms.PSet parameters
def parse_cfi_parameters(content):
    param_pattern = re.compile(r'([\w]+)\s*=\s*(cms\.[\w]+\(.*?\))', re.DOTALL)
    pset_pattern = re.compile(r'([\w]+)\s*=\s*cms\.PSet\((.*?)\)', re.DOTALL)

    def extract_params(text):
        params = {}
        for match in param_pattern.findall(text):
            param_name, param_value = match
            params[param_name] = param_value

        for match in pset_pattern.findall(text):
            pset_name, pset_content = match
            params[pset_name] = extract_params(pset_content)  # Recurse into PSet
        return params

    return extract_params(content)


# Update target modules
def update_modules(supported_modules, target_directory):
    for root, _, files in os.walk(target_directory):
        for file in files:
            if file.endswith('_cfi.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()

                match = re.search(r'cms\.EDProducer\(["\']([\w]+)["\']', content)
                if not match:
                    continue

                module_name = match.group(1)
                if module_name not in supported_modules:
                    print(f"Auto-generated CFI for {module_name} not found in supported_modules")
                    continue

                auto_file, auto_path = supported_modules[module_name][0]
                auto_module_name = os.path.splitext(auto_file)[0]
                auto_dir = os.path.dirname(auto_path).replace('/', '.')
                import_path = f"{auto_dir}.{auto_module_name}"

                # Split the string by "."
                fields = import_path.split(".")
                
                # Get the last two fields
                last_two_fields = ".".join(fields[-3:])
                
                with open(auto_path, 'r') as af:
                    auto_content = af.read()

                pp = pprint.PrettyPrinter(indent=2, width=100, sort_dicts=False)
                    
                auto_params = parse_cfi_parameters(auto_content)
                #pp.pprint(auto_params)
                current_params = parse_cfi_parameters(content)
                #pp.pprint(current_params)
                
                differences = get_param_differences(auto_params, current_params)

                #pp.pprint(differences)    
                
                #print(differences)
                
                new_content = (f"from {last_two_fields} import {module_name} as _{module_name}\n\n"
                               f"{file.replace('_cfi.py', '')} = _{module_name}.clone(\n")


                # Read the old content
                with open(file_path, 'r') as f:
                    old_content = f.readlines()

                # Modify the content
                new_lines = []
                for line in old_content:
                    if "EDProducer" in line:
                        new_lines.append(new_content)  # Replace the line with new_content
                    else:
                        new_lines.append(line)  # Keep other lines unchanged

                # Write the modified content back
                with open(file_path, 'w') as f:
                    f.writelines(new_lines)
                
                # for param, value in differences.items():
                #     if "cms.ED" in str(value):  # Convert to string in case value isn't a string
                #         continue
                #     new_content += f"    {param} = {value},\n"
                # new_content = new_content.rstrip(',\n') + '\n)\n'

                #with open(file_path, 'w') as f:
                #    f.write(new_content)
                print(f"Updated {file_path}")

# Example usage
directory = 'cfipython/el9_amd64_gcc12'
target_directory = 'HLTrigger/Configuration/python/HLT_75e33/modules'
supported_modules = load_modules(directory)
pp = pprint.PrettyPrinter(indent=2, width=100, sort_dicts=False)
#pp.pprint(supported_modules)

update_modules(supported_modules, target_directory)
