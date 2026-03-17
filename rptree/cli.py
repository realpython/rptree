"""This module provides the RP Tree CLI."""

import argparse

from . import __version__


def parse_cmd_line_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="rptree",
        description="Generate a directory tree",
        epilog="Thanks for using RP Tree!",
    )

    parser.version = f"RP Tree v{__version__}"

    parser.add_argument("-v", "--version", action="version")

    parser.add_argument(
        "root_dir",
        metavar="ROOT_DIR",
        nargs="?",
        default=".",
        help="generate a full directory tree starting at ROOT_DIR",
    )

    parser.add_argument(
        "-d",
        "--dir-only",
        action="store_true",
        help="generate a directory-only tree",
    )

    parser.add_argument(
        "-o",
        "--output-file",
        metavar="OUTPUT_FILE",
        default=None,
        help="generate a full directory tree and save it to a file",
    )

    return parser.parse_args()