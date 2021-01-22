"""This module provides RP Tree cli."""

import argparse
import pathlib
import sys

from . import __version__
from .rptree import DirectoryTree


def main():
    args = parse_cmd_line_arguments()
    root_dir = pathlib.Path(args.root_dir)

    if not root_dir.is_dir():
        print("The specified root directory doesn't exist")
        sys.exit()

    tree = DirectoryTree(root_dir, args.output_file, args.dir_only)
    tree.generate()


def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser(
        prog="RP Tree",
        description="Directory Tree Generator",
        epilog="Thanks for Using RP Tree!",
    )
    parser.version = f"{parser.prog} {__version__}"
    parser.add_argument(
        "root_dir",
        metavar="ROOT_DIR",
        nargs="?",
        default=".",
        type=str,
        help="Generate a Full and Recursive Directory Tree",
    )
    parser.add_argument(
        "-d",
        "--dir-only",
        action="store_true",
        help="Generate a Directory-Only Tree",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        metavar="OUTPUT_FILE",
        nargs="?",
        default=sys.stdout,
        type=str,
        help="Generate a Full Directory Tree and Save it to a File",
    )
    parser.add_argument("-v", "--version", action="version")
    return parser.parse_args()
