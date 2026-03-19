"""Entry point for RP Tree CLI."""

import pathlib
import sys

from .cli import parse_cmd_line_arguments
from .rptree import DirectoryTree


def main() -> None:
    args = parse_cmd_line_arguments()
    root_dir = pathlib.Path(args.root_dir).resolve()

    if not root_dir.exists():
        print(f"Error: directory not found: {root_dir}", file=sys.stderr)
        sys.exit(1)

    if not root_dir.is_dir():
        print(f"Error: path is not a directory: {root_dir}", file=sys.stderr)
        sys.exit(1)

    try:
        tree = DirectoryTree(
            root_dir=root_dir,
            dir_only=args.dir_only,
            files_only=args.files_only,
            dirs_first=args.dirs_first,
            files_first=args.files_first,
            no_pipes=args.no_pipes,
            ignore=args.ignore,
            use_gitignore=args.gitignore,
            depth_level=args.depth_level,
            output_file=args.output_file,
        )

        tree.generate()

    except KeyboardInterrupt:
        print("\nOperation cancelled.", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()