"""Tests for the CLI module."""

import pytest
import sys
from io import StringIO
from unittest.mock import patch
import tempfile
import os

from parstoken.cli import create_parser, main, cmd_count


class TestCLI:
    """Tests for CLI commands."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = create_parser()
    
    def test_parser_creation(self):
        """Parser should be created without errors."""
        assert self.parser is not None
    
    def test_normalize_command_parse(self):
        """Normalize command should parse correctly."""
        args = self.parser.parse_args(['normalize', 'input.txt'])
        assert args.command == 'normalize'
        assert args.input == 'input.txt'
    
    def test_clean_command_parse(self):
        """Clean command should parse correctly."""
        args = self.parser.parse_args(['clean', 'input.txt', '--remove-emojis'])
        assert args.command == 'clean'
        assert args.remove_emojis is True
    
    def test_optimize_command_parse(self):
        """Optimize command should parse correctly."""
        args = self.parser.parse_args(['optimize', 'input.txt', '--stats'])
        assert args.command == 'optimize'
        assert args.stats is True
    
    def test_count_command_parse(self):
        """Count command should parse correctly."""
        args = self.parser.parse_args(['count', 'input.txt', '--model', 'claude'])
        assert args.command == 'count'
        assert args.model == 'claude'
    
    def test_pipeline_command_parse(self):
        """Pipeline command should parse correctly."""
        args = self.parser.parse_args([
            'pipeline', 'input.txt',
            '--normalize', '--clean', '--optimize',
        ])
        assert args.command == 'pipeline'
        assert args.normalize is True
        assert args.clean is True
        assert args.optimize is True
    
    def test_normalize_with_file(self):
        """Normalize command should process a file."""
        with tempfile.NamedTemporaryFile(
            mode='w', suffix='.txt', delete=False, encoding='utf-8'
        ) as f:
            f.write("متن فارسي با كاراكترهاي عربي")
            f.flush()
            input_path = f.name
        
        try:
            output_path = input_path + '.out'
            with patch('sys.argv', ['parstoken', 'normalize', input_path, '-o', output_path]):
                main()
            
            with open(output_path, 'r', encoding='utf-8') as f:
                result = f.read()
            
            assert "فارسی" in result
            assert "کاراکترهای" in result
        finally:
            os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_no_command_shows_help(self):
        """Running without command should exit with code 1."""
        with patch('sys.argv', ['parstoken']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
    
    def test_file_not_found(self):
        """Non-existent file should exit with error."""
        with patch('sys.argv', ['parstoken', 'normalize', 'nonexistent.txt']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
