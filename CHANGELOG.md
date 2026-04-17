# Changelog

## [0.3.0] - 2026-04-17

### Added
- Support for additional RAW formats (`.cr2`, `.cr3`, `.nef`, `.arw`, `.orf`, `.rw2`, `.dng`, `.pef`, `.srw`, `.x3f`)

### Changed
- Centralised file type detection into shared utilities (`is_raw`, `is_jpg`)
- Improved consistency across commands by removing duplicated extension logic

### Documentation
- Added CHANGELOG.md to track release history

### Notes
- File type detection is based on file extensions only (case-insensitive)

## [0.2.0] - 2026-04-16

### Added
- New command to keep only 5-star RAW files (`keep-5star-raws`)


## [0.1.1] - 2026-03-30

### Added
- GitHub Actions workflow for automated PyPI publishing
- Trusted Publishing (OIDC) configuration for secure releases

### Changed
- Updated project configuration for automated releases


## [0.1.0] - 2026-03-30

### Added
- Initial release of Photo Tools CLI
- Command to organise images into date-based folders (based on EXIF metadata) (`by-date`)
- RAW/JPG workflow commands:
  - separate RAW files (`raws`)
  - clean unpaired RAW files (`clean-raws`)
- Image optimisation command (`optimise`)
- CLI interface with support for `--dry-run` and verbose output

### Notes
- Focus on non-destructive operations (files are moved, not deleted)
- Relies on ExifTool for metadata extraction