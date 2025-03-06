"""This module provides RP Tree main module."""

import os
import pathlib
import sys
from collections import deque
from typing import TextIO

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class DirectoryTree:
    def __init__(
        self,
        root_dir: str,
        dir_only: bool = False,
        output_file: str | TextIO = sys.stdout,
        max_depth: int | None = None,
    ) -> None:
        self._output_file = output_file
        self._generator = _TreeGenerator(root_dir, dir_only, max_depth)

    def generate(self) -> None:
        tree = self._generator.build_tree()

        if isinstance(self._output_file, str):
            # Wrap the tree in a markdown code block
            tree.appendleft("```")
            tree.append("```")

            with open(self._output_file, mode="w", encoding="UTF-8") as stream:
                for entry in tree:
                    print(entry, file=stream)
        else:
            for entry in tree:
                print(entry, file=self._output_file)


class _TreeGenerator:
    def __init__(
        self,
        root_dir: str,
        dir_only: bool = False,
        max_depth: int | None = None,
    ) -> None:
        self._root_dir = pathlib.Path(root_dir)
        self._dir_only = dir_only
        self._max_depth = max_depth
        self._tree: deque[str] = deque()

    def build_tree(self) -> deque[str]:
        self._tree_head()
        self._tree_body(self._root_dir, current_depth=0)
        return self._tree

    def _tree_head(self) -> None:
        self._tree.append(f"{self._root_dir}{os.sep}")

    def _tree_body(
        self,
        directory: pathlib.Path,
        prefix: str = "",
        current_depth: int = 0,
    ) -> None:
        # Stop recursion if max_depth is reached
        if self._max_depth is not None and current_depth >= self._max_depth:
            return

        entries = self._prepare_entries(directory)
        last_index = len(entries) - 1
        for index, entry in enumerate(entries):
            connector = ELBOW if index == last_index else TEE
            if entry.is_dir():
                if index == 0:
                    self._tree.append(prefix + PIPE)
                self._add_directory(
                    entry,
                    index,
                    last_index,
                    prefix,
                    connector,
                    current_depth,
                )
            else:
                self._add_file(entry, prefix, connector)

    def _prepare_entries(self, directory: pathlib.Path) -> list[pathlib.Path]:
        entries = sorted(directory.iterdir(), key=lambda entry: str(entry))
        if self._dir_only:
            return [entry for entry in entries if entry.is_dir()]
        return sorted(entries, key=lambda entry: entry.is_file())

    def _add_directory(
        self,
        directory: pathlib.Path,
        index: int,
        last_index: int,
        prefix: str,
        connector: str,
        current_depth: int,
    ) -> None:
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        if index != last_index:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(
            directory=directory,
            prefix=prefix,
            current_depth=current_depth + 1,
        )
        if prefix := prefix.rstrip():
            self._tree.append(prefix)

    def _add_file(self, file: pathlib.Path, prefix: str, connector: str) -> None:
        self._tree.append(f"{prefix}{connector} {file.name}")
