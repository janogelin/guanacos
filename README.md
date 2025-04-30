# AI Test Programs Collection

This repository contains a collection of experimental programs exploring different AI technologies and APIs.

## Current Programs

### ollama_music.py
A command-line program that interacts with the Ollama API using a music lover persona. The program:
- Uses the `gemma3:4b` model
- Implements a knowledgeable music enthusiast personality
- Accepts command-line queries about music, composers, theory, and more
- Processes streaming responses from the Ollama API

## Requirements
- Python 3.x
- Ollama server running locally (default port: 11434)
- Required Python packages in virtual environment:
  - requests

## Setup
1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/Linux
```

2. Install dependencies:
```bash
pip install requests
```

3. Ensure Ollama server is running with the gemma3:4b model installed

## Usage
Run queries about music using:
```bash
python ollama_music.py "your music-related question here"
```

Example:
```bash
python ollama_music.py "What makes Beethoven's 9th Symphony so significant?"
``` 