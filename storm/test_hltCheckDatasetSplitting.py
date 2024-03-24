import FWCore.ParameterSet.Config as cms
import pprint
import sys

# Create an empty Process object
process = cms.Process("HLT")

process.load("HLTrigger.Configuration.HLT_FULL_cff")

# Get all process attributes
attributes = dir(process)
#print(attributes)

# Define a dictionary to store the offset values for each fragment
offset_values = {}

# Iterate over the attributes
for attr in attributes:
    # Check if the attribute starts with 'fragment.hltPreDataset'
    if attr.startswith('hltPreDataset'):
        fragment = getattr(process, attr)
        #print(fragment)
        # Check if the fragment is an HLT Prescaler filter
        if isinstance(fragment, cms.EDFilter) and fragment.type_() == 'HLTPrescaler':
            # Get the offset value
            offset = fragment.offset.value()            
            # Store the offset value in the dictionary
            offset_values[attr] = offset

# Pretty print offset_values
pprint.pprint(offset_values)

# Define a variable to track errors
has_errors = False

# Check for attributes that differ only by the value of the last digit
for key1 in offset_values:
    for key2 in offset_values:
        if key1 < key2:
            # Extract the last digit of each key
            last_digit1 = key1[-1]
            last_digit2 = key2[-1]
            # Check if the keys have the same prefix and differ only by the value of the last digit
            if key1[:-1] == key2[:-1] and last_digit1 != last_digit2:
                offset1 = offset_values[key1]
                offset2 = offset_values[key2]
                # Check if the keys have the same offset
                if offset1 == offset2:
                    print(f"Error: Attributes {key1} and {key2} have the same offset {offset1}")
                    has_errors = True

# Check if there were any errors
if has_errors:
    # If errors were found, exit with status 1
    print("There were errors detected during attribute comparison. Exiting with status 1.")
    sys.exit(1)
else:
    # If no errors were found, exit with status 0
    print("No errors were detected during attribute comparison. Exiting with status 0.")
    sys.exit(0)
