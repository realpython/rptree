"""This module provides the RP Tree CLI."""

import argparse
import sys

from . import __version__


def parse_cmd_line_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="tree",
        description="RP Tree, a directory tree diagram generator",
        epilog="Thanks for using RP Tree!",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"RP Tree v{__version__}",
        help="displays the version of RP Tree",
    )
    parser.add_argument(
        "root_dir",
        metavar="ROOT_DIR",
        nargs="?",
        default=".",
        help="generates a directory tree diagram starting at ROOT_DIR",
    )
    parser.add_argument(
        "-d",
        "--dir-only",
        action="store_true",
        help="generates a directory-only (no files) tree diagram",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        metavar="OUTPUT_FILE",
        nargs="?",
        default=sys.stdout,
        help="saves the directory tree diagram to OUTPUT_FILE in Markdown format",
    )
    parser.add_argument(
        "--depth",
        type=int,
        metavar="N",
        default=None,
        help="limits the depth of the directory tree diagram to N levels",
    )
    return parser.parse_args()
