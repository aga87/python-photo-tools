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

#### organise-by-date

- Organise images into date-based folders (`YYYY-MM-DD`, optional suffix).
- Files are moved (not copied) into the output directory.
- Supports a dry-run mode to preview changes without modifying the filesystem.


```shell
photo-tools organise-by-date <INPUT_DIR> <OUTPUT_DIR>
```
```shell
photo-tools organise-by-date <INPUT_DIR> <OUTPUT_DIR> --suffix <SUFFIX>
```
```shell
photo-tools organise-by-date <INPUT_DIR> <OUTPUT_DIR> --dry-run
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
python -m photo_tools.cli ./data/input ./data/output
```

If the CLI uses subcommands, the command will look like:

```shell
python -m photo_tools.cli organise-by-date ./data/input ./data/output
```