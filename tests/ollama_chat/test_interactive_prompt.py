"""
Tests for the interactive prompt module.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.ollama_chat.interactive_prompt import InteractivePrompt

@patch('sys.stdout')
def test_init(mock_stdout):
    """Test prompt initialization."""
    prompt = InteractivePrompt()
    assert prompt.prompt_text == ">>> "
    assert prompt.current_input == ""
    assert prompt.cursor_pos == 0
    
    custom_prompt = InteractivePrompt("Test> ")
    assert custom_prompt.prompt_text == "Test> "

@patch('sys.stdout')
@patch('sys.stdin')
def test_get_input_basic(mock_stdin, mock_stdout):
    """Test basic input functionality."""
    prompt = InteractivePrompt()
    
    # Simulate typing "hello" and pressing enter
    mock_stdin.fileno.return_value = 0
    mock_stdin.read.side_effect = ['h', 'e', 'l', 'l', 'o', '\r']
    
    with patch('termios.tcgetattr') as mock_tcgetattr, \
         patch('termios.tcsetattr') as mock_tcsetattr, \
         patch('tty.setraw') as mock_setraw:
        result = prompt.get_input()
    
    assert result == "hello"
    assert "hello" in prompt.get_history()

@patch('sys.stdout')
@patch('sys.stdin')
def test_arrow_key_navigation(mock_stdin, mock_stdout):
    """Test arrow key navigation."""
    prompt = InteractivePrompt()
    
    # Add some history
    prompt.history.add_command("first")
    prompt.history.add_command("second")
    
    # Simulate pressing up arrow, then down arrow, then enter
    mock_stdin.fileno.return_value = 0
    mock_stdin.read.side_effect = [
        '\x1b', '[', 'A',  # Up arrow
        '\x1b', '[', 'B',  # Down arrow
        '\r'
    ]
    
    with patch('termios.tcgetattr') as mock_tcgetattr, \
         patch('termios.tcsetattr') as mock_tcsetattr, \
         patch('tty.setraw') as mock_setraw:
        result = prompt.get_input()
    
    # Should have navigated through history
    mock_stdout.write.assert_called()

@patch('sys.stdout')
@patch('sys.stdin')
def test_backspace(mock_stdin, mock_stdout):
    """Test backspace functionality."""
    prompt = InteractivePrompt()
    
    # Simulate typing "hello", backspace twice, then enter
    mock_stdin.fileno.return_value = 0
    mock_stdin.read.side_effect = [
        'h', 'e', 'l', 'l', 'o',
        '\x7f', '\x7f',  # Backspace twice
        '\r'
    ]
    
    with patch('termios.tcgetattr') as mock_tcgetattr, \
         patch('termios.tcsetattr') as mock_tcsetattr, \
         patch('tty.setraw') as mock_setraw:
        result = prompt.get_input()
    
    assert result == "hel"
    assert "hel" in prompt.get_history()

@patch('sys.stdout')
@patch('sys.stdin')
def test_ctrl_c(mock_stdin, mock_stdout):
    """Test Ctrl+C handling."""
    prompt = InteractivePrompt()
    
    # Simulate pressing Ctrl+C
    mock_stdin.fileno.return_value = 0
    mock_stdin.read.side_effect = ['\x03']
    
    with patch('termios.tcgetattr') as mock_tcgetattr, \
         patch('termios.tcsetattr') as mock_tcsetattr, \
         patch('tty.setraw') as mock_setraw:
        result = prompt.get_input()
    
    assert result is None 