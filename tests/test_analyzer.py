"""Tests for GitAnalyzer core functionality."""
import pytest
from pathlib import Path
from git import Repo
from git_size.analyzer import GitAnalyzer


class TestGitAnalyzer:
    """Test GitAnalyzer class."""

    @pytest.fixture
    def temp_repo(self, tmp_path):
        """Create a temporary git repository."""
        repo = Repo.init(tmp_path)
        
        # Create test files
        (tmp_path / "large.txt").write_text("x" * 1000)
        (tmp_path / "small.txt").write_text("y" * 100)
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "nested.py").write_text("z" * 500)
        
        repo.index.add(["large.txt", "small.txt", "subdir/nested.py"])
        repo.index.commit("Initial commit")
        
        # Create and delete a file
        (tmp_path / "deleted.txt").write_text("d" * 800)
        repo.index.add(["deleted.txt"])
        repo.index.commit("Add deleted file")
        (tmp_path / "deleted.txt").unlink()
        repo.index.remove(["deleted.txt"])
        repo.index.commit("Delete file")
        
        return tmp_path

    def test_init_valid_repo(self, temp_repo):
        """Test initialization with valid repository."""
        analyzer = GitAnalyzer(str(temp_repo))
        assert analyzer.repo is not None
        assert analyzer.repo_path == temp_repo

    def test_init_invalid_repo(self, tmp_path):
        """Test initialization with invalid repository."""
        with pytest.raises(ValueError, match="Not a git repository"):
            GitAnalyzer(str(tmp_path))

    def test_get_largest_files(self, temp_repo):
        """Test getting largest files."""
        analyzer = GitAnalyzer(str(temp_repo))
        files = analyzer.get_largest_files(limit=10)
        
        assert len(files) > 0
        assert files[0]['size'] >= files[-1]['size']
        assert 'path' in files[0]
        assert 'size' in files[0]
        assert 'sha' in files[0]

    def test_get_largest_files_with_threshold(self, temp_repo):
        """Test filtering by minimum size."""
        analyzer = GitAnalyzer(str(temp_repo))
        files = analyzer.get_largest_files(limit=10, min_size=600)
        
        assert all(f['size'] >= 600 for f in files)

    def test_get_largest_files_with_extension(self, temp_repo):
        """Test filtering by file extension."""
        analyzer = GitAnalyzer(str(temp_repo))
        files = analyzer.get_largest_files(limit=10, extensions=('.py',))
        
        assert all(f['path'].endswith('.py') for f in files)

    def test_get_largest_directories(self, temp_repo):
        """Test directory size calculation."""
        analyzer = GitAnalyzer(str(temp_repo))
        dirs = analyzer.get_largest_directories(limit=5)
        
        assert len(dirs) > 0
        assert dirs[0]['size'] >= dirs[-1]['size']
        assert 'path' in dirs[0]
        assert 'size' in dirs[0]

    def test_get_deleted_files(self, temp_repo):
        """Test finding deleted files."""
        analyzer = GitAnalyzer(str(temp_repo))
        deleted = analyzer.get_deleted_files(limit=10)
        
        assert len(deleted) > 0
        assert any('deleted.txt' in f['path'] for f in deleted)
        assert all('size' in f for f in deleted)

    def test_get_stats(self, temp_repo):
        """Test repository statistics."""
        analyzer = GitAnalyzer(str(temp_repo))
        stats = analyzer.get_stats()
        
        assert 'total_size' in stats
        assert 'object_count' in stats
        assert 'commit_count' in stats
        assert stats['total_size'] > 0
        assert stats['commit_count'] >= 3

    def test_suggest_lfs_candidates(self, temp_repo):
        """Test LFS candidate suggestion."""
        analyzer = GitAnalyzer(str(temp_repo))
        candidates = analyzer.suggest_lfs_candidates(threshold=500)
        
        assert isinstance(candidates, list)
        assert all(c['size'] >= 500 for c in candidates)