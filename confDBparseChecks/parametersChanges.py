import os
import re

def should_skip_file(content):
    # Skip files containing any of these patterns
    skip_patterns = [
        r'cms\.EDProducer',
        r'cms\.EDFilter',
        r'cms\.EDAnalyzer',
        r'cms\.ESProducer'
    ]
    return any(re.search(pattern, content) for pattern in skip_patterns)

def convert_pset_to_dict(content):
    # Convert cms.PSet to dict by handling nested structures
    content = re.sub(r'cms\.PSet\(', r'dict(', content)
    return content

def process_file(file_path):
    # Read the file
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Skip files that contain specific cms.ED* or cms.ESProducer references
    if should_skip_file(content):
        print(f"Skipping: {file_path}")
        return
    
    # Replace all cms.XXX("...") with just "..."
    updated_content = re.sub(r'cms\.string\("(.*?)"\)', r'"\1"', content)
    updated_content = re.sub(r'cms\.double\((.*?)\)', r'\1', updated_content)
    updated_content = re.sub(r'cms\.int32\((.*?)\)', r'\1', updated_content)
    updated_content = re.sub(r'cms\.bool\((True|False)\)', r'\1', updated_content)
    updated_content = re.sub(r'cms\.uint32\((\d+)\)', r'\1', updated_content)
    updated_content = re.sub(r'cms\.vdouble\((.*?)\)', r'[\1]', updated_content)
    updated_content = re.sub(r'cms\.vint32\((.*?)\)', r'[\1]', updated_content)
    updated_content = re.sub(r'cms\.vuint32\((.*?)\)', r'[\1]', updated_content)

    # Convert cms.InputTag("...") with one argument to ("...",)
    updated_content = re.sub(r'cms\.InputTag\("(.*?)"\)', r'("\1")', updated_content)

    # Convert cms.InputTag("...", "...") to ("...", "...")
    updated_content = re.sub(r'cms\.InputTag\("(.*?)",\s*"(.*?)"\)', r'("\1", "\2")', updated_content)

    # Convert cms.PSet to dict
    updated_content = convert_pset_to_dict(updated_content)
    
    # Write back to the file if changes were made
    if updated_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Updated: {file_path}")
    else:
        print(f"No changes: {file_path}")

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith("_cfi.py"):
                process_file(os.path.join(root, file))

# Directories to process
directories = [
    "HLTrigger/Configuration/python/HLT_75e33/modules/",
    "HLTrigger/Configuration/python/HLT_75e33/eventsetup/"
]

# Process each directory
for directory in directories:
    process_directory(directory)
