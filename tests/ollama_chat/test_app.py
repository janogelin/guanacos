"""
Tests for the main application module.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.ollama_chat.app import OllamaChatApp

def test_init():
    """Test application initialization."""
    app = OllamaChatApp()
    assert app.client.host == 'http://localhost:11434'
    assert app.client.model == 'gemma:4b'
    assert app.prompt.prompt_text == "Chat 🗣️ > "
    assert app.client.system_prompt is not None  # Should have music lover persona

def test_init_custom_params():
    """Test initialization with custom parameters."""
    app = OllamaChatApp('http://example.com', 'custom-model')
    assert app.client.host == 'http://example.com'
    assert app.client.model == 'custom-model'

@patch('src.ollama_chat.ollama_client.OllamaClient.check_connection')
def test_check_ollama_connection(mock_check):
    """Test Ollama server connection check."""
    app = OllamaChatApp()
    
    # Test successful connection
    mock_check.return_value = True
    assert app.check_ollama_connection() is True
    
    # Test failed connection
    mock_check.return_value = False
    assert app.check_ollama_connection() is False

@patch('src.ollama_chat.app.OllamaChatApp.check_ollama_connection')
@patch('src.ollama_chat.interactive_prompt.InteractivePrompt.get_input')
@patch('src.ollama_chat.ollama_client.OllamaClient.chat')
def test_run_normal_flow(mock_chat, mock_input, mock_check):
    """Test normal application flow."""
    app = OllamaChatApp()
    
    # Mock successful connection
    mock_check.return_value = True
    
    # Mock user input and chat response
    mock_input.side_effect = ["test question", None]  # None simulates Ctrl+C
    mock_chat.return_value = iter(["Response part 1", "Response part 2"])
    
    # Run the application
    app.run()
    
    # Verify interactions
    mock_chat.assert_called_once_with("test question")
    assert mock_input.call_count == 2

@patch('src.ollama_chat.app.OllamaChatApp.check_ollama_connection')
@patch('src.ollama_chat.interactive_prompt.InteractivePrompt.get_input')
@patch('src.ollama_chat.ollama_client.OllamaClient.chat')
def test_run_empty_input(mock_chat, mock_input, mock_check):
    """Test handling of empty input."""
    app = OllamaChatApp()
    
    # Mock successful connection
    mock_check.return_value = True
    
    # Mock empty input followed by exit
    mock_input.side_effect = ["", "   ", None]
    
    # Run the application
    app.run()
    
    # Verify that chat was never called
    mock_chat.assert_not_called()

@patch('src.ollama_chat.app.OllamaChatApp.check_ollama_connection')
def test_run_connection_failure(mock_check):
    """Test handling of Ollama server connection failure."""
    app = OllamaChatApp()
    
    # Mock failed connection
    mock_check.return_value = False
    
    with pytest.raises(SystemExit) as exc_info:
        app.run()
    
    assert exc_info.value.code == 1

@patch('src.ollama_chat.app.OllamaChatApp.check_ollama_connection')
@patch('src.ollama_chat.interactive_prompt.InteractivePrompt.get_input')
@patch('src.ollama_chat.ollama_client.OllamaClient.chat')
def test_run_chat_error(mock_chat, mock_input, mock_check):
    """Test handling of chat errors."""
    app = OllamaChatApp()
    
    # Mock successful connection but failed chat
    mock_check.return_value = True
    mock_input.side_effect = ["test question", None]
    mock_chat.side_effect = Exception("Test error")
    
    # Run should continue despite chat error
    app.run()
    
    # Verify error was handled
    mock_chat.assert_called_once() 