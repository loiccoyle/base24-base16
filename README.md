# base24-base16

Convert base16 color schemes to base24

## Base24 spec

| Colour                                                  | BaseNN | Ansi | Terminal/Colour Use | Text Editor                                                                                                 |
| ------------------------------------------------------- | ------ | ---- | ------------------- | ----------------------------------------------------------------------------------------------------------- |
| ![Colour](https://placehold.it/25/282c34/000000?text=+) | base00 | -    | Background          | Default Background                                                                                          |
| ![Colour](https://placehold.it/25/3f4451/000000?text=+) | base01 | 0    | Black               | Lighter Background (Used for status bars)                                                                   |
| ![Colour](https://placehold.it/25/4f5666/000000?text=+) | base02 | 8    | Bright Black        | Selection Background                                                                                        |
| ![Colour](https://placehold.it/25/545862/000000?text=+) | base03 | -    | (Grey)              | Comments, Invisibles, Line Highlighting                                                                     |
| ![Colour](https://placehold.it/25/9196a1/000000?text=+) | base04 | -    | (Light Grey)        | Dark Foreground (Used for status bars)                                                                      |
| ![Colour](https://placehold.it/25/abb2bf/000000?text=+) | base05 | -    | Foreground          | Default Foreground, Caret, Delimiters, Operators                                                            |
| ![Colour](https://placehold.it/25/e6e6e6/000000?text=+) | base06 | 7    | White               | Light Foreground (Not often used)                                                                           |
| ![Colour](https://placehold.it/25/ffffff/000000?text=+) | base07 | 15   | Bright White        | The Lightest Foreground (Not often used)                                                                    |
| ![Colour](https://placehold.it/25/e06c75/000000?text=+) | base08 | 1    | Red                 | Variables, XML Tags, Markup Link Text, Markup Lists, Diff Deleted                                           |
| ![Colour](https://placehold.it/25/d19a66/000000?text=+) | base09 | ~3   | (Orange)            | Integers, Boolean, Constants, XML Attributes, Markup Link Url                                               |
| ![Colour](https://placehold.it/25/e5c07b/000000?text=+) | base0A | 3    | Yellow              | Classes, Markup Bold, Search Text Background                                                                |
| ![Colour](https://placehold.it/25/98c379/000000?text=+) | base0B | 2    | Green               | Strings, Inherited Class, Markup Code, Diff Inserted                                                        |
| ![Colour](https://placehold.it/25/56b6c2/000000?text=+) | base0C | 6    | Cyan                | Support, Regular Expressions, Escape Characters, Markup Quotes                                              |
| ![Colour](https://placehold.it/25/61afef/000000?text=+) | base0D | 4    | Blue                | Functions, Methods, Attribute IDs, Headings                                                                 |
| ![Colour](https://placehold.it/25/c678dd/000000?text=+) | base0E | 5    | Purple              | Keywords, Storage, Selector, Markup Italic, Diff Changed                                                    |
| ![Colour](https://placehold.it/25/be5046/000000?text=+) | base0F | -    | (Dark Red or Brown) | Deprecated Highlighting for Methods and Functions, Opening/Closing Embedded Language Tags, e.g., `<?php ?>` |
| ![Colour](https://placehold.it/25/21252b/000000?text=+) | base10 | -    | (Darker Black)      | Darker Background                                                                                           |
| ![Colour](https://placehold.it/25/181a1f/000000?text=+) | base11 | -    | (Darkest Black)     | The Darkest Background                                                                                      |
| ![Colour](https://placehold.it/25/ff7b86/000000?text=+) | base12 | 9    | Bright Red          | NA                                                                                                          |
| ![Colour](https://placehold.it/25/efb074/000000?text=+) | base13 | 11   | Bright Yellow       | NA                                                                                                          |
| ![Colour](https://placehold.it/25/b1e18b/000000?text=+) | base14 | 10   | Bright Green        | NA                                                                                                          |
| ![Colour](https://placehold.it/25/63d4e0/000000?text=+) | base15 | 14   | Bright Cyan         | NA                                                                                                          |
| ![Colour](https://placehold.it/25/67cdff/000000?text=+) | base16 | 12   | Bright Blue         | NA                                                                                                          |
| ![Colour](https://placehold.it/25/e48bff/000000?text=+) | base17 | 13   | Bright Purple       | NA                                                                                                          |

## Method

```
base10 = darken(base00, 10%)
base10 = darken(base10, 10%)
base12 = lighten(base08, 10%)
base13 = lighten(base0A, 10%)
base14 = lighten(base0B, 10%)
base15 = lighten(base0C, 10%)
base16 = lighten(base0D, 10%)
base17 = lighten(base0E, 10%)
```
