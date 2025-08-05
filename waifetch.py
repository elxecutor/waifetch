#!/usr/bin/env python3
"""
waifetch - Display anime girls holding programming books in your terminal uWu

A fun CLI that displays random anime girls holding programming books directly
in your terminal using Python.
"""

import os
import sys
import json
import random
import tempfile
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple
import requests
import click


# Constants
BASE_URL = "https://api.github.com/repos/cat-milk/Anime-Girls-Holding-Programming-Books/contents"
RAW_BASE_URL = "https://raw.githubusercontent.com/cat-milk/Anime-Girls-Holding-Programming-Books/master"
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
REQUEST_TIMEOUT = 30


class GitHubContent:
    """Represents a GitHub repository content item."""
    
    def __init__(self, data: dict):
        self.name = data.get('name', '')
        self.path = data.get('path', '')
        self.type = data.get('type', '')
        self.download_url = data.get('download_url', '')
        self.url = data.get('url', '')


class WaifetchError(Exception):
    """Custom exception for waifetch errors."""
    pass


class Fetcher:
    """Handles fetching and displaying anime girl images."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.timeout = REQUEST_TIMEOUT
        
        # Add GitHub token authentication if available
        github_token = os.getenv('GITHUB_TOKEN')
        if github_token:
            self.session.headers.update({
                'Authorization': f'Bearer {github_token}'
            })
    
    def get_language_folders(self) -> List[str]:
        """Fetch available programming language folders from the repository."""
        try:
            response = self.session.get(BASE_URL)
            response.raise_for_status()
            
            contents = response.json()
            languages = []
            
            for item in contents:
                content = GitHubContent(item)
                if content.type == 'dir' and not content.name.startswith('.'):
                    languages.append(content.name)
            
            if not languages:
                raise WaifetchError("No language folders found in repository")
            
            return sorted(languages)
            
        except requests.RequestException as e:
            raise WaifetchError(f"Failed to fetch repository contents: {e}")
        except json.JSONDecodeError as e:
            raise WaifetchError(f"Failed to decode response: {e}")
    
    def get_images_in_folder(self, language: str) -> List[str]:
        """Get all image files in a specific language folder."""
        url = f"{BASE_URL}/{language}"
        
        try:
            response = self.session.get(url)
            
            if response.status_code == 404:
                raise WaifetchError(f"Language folder '{language}' not found")
            
            response.raise_for_status()
            contents = response.json()
            
            images = []
            for item in contents:
                content = GitHubContent(item)
                if content.type == 'file':
                    ext = Path(content.name).suffix.lower()
                    if ext in SUPPORTED_EXTENSIONS:
                        images.append(content.name)
            
            if not images:
                raise WaifetchError(f"No images found in folder '{language}'")
            
            return images
            
        except requests.RequestException as e:
            raise WaifetchError(f"Failed to fetch folder contents for {language}: {e}")
        except json.JSONDecodeError as e:
            raise WaifetchError(f"Failed to decode response for folder {language}: {e}")
    
    def download_image(self, language: str, filename: str) -> str:
        """Download an image to a temporary file and return the path."""
        url = f"{RAW_BASE_URL}/{language}/{filename}"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            # Create temporary file
            suffix = Path(filename).suffix
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
                temp_file.write(response.content)
                return temp_file.name
                
        except requests.RequestException as e:
            raise WaifetchError(f"Failed to download image: {e}")
    
    def get_terminal_size(self) -> Tuple[int, int]:
        """Get terminal size with fallback to default values."""
        try:
            size = shutil.get_terminal_size()
            return size.columns, size.lines
        except OSError:
            return 80, 40  # Default fallback
    
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
        display_width = max(20, min(300, width - 4))
        display_height = max(10, min(200, height - 6))
        
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
    
    def fetch_random_image(self, language: Optional[str] = None) -> None:
        """Fetch and display a random image, optionally from a specific language."""
        try:
            # Get available languages
            languages = self.get_language_folders()
            
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
            images = self.get_images_in_folder(language)
            selected_image = random.choice(images)
            
            # Download and display the image
            temp_path = self.download_image(language, selected_image)
            
            try:
                print()  # Add blank line before image
                self.display_image(temp_path)
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


@click.command()
@click.option(
    '--lang', '-l',
    help='Specify programming language (e.g., C, Go, Rust)',
    metavar='LANGUAGE'
)
@click.option(
    '--list',
    is_flag=True,
    help='List all available programming languages'
)
@click.version_option(version='1.0.0', prog_name='waifetch')
def main(lang: Optional[str], list: bool) -> None:
    """Display anime girls holding programming books in your terminal uWu
    
    Examples:
    
        waifetch
        
        waifetch --list
        
        waifetch --lang Go
        
        waifetch -l Rust
    """
    try:
        fetcher = Fetcher()
        
        if list:
            languages = fetcher.get_language_folders()
            click.echo("Available programming languages:")
            
            # Display in columns like the Go version
            for i, language in enumerate(languages):
                if i > 0 and i % 6 == 0:
                    click.echo()
                click.echo(f"{language:<20}", nl=False)
            click.echo()  # Final newline
            
        else:
            fetcher.fetch_random_image(lang)
            
    except WaifetchError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\nInterrupted by user", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
