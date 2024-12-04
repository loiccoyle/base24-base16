#!/bin/bash

# clear README
PREVIEW_DIR="preview"
README_FILE="${PREVIEW_DIR}/README.md"
true >${README_FILE}

for file in output/*.yaml; do
  style="$(basename "${file%.yaml}")"
  output="${PREVIEW_DIR}/svgs/${style}.svg"
  python preview.py "$file" -o "$output"
  echo "<h3 align='center'>
  <p>${style}</p>
  <img src='./${output}' />
</h3>" >>"${README_FILE}"
done
