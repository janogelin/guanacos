"""
Interactive prompt module with command history navigation using arrow keys.
"""

import sys
import termios
import tty
from typing import Optional

from .command_history import CommandHistory

class InteractivePrompt:
    """Handles interactive command input with history navigation."""
    
    ARROW_UP = '\x1b[A'
    ARROW_DOWN = '\x1b[B'
    BACKSPACE = '\x7f'
    CTRL_C = '\x03'
    
    def __init__(self, prompt_text: str = ">>> "):
        self.prompt_text = prompt_text
        self.history = CommandHistory()
        self.current_input = ""
        self.cursor_pos = 0

    def _get_char(self) -> str:
        """Get a single character from stdin without echo."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            
            # Check if it's an escape sequence
            if ch == '\x1b':
                ch += sys.stdin.read(2)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def _clear_line(self) -> None:
        """Clear the current line and move cursor to the start."""
        sys.stdout.write('\r' + ' ' * (len(self.prompt_text) + len(self.current_input)) + '\r')
        sys.stdout.flush()

    def _redraw_line(self) -> None:
        """Redraw the current line with prompt and input."""
        self._clear_line()
        sys.stdout.write(self.prompt_text + self.current_input)
        sys.stdout.flush()

    def get_input(self) -> Optional[str]:
        """
        Get input from the user with command history navigation.
        
        Returns:
            The entered command or None if Ctrl+C was pressed
        """
        self.current_input = ""
        self.cursor_pos = 0
        sys.stdout.write(self.prompt_text)
        sys.stdout.flush()
        
        while True:
            char = self._get_char()
            
            if char == self.CTRL_C:
                print("\nExiting...")
                return None
                
            elif char == '\r':  # Enter key
                print()  # Move to next line
                command = self.current_input
                if command:
                    self.history.add_command(command)
                return command
                
            elif char == self.BACKSPACE:
                if self.current_input:
                    self.current_input = self.current_input[:-1]
                    self._redraw_line()
                    
            elif char == self.ARROW_UP:
                prev_command = self.history.get_previous_command()
                if prev_command:
                    self.current_input = prev_command
                    self._redraw_line()
                    
            elif char == self.ARROW_DOWN:
                next_command = self.history.get_next_command()
                self.current_input = next_command  # Will be empty string if no next command
                self._redraw_line()
                
            elif len(char) == 1 and char.isprintable():
                self.current_input += char
                self._redraw_line()

    def get_history(self) -> list[str]:
        """Return all commands in history."""
        return self.history.get_all_commands()


class MusicPrompt(InteractivePrompt):
    """Enhanced interactive prompt for music-focused conversations."""
    
    def __init__(self, prompt_text: str = "🎵 > "):
        super().__init__(prompt_text)
        self.music_keywords = {
            "song": "musical piece",
            "album": "studio album",
            "band": "musical group",
            "singer": "vocalist",
            "musician": "artist",
        }
        
    def _enhance_music_query(self, query: str) -> str:
        """
        Enhance the query with music-focused context and terminology.
        Helps guide the model towards music-related responses.
        """
        # Don't enhance if query is too short or empty
        if not query or len(query.strip()) < 3:
            return query
            
        # Replace common terms with more specific music terminology
        enhanced = query
        for key, value in self.music_keywords.items():
            # Only replace if it's a whole word
            enhanced = enhanced.replace(f" {key} ", f" {value} ")
            
        # Add music-focused context if query doesn't seem music-related
        music_terms = ["music", "song", "album", "artist", "band", "concert", 
                      "genre", "rhythm", "melody", "instrument", "performance"]
                      
        has_music_context = any(term in query.lower() for term in music_terms)
        
        if not has_music_context:
            # Add music context while preserving the original question
            if "?" in query:
                enhanced = f"From a music perspective, {enhanced}"
            else:
                enhanced = f"Tell me about the musical aspects of {enhanced}"
                
        return enhanced

    def get_input(self) -> Optional[str]:
        """
        Get enhanced music-focused input from the user.
        
        Returns:
            The enhanced command or None if Ctrl+C was pressed
        """
        command = super().get_input()
        if command is not None:
            return self._enhance_music_query(command)
        return None 