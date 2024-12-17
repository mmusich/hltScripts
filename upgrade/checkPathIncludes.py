import re
import os
import glob

def find_unused_imports_in_path(file_path):
    # Load the file content
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Step 1: Collect all imports
    imports = {}
    for i, line in enumerate(lines):
        # Match imports like: `from ..sequences.HLTBeginSequence_cfi import *`
        # Also matches imports like: `from ..sequences.HLTDoFullUnpackingEgammaEcalL1SeededSequence_cfi import hltEG30EtL1SeededFilter`
        match = re.match(r'^from \.\.(.*) import (.*)', line)
        if match:
            # Extract module name (after '..sequences' or other parts)
            module_name = match.group(1).strip()
            imported_items = match.group(2).strip()

            # Clean module name to remove the 'sequences.' or 'modules.' part
            module_name_clean = module_name.split('.')[-1]  # Get the last part (e.g., HLTMuonsSequence_cfi)

            # Remove the '_cfi' suffix if it exists
            if module_name_clean.endswith('_cfi'):
                module_name_clean = module_name_clean[:-4]  # Remove last 4 characters (_cfi)
            
            # If it is a wildcard import, just store the module name
            if imported_items == "*":
                imports[module_name_clean] = i + 1  # Store line number where module is imported
            else:
                # Split by commas if multiple items are imported
                for item in imported_items.split(','):
                    item_name = item.strip().split(" as ")[0]  # Capture the name before 'as' if it exists
                    imports[item_name] = i + 1  # Store the line number

    # Print out the collected imports and their line numbers
    #for import_name, line_number in imports.items():
    #    print(f"Imported: {import_name} on line {line_number}")

    # Step 2: Extract modules and sequences used in cms.Path
    in_path = False
    path_modules = set()
    sequence_modules = set()

    for line in lines:
        if 'cms.Path' in line:  # Start of cms.Path definition
            in_path = True
        if in_path:
            # Collect all modules and sequences referenced in the path
            path_modules.update(re.findall(r'\b(\w+)\b', line))
        if ')' in line and in_path:  # End of cms.Path definition
            in_path = False

        # Collect all modules referenced in cms.Sequence
        if 'cms.Sequence' in line:
            sequence_modules.update(re.findall(r'\b(\w+)\b', line))

    # Add modules from sequences to the path_modules set
    path_modules.update(sequence_modules)

    # Step 3: Compare imports and path modules
    unused_imports = set(imports.keys()) - path_modules

    # Step 4: Report results
    if unused_imports:
        print("Unused imports found in cms.Path:")
        for module in unused_imports:
            print(f"{module} at line {imports[module]}")
    else:
        print("All imports are used in cms.Path!")

# Replace with the path to your CMSSW Python file
#find_unused_imports_in_path("HLT_Ele30_WPTight_L1Seeded_LooseDeepTauPFTauHPS30_eta2p1_CrossL1_cfi.py")


# Get all the files ending with '_cfi.py' in the current working directory
cfi_files = glob.glob('*_cfi.py')

# Run the function on all the files
for cfi_file in cfi_files:
    print(f"\nAnalyzing file: {cfi_file}")
    find_unused_imports_in_path(cfi_file)
