"""Pytest configuration and fixtures."""

import pytest


@pytest.fixture(autouse=True)
def mock_env_setup(monkeypatch):
    """Set up clean environment for tests."""
    # Ensure no real API key is used
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
