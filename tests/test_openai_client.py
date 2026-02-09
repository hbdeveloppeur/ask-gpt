"""Tests for OpenAI client module."""

from unittest.mock import Mock, patch

import pytest

from ask_gpt.openai_client import chunk_input, get_client, query_openai


class TestChunkInput:
    """Test input chunking functionality."""

    def test_short_input_not_truncated(self):
        """Test short input is not truncated."""
        text = "Short text"
        result = chunk_input(text, max_chars=100)
        assert result == text

    def test_long_input_truncated(self):
        """Test long input is truncated."""
        text = "a" * 3000
        result = chunk_input(text, max_chars=2000)
        assert len(result) == 2000

    def test_exact_length_input(self):
        """Test input at exact max length."""
        text = "a" * 2000
        result = chunk_input(text, max_chars=2000)
        assert result == text


class TestGetClient:
    """Test OpenAI client initialization."""

    def test_get_client_with_api_key(self):
        """Test client creation with API key."""
        with patch("ask_gpt.openai_client.config") as mock_config:
            mock_config.get_api_key.return_value = "sk-test-key"
            with patch("ask_gpt.openai_client.OpenAI") as mock_openai:
                mock_openai.return_value = Mock()
                client = get_client()
                assert client is not None
                mock_openai.assert_called_once_with(api_key="sk-test-key")

    def test_get_client_without_api_key_exits(self):
        """Test client creation without API key exits."""
        with patch("ask_gpt.openai_client.config") as mock_config:
            mock_config.get_api_key.return_value = None
            with patch("ask_gpt.openai_client.sys.exit") as mock_exit:
                get_client()
                mock_exit.assert_called_once_with(1)


class TestQueryOpenAI:
    """Test OpenAI query functionality."""

    def test_query_openai_success(self):
        """Test successful query to OpenAI."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "One liner---Detailed answer here"
        
        with patch("ask_gpt.openai_client.get_client") as mock_get_client:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_get_client.return_value = mock_client
            
            one_liner, answer = query_openai("What is this?", "Some content")
            
            assert one_liner == "One liner"
            assert answer == "Detailed answer here"

    def test_query_openai_no_separator(self):
        """Test query without separator in response."""
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "First line\nSecond line\nThird line"
        
        with patch("ask_gpt.openai_client.get_client") as mock_get_client:
            mock_client = Mock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_get_client.return_value = mock_client
            
            one_liner, answer = query_openai("What is this?", "content")
            
            assert one_liner == "First line"
            assert answer == "Second line\nThird line"

    def test_query_openai_api_error(self):
        """Test handling of API error."""
        from openai import OpenAIError
        
        with patch("ask_gpt.openai_client.get_client") as mock_get_client:
            mock_client = Mock()
            mock_client.chat.completions.create.side_effect = OpenAIError("API Error")
            mock_get_client.return_value = mock_client
            
            one_liner, answer = query_openai("What?", "content")
            
            assert "Error" in one_liner
            assert "API Error" in answer
