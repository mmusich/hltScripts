#!/bin/bash

# Function to get the base release name without MULTIARCHS and without trailing underscore
get_base_release() {
  local release=$1
  local base_release="${release/MULTIARCHS/}"
  echo "${base_release%_}"
}

# Ensure CMSSW environment is set up
if [ -z "$CMSSW_VERSION" ]; then
  echo "CMSSW environment is not set. Please set up your CMSSW environment."
  exit 1
fi

# Check if the CMSSW version contains MULTIARCHS
if [[ "$CMSSW_VERSION" == *MULTIARCHS* ]]; then
  # Extract the base release name
  BASE_RELEASE=$(get_base_release "$CMSSW_VERSION")
  
  echo "CMSSW version contains MULTIARCHS: $CMSSW_VERSION"
  echo "Base release: $BASE_RELEASE"

  # Check if both versions exist in the local git repository
  if git show-ref --quiet "refs/tags/$CMSSW_VERSION" && git show-ref --quiet "refs/tags/$BASE_RELEASE"; then
    echo "Both versions exist in the local git repository. Proceeding with git diff."
    
    # Compare the commits between the two versions
    DIFF_OUTPUT=$(git diff "refs/tags/$CMSSW_VERSION" "refs/tags/$BASE_RELEASE")
    
    if [ -n "$DIFF_OUTPUT" ]; then
      echo "Differences found between $CMSSW_VERSION and $BASE_RELEASE:"
      echo "$DIFF_OUTPUT"
      exit 1
    else
      echo "No differences found between $CMSSW_VERSION and $BASE_RELEASE."
    fi
  else
    echo "One or both of the releases do not exist in the local git repository."
    exit 1
  fi
else
  echo "CMSSW version does not contain MULTIARCHS: $CMSSW_VERSION"
fi
