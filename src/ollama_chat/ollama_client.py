"""
Ollama API client module for handling interactions with the Ollama server.
"""

import json
import requests
from typing import Generator, Optional, Tuple

class OllamaClient:
    """Client for interacting with Ollama API."""
    
    def __init__(self, host: str = 'http://localhost:11434', model: str = 'gemma3:4b'):
        self.host = host.rstrip('/')
        self.model = model
        self.system_prompt: Optional[str] = None
        self.timeout = 10  # Default timeout in seconds

    def set_system_prompt(self, prompt: str) -> None:
        """Set the system prompt for the model."""
        self.system_prompt = prompt

    def set_timeout(self, timeout: int) -> None:
        """Set the request timeout in seconds."""
        self.timeout = timeout

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
            # Use a longer timeout for streaming responses
            response = requests.post(url, json=data, stream=True, timeout=self.timeout * 2)
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
                            
        except requests.exceptions.Timeout:
            yield f"Error: Request timed out after {self.timeout * 2} seconds"
            return
        except requests.exceptions.ConnectionError:
            yield f"Error: Could not connect to Ollama server at {self.host}"
            return
        except requests.exceptions.RequestException as e:
            yield f"Error: Request failed: {str(e)}"
            return
        except Exception as e:
            yield f"Error: An unexpected error occurred: {str(e)}"
            return
            
    def check_connection(self) -> Tuple[bool, str]:
        """
        Check if the Ollama server is accessible and the model is available.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Check server version
            version_response = requests.get(f"{self.host}/api/version", timeout=self.timeout)
            version_response.raise_for_status()
            version_data = version_response.json()
            
            # Check model availability
            model_url = f"{self.host}/api/show"
            model_response = requests.post(model_url, json={"name": self.model}, timeout=self.timeout)
            
            if model_response.status_code == 404:
                return False, f"Model '{self.model}' is not available on the server"
            
            model_response.raise_for_status()
            
            return True, f"Connected to Ollama {version_data.get('version', 'unknown version')}"
            
        except requests.exceptions.Timeout:
            return False, f"Connection timed out after {self.timeout} seconds"
        except requests.exceptions.ConnectionError:
            return False, f"Could not connect to Ollama server at {self.host}"
        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}"
        except Exception as e:
            return False, f"An unexpected error occurred: {str(e)}" 