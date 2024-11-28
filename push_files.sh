#!/bin/bash

# Ensure the script exits on error
set -e

# Check if we are inside a git repository
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
  echo "Not inside a Git repository."
  exit 1
fi

# Loop until there are no untracked files
while true; do
  # List untracked files and their sizes, sort by size
  smallest_file=$(git ls-files --others --exclude-standard -z | xargs -0 du -b | sort -n | head -n 1 | awk '{print $2}')

  # Exit if no untracked files are found
  if [ -z "$smallest_file" ]; then
    echo "All untracked files have been processed."
    break
  fi

  # Add the smallest untracked file
  git add "$smallest_file"

  # Commit the added file
  git commit -m "Add $(basename "$smallest_file")"

  # Push the commit to the remote
  git push

  echo "Processed: $smallest_file"
done
