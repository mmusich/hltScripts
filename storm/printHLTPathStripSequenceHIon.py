import FWCore.ParameterSet.Config as cms
import re
from OnLine_HLT_HIon import process  # Import your CMSSW process from the config file

# Function to map datasets to streams
def map_datasets_to_streams(process):
    stream_map = {}

    # Get the 'streams' attribute from the process (which is a cms.PSet)
    if hasattr(process, 'streams'):
        streams = process.streams

        # Loop through each stream (attribute of the 'streams' PSet)
        for stream_name in streams.parameterNames_():
            stream_datasets = getattr(streams, stream_name)

            # Check if it's a cms.vstring (list of datasets)
            if isinstance(stream_datasets, cms.vstring):
                for dataset in stream_datasets:
                    # Map each dataset to its stream
                    stream_map[dataset] = stream_name

    return stream_map

# Debug: Print the mapping to verify
#datasets_to_streams = map_datasets_to_streams(process)
#print("Dataset to Stream Mapping:")
#for dataset, stream in datasets_to_streams.items():
#    print(f"Dataset: {dataset}, Stream: {stream}")

# Function to print HLT Paths and Output Modules for each dataset
def printHLTPathsAndOutputModules(process):
    dataset_to_stream = map_datasets_to_streams(process)
    unique_datasets = {}

    # Collapse similar dataset names by stripping trailing numbers
    for dataset_name, trigger_list in process.datasets.parameters_().items():
        base_name = re.sub(r'\d+$', '', dataset_name)
        if base_name not in unique_datasets:
            unique_datasets[base_name] = trigger_list
        else:
            unique_datasets[base_name].extend(trigger_list)  # Combine triggers from similar datasets

    output_modules = {mod: getattr(process, mod) for mod in dir(process) if mod.startswith('hltOutput')}

    # Iterate through unique datasets
    for dataset_name, trigger_list in unique_datasets.items():
        print("*"*40)
        print(f"Dataset: {dataset_name}")

        # Find the stream for the current dataset
        stream_name = dataset_to_stream.get(dataset_name, None)

        if not stream_name:
            # Attempt to append numeric suffixes and check again
            for i in range(1):  # Check for suffixes 0-9
                suffix_attempt = f"{dataset_name}{i}"
                #print(suffix_attempt)  # Debugging output
                #print(dataset_to_stream)  # Debugging output
                stream_name = dataset_to_stream.get(suffix_attempt, None)

                # Check if stream_name is found
                #if stream_name is not None:
                #    break  # Break out of loop if found

                
        if stream_name:
            # Get the output module for the stream
            relevant_output_module = output_modules.get(f"hltOutput{stream_name}", None)

            if relevant_output_module and hasattr(relevant_output_module, 'outputCommands'):
                fed_entries = [cmd for cmd in relevant_output_module.outputCommands if 'FEDRawDataCollection' in cmd]

                if fed_entries:
                    print(f"Output Module for Dataset: hltOutput{stream_name}")
                    print("FEDRawDataCollection entries:")
                    for entry in fed_entries:
                        print(f"  {entry}")
                else:
                    print(f"Output Module for Dataset: hltOutput{stream_name}")
                    entries = [cmd for cmd in relevant_output_module.outputCommands if 'keep' in cmd]                      
                    for entry in entries:
                        print(f" {entry}")
                        
        print("")
        # Print HLT paths and relevant Strip components
        for trigger in set(trigger_list):  # Avoid duplicates
            trigger_path_name = f"process.{trigger}"
            if hasattr(process, trigger):
                trigger_path = getattr(process, trigger)

                # Extract only the parts that contain "Strip"
                path_content = trigger_path.dumpPython()
                strip_parts = [part.strip() for part in path_content.split('+') if 'Strip' in part]

                if strip_parts:
                    # Print path name and relevant parts containing 'Strip'
                    strip_part_str = ', '.join(strip_parts)
                    print(f"Path: {trigger} | Strip Local Reco: {strip_part_str}")
                else:
                    # Print path name even if no 'Strip' components are found
                    print(f"Path: {trigger} | Strip Local Reco: None")

# Call the function to print the combined output for datasets
printHLTPathsAndOutputModules(process)
