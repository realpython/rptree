# RP Tree

RP Tree is a command-line tool to generate directory tree diagrams.

## Installation

To install **RP Tree**, just run the following command:

```sh
$ pip install rptree
```

## Usage

```sh
$ rptree /path/to/directory/
```

**Note:** The `-h` or `--help` option provides help on using RP Tree.

## Sample Output

```sh
$ rptree hello/
./hello/
│
├── hello/
│   ├── __init__.py
│   └── hello.py
│
├── tests/
│   └── test_hello.py
│
├── LICENSE
├── README.md
├── requirements.txt
└── setup.py
```

That's it! You've generated a nice directory tree diagram.

## Features

If you run RP Tree with a directory path as an argument, then you get a full directory tree diagram printed on your screen. The default input directory is your current directory.

RP Tree also provides the following options:

- `-v`, `--version` shows the application version and exits
- `-h`, `--help` show a usage message
- `-d`, `--dir-only` generates a directory-only tree diagram
- `-o`, `--output-file` generates a full directory tree diagram and save it to a file in markdown format

## Release History

- 0.1.1
  - Display the entries in alphabetical order
- 0.1.0
  - A work in progress

## About the Author

Leodanis Pozo Ramos - Email: leodanis@realpython.com
