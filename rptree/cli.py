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
        "-f",
        "--files-only",
        action="store_true",
        help="generate a file-only tree",
    )

    ordering = parser.add_mutually_exclusive_group()

    ordering.add_argument(
        "-df",
        "--dirs-first",
        action="store_true",
        help="list directories before files",
    )

    ordering.add_argument(
        "-ff",
        "--files-first",
        action="store_true",
        help="list files before directories",
    )

    parser.add_argument(
        "-i",
        "--ignore",
        metavar="PATTERN",
        nargs="*",
        default=None,
        help="ignore files or directories (supports patterns, e.g. *.py)",
    )

    parser.add_argument(
        "-gi",
        "--gitignore",
        action="store_true",
        help="respect .gitignore rules",
    )

    parser.add_argument(
        "-dl",
        "--depth-level",
        metavar="N",
        type=int,
        default=None,
        help="limit tree depth to N levels",
    )

    parser.add_argument(
        "-o",
        "--output-file",
        metavar="OUTPUT_FILE",
        default=None,
        help="save the generated tree to a file",
    )

    args = parser.parse_args()

    if args.dir_only and args.files_only:
        parser.error("cannot use --dir-only and --files-only together")

    if args.dir_only and (args.dirs_first or args.files_first):
        parser.error("ordering options are not valid with --dir-only")

    if args.files_only and (args.dirs_first or args.files_first):
        parser.error("ordering options are not valid with --files-only")

    if args.depth_level is not None and args.depth_level < 0:
        parser.error("--depth-level must be >= 0")

    return args