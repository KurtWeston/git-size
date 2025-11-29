"""Tests for formatting utilities."""
import pytest
import json
from git_size.formatter import format_size, format_table, format_json


class TestFormatter:
    """Test formatting functions."""

    def test_format_size_bytes(self):
        """Test formatting bytes."""
        assert format_size(500) == "500.00 B"
        assert format_size(0) == "0.00 B"

    def test_format_size_kilobytes(self):
        """Test formatting kilobytes."""
        assert format_size(1024) == "1.00 KB"
        assert format_size(2048) == "2.00 KB"

    def test_format_size_megabytes(self):
        """Test formatting megabytes."""
        assert format_size(1024 * 1024) == "1.00 MB"
        assert format_size(5 * 1024 * 1024) == "5.00 MB"

    def test_format_size_gigabytes(self):
        """Test formatting gigabytes."""
        assert format_size(1024 * 1024 * 1024) == "1.00 GB"

    def test_format_table_files(self):
        """Test table formatting for files."""
        data = [
            {'path': 'test.txt', 'size': 1024, 'sha': 'abc123'},
            {'path': 'file.py', 'size': 2048, 'commit': 'def456'}
        ]
        table = format_table(data, "Test Files")
        
        assert table is not None
        assert table.title == "Test Files"

    def test_format_table_directories(self):
        """Test table formatting for directories."""
        data = [
            {'path': 'src', 'size': 10240},
            {'path': 'tests', 'size': 5120}
        ]
        table = format_table(data, "Directories", is_dir=True)
        
        assert table is not None
        assert table.title == "Directories"

    def test_format_json_output(self):
        """Test JSON formatting."""
        data = [
            {'path': 'test.txt', 'size': 1024, 'sha': 'abc123'},
            {'path': 'file.py', 'size': 2048}
        ]
        result = format_json(data)
        
        parsed = json.loads(result)
        assert len(parsed) == 2
        assert 'size_human' in parsed[0]
        assert parsed[0]['size'] == 1024

    def test_format_json_preserves_fields(self):
        """Test JSON formatting preserves original fields."""
        data = [{'path': 'test.txt', 'size': 1024, 'custom': 'value'}]
        result = format_json(data)
        
        parsed = json.loads(result)
        assert parsed[0]['custom'] == 'value'
        assert parsed[0]['path'] == 'test.txt'