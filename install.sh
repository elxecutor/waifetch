#!/bin/bash

# Installation script for waifetch Python version

set -e

echo "🎌 Installing waifetch (Python version)..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "✅ Python $python_version detected"
else
    echo "❌ Error: Python 3.8 or later is required. Found Python $python_version"
    exit 1
fi

# Check if chafa is installed
if ! command -v chafa &> /dev/null; then
    echo "⚠️  Warning: chafa is not installed. Installing chafa..."
    
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y chafa
    elif command -v brew &> /dev/null; then
        brew install chafa
    elif command -v pacman &> /dev/null; then
        sudo pacman -S chafa
    elif command -v dnf &> /dev/null; then
        sudo dnf install chafa
    else
        echo "❌ Error: Could not automatically install chafa."
        echo "Please install chafa manually for your system:"
        echo "  Ubuntu/Debian: sudo apt install chafa"
        echo "  macOS: brew install chafa"
        echo "  Arch Linux: sudo pacman -S chafa"
        echo "  Fedora: sudo dnf install chafa"
        exit 1
    fi
fi

echo "✅ chafa is installed"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "📥 Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install requests click

# Make script executable
chmod +x waifetch.py

echo "🎉 Installation complete!"
echo ""
echo "Usage:"
echo "  # Activate the virtual environment:"
echo "  source venv/bin/activate"
echo ""
echo "  # Run waifetch:"
echo "  python waifetch.py"
echo "  python waifetch.py --list"
echo "  python waifetch.py --lang Python"
echo ""
echo "  # Or install as a package:"
echo "  pip install ."
echo "  waifetch"
echo ""
echo "Enjoy your anime waifus! 🎌✨"
