# Python Photo Tools

A command-line tool for organising and processing photos using Python.

## Branches

- `main` – Stable branch. Contains production-ready code and reflects the latest completed features.
- `dev` – Integration branch. Used to combine and test feature branches before merging into `main`.

## Usage

List available commands:

```bash
python -m photo_tools.cli --help
```

## Local Testing Setup

You can pass any input and output paths to the CLI.

For convenience during development, you can create a local structure:

```bash
mkdir -p data/input data/output
```

Place test photos in:

```
data/input/
```
