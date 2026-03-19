# RP Tree

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-0.2.0-orange)

RP Tree is a simple and fast CLI tool to generate directory tree diagrams.

## Installation

```bash
pip install rptree
```

## Usage

```bash
rptree [ROOT_DIR]
```

If no directory is provided, the current directory is used:

```bash
rptree
```

Show help:

```bash
rptree -h
```

## Options

### General

- `-h`, `--help` Show help message
- `-v`, `--version` Show version

### Modes

- `-d`, `--dir-only` Show directories only
- `-f`, `--files-only` Show files only

### Ordering

- `-df`, `--dirs-first` List directories before files
- `-ff`, `--files-first` List files before directories

> Alphabetical order is always applied as base sorting.

### Display

- `-n`, `--no-pipes` Remove vertical pipes between branches

### Ignoring

- `-i`, `--ignore PATTERN [PATTERN ...]` Ignore files/directories
- `-gi`, `--gitignore` Respect `.gitignore` rules

### Depth

- `-dl`, `--depth-level N` Limit depth

### Output

- `-o`, `--output-file FILE` Save output to file (Markdown format)

## Examples

Basic:

```bash
rptree
```

Directories first:

```bash
rptree . -df
```

Files only:

```bash
rptree . -f
```

Limit depth:

```bash
rptree . -dl 2
```

Ignore entries:

```bash
rptree . -i node_modules dist .git
```

Use `.gitignore`:

```bash
rptree . -gi
```

No pipes mode:

```bash
rptree . -n
```

Save to file:

```bash
rptree . -o tree.md
```

## Sample Output

### Default

```text
project/
│
├── src/
│   ├── main.py
│   └── utils.py
│
├── tests/
│   └── test_main.py
│
└── README.md
```

### No pipes (`-n`)

```text
project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
└── README.md
```

## Features

- Clean and readable tree output
- `.gitignore` support
- Custom ignore patterns
- Depth limiting
- Flexible sorting
- Optional compact mode (`--no-pipes`)

## Release History

### 0.3.0

- Fixed `--no-pipes` behavior
- Fixed `.gitignore` directory handling
- Improved tree formatting (matches classic `tree`)
- Added modern packaging (`pyproject.toml`)

### 0.2.0

- Added filtering and ordering options
- Added `.gitignore` support
- Added depth control

### 0.1.0

- Initial release

## Author

Leodanis Pozo Ramos

## License

^RP Tree^ is distributed under the MIT license. See [LICENSE](LICENSE) for more information.
