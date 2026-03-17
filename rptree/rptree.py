"""This module provides RP Tree main module."""

import pathlib
from collections import deque
from typing import Iterable, Optional, Set

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class DirectoryTree:
    def __init__(
        self,
        root_dir: str | pathlib.Path,
        dir_only: bool = False,
        files_only: bool = False,
        dirs_first: bool = False,
        files_first: bool = False,
        output_file: Optional[str] = None,
        ignore: Optional[Iterable[str]] = None,
        use_gitignore: bool = False,
    ) -> None:
        self._root_dir = pathlib.Path(root_dir)
        self._output_file = output_file

        if dir_only and files_only:
            raise ValueError("Cannot use dir_only and files_only together")

        if dir_only and (dirs_first or files_first):
            raise ValueError("Ordering options are not valid with dir_only")

        if files_only and (dirs_first or files_first):
            raise ValueError("Ordering options are not valid with files_only")

        if dirs_first and files_first:
            raise ValueError("Cannot enable dirs_first and files_first together")

        self._generator = _TreeGenerator(
            root_dir=self._root_dir,
            dir_only=dir_only,
            files_only=files_only,
            dirs_first=dirs_first,
            files_first=files_first,
            ignore=ignore,
            use_gitignore=use_gitignore,
        )

    def generate(self) -> None:
        tree = self._generator.build_tree()

        if self._output_file:
            with open(self._output_file, "w", encoding="utf-8") as stream:
                for entry in tree:
                    print(entry, file=stream)
        else:
            for entry in tree:
                print(entry)


class _TreeGenerator:
    def __init__(
        self,
        root_dir: pathlib.Path,
        dir_only: bool = False,
        files_only: bool = False,
        dirs_first: bool = False,
        files_first: bool = False,
        ignore: Optional[Iterable[str]] = None,
        use_gitignore: bool = False,
    ) -> None:
        self._root_dir: pathlib.Path = root_dir
        self._dir_only: bool = dir_only
        self._files_only: bool = files_only
        self._dirs_first: bool = dirs_first
        self._files_first: bool = files_first
        self._ignore: Set[str] = set(ignore or [])
        self._tree: deque[str] = deque()
        self._gitignore_spec = None

        if use_gitignore:
            self._load_gitignore()

    def _load_gitignore(self) -> None:
        gitignore = self._root_dir / ".gitignore"
        if not gitignore.exists():
            return

        try:
            import pathspec

            with open(gitignore) as f:
                self._gitignore_spec = pathspec.PathSpec.from_lines(
                    "gitwildmatch", f
                )
        except ImportError:
            pass

    def build_tree(self) -> deque[str]:
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self) -> None:
        self._tree.append(f"{self._root_dir}/")

    def _tree_body(self, directory: pathlib.Path, prefix: str = "") -> None:
        entries = self._prepare_entries(directory)
        last_index = len(entries) - 1

        for index, entry in enumerate(entries):
            connector = ELBOW if index == last_index else TEE

            if entry.is_dir():
                self._add_directory(entry, index, last_index, prefix, connector)
            else:
                self._add_file(entry, prefix, connector)

    def _prepare_entries(self, directory: pathlib.Path) -> list[pathlib.Path]:
        entries: list[pathlib.Path] = []

        for entry in directory.iterdir():
            if entry.name in self._ignore:
                continue

            if self._gitignore_spec and self._gitignore_spec.match_file(
                str(entry.relative_to(self._root_dir))
            ):
                continue

            entries.append(entry)

        if self._dir_only:
            entries = [e for e in entries if e.is_dir()]

        if self._files_only:
            entries = [e for e in entries if e.is_file()]

        entries.sort(key=lambda e: e.name.lower())

        if self._dirs_first:
            entries.sort(key=lambda e: e.is_file())

        if self._files_first:
            entries.sort(key=lambda e: e.is_dir())

        return entries

    def _add_directory(
        self,
        directory: pathlib.Path,
        index: int,
        last_index: int,
        prefix: str,
        connector: str,
    ) -> None:
        self._tree.append(f"{prefix}{connector} {directory.name}/")

        if index != last_index:
            new_prefix = prefix + PIPE_PREFIX
        else:
            new_prefix = prefix + SPACE_PREFIX

        self._tree_body(directory, new_prefix)

    def _add_file(
        self,
        file: pathlib.Path,
        prefix: str,
        connector: str,
    ) -> None:
        self._tree.append(f"{prefix}{connector} {file.name}")