"""This module provides the RP Tree CLI."""

import argparse

from . import __version__


def parse_cmd_line_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="rptree",
        description="Generate a directory tree",
        epilog="Thanks for using RP Tree!",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"RP Tree v{__version__}",
    )

    parser.add_argument(
        "root_dir",
        metavar="ROOT_DIR",
        nargs="?",
        default=".",
        help="root directory to generate the tree from",
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "-d",
        "--dir-only",
        action="store_true",
        help="show directories only",
    )
    mode.add_argument(
        "-f",
        "--files-only",
        action="store_true",
        help="show files only",
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
        "-n",
        "--no-pipes",
        action="store_true",
        help="remove vertical pipes between branches",
    )

    parser.add_argument(
        "-i",
        "--ignore",
        metavar="PATTERN",
        nargs="*",
        default=None,
        help="ignore files or directories (e.g. *.py __pycache__)",
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
        help="limit tree depth (>= 0)",
    )

    parser.add_argument(
        "-o",
        "--output-file",
        metavar="FILE",
        help="write output to file (markdown format)",
    )

    args = parser.parse_args()

    # validações
    if (args.dir_only or args.files_only) and (
        args.dirs_first or args.files_first
    ):
        parser.error("ordering options cannot be used with --dir-only or --files-only")

    if args.depth_level is not None and args.depth_level < 0:
        parser.error("--depth-level must be >= 0")

    return args