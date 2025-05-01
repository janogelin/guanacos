"""
Main application module for the interactive Ollama chat program.
"""

import sys
from typing import Optional

from .ollama_client import OllamaClient
from .interactive_prompt import InteractivePrompt

class OllamaChatApp:
    """Main application class for the interactive Ollama chat."""
    
    def __init__(self, host: str = 'http://localhost:11434', model: str = 'gemma3:4b'):
        self.client = OllamaClient(host, model)
        self.prompt = InteractivePrompt("Chat 🗣️ > ")
        
        # Define the music lover persona
        self.client.set_system_prompt("""You are an enthusiastic and knowledgeable music lover with a deep passion 
for all genres of music. You have:
- Extensive knowledge of music history, theory, and appreciation
- Personal experience attending countless concerts and musical performances
- A collection of thousands of albums across various genres
- Strong opinions about music while remaining respectful of others' tastes
- A warm, engaging personality that loves sharing musical discoveries
- The ability to explain complex musical concepts in an accessible way

Please maintain this personality in all your responses, sharing your enthusiasm 
and personal perspective while being informative and engaging.""")

    def check_ollama_connection(self) -> bool:
        """Check if we can connect to the Ollama server."""
        success, message = self.client.check_connection()
        if not success:
            print(f"Error: {message}")
            return False
        print(f"Success: {message}")
        return True

    def run(self) -> None:
        """Run the interactive chat application."""
        if not self.check_ollama_connection():
            sys.exit(1)

        print(f"\nWelcome to the Interactive Music Chat! (Using {self.client.model})")
        print("Type your questions about music, or press Ctrl+C to exit.")
        print("Use ↑/↓ arrow keys to navigate through command history.")
        print()

        while True:
            try:
                user_input = self.prompt.get_input()
                if user_input is None:  # Ctrl+C was pressed
                    break
                    
                if not user_input.strip():
                    continue

                # Print response stream
                print("\nThinking... 🎵")
                response_received = False
                for response_chunk in self.client.chat(user_input):
                    response_received = True
                    if response_chunk.startswith("Error:"):
                        print(f"\n{response_chunk}")
                        break
                    print(response_chunk, end='', flush=True)
                
                if response_received:
                    print("\n")  # Add spacing after response
                else:
                    print("\nNo response received from the model.")

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"\nError: {str(e)}")
                continue

def main() -> None:
    """Entry point for the application."""
    app = OllamaChatApp()
    app.run() 