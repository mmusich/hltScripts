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

    # Extract the changelog entries from the release notes JSON
    changelog_entries=$(echo "$release_notes" | jq -r '.body' | grep -i -E '`hlt`|`l1`')

    # Print the release note link
    echo "[[https://github.com/cms-sw/cmssw/releases/$release][Release notes]] for !$release"

    # Print the filtered changelog entries that have [hlt] or [l1]
    if [ -n "$changelog_entries" ]; then
        while IFS= read -r entry; do
            # Only print entries that contain `hlt` or `l1`
	    if echo "$entry" | grep -E 'hlt|l1' > /dev/null; then

		# Remove everything before the first hyphen (-) and the first colon (:)
		commit_message=$(echo "$entry" | sed -E 's/^[^-]*- //' | sed -E 's/^[^:]*: //')

		# Replace backticks with '='
		commit_message=$(echo "$commit_message" | sed -E 's/\[`/\[ =/g; s/`\]/= \]/g; s/`/=/g')

		# preprend ! to avoid WikiWords
		commit_message=$(echo "$commit_message" | sed -E 's/(\s)([A-Z][a-zA-Z]*)/\1!\2/g; s/^([A-Z][a-zA-Z]*)/!\1/')
				
		# Get the PR number (the part after the #)
		pr_number=$(echo "$entry" | grep -oP '#\d+' | head -n 1 | tr -d '#')

		# Format the output with the PR link, number, and the cleaned message
		if [[ "$entry" =~ \`hlt\` ]]; then
		    echo "   * [[https://github.com/cms-sw/cmssw/pull/$pr_number][$pr_number]]: $commit_message [hlt]"
		elif [[ "$entry" =~ \`l1\` ]]; then
		    echo "   * [[https://github.com/cms-sw/cmssw/pull/$pr_number][$pr_number]]: $commit_message [l1]"
		fi		            
            fi
        done <<< "$changelog_entries"
    else
        echo "No HLT or L1 changes found for $release"
    fi
}

# Check if an argument is passed, if not, print help message
if [ -z "$1" ]; then
    echo "Usage: $0 <release>"
    echo "Example: $0 CMSSW_14_1_0_pre3"
    echo "Please provide a release name as an argument to check for changes."
    exit 1
fi

release=$1

# Print the header for the release
echo "---++++ $release"

# Check for the changes in this release related to HLT or L1
filter_hlt_l1_changes "$release"
