#!/bin/bash -ex

# Check if the run number is provided as an argument
if [ $# -lt 1 ]; then
    echo "Usage: $0 <run_number>"
    exit 1
fi

# Get the run number from the first argument
RUN_NUMBER=$1

# Define the source and destination directories using the run number
SRC_DIR="hilton-c2b02-44-01:/store/error_stream/run${RUN_NUMBER}/"
DEST_DIR="/eos/cms/store/group/tsg/FOG/error_stream/"
ROOT_SCRIPT="/eos/cms/store/group/tsg/FOG/error_stream_root.sh"
ROOT_DIR="/eos/cms/store/group/tsg/FOG/error_stream_root/run${RUN_NUMBER}/"

# Copy files from the source to the destination
scp -r -o ProxyJump=cmsusr "$SRC_DIR" "$DEST_DIR"

# Run the external root script with the provided run number
"$ROOT_SCRIPT" "$RUN_NUMBER"

# List the contents of the target directory
ls "$ROOT_DIR"
