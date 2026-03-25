# Python Photo Tools

A command-line tool for organising and processing photos using Python.

## Branches

- `main` – Stable branch. Contains production-ready code and reflects the latest completed features.
- `dev` – Integration branch. Used to combine and test feature branches before merging into `main`.

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

The application will fail if it is not installed.

If running in a Docker container, include:

```Dockerfile
RUN apt-get update && apt-get install -y exiftool
```

## Usage

List available commands:

```bash
photo-tools --help
```

### Commands

All commands support a `--dry-run` flag. Use this to safely preview changes before running a command.

- No files are modified
- No directories are created
- Actions are only printed


#### organise-by-date

- Organise images into date-based folders (`YYYY-MM-DD`, optional suffix)
- Files are moved (not copied) into the output directory
- If a destination file already exists, it is skipped (no overwrite)

```shell
photo-tools organise-by-date <INPUT_DIR> <OUTPUT_DIR>
```
```shell
photo-tools organise-by-date <INPUT_DIR> <OUTPUT_DIR> --suffix <SUFFIX>
```
```shell
photo-tools organise-by-date <INPUT_DIR> <OUTPUT_DIR> --dry-run
```

#### organise-by-type

- Organise images into `raws/` and `jpgs/` subfolders within the input directory
- Files are moved (not copied) in place
- If a destination file already exists, it is skipped (no overwrite)

```shell
photo-tools organise-by-type <INPUT_DIR>
```
```shell
photo-tools organise-by-type <INPUT_DIR> --dry-run
```

#### soft-delete-unpaired-raws

- Move RAW files to `raws-to-delete/` if no matching JPG (same prefix) exists
- Matching is based on filename prefix (e.g. `abcd.RAF` matches `abcd_edit.jpg`)
- Files are moved (not deleted), making the operation reversible

```shell
photo-tools soft-delete-unpaired-raws <RAW_DIR> <JPG_DIR>
```

```shell
photo-tools soft-delete-unpaired-raws <RAW_DIR> <JPG_DIR> --dry-run
```

#### optimise

- Resize images to a maximum width of `2500px`
- Choose the highest quality that results in a file size ≤ `500 KB` (never below `70%`)
- Saves optimised images with prefix `lq_` in the same directory (existing files are overwritten)


```shell
photo-tools optimise <INPUT_DIR>
```

```shell
photo-tools optimise <INPUT_DIR> --dry-run
```

## Local Testing Setup

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
python -m photo_tools.cli organise-by-date ./data/input ./data/output
```

### Running tests

This project uses `pytest`:

```bash
pytest
```

### Test coverage

The testing pattern is fully implemented for organise-by-date, including:
- dry-run safety
- file movement
- edge cases (unsupported files, missing metadata, collisions)

Other commands follow the same structure but are not yet covered.

### Makefile

Common development tasks are available via the Makefile.