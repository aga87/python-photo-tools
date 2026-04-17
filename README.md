[![CI](https://github.com/aga87/python-photo-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/aga87/python-photo-tools/actions)

# Photo Tools CLI

Command-line tools for organising photos by date, managing RAW/JPG pairs, and optimising images.

## Changelog

See [CHANGELOG.md](https://github.com/aga87/python-photo-tools/blob/main/CHANGELOG.md) for release history.


## Supported formats

- **RAW**: `.cr2`, `.cr3`, `.nef`, `.arw`, `.raf`, `.orf`, `.rw2`, `.dng`, `.pef`, `.srw`, `.x3f`
- JPG: `.jpg`, `.jpeg`


> ⚠️ **Note:** Detection is based on file extensions only (case-insensitive). Files with incorrect or missing extensions may not be handled correctly.

## Prerequisites - System Tools

This project depends on external system tools in addition to Python.

### ExifTool

Used for extracting image metadata (including RAW formats).
- Supports all major image formats, including RAW
- Provides consistent metadata fields across formats
- More reliable than Python-only EXIF libraries

If `exiftool` is not installed, the CLI will fail with a clear error message and exit code `1`.

Install (macOS)

```shell
brew install exiftool
```

On Linux, install via your package manager (e.g. `apt install exiftool`).

## Installation

### Using pipx (recommended)

```shell
pipx install photo-tools-cli
```
Installs the CLI in an isolated environment and makes `photo-tools` available globally, avoiding dependency conflicts.

Check installed version:

```shell
photo-tools --version
```

### Using pip (if pipx not available)

```shell
pip install photo-tools-cli
```

### Local development

Clone the repository and install:

```shell
pip install -e .
pip install --group dev -e .
```

## Usage

List available commands:

```bash
photo-tools --help
```
Each command provides detailed usage, including arguments and options:

```shell
photo-tools <command> --help
```

**Note: All commands currently process files in the top-level input directory only.**

### Global flags

All commands support:

- `--dry-run` — preview changes without modifying files
- `--verbose` / `-v` — show per-file output

Flags can be combined:

```shell
photo-tools <command> ... --dry-run --verbose
```

### Organise by date (`by-date`)

- Organise images into date-based folders (`YYYY-MM-DD`, optional suffix)
- Files are moved (not copied) into the output directory
- If a destination file already exists, it is skipped (no overwrite)

```shell
photo-tools by-date <INPUT_DIR> <OUTPUT_DIR>
```
```shell
photo-tools by-date <INPUT_DIR> <OUTPUT_DIR> --suffix <SUFFIX>
```


### Separate RAW files (`raws`)

- Move RAW images into a `raws/` subfolder within the input directory
- Non-RAW files are left unchanged
- Files are moved (not copied) in place
- If a destination file already exists, it is skipped (no overwrite)

```shell
photo-tools raws <INPUT_DIR>
```

### Clean unpaired RAW files (`clean-raws`)

- Move RAW files to `raws-to-delete/` if no matching JPG (same prefix) exists
- Matching is based on filename prefix (e.g. `abcd.RAF` matches `abcd_edit.jpg`)
- Files are moved (not deleted), making the operation reversible

```shell
photo-tools clean-raws <RAW_DIR> <JPG_DIR>
```

### Keep RAW files for 5-star JPGs (`keep-5star-raws`)

- Move RAW files to raws-5-star/ if a matching JPG has a 5-star rating
- Ratings are read from the JPG files, not the RAW files
- Matching is based on filename prefix (e.g. abcd.RAF matches abcd.jpg or abcd_edit.jpg)
- Files are moved (not copied), making the operation reversible

```shell
photo-tools keep-5star-raws <RAW_DIR> <JPG_DIR>
```

### Optimise images (`optimise`)

- Resize images to a maximum width of `2500px`
- Choose the highest quality that results in a file size ≤ `500 KB` (never below `70%`)
- Saves optimised images with prefix `lq_` in the same directory (overwrites existing files)


```shell
photo-tools optimise <INPUT_DIR>
```


## Local Development Setup

### Data 

For convenience during development, you can create a local structure:

```bash
mkdir -p data/input data/output
```

Place test photos in:

```
data/input/
```

### Running the CLI

You can run the CLI module directly for testing:

```shell
python -m photo_tools.cli by-date ./data/input ./data/output
```

### Running tests

This project uses `pytest`:

```bash
pytest
```

### Makefile

Common development tasks are available via the Makefile.
