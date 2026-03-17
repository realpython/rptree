"""This module provides RP Tree main module."""

from __future__ import annotations

import pathlib
import sys
from collections import deque
from fnmatch import fnmatch
from typing import Deque, List, Optional, Set

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class DirectoryTree:
    def __init__(
        self,
        root_dir: pathlib.Path,
        *,
        dir_only: bool = False,
        files_only: bool = False,
        dirs_first: bool = False,
        files_first: bool = False,
        ignore: Optional[List[str]] = None,
        use_gitignore: bool = False,
        depth_level: Optional[int] = None,
        output_file: Optional[str] = None,
    ) -> None:
        self._output_file = output_file
        self._generator = _TreeGenerator(
            root_dir=root_dir,
            dir_only=dir_only,
            files_only=files_only,
            dirs_first=dirs_first,
            files_first=files_first,
            ignore=ignore,
            use_gitignore=use_gitignore,
            depth_level=depth_level,
        )

    def generate(self) -> None:
        tree = self._generator.build_tree()

        if self._output_file:
            tree.appendleft("```")
            tree.append("```")
            with open(self._output_file, "w", encoding="utf-8") as f:
                for line in tree:
                    print(line, file=f)
        else:
            for line in tree:
                print(line)


class _TreeGenerator:
    def __init__(
        self,
        *,
        root_dir: pathlib.Path,
        dir_only: bool,
        files_only: bool,
        dirs_first: bool,
        files_first: bool,
        ignore: Optional[List[str]],
        use_gitignore: bool,
        depth_level: Optional[int],
    ) -> None:
        self._root_dir = root_dir
        self._dir_only = dir_only
        self._files_only = files_only
        self._dirs_first = dirs_first
        self._files_first = files_first
        self._ignore: Set[str] = set(ignore or [])
        self._depth_level = depth_level
        self._tree: Deque[str] = deque()

        self._gitignore = None
        if use_gitignore:
            try:
                import pathspec

                gitignore = root_dir / ".gitignore"
                if gitignore.exists():
                    patterns = gitignore.read_text().splitlines()
                    self._gitignore = pathspec.PathSpec.from_lines(
                        "gitwildmatch", patterns
                    )
            except ImportError:
                print(
                    "Warning: pathspec not installed, .gitignore ignored",
                    file=sys.stderr,
                )

    def build_tree(self) -> Deque[str]:
        self._tree.append(f"{self._root_dir.name}/")
        self._tree_body(self._root_dir, depth=0)
        return self._tree

    def _tree_body(
        self,
        directory: pathlib.Path,
        prefix: str = "",
        depth: int = 0,
    ) -> None:
        if self._depth_level is not None and depth >= self._depth_level:
            return

        entries = self._prepare_entries(directory)
        last_index = len(entries) - 1

        for index, entry in enumerate(entries):
            connector = ELBOW if index == last_index else TEE

            if entry.is_dir():
                self._tree.append(f"{prefix}{connector} {entry.name}/")
                extension = SPACE_PREFIX if index == last_index else PIPE_PREFIX
                self._tree_body(entry, prefix + extension, depth + 1)
            else:
                self._tree.append(f"{prefix}{connector} {entry.name}")

    def _prepare_entries(self, directory: pathlib.Path) -> List[pathlib.Path]:
        entries = sorted(directory.iterdir(), key=lambda e: e.name.lower())

        entries = [e for e in entries if not self._is_ignored(e)]

        if self._dir_only:
            return [e for e in entries if e.is_dir()]

        if self._files_only:
            return [e for e in entries if e.is_file()]

        if self._dirs_first:
            entries.sort(key=lambda e: (e.is_file(), e.name.lower()))
        elif self._files_first:
            entries.sort(key=lambda e: (e.is_dir(), e.name.lower()))

        return entries

    def _is_ignored(self, entry: pathlib.Path) -> bool:
        for pattern in self._ignore:
            if fnmatch(entry.name, pattern):
                return True

        if self._gitignore:
            try:
                rel = entry.relative_to(self._root_dir)
                if self._gitignore.match_file(str(rel)):
                    return True
            except ValueError:
                pass

        return False