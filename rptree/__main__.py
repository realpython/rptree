"""This module provides RP Tree entry point script."""

import pathlib
import sys

from . import cli
from .rptree import DirectoryTree


def main() -> None:
    args = cli.parse_cmd_line_arguments()

    root_dir = pathlib.Path(args.root_dir)
    if not root_dir.is_dir():
        print("The specified root directory doesn't exist")
        sys.exit(1)

    tree = DirectoryTree(
        root_dir=args.root_dir,
        dir_only=args.dir_only,
        output_file=args.output_file,
        max_depth=args.depth,
    )
    tree.generate()


if __name__ == "__main__":
    main()
