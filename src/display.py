"""Display functionality for waifetch."""

import os
import shutil
import subprocess
from typing import Tuple

from .config import (
    DEFAULT_TERMINAL_WIDTH, 
    DEFAULT_TERMINAL_HEIGHT,
    MIN_DISPLAY_WIDTH,
    MAX_DISPLAY_WIDTH,
    MIN_DISPLAY_HEIGHT,
    MAX_DISPLAY_HEIGHT
)


class WaifetchError(Exception):
    """Custom exception for waifetch errors."""
    pass


class DisplayManager:
    """Handles image display functionality."""
    
    def get_terminal_size(self) -> Tuple[int, int]:
        """Get terminal size with fallback to default values."""
        try:
            size = shutil.get_terminal_size()
            return size.columns, size.lines
        except OSError:
            return DEFAULT_TERMINAL_WIDTH, DEFAULT_TERMINAL_HEIGHT
    
    def display_image(self, image_path: str) -> None:
        """Display image using chafa."""
        # Check if chafa is installed
        if not shutil.which('chafa'):
            raise WaifetchError(
                "chafa is not installed or not in PATH. "
                "Please install chafa to display images"
            )
        
        # Get terminal size and calculate display dimensions
        width, height = self.get_terminal_size()
        display_width = max(MIN_DISPLAY_WIDTH, min(MAX_DISPLAY_WIDTH, width - 4))
        display_height = max(MIN_DISPLAY_HEIGHT, min(MAX_DISPLAY_HEIGHT, height - 6))
        
        size_str = f"{display_width}x{display_height}"
        
        # Build chafa command
        cmd = [
            'chafa',
            '--size', size_str,
            '--symbols', 'block',
            '--colors', '256',
            '--dither', 'ordered',
            image_path
        ]
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            raise WaifetchError(f"Failed to display image with chafa: {e}")
