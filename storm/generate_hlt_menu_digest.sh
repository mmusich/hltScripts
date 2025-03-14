#!/bin/bash

filter_hlt_l1_changes() {
    local release=$1
    # Fetch the release notes using curl
    release_notes=$(curl -s "https://api.github.com/repos/cms-sw/cmssw/releases/tags/$release")

    # Check if the API returned a rate limit exceeded message
    if echo "$release_notes" | grep -q "API rate limit exceeded"; then
        echo "GitHub API rate limit exceeded. Please authenticate to increase your request limit."
        return
    fi
    
    # Check if there are any release notes or if the release doesn't exist
    if [[ "$release_notes" == *"Not Found"* ]]; then
        echo "Release $release does not exist."
        return
    fi

    # Check if there are any release notes
    if [ -z "$release_notes" ]; then
        echo "No release notes found for $release"
        return
    fi

    #echo $release_notes
    
    # Extract the changelog entries from the release notes JSON
    changelog_entries=$(echo "$release_notes" | jq -r '.body' | grep -i -E '`hlt`|`l1`')

    # Print the filtered changelog entries that have [hlt] or [l1]
    if [ -n "$changelog_entries" ]; then
        while IFS= read -r entry; do
	    # Only print entries that contain `hlt` or `l1`
	    if echo "$entry" | grep -E 'hlt|l1' > /dev/null; then

		# Remove everything before the first hyphen (-) and the first colon (:)
                commit_message=$(echo "$entry" | sed -E 's/^[^-]*- //' | sed -E 's/^[^:]*: //')

		# Replace backticks with '=' (special case for [` and `]
		commit_message=$(echo "$commit_message" | sed -E 's/\[`/\[ =/g; s/`\]/= \]/g; s/`/=/g')

		# preprend ! to avoid WikiWords
		commit_message=$(echo "$commit_message" | sed -E 's/(\s)([A-Z][a-zA-Z]*)/\1!\2/g; s/^([A-Z][a-zA-Z]*)/!\1/')
		
		# Get the PR number (the part after the first #)
		pr_number=$(echo "$entry" | grep -oP '#\d+' | head -n 1 | tr -d '#')

                # Format the output with the PR link, number, and the cleaned message
                if [[ "$entry" =~ \`hlt\` ]]; then
                    echo "   * [[https://github.com/cms-sw/cmssw/pull/$pr_number][$pr_number]]: $commit_message"
                elif [[ "$entry" =~ \`l1\` ]]; then
                    echo "   * [[https://github.com/cms-sw/cmssw/pull/$pr_number][$pr_number]]: $commit_message"
                fi
            fi
        done <<< "$changelog_entries"
    else
        echo "No HLT or L1 changes found for $release"
    fi
}

# Define the CMSSW cycle (e.g., "CMSSW_14_1") as an argument
cycle="$1"

# Check if cycle is provided
if [[ -z "$cycle" ]]; then
  echo "Usage: $0 <CMSSW cycle (e.g., CMSSW_14_1)>"
  exit 1
fi

# Get the list of releases, split them into pre-releases and regular releases, then sort them separately
mapfile -t releases < <(scram list CMSSW | grep -oP "$cycle[^ ]+" | sort -V | uniq)

# Separate pre-releases from regular releases
pre_releases=()
regular_releases=()

for release in "${releases[@]}"; do
    if [[ "$release" == *pre* ]]; then
        pre_releases+=("$release")
    else
        regular_releases+=("$release")
    fi
done

# Sort pre-releases and regular releases separately
sorted_pre_releases=$(for release in "${pre_releases[@]}"; do echo "$release"; done | sort -V)
sorted_regular_releases=$(for release in "${regular_releases[@]}"; do echo "$release"; done | sort -V)

# Combine pre-releases first, then regular releases
releases=()
mapfile -t releases < <(echo -e "$sorted_pre_releases\n$sorted_regular_releases")

# Base URL for GitHub links
github_base="https://github.com/cms-sw/cmssw/blob"

# Iterate through each release by index
for i in "${!releases[@]}"; do
    release="${releases[$i]}"

    # If the release contains "X" (so it's an IB), skip this iteration and move to the next one
    if [[ "$release" == *X* ]]; then
        continue
    fi

    # Print the release header
    echo "---+++ $release"

    # Get the previous release, if it exists (i.e., for all indices except 0)
    previous_release="${releases[$((i - 1))]}"

    # Get the previous release, if it exists (i.e., for all indices except 0)
    if (( i > 0 )); then
        previous_release="${releases[$((i - 1))]}"
        echo "---++++ CMSSW code changes potentially relevant to HLT in $release with respect to $previous_release"
    else
        previous_release=""
    fi

    # Print the release notes link dynamically
    echo "[[https://github.com/cms-sw/cmssw/releases/$release][Release notes]] for *$release*"
    # Check for the changes in this release related to HLT or L1
    filter_hlt_l1_changes "$release"

    echo "---++++ HLT menus in $release"
    
    # Check if the release contains "patch"
    if [[ "$release" == *patch* ]]; then
	# If it contains "patch", use the patch directory
	cvmfs_dir="/cvmfs/cms.cern.ch/$(scram arch)/cms/cmssw-patch/$release/src/HLTrigger/Configuration/python"
    else
	# Otherwise, use the default directory
	cvmfs_dir="/cvmfs/cms.cern.ch/$(scram arch)/cms/cmssw/$release/src/HLTrigger/Configuration/python"
    fi
        
    # Check if the directory exists
    if [[ -d "$cvmfs_dir" ]]; then
	# Find all HLT_* files in the directory
	for hlt_file in "$cvmfs_dir"/HLT_*; do
	    # Skip if no files are found
	    [[ -e "$hlt_file" ]] || continue

	    # Check if it's a file (not a directory) and does not contain '75e33' or 'NGTScouting' (i.e. Phase-2 menu)
	    if [[ -f "$hlt_file" && "$hlt_file" != *75e33* && "$hlt_file" != *NGTScouting* ]]; then
		# Proceed with your logic for the valid file
		#echo "Processing file: $hlt_file"
   
		# Extract the HLT menu name from the filename
		hlt_menu_name=$(basename "$hlt_file" .py)

		#echo "$hlt_menu_name : $hlt_file"

		# Extract the table name
		table_name=$(grep -oP 'tableName\s*=\s*cms\.string\((["\x27])\K[^\1]+(?=\1)' "$hlt_file")
	    
		# Generate the GitHub link and formatted output
		github_link="${github_base}/${release}/HLTrigger/Configuration/python/${hlt_menu_name}.py"
		echo "   * [[${github_link}][${hlt_menu_name}]]: =${table_name}="
	    fi
	done
    else
	echo "   * No HLT menus found for $release (CVMFS directory missing)"
    fi
    echo
done

# Final message at the end of the page
echo ""
echo "Page auto-generated with [[https://github.com/mmusich/hltScripts/blob/master/storm/generate_hlt_menu_digest.sh][generate_hlt_menu_digest]]."
