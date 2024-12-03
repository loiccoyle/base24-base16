import argparse
from pathlib import Path

import yaml
from tqdm import tqdm
from colorzero import Color, Lightness

BASE16_SCHEME_DIR = Path("schemes") / "base16"
BASE24_BASE16_SCHEME_DIR = Path("output")


def lighten(color: str, perc: float) -> str:
    """
    Adjusts the lightness of a given color.

    Args:
        color: The base color in a string format (e.g., "#RRGGBB").
        perc: The percentage to adjust the lightness by. Values >1 lighten, <1 darken.

    Returns:
        The adjusted color as a hexadecimal string.
    """
    return str(Color(color) * Lightness(perc)).upper()


def base16_scheme_files(scheme_dir: Path):
    """
    Yields all Base16 scheme files in the `BASE16_SCHEME_DIR` directory.

    Yields:
        Path: Path objects representing YAML files in the Base16 schemes directory.
    """
    yield from scheme_dir.glob("*.yaml")


def convert(scheme: dict, contrast: float = 0.1) -> None:
    """
    Converts a Base16 color scheme to a Base24 color scheme by adding new colors
    to the palette based on lightness adjustments.

    Args:
        scheme (dict): A dictionary representing the Base16 color scheme.
                       It must include a "palette" key containing base colors.

    Modifies:
        The `scheme` dictionary is updated in-place with the new Base24 colors
        and the "system" key set to "base24".
    """
    darken_amount = 1 - contrast
    lighten_amount = 1 + contrast

    base24_colors = {
        "base10": lambda palette: lighten(palette["base00"], darken_amount),
        "base11": lambda palette: lighten(
            palette["base00"], darken_amount * darken_amount
        ),
        "base12": lambda palette: lighten(palette["base08"], lighten_amount),
        "base13": lambda palette: lighten(palette["base0A"], lighten_amount),
        "base14": lambda palette: lighten(palette["base0B"], lighten_amount),
        "base15": lambda palette: lighten(palette["base0C"], lighten_amount),
        "base16": lambda palette: lighten(palette["base0D"], lighten_amount),
        "base17": lambda palette: lighten(palette["base0E"], lighten_amount),
    }
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

Fills in missing colors with lightened/darkened colors from the base16 scheme:

base10 = darken(base00, 1 - contrast)
base10 = darken(base00, (1 - contrast)**2)
base12 = lighten(base08, 1 + contrast)
base13 = lighten(base0A, 1 + contrast)
base14 = lighten(base0B, 1 + contrast)
base15 = lighten(base0C, 1 + contrast)
base16 = lighten(base0D, 1 + contrast)
base17 = lighten(base0E, 1 + contrast)
""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-c",
        "--contrast",
        type=float,
        help="How much to lighten/darken the base16 colors.\ndefault: [0.1]",
        const=0.1,
        default=0.1,
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

    for scheme_file in base16_schemes:
        with scheme_file.open("r") as fp:
            scheme = yaml.safe_load(fp)
        convert(scheme, args.contrast)
        out_file = args.output_dir / scheme_file.name
        with out_file.open("w") as fp:
            yaml.safe_dump(scheme, fp, sort_keys=False)


if __name__ == "__main__":
    main()
