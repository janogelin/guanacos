"""
Ollama API client module for handling interactions with the Ollama server.
"""

import json
import requests
from typing import Generator, Optional

class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(self, host: str = 'http://localhost:11434', model: str = 'gemma:4b'):
        self.host = host.rstrip('/')
        self.model = model
        self.system_prompt: Optional[str] = None

    def set_system_prompt(self, prompt: str) -> None:
        """Set the system prompt for the model."""
        self.system_prompt = prompt

    def chat(self, message: str) -> Generator[str, None, None]:
        """
        Send a chat message to Ollama and yield the response stream.
        
        Args:
            message: The user's message to send to the model
            
        Yields:
            Chunks of the model's response as they arrive
        """
        url = f"{self.host}/api/chat"
        
        # Prepare the messages list
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": message})
        
        data = {
            "model": self.model,
            "messages": messages,
            "stream": True
        }
        
        try:
            response = requests.post(url, json=data, stream=True)
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    try:
                        json_response = json.loads(line)
                        if 'message' in json_response:
                            content = json_response['message'].get('content', '')
                            if content:
                                yield content
                    except json.JSONDecodeError:
                        yield "Error: Invalid response format from Ollama server"
                        return
                            
        except requests.exceptions.RequestException as e:
            yield f"Error: Could not connect to Ollama server: {str(e)}"
            return
        except Exception as e:
            yield f"Error: An unexpected error occurred: {str(e)}"
            return
            
    def check_connection(self) -> bool:
        """Check if the Ollama server is accessible."""
        try:
            response = requests.get(f"{self.host}/api/version")
            return response.status_code == 200
        except (requests.exceptions.RequestException, Exception):
            return False 