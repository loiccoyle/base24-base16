#!/bin/bash

# clear README
true >README.md

for file in ../output/*.yaml; do
  style="$(basename "${file%.yaml}")"
  output="svgs/${style}.svg"
  python preview.py "$file" -o "$output"
  echo "<h3 align='center'>
  <p>${style}</p>
  <img src='./${output}' />
</h3>" >>README.md

done
