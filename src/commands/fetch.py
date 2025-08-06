"""Fetch command implementation for waifetch."""

import os
import sys
import random
from typing import Optional

from ..github_client import GitHubClient
from ..display import DisplayManager, WaifetchError


def handle_fetch(language: Optional[str] = None):
    """Handle the fetch command to display a random anime girl image."""
    try:
        client = GitHubClient()
        display_manager = DisplayManager()
        
        # Get available languages
        languages = client.get_language_folders()
        
        # Validate or select language
        if language:
            # Case-insensitive search for the language
            matching_lang = None
            for lang in languages:
                if lang.lower() == language.lower():
                    matching_lang = lang
                    break
            
            if not matching_lang:
                available = ', '.join(languages)
                raise WaifetchError(
                    f"Language '{language}' not found. "
                    f"Available languages: {available}"
                )
            language = matching_lang
        else:
            # Select random language
            language = random.choice(languages)
        
        # Get images in the selected language folder
        images = client.get_images_in_folder(language)
        selected_image = random.choice(images)
        
        # Download and display the image
        temp_path = client.download_image(language, selected_image)
        
        try:
            print()  # Add blank line before image
            display_manager.display_image(temp_path)
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_path)
            except OSError as e:
                print(f"Warning: failed to clean up temporary file: {e}", 
                      file=sys.stderr)
                
    except WaifetchError:
        raise
    except Exception as e:
        raise WaifetchError(f"Unexpected error: {e}")
