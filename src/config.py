"""Configuration constants and settings for waifetch."""

# GitHub repository constants
BASE_URL = "https://api.github.com/repos/cat-milk/Anime-Girls-Holding-Programming-Books/contents"
RAW_BASE_URL = "https://raw.githubusercontent.com/cat-milk/Anime-Girls-Holding-Programming-Books/master"

# Supported image file extensions
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

# Request timeout in seconds
REQUEST_TIMEOUT = 30

# Default terminal size fallback
DEFAULT_TERMINAL_WIDTH = 80
DEFAULT_TERMINAL_HEIGHT = 40

# Display size constraints
MIN_DISPLAY_WIDTH = 20
MAX_DISPLAY_WIDTH = 300
MIN_DISPLAY_HEIGHT = 10
MAX_DISPLAY_HEIGHT = 200
