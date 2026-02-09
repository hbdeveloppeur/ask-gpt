"""Tests for config module."""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from ask_gpt.config import Config, AVAILABLE_MODELS, DEFAULT_CONFIG, config


class TestConfig:
    """Test configuration management."""

    def test_default_config_values(self):
        """Test default configuration values."""
        assert DEFAULT_CONFIG["model"] == "gpt-4.1"
        assert DEFAULT_CONFIG["max_input_chars"] == 3000
        assert DEFAULT_CONFIG["temperature"] == 0.7

    def test_available_models(self):
        """Test available models list."""
        assert "gpt-4.1" in AVAILABLE_MODELS
        assert "gpt-4.1-mini" in AVAILABLE_MODELS
        assert "gpt-4.1-nano" in AVAILABLE_MODELS
        assert "gpt-5.2" in AVAILABLE_MODELS
        assert "gpt-5.1" in AVAILABLE_MODELS
        assert "gpt-5.2-mini" in AVAILABLE_MODELS
        assert "gpt-4o" in AVAILABLE_MODELS
        assert "gpt-4o-mini" in AVAILABLE_MODELS

    def test_config_loads_defaults(self):
        """Test config loads default values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(Path, "home", return_value=Path(tmpdir)):
                cfg = Config()
                assert cfg.model == "gpt-4.1"
                assert cfg.max_input_chars == 3000
                assert cfg.temperature == 0.7

    def test_config_save_and_load(self):
        """Test saving and loading configuration."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(Path, "home", return_value=Path(tmpdir)):
                cfg = Config()
                cfg.model = "gpt-5.2"
                cfg.save()
                
                # Load again
                cfg2 = Config()
                assert cfg2.model == "gpt-5.2"

    def test_config_get_api_key_from_env(self):
        """Test getting API key from environment."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-123"}):
            assert config.get_api_key() == "test-key-123"

    def test_config_get_api_key_missing(self):
        """Test getting API key when not set."""
        with patch.dict(os.environ, {}, clear=True):
            assert config.get_api_key() is None

    def test_config_properties(self):
        """Test config property setters."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(Path, "home", return_value=Path(tmpdir)):
                cfg = Config()
                
                cfg.model = "gpt-5.2"
                assert cfg.model == "gpt-5.2"
                
                cfg.max_input_chars = 3000
                assert cfg.max_input_chars == 3000
                
                cfg.temperature = 0.5
                assert cfg.temperature == 0.5

    def test_config_migration_old_max_input_chars(self):
        """Test config auto-migrates old max_input_chars value."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.object(Path, "home", return_value=Path(tmpdir)):
                # Create config file with old value
                config_dir = Path(tmpdir) / ".config" / "ask-gpt"
                config_dir.mkdir(parents=True)
                config_file = config_dir / "config.json"
                config_file.write_text('{"max_input_chars": 2000, "model": "gpt-4"}')
                
                # Load config - should auto-migrate
                cfg = Config()
                assert cfg.max_input_chars == 3000  # Migrated to new default
                
                # Verify it was saved
                cfg2 = Config()
                assert cfg2.max_input_chars == 3000
