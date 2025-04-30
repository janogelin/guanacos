"""
Tests for the command history module.
"""

import pytest
from src.ollama_chat.command_history import CommandHistory

def test_add_command():
    """Test adding commands to history."""
    history = CommandHistory()
    
    # Test adding a single command
    history.add_command("test1")
    assert history.get_all_commands() == ["test1"]
    
    # Test adding multiple commands
    history.add_command("test2")
    history.add_command("test3")
    assert history.get_all_commands() == ["test1", "test2", "test3"]
    
    # Test that empty commands are not added
    history.add_command("")
    history.add_command("   ")
    assert history.get_all_commands() == ["test1", "test2", "test3"]

def test_navigation():
    """Test navigating through command history."""
    history = CommandHistory()
    
    # Add some test commands
    history.add_command("first")
    history.add_command("second")
    history.add_command("third")
    
    # Test navigation from most recent
    assert history.get_previous_command() == "second"
    assert history.get_previous_command() == "first"
    assert history.get_previous_command() == ""  # No more previous commands
    
    # Test navigation forward
    assert history.get_next_command() == "second"
    assert history.get_next_command() == "third"
    assert history.get_next_command() == ""  # No more next commands

def test_max_size():
    """Test that history respects maximum size limit."""
    history = CommandHistory()
    history.max_size = 3  # Set a small max size for testing
    
    # Add more commands than max_size
    history.add_command("one")
    history.add_command("two")
    history.add_command("three")
    history.add_command("four")
    
    # Check that only the most recent max_size commands are kept
    commands = history.get_all_commands()
    assert len(commands) == 3
    assert commands == ["two", "three", "four"]

def test_reset_navigation():
    """Test resetting navigation pointer."""
    history = CommandHistory()
    
    # Add some commands
    history.add_command("first")
    history.add_command("second")
    
    # Navigate back
    assert history.get_previous_command() == "first"
    
    # Reset navigation
    history.reset_navigation()
    
    # Should start from most recent again
    assert history.get_previous_command() == "first" 