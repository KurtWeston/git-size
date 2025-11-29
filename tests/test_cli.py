"""Tests for CLI commands."""
import pytest
from click.testing import CliRunner
from git import Repo
from git_size.cli import cli


class TestCLI:
    """Test CLI commands."""

    @pytest.fixture
    def temp_repo(self, tmp_path):
        """Create a temporary git repository."""
        repo = Repo.init(tmp_path)
        (tmp_path / "test.txt").write_text("x" * 1000)
        repo.index.add(["test.txt"])
        repo.index.commit("Initial commit")
        return tmp_path

    @pytest.fixture
    def runner(self):
        """Create CLI runner."""
        return CliRunner()

    def test_top_command(self, runner, temp_repo):
        """Test top command."""
        result = runner.invoke(cli, ['top', '-p', str(temp_repo)])
        assert result.exit_code == 0
        assert 'test.txt' in result.output or result.output != ''

    def test_top_command_with_limit(self, runner, temp_repo):
        """Test top command with limit."""
        result = runner.invoke(cli, ['top', '-n', '5', '-p', str(temp_repo)])
        assert result.exit_code == 0

    def test_top_command_json_output(self, runner, temp_repo):
        """Test top command JSON output."""
        result = runner.invoke(cli, ['top', '--json', '-p', str(temp_repo)])
        assert result.exit_code == 0
        assert '[' in result.output or '{' in result.output

    def test_top_command_invalid_repo(self, runner, tmp_path):
        """Test top command with invalid repository."""
        result = runner.invoke(cli, ['top', '-p', str(tmp_path)])
        assert result.exit_code != 0

    def test_dirs_command(self, runner, temp_repo):
        """Test dirs command."""
        result = runner.invoke(cli, ['dirs', '-p', str(temp_repo)])
        assert result.exit_code == 0

    def test_deleted_command(self, runner, temp_repo):
        """Test deleted command."""
        result = runner.invoke(cli, ['deleted', '-p', str(temp_repo)])
        assert result.exit_code == 0

    def test_lfs_command(self, runner, temp_repo):
        """Test lfs command."""
        result = runner.invoke(cli, ['lfs', '-p', str(temp_repo)])
        assert result.exit_code == 0

    def test_stats_command(self, runner, temp_repo):
        """Test stats command."""
        result = runner.invoke(cli, ['stats', '-p', str(temp_repo)])
        assert result.exit_code == 0