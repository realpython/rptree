# RP Tree

RP Tree is a command-line tool to generate directory tree diagrams.

## Installation

```bash
pip install rptree
```

## Usage

```bash
rptree [ROOT_DIR]
```

If no directory is provided, the current directory is used.

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
- `-v`, `--version` Show application version

### Modes

- `-d`, `--dir-only` Display directories only
- `-f`, `--files-only` Display files only

### Ordering

- `-df`, `--dirs-first` List directories before files
- `-ff`, `--files-first` List files before directories

> Note: Alphabetical order is always used as the base ordering.

### Ignoring

- `-i`, `--ignore NAME [NAME ...]` Ignore specific files or directories
- `-gi`, `--gitignore` Respect `.gitignore` rules

### Depth

- `-dl`, `--depth-level N` Limit the tree depth to N levels

### Output

- `-o`, `--output-file FILE` Save the generated tree to a file

## Examples

Generate tree for current directory:

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

Ignore specific entries:

```bash
rptree . -i node_modules dist .git
```

Use `.gitignore` rules:

```bash
rptree . -gi
```

Save output to file:

```bash
rptree . -o tree.txt
```

## Sample Output

```bash
project/
├── src/
│   ├── main.py
│   └── utils.py
├── tests/
│   └── test_main.py
└── README.md
```

## Release History

### 0.2.0

- Added `--files-only` (`-f`)
- Added `--dirs-first` (`-df`)
- Added `--files-first` (`-ff`)
- Added `--ignore` (`-i`)
- Added `.gitignore` support (`-gi`)
- Added `--depth-level` (`-dl`)
- Improved tree formatting
- Added type hints

### 0.1.1

- Display entries in alphabetical order

### 0.1.0

- Initial release

## Author

Leodanis Pozo Ramos
