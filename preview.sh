#!/bin/bash

# clear README
PREVIEW_DIR="preview"
README_FILE="${PREVIEW_DIR}/README.md"
true >${README_FILE}

for file in output/*.yaml; do
  style="$(basename "${file%.yaml}")"
  src="svgs/${style}.svg"
  svg_file="${PREVIEW_DIR}/svgs/${style}.svg"
  python preview.py "$file" -o "$svg_file"
  echo "<h3 align='center'>
  <p>${style}</p>
  <img src='./${src}' />
</h3>" >>"${README_FILE}"
done
