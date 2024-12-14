#!/bin/bash

echo "## 📖 Resource List" > README.md
echo "" >> README.md
echo "### Example Entry:" >> README.md

for file in websites/*.md; do
    filename=$(basename "$file" .md)
    echo "#### 🌟 [$(echo $filename | sed 's/-/ /g')](websites/$filename.md)" >> README.md
    echo "" >> README.md
done

echo "Update complete. Check README.md for changes."
