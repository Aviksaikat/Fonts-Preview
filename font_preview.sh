#!/bin/bash

# Get a list of all font files
fonts=$(find /usr/share/fonts ~/.local/share/fonts -name '*.[to]tf' -type f)

# Loop through the font files and test each font
for font in $fonts; do
  if echo "$font" | grep -qiE 'nerd|nf'; then
    font_name=$(echo "$font" | rev | cut -d/ -f1 | rev)
    echo "Font Name: $font_name"
    convert -background black -fill white -font "$font_name" -size 200x50 \
    -gravity center label:"Sample text printed in $font_name font" "$font_name.png" 2>/dev/null
    display "$font_name.png"
  fi
done
