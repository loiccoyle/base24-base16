# base24-base16

> Still WIP, just playing around to see what stuff looks like.

Convert base16 color schemes to base24.

See the [preview](./preview/README.md).

## Usage

Use `uv` to setup the `venv` and activate it.

```sh
uv venv
source venv/bin/activate
```

> A `requirements.txt` file is included in the repo if you don't want to use `uv`.

A `Makefile` recipe is setup to convert the schemes and generate the previews.

```sh
make build
```

Alternatively, for more control, each step is documented below.

### Convert the base16 schemes to base24

```sh
python base24-base16.py
```

Use the `--contrast` flag to control how much to brighten/darken the fallback colors. Use `--help` to show the help message.

### Generate the preview svgs and README

```sh
./preview.sh
```
