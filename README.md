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
- Intelligent music-focused query enhancement
- Genre-specific terminology and context
- Music theory integration
- Debug mode for query transformations

#### Music Features
The chat application includes sophisticated music-focused enhancements:

1. **Genre Recognition & Context**
   - Automatically detects musical genres in queries
   - Adds genre-specific context and terminology
   - Supports: Classical, Jazz, Rock, Electronic, Hip-Hop, Folk
   - Example: "Tell me about power chords" → "Tell me about power chords in the rock style"

2. **Music Theory Integration**
   - Enhances queries with relevant music theory concepts
   - Categories include: Tempo, Dynamics, Structure, Harmony, Rhythm
   - Adds appropriate theoretical context based on genre
   - Example: "How do you write a chorus?" → "How do you write a chorus (considering aspects like verse)?"

3. **Enhanced Music Terminology**
   - Converts casual terms to precise musical language
   - Maintains natural conversation flow while adding precision
   - Examples:
     - "song" → "musical piece"
     - "band" → "musical group"
     - "singer" → "vocalist"

4. **Intelligent Query Processing**
   - Adds musical context to non-musical queries
   - Preserves original meaning while adding musical perspective
   - Examples:
     - "What makes summer special?" → "From a musical perspective, what makes summer special?"
     - "Tell me about the 1960s" → "Tell me about the musical aspects of the 1960s"

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

# Enable debug mode to see query enhancements
ollama-chat --debug
```

### Using the Chat
1. The application will first verify the connection to Ollama and check model availability
2. Once connected, you can start chatting about music!
3. Use the up and down arrow keys to navigate through your command history
4. Your queries will be automatically enhanced with musical context
5. Try different types of questions:
   - Direct music questions: "What makes a good melody?"
   - Genre-specific: "Explain jazz improvisation"
   - Theory-focused: "How do dynamics work in classical music?"
   - General topics: "How does weather affect mood?" (will add musical perspective)
6. Use debug mode to see how your queries are enhanced
7. Press Ctrl+C to exit

### Query Enhancement Examples
Here are some examples of how the chat enhances your queries:

1. **Genre-Specific Enhancement**:
   ```
   Input: "Tell me about power chords"
   Enhanced: "Tell me about power chords in the rock style"
   ```

2. **Theory Integration**:
   ```
   Input: "How do you write a chorus?"
   Enhanced: "How do you write a chorus (considering aspects like verse)?"
   ```

3. **Terminology Precision**:
   ```
   Input: "What makes a good song?"
   Enhanced: "What makes a good musical piece?"
   ```

4. **Adding Musical Context**:
   ```
   Input: "What makes summer special?"
   Enhanced: "From a musical perspective, what makes summer special?"
   ```

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
   - Try running with --debug flag to see query processing

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
- `interactive_prompt.py`: Handles terminal input and command history navigation, including music-focused query enhancement
- `ollama_client.py`: Manages communication with the Ollama API, including error handling and connection verification
- `app.py`: Ties everything together into a cohesive application 