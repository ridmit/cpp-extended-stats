import os
import subprocess
from typing import List
from clang.cindex import Config, Index

from src.cursor_classes.file_cursor import FileCursor


class NumberOfFiles:
    """
    Collects FileCursors and calculates number of C/C++ files
    """
    __extensions: List[str] = [".cpp", ".h", ".c"]

    def __init__(self, repo_path: str):
        self._name = "NUMBER_OF_FILES"
        self._file_cursors = self._collect_files(repo_path)

    @property
    def name(self) -> str:
        return self._name

    def get_files(self) -> List[FileCursor]:
        return self._file_cursors

    @property
    def result(self) -> int:
        return len(self._file_cursors)

    def _collect_files(self, repo_path: str) -> List[FileCursor]:
        """ Iterates over a folder and collects FileCursors"""

        # Set the path in which to search for libclang
        if not Config.library_file:
            Config.set_library_file("/path/to/libclang.dll")
        index = Index.create()

        # Gets all tracked (--cached) and untracked (--others) filenames except standard git
        # exclusions: .gitignore in each directory, and the user’s global exclusion file.
        filenames = subprocess.run(
            args=["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=repo_path, capture_output=True, text=True).stdout.splitlines()

        file_cursors = []
        for file in filenames:
            _, ext = os.path.splitext(file)
            if ext in self.__extensions:
                cursor = index.parse(os.path.join(repo_path, file)).cursor
                file_cursors.append(FileCursor(cursor, os.path.join(repo_path, file)))
        return file_cursors
