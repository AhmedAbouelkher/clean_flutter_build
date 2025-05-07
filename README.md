# Flutter Cleaner

A Python utility to clean Flutter projects and free up disk space by removing build artifacts and cached dependencies.

## Features

- Intelligently detects Flutter applications
- Runs `flutter clean` to remove build directories
- Automatically cleans platform-specific artifacts:
  - **iOS**: Removes Pods, .symlinks directories, and Podfile.lock
  - **Android**: Removes .gradle directories
- Multi-threaded operation using available CPU cores
- Recursively scans directories to find and clean all Flutter projects

## Requirements

- Python 3.6+
- Flutter SDK installed and available in PATH

## Installation

```bash
git clone https://github.com/AhmedAbouelkher/flutter-cleaner.git
cd flutter-cleaner
```

## Usage

```bash
python flutter_cleaner.py /path/to/flutter/projects
```

This will scan the specified directory recursively, detect Flutter projects, and clean them.

## Example

```bash
python flutter_cleaner.py ~/Development/FlutterProjects
```

## How It Works

1. The script walks through the specified directory tree
2. It identifies Flutter projects by looking for key files (pubspec.yaml, .metadata, etc.)
3. For each Flutter project:
   - Runs `flutter clean`
   - Removes iOS build artifacts if present (Pods, .symlinks, Podfile.lock)
   - Removes Android build artifacts if present (.gradle)
4. All operations are performed concurrently using a thread pool

## Disclaimer

Cleaning build artifacts won't affect your compiled app (IPA and AAB) size. This tool is meant to free up disk space on your development machine, not to optimize the size of production builds.

## License

MIT
