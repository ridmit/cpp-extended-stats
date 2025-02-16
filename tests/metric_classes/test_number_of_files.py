import os
import pytest

from src.metric_classes.number_of_files import NumberOfFiles


class TestNumberOfFiles:
    @pytest.mark.parametrize(
        "repo_path, short_paths",
        [("tests/data/gitignore", ["inner/A.h", "inner/B.hpp", "inner/C.c", "inner/D.C",
                                   "inner/E.cc", "F.cpp", "G.CPP", "H.c++", "K.cp", "L.cxx"]),
         ("tests/data/inheritance/multiple", ["C.cpp", "B.cpp", "dir/A.cpp"]),
         ("tests/data/several_classes_in_file", ["ABCD/innerABCD/ABCD.cpp"]),
         ("tests/data/empty", [])])
    def test_get_files(self, repo_path, short_paths):
        number_of_files = NumberOfFiles(repo_path)

        filenames = sorted([file_cursor.path for file_cursor in number_of_files.get_files()])
        expected = sorted([os.path.join(repo_path, path) for path in short_paths])
        assert filenames == expected

    @pytest.mark.parametrize(
        "repo_path, expected",
        [("tests/data/gitignore", 10),
         ("tests/data/inheritance/multiple", 3),
         ("tests/data/inheritance", 12),
         ("tests/data/several_classes_in_file", 1),
         ("tests/data/empty", 0)])
    def test_result(self, repo_path, expected):
        number_of_files = NumberOfFiles(repo_path)

        assert number_of_files.result == expected
