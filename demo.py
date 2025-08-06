#!/usr/bin/env python3
"""
Demo script for waifetch Python version
Shows the basic usage and functionality
"""

import sys
from src.commands.fetch import handle_fetch
from src.commands.list import handle_list
from src.display import WaifetchError


def demo_basic_usage():
    """Demo basic usage"""
    print("=== waifetch Python Version Demo ===\n")
    print("1. Basic Usage:")
    print("   python waifetch.py")
    print("   - Displays a random anime girl holding a programming book")
    print("   - Automatically selects random programming language")
    print()


def demo_commands():
    """Demo available commands"""
    print("2. Available Commands:")
    print("   # Fetch random image")
    print("   python waifetch.py fetch")
    print()
    print("   # Fetch image from specific language")
    print("   python waifetch.py fetch --lang Python")
    print("   python waifetch.py fetch -l Go")
    print()
    print("   # List all available languages")
    print("   python waifetch.py list")
    print()


def demo_features():
    """Demo key features"""
    print("3. Key Features:")
    print("   ✓ Beautiful terminal display using chafa")
    print("   ✓ Support for multiple programming languages")
    print("   ✓ Random image selection from GitHub repository")
    print("   ✓ Cross-platform support (Linux, macOS, Windows)")
    print("   ✓ Responsive image sizing based on terminal dimensions")
    print("   ✓ Clean error handling and user feedback")
    print()


def demo_requirements():
    """Demo requirements"""
    print("4. Requirements:")
    print("   ✓ Python 3.8+")
    print("   ✓ chafa (for image display)")
    print("   ✓ Internet connection (fetches from GitHub)")
    print()
    print("   Install chafa:")
    print("   # Ubuntu/Debian: sudo apt install chafa")
    print("   # Fedora: sudo dnf install chafa")
    print("   # macOS: brew install chafa")
    print("   # Arch: sudo pacman -S chafa")
    print()


def run_demo():
    """Run the complete demo"""
    try:
        demo_basic_usage()
        demo_commands()
        demo_features()
        demo_requirements()
        
        print("5. Live Demo:")
        print("   Listing available languages...")
        handle_list()
        
        print("\n   Fetching a random image...")
        print("   (This will display an anime girl image in your terminal)")
        
        # Ask user if they want to see the image
        try:
            response = input("\n   Display random image? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                handle_fetch()
            else:
                print("   Demo completed without image display.")
        except (EOFError, KeyboardInterrupt):
            print("\n   Demo cancelled.")
            
    except WaifetchError as e:
        print(f"Demo error: {e}")
    except Exception as e:
        print(f"Unexpected demo error: {e}")


if __name__ == '__main__':
    run_demo()
