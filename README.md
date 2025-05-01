# AI Test Programs Collection

This repository contains a collection of experimental programs exploring different AI technologies and APIs.

## Current Programs

### Interactive Music Chat (src/ollama_chat)
A modular interactive chat application that uses the Ollama API with a music lover persona. Features include:
- Interactive command-line interface with command history
- Up/Down arrow key navigation through previous commands
- Streaming responses from the Ollama API
- Uses the `gemma3:4b` model by default
- Implements a knowledgeable music enthusiast personality
- Enhanced error handling and connection verification
- Configurable timeout settings

#### Project Structure
```
.
├── src/
│   └── ollama_chat/
│       ├── __init__.py
│       ├── app.py              # Main application
│       ├── command_history.py  # Command history management
│       ├── interactive_prompt.py # Interactive CLI with arrow navigation
│       └── ollama_client.py    # Ollama API client
├── tests/
│   └── ollama_chat/
│       ├── conftest.py
│       ├── test_app.py
│       ├── test_command_history.py
│       ├── test_interactive_prompt.py
│       └── test_ollama_client.py
├── requirements.txt
└── setup.py
```

## Prerequisites
- Python 3.7+
- Ollama server running locally (default port: 11434)
- Linux-based system (uses tty module for terminal interaction)
- `gemma3:4b` model installed in Ollama (or another model of your choice)

### Installing Ollama and Models
1. Install Ollama by following the instructions at [Ollama's website](https://ollama.ai)
2. Start the Ollama server:
```bash
systemctl start ollama  # If using systemd
# or
ollama serve           # If running manually
```
3. Pull the required model:
```bash
ollama pull gemma:3b
```

## Setup
1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/Linux
```

2. Install the package in development mode:
```bash
pip install -e ".[dev]"
```

## Running the Chat Application

### Method 1: Using the Command-Line Tool
The simplest way to run the chat:
```bash
ollama-chat
```

### Method 2: Using Python Module
Run directly with Python:
```bash
python -m ollama_chat.app
```

### Advanced Usage
You can customize the model and server:
```bash
# Use a different model
ollama-chat --model codellama

# Connect to a remote Ollama server
ollama-chat --host http://remote-server:11434

# Set custom timeout
ollama-chat --timeout 30
```

### Using the Chat
1. The application will first verify the connection to Ollama and check model availability
2. Once connected, you can start chatting about music!
3. Use the up and down arrow keys to navigate through your command history
4. Press Ctrl+C to exit

### Troubleshooting
If you encounter issues:

1. Connection Problems:
   - Verify Ollama is running: `systemctl status ollama`
   - Check the server port: `netstat -tuln | grep 11434`
   - Ensure the model is installed: `ollama list`

2. Model Issues:
   - Try pulling the model again: `ollama pull gemma:3b`
   - Check model status: `ollama show gemma:3b`

3. Application Errors:
   - Check Python environment is activated
   - Verify all dependencies are installed
   - Look for error messages in the output

## Development

### Running Tests
Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest tests/ --cov=src/ollama_chat
```

### Project Components
- `command_history.py`: Implements a doubly-linked list for command history
- `interactive_prompt.py`: Handles terminal input and command history navigation
- `ollama_client.py`: Manages communication with the Ollama API, including error handling and connection verification
- `app.py`: Ties everything together into a cohesive application 