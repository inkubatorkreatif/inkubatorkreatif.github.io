#!/bin/bash

# Script to rename all penilaian.md files to presentasi.md
# Created: May 6, 2025

# Base directory for products
BASE_DIR="/home/krypton-byte/Inkraf/Inkraf/content/docs"

# Find all penilaian.md files and rename them
find "$BASE_DIR" -name "penilaian.md" | while read -r file; do
    dir=$(dirname "$file")
    new_file="$dir/presentasi.md"
    echo "Renaming: $file → $new_file"
    cp "$file" "$new_file"
    rm "$file"
done

echo "Renaming complete!"
