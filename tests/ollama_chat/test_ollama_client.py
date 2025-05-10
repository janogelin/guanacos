"""
Tests for the Ollama client module.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.ollama_chat.ollama_client import OllamaClient
import requests
from requests.exceptions import HTTPError

def test_init():
    """Test client initialization."""
    client = OllamaClient()
    assert client.host == 'http://localhost:11434'
    assert client.model == 'gemma3:4b'
    assert client.system_prompt is None
    
    client = OllamaClient('http://example.com/', 'different-model')
    assert client.host == 'http://example.com'
    assert client.model == 'different-model'

def test_set_system_prompt():
    """Test setting system prompt."""
    client = OllamaClient()
    test_prompt = "Test system prompt"
    client.set_system_prompt(test_prompt)
    assert client.system_prompt == test_prompt

@patch('requests.post')
def test_chat_success(mock_post):
    """Test successful chat interaction."""
    # Mock the streaming response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.iter_lines.return_value = [
        b'{"message": {"content": "Hello"}}',
        b'{"message": {"content": " world"}}'
    ]
    mock_post.return_value = mock_response
    
    client = OllamaClient()
    responses = list(client.chat("Test message"))
    
    assert responses == ["Hello", " world"]
    mock_post.assert_called_once()
    
    # Verify the request payload
    call_args = mock_post.call_args
    assert call_args[1]['json']['model'] == 'gemma3:4b'
    assert call_args[1]['json']['messages'][0]['content'] == "Test message"

@patch('requests.post')
def test_chat_with_system_prompt(mock_post):
    """Test chat with system prompt set."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.iter_lines.return_value = [b'{"message": {"content": "Response"}}']
    mock_post.return_value = mock_response
    
    client = OllamaClient()
    client.set_system_prompt("System instruction")
    list(client.chat("Test message"))
    
    # Verify system prompt was included
    call_args = mock_post.call_args
    messages = call_args[1]['json']['messages']
    assert len(messages) == 2
    assert messages[0]['role'] == 'system'
    assert messages[0]['content'] == "System instruction"
    assert messages[1]['content'] == "Test message"

@patch('requests.post')
def test_chat_error_handling(mock_post):
    """Test error handling in chat."""
    # Test generic exception
    mock_post.side_effect = Exception("Test error")
    client = OllamaClient()
    responses = list(client.chat("Test message"))
    assert len(responses) == 1
    assert "Error: An unexpected error occurred: Test error" in responses[0]
    
    # Test request exception
    mock_post.side_effect = requests.exceptions.RequestException("Connection failed")
    responses = list(client.chat("Test message"))
    assert len(responses) == 1
    assert "Error: Request failed: Connection failed" in responses[0]
    
    # Test JSON decode error
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.iter_lines.return_value = [b'invalid json']
    mock_post.side_effect = None
    mock_post.return_value = mock_response
    
    responses = list(client.chat("Test message"))
    assert len(responses) == 1
    assert "Error: Invalid response format from Ollama server" in responses[0]

@patch('requests.get')
def test_check_connection(mock_get):
    """Test connection check functionality."""
    client = OllamaClient()
    
    # Test successful connection
    mock_get.return_value.status_code = 200
    mock_get.return_value.raise_for_status.side_effect = None
    success, message = client.check_connection()
    assert success is True
    
    # Test failed connection
    mock_get.return_value.status_code = 500
    mock_get.return_value.raise_for_status.side_effect = HTTPError("Server error")
    success, message = client.check_connection()
    assert success is False
    
    # Test connection error
    mock_get.side_effect = Exception("Connection error")
    success, message = client.check_connection()
    assert success is False 