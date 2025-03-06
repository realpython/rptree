from collections import deque
from io import StringIO

import pytest

from rptree.rptree import DirectoryTree, _TreeGenerator


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory structure for testing."""
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir2").mkdir()
    (tmp_path / "dir1" / "file1.txt").write_text("content")
    (tmp_path / "dir2" / "file2.txt").write_text("content")
    (tmp_path / "file3.txt").write_text("content")
    return tmp_path


def test_directory_tree_full(temp_dir):
    """Test generating a full directory tree including files."""
    output = StringIO()
    tree = DirectoryTree(str(temp_dir), output_file=output)
    tree.generate()
    result = output.getvalue()
    assert "dir1/" in result
    assert "dir2/" in result
    assert "file3.txt" in result
    assert "file1.txt" in result
    assert "file2.txt" in result


def test_directory_tree_dir_only(temp_dir):
    """Test generating a directory tree with only directories."""
    output = StringIO()
    tree = DirectoryTree(str(temp_dir), dir_only=True, output_file=output)
    tree.generate()
    result = output.getvalue()
    assert "dir1/" in result
    assert "dir2/" in result
    assert "file3.txt" not in result
    assert "file1.txt" not in result
    assert "file2.txt" not in result


def test_directory_tree_max_depth(temp_dir):
    """Test generating a directory tree with max depth constraint."""
    output = StringIO()
    tree = DirectoryTree(str(temp_dir), output_file=output, max_depth=1)
    tree.generate()
    result = output.getvalue()
    assert "dir1/" in result
    assert "dir2/" in result
    assert "file3.txt" in result
    assert "file1.txt" not in result
    assert "file2.txt" not in result


def test_tree_generator(temp_dir):
    """Test the _TreeGenerator class separately."""
    generator = _TreeGenerator(str(temp_dir))
    tree = generator.build_tree()
    assert isinstance(tree, deque)
    assert len(tree) > 0
    assert any("dir1/" in line for line in tree)
    assert any("dir2/" in line for line in tree)
    assert any("file3.txt" in line for line in tree)
