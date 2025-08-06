"""GitHub repository client for waifetch."""

import os
import json
import tempfile
from pathlib import Path
from typing import List
import requests

from .config import BASE_URL, RAW_BASE_URL, SUPPORTED_EXTENSIONS, REQUEST_TIMEOUT
from .display import WaifetchError


class GitHubContent:
    """Represents a GitHub repository content item."""
    
    def __init__(self, data: dict):
        self.name = data.get('name', '')
        self.path = data.get('path', '')
        self.type = data.get('type', '')
        self.download_url = data.get('download_url', '')
        self.url = data.get('url', '')


class GitHubClient:
    """Handles GitHub repository interactions."""
    
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
