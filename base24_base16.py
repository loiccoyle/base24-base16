#!/usr/bin/env python3

import argparse
from pathlib import Path
from typing import Iterable, OrderedDict

import colorspacious as cs
from ruamel.yaml import YAML
from tqdm import tqdm

CONTRAST = 0.5
BASE16_SCHEME_DIR = Path("schemes") / "base16"
BASE24_BASE16_SCHEME_DIR = Path("output")


def hex_to_rgb(hex_color: str) -> tuple[float, ...]:
    """Convert a hex color string to an RGB tuple normalized to [0, 1]."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4))


def rgb_to_hex(rgb: Iterable[float]) -> str:
    """Convert an RGB tuple normalized to [0, 1] to a hex color string."""
    return "#{:02x}{:02x}{:02x}".format(
        *(max(0, min(255, int(channel * 255))) for channel in rgb)
    )


def brighten(hex_color: str, brighten_factor: float) -> str:
    """
    Brightens or darkens a hex color in a perceptually uniform color space by a multiplier.

    Args:
        hex_color: The input color in hex format (e.g., "#RRGGBB").
        brighten_factor: Multiplier for brightness, values>1 brighten, <1 darken

    Returns:
        The adjusted color in hex format.
    """
    rgb = hex_to_rgb(hex_color)

    jch = cs.cspace_convert(rgb, "sRGB1", "JCh")

    jch[0] *= brighten_factor
    # Clamp J to valid range [0, 100]
    jch[0] = max(0, min(100, jch[0]))

    adjusted_rgb = cs.cspace_convert(jch, "JCh", "sRGB1")
    adjusted_rgb_clamped = [max(0, min(1, channel)) for channel in adjusted_rgb]

    return rgb_to_hex(adjusted_rgb_clamped)


def base16_scheme_files(scheme_dir: Path):
    """
    Yields all Base16 scheme files in the `BASE16_SCHEME_DIR` directory.

    Yields:
        Path: Path objects representing YAML files in the Base16 schemes directory.
    """
    yield from scheme_dir.glob("*.yaml")


def convert(scheme: dict, contrast: float = CONTRAST) -> None:
    """
    Converts a Base16 color scheme to a Base24 color scheme by adding new colors
    to the palette based on lightness adjustments.

    Args:
        scheme: A dictionary representing the Base16 color scheme.
                It must include a "palette" key containing base colors.
        contrast: Controls how much to brighten/darken the colors.

    Modifies:
        The `scheme` dictionary is updated in-place with the new Base24 colors
        and the "system" key set to "base24".
    """
    is_light = scheme["variant"] == "light"
    darken_amount = 1 - contrast
    brighten_amount = 1 + contrast

    base24_colors = OrderedDict(
        {
            "base10": lambda palette: brighten(
                palette["base00"], brighten_amount if is_light else darken_amount
            ),
            "base11": lambda palette: brighten(
                palette["base10"], brighten_amount if is_light else darken_amount
            ),
            "base12": lambda palette: brighten(palette["base08"], brighten_amount),
            "base13": lambda palette: brighten(palette["base0A"], brighten_amount),
            "base14": lambda palette: brighten(palette["base0B"], brighten_amount),
            "base15": lambda palette: brighten(palette["base0C"], brighten_amount),
            "base16": lambda palette: brighten(palette["base0D"], brighten_amount),
            "base17": lambda palette: brighten(palette["base0E"], brighten_amount),
        }
    )
    for color, func in base24_colors.items():
        scheme["palette"][color] = func(scheme["palette"])
    scheme["system"] = "base24"


def is_dir(path: str) -> Path:
    path_dir = Path(path)
    if not path_dir.is_dir():
        raise NotADirectoryError(f"Path: '{path}' is not a directory")
    return path_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="""Convert base16 color schemes to base24.

Fills in missing colors with brightened/darkened colors from the base16 scheme.
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-c",
        "--contrast",
        type=float,
        help=f"How much to brighten/darken the base16 colors.\ndefault: [{CONTRAST}]",
        const=CONTRAST,
        default=CONTRAST,
        nargs="?",
    )
    parser.add_argument(
        "--input_dir",
        help=f"Path to the directory holding the base16 yaml file.\ndefault: ['{BASE16_SCHEME_DIR}']",
        type=is_dir,
        const=BASE16_SCHEME_DIR,
        default=BASE16_SCHEME_DIR,
        nargs="?",
    )
    parser.add_argument(
        "--output_dir",
        help=f"Path to the directory to write the converted schemes.\ndefault: ['{BASE24_BASE16_SCHEME_DIR}']",
        type=is_dir,
        const=BASE24_BASE16_SCHEME_DIR,
        default=BASE24_BASE16_SCHEME_DIR,
        nargs="?",
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Disable progress bar."
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(exist_ok=True)

    base16_schemes = list(base16_scheme_files(args.input_dir))
    if not args.quiet:
        base16_schemes = tqdm(base16_schemes, desc="converting")

    yaml = YAML()
    yaml.preserve_quotes = True

    for scheme_file in base16_schemes:
        with scheme_file.open("r") as fp:
            scheme = yaml.load(fp)
        convert(scheme, args.contrast)
        out_file = args.output_dir / scheme_file.name
        with out_file.open("w") as fp:
            yaml.dump(scheme, fp)


if __name__ == "__main__":
    main()
