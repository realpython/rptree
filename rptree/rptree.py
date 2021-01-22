"""This module provides RP Tree main module."""

import os
import pathlib
import sys

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "


class DirectoryTree:
    def __init__(self, root_dir, output_file=sys.stdout, dir_only=False):
        self._output_file = output_file
        self._generator = _TreeGenerator(root_dir, dir_only)

    def generate(self):
        tree = self._generator.generate_tree()
        if self._output_file != sys.stdout:
            tree.appendleft("```")
            tree.append("```")
            self._output_file = open(
                self._output_file, mode="w", encoding="UTF-8"
            )
        with self._output_file as stream:
            for item in tree:
                print(item, file=stream)


class _TreeGenerator:
    def __init__(self, root, dir_only=False):
        self._root = pathlib.Path(root)
        self.dir_only = dir_only
        self._tree = []

    def generate_tree(self):
        self._tree_head()
        self._tree_tail(self._root)
        return self._tree

    def _tree_head(self):
        self._tree.append(f"{self._root}{os.sep}")
        self._tree.append(PIPE)

    def _tree_tail(self, dir, prefix=""):
        entries = self._prepare_entries(dir)
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            path = dir.joinpath(entry)
            if path.is_dir():
                self._add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(prefix, connector, path)

    def _prepare_entries(self, dir):
        entries = dir.iterdir()
        if self.dir_only:
            entries = [e for e in entries if dir.joinpath(e).is_dir()]
            return entries
        entries = sorted(entries, key=lambda e: dir.joinpath(e).is_file())
        return entries

    def _add_directory(self, entry, index, entries_count, prefix, connector):
        self._tree.append(f"{prefix}{connector}{entry.name}{os.sep}")
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        self._tree_tail(
            dir=entry,
            prefix=prefix,
        )
        self._tree.append(prefix)

    def _add_file(self, prefix, connector, path):
        self._tree.append(f"{prefix}{connector} {path.name}")
