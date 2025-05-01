"""
Interactive prompt module with command history navigation using arrow keys.
"""

import sys
import termios
import tty
from typing import Optional, Dict, List, Tuple

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
    
    def __init__(self, prompt_text: str = "🎵 > ", debug: bool = False):
        super().__init__(prompt_text)
        self.debug = debug
        
        # Enhanced music terminology dictionary
        self.music_keywords: Dict[str, str] = {
            "song": "musical piece",
            "album": "studio album",
            "band": "musical group",
            "singer": "vocalist",
            "musician": "artist",
            "tune": "melody",
            "beat": "rhythm",
            "sound": "timbre",
            "notes": "musical notation",
            "key": "tonality",
            "chord": "harmony",
            "mix": "arrangement",
            "record": "recording",
            "gig": "performance",
            "show": "concert",
            "play": "perform",
            "hear": "listen to",
        }
        
        # Genre-specific terminology and context
        self.genre_terms: Dict[str, List[str]] = {
            "classical": ["symphony", "concerto", "sonata", "opus", "movement", "conductor", "orchestra"],
            "jazz": ["improvisation", "swing", "bebop", "ensemble", "solo", "standards", "chord progression"],
            "rock": ["riff", "power chord", "distortion", "amplification", "backbeat", "hook"],
            "electronic": ["synthesizer", "sequencer", "beat", "production", "mix", "sampling"],
            "hip-hop": ["flow", "bars", "beat", "sampling", "production", "rhyme scheme"],
            "folk": ["acoustic", "traditional", "ballad", "storytelling", "fingerpicking"],
        }
        
        # Musical theory terms
        self.theory_terms: Dict[str, List[str]] = {
            "tempo": ["allegro", "andante", "adagio", "presto"],
            "dynamics": ["forte", "piano", "crescendo", "diminuendo"],
            "structure": ["verse", "chorus", "bridge", "coda", "intro", "outro"],
            "harmony": ["major", "minor", "chord progression", "modulation"],
            "rhythm": ["time signature", "meter", "syncopation", "polyrhythm"],
        }

    def _detect_genre_context(self, query: str) -> Optional[str]:
        """Detect if the query is related to a specific music genre."""
        query_lower = query.lower()
        for genre, terms in self.genre_terms.items():
            if genre in query_lower or any(term in query_lower for term in terms):
                return genre
        return None

    def _add_theory_context(self, query: str, genre: Optional[str] = None) -> str:
        """Add relevant music theory context based on query content and genre."""
        query_lower = query.lower()
        
        # Look for theory-related terms
        relevant_terms = []
        for category, terms in self.theory_terms.items():
            if any(term in query_lower for term in terms):
                if genre:
                    # Add genre-specific theory context
                    if genre == "classical" and category in ["tempo", "dynamics"]:
                        relevant_terms.extend(terms[:2])  # Add some classical terminology
                    elif genre == "jazz" and category == "harmony":
                        relevant_terms.append("chord voicing")  # Add jazz-specific terms
                else:
                    relevant_terms.append(terms[0])  # Add general theory term
                    
        if relevant_terms:
            theory_context = f" (considering aspects like {', '.join(relevant_terms)})"
            # Insert before question mark if it exists, otherwise append
            if "?" in query:
                return query.replace("?", f"{theory_context}?")
            return f"{query}{theory_context}"
            
        return query

    def _enhance_music_query(self, query: str) -> str:
        """
        Enhance the query with music-focused context and terminology.
        Helps guide the model towards music-related responses.
        """
        if not query or len(query.strip()) < 3:
            return query
            
        original_query = query
        enhanced = query
        
        # Replace common terms with more specific music terminology
        for key, value in self.music_keywords.items():
            # Only replace if it's a whole word (using word boundaries)
            enhanced = enhanced.replace(f" {key} ", f" {value} ")
            # Also check at start and end of string
            if enhanced.startswith(f"{key} "):
                enhanced = f"{value} {enhanced[len(key)+1:]}"
            if enhanced.endswith(f" {key}"):
                enhanced = f"{enhanced[:-len(key)]} {value}"
            
        # Detect genre context
        genre = self._detect_genre_context(enhanced)
        
        # Add genre-specific enhancements if detected
        if genre:
            genre_terms = self.genre_terms[genre]
            if "?" in enhanced:
                enhanced = enhanced.replace("?", f" in the context of {genre} music?")
            else:
                enhanced = f"{enhanced} in the {genre} style"
                
        # Add music theory context
        enhanced = self._add_theory_context(enhanced, genre)
            
        # Add general music context if needed
        music_terms = ["music", "song", "album", "artist", "band", "concert", 
                      "genre", "rhythm", "melody", "instrument", "performance",
                      "compose", "symphony", "opera", "jazz", "rock", "classical"]
                      
        has_music_context = any(term in enhanced.lower() for term in music_terms)
        
        if not has_music_context:
            if "?" in enhanced:
                enhanced = f"From a musical perspective, {enhanced}"
            else:
                enhanced = f"Tell me about the musical aspects of {enhanced}"
        
        # Show debug information if enabled
        if self.debug and enhanced != original_query:
            print("\nQuery enhancement:")
            print(f"Original: {original_query}")
            print(f"Enhanced: {enhanced}")
            if genre:
                print(f"Detected genre: {genre}")
            print()
            
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