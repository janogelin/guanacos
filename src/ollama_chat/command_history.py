"""
Command history management using a doubly-linked list implementation.
Provides functionality for storing and navigating through command history.
"""

class HistoryNode:
    """A node in the command history linked list."""
    def __init__(self, command: str):
        self.command = command
        self.next = None
        self.prev = None

class CommandHistory:
    """Manages command history using a doubly-linked list."""
    def __init__(self):
        self.head = None  # First command
        self.tail = None  # Most recent command
        self.current = None  # Current position when navigating
        self.size = 0
        self.max_size = 1000  # Maximum number of commands to store

    def add_command(self, command: str) -> None:
        """Add a new command to the history."""
        if not command.strip():  # Don't store empty commands
            return

        new_node = HistoryNode(command)
        
        if self.tail:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        else:
            self.head = new_node
            self.tail = new_node
        
        self.current = new_node
        self.size += 1

        # Remove oldest command if we exceed max_size
        if self.size > self.max_size:
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            self.size -= 1

    def get_previous_command(self) -> str:
        """Navigate to and return the previous command."""
        if not self.current or not self.current.prev:
            return ""
        
        self.current = self.current.prev
        return self.current.command

    def get_next_command(self) -> str:
        """Navigate to and return the next command."""
        if not self.current or not self.current.next:
            return ""
        
        self.current = self.current.next
        return self.current.command

    def reset_navigation(self) -> None:
        """Reset navigation pointer to most recent command."""
        self.current = self.tail

    def get_all_commands(self) -> list[str]:
        """Return all commands in history as a list."""
        commands = []
        current = self.head
        while current:
            commands.append(current.command)
            current = current.next
        return commands 