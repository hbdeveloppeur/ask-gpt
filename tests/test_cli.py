"""Tests for CLI module."""

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner

from ask_gpt.cli import app, is_pipe_input, main, read_stdin

runner = CliRunner()


class TestIsPipeInput:
    """Test pipe input detection."""

    def test_is_pipe_input_tty(self):
        """Test detection when stdin is a TTY."""
        with patch.object(sys.stdin, "isatty", return_value=True):
            assert is_pipe_input() is False

    def test_is_pipe_input_not_tty(self):
        """Test detection when stdin is not a TTY (piped)."""
        with patch.object(sys.stdin, "isatty", return_value=False):
            assert is_pipe_input() is True


class TestReadStdin:
    """Test stdin reading."""

    def test_read_stdin(self):
        """Test reading from stdin."""
        with patch.object(sys.stdin, "read", return_value="test content"):
            assert read_stdin() == "test content"


class TestCLICommands:
    """Test CLI commands."""

    def test_models_command(self):
        """Test models list command."""
        result = runner.invoke(app, ["models"])
        assert result.exit_code == 0
        assert "gpt-4.1" in result.output

    def test_ask_command_missing_query(self):
        """Test ask command without query argument."""
        result = runner.invoke(app, ["ask"])
        assert result.exit_code != 0

    def test_ask_command_no_input(self):
        """Test ask command with no input source."""
        with patch.object(sys.stdin, "isatty", return_value=True):
            result = runner.invoke(app, ["ask", "test question"])
            assert result.exit_code == 1
            assert "input" in result.output.lower()

    def test_ask_command_with_file(self, tmp_path):
        """Test ask command with file input."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        with patch("ask_gpt.cli.query_openai") as mock_query:
            mock_query.return_value = ("One liner", "Detailed answer")
            result = runner.invoke(app, [
                "ask", 
                "test question",
                "-f", str(test_file)
            ])
            
            assert result.exit_code == 0
            mock_query.assert_called_once()

    def test_ask_command_file_not_found(self):
        """Test ask command with non-existent file."""
        result = runner.invoke(app, ["ask", "test", "-f", "/nonexistent/file.txt"])
        assert result.exit_code == 1
        assert "File not found" in result.output

    def test_ask_command_with_model_override(self, tmp_path):
        """Test ask command with model override."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        with patch("ask_gpt.cli.query_openai") as mock_query:
            mock_query.return_value = ("One", "Answer")
            result = runner.invoke(app, [
                "ask",
                "question",
                "-f", str(test_file),
                "-m", "gpt-5.2"
            ])
            
            assert result.exit_code == 0


class TestMainEntryPoint:
    """Test main entry point."""

    def test_main_no_args(self):
        """Test main with no arguments."""
        with patch("ask_gpt.cli.sys.exit") as mock_exit:
            with patch("ask_gpt.cli.console.print"):
                # Pass empty args directly
                main(args=[])
                # Verify sys.exit was called with 1
                mock_exit.assert_called_with(1)

    def test_main_with_subcommand(self):
        """Test main with subcommand."""
        with patch.object(sys, "argv", ["ask-gpt", "models"]):
            # Should not raise
            main()
