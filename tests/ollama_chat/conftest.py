"""
Pytest configuration file for ollama_chat tests.
"""

import pytest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Common fixtures can be added here if needed 