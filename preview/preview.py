#!/usr/bin/env python3

import yaml
import argparse
from typing import List, Tuple


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an SVG image from a YAML file."
    )

    parser.add_argument(
        "inputfile",
        help="Input .yaml file",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="outputfile",
        help="Output file (default: ./output.svg)",
        default="./output.svg",
        type=argparse.FileType("w"),
    )
    parser.add_argument(
        "-r",
        "--rows",
        dest="rows",
        help="Number of rows in the output image",
        default=3,
        type=int,
        metavar="N",
    )
    parser.add_argument(
        "-b",
        "--bordersize",
        dest="bordersize",
        help="Size of border padding",
        default=15,
        type=int,
        metavar="N",
    )
    parser.add_argument(
        "-t",
        "--tilesize",
        dest="tilesize",
        help="Size of the individual color tiles",
        default=45,
        type=int,
        metavar="N",
    )
    parser.add_argument(
        "-g",
        "--gapsize",
        dest="gapsize",
        help="Size of the padding between tiles",
        default=15,
        type=int,
        metavar="N",
    )

    return parser.parse_args()


def extract_colors(file_content: str) -> List[str]:
    """Extract color codes from the YAML file."""
    scheme = yaml.safe_load(file_content)
    return [color for color in scheme["palette"].values()]


def calculate_svg_dimensions(
    num_colors: int, rows: int, tile_size: int, gap_size: int, border_size: int
) -> Tuple[int, int]:
    """Calculate SVG canvas dimensions."""
    tiles_per_row = num_colors // rows
    width = (
        (tiles_per_row * tile_size)
        + ((tiles_per_row + 1) * gap_size)
        + (border_size * 2)
    )
    height = (rows * tile_size) + ((rows + 1) * gap_size) + (border_size * 2)
    return width, height


def generate_svg(
    colors: List[str],
    rows: int,
    tile_size: int,
    gap_size: int,
    border_size: int,
    width: int,
    height: int,
) -> str:
    """Generate SVG."""
    svg = [
        '<?xml version="1.0" encoding="UTF-8" ?>',
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        f'<rect x="0" y="0" width="{width}" height="{height}" style="fill:{colors[0]}" />',
    ]

    tiles_per_row = len(colors) // rows
    for index, color in enumerate(colors):
        row = index // tiles_per_row
        col = index % tiles_per_row

        x = border_size + gap_size + col * (tile_size + gap_size)
        y = border_size + gap_size + row * (tile_size + gap_size)

        svg.append(
            f'<rect x="{x}" y="{y}" width="{tile_size}" height="{tile_size}" style="fill:{color}" />'
        )

    svg.append("</svg>")
    return "\n".join(svg)


def main() -> None:
    args = parse_arguments()

    with args.inputfile as input_file:
        colors = extract_colors(input_file.read())

    width, height = calculate_svg_dimensions(
        num_colors=len(colors),
        rows=args.rows,
        tile_size=args.tilesize,
        gap_size=args.gapsize,
        border_size=args.bordersize,
    )

    svg_content = generate_svg(
        colors=colors,
        rows=args.rows,
        tile_size=args.tilesize,
        gap_size=args.gapsize,
        border_size=args.bordersize,
        width=width,
        height=height,
    )

    with args.outputfile as output_file:
        output_file.write(svg_content)


if __name__ == "__main__":
    main()
