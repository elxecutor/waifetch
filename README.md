# waifetch

A CLI tool that displays anime girls holding programming books in your terminal.

---

## Acknowledgments

This project is originally created and maintained by [ashish0kumar](https://github.com/ashish0kumar). Please visit the [original repository](https://github.com/ashish0kumar/waifetch) to show your support.

---

## Features

- **Dynamic terminal display** with images rendered directly in your terminal
- **Smart sizing** that automatically adapts to your terminal dimensions  
- **Language-specific fetching** with support for all major programming languages
- **High-quality rendering** using chafa with 256 colors and ordered dithering
- **Cross-platform compatibility** with Python 3.8+

## Installation

### Method 1: Direct execution

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Make the script executable:
```bash
chmod +x waifetch.py
```

3. Run directly:
```bash
python waifetch.py fetch
```

### Method 2: Install as package

```bash
pip install .
```

Then use as:
```bash
waifetch fetch
```

### Required Dependencies

For image rendering, install [`chafa`](https://github.com/hpjansson/chafa):

> [!IMPORTANT]
> `chafa` is required for displaying images in the terminal. The CLI will not work without it.

```bash
# Ubuntu/Debian
sudo apt install chafa

# macOS (with Homebrew)
brew install chafa

# Arch Linux
sudo pacman -S chafa

# Fedora
sudo dnf install chafa
```

## Usage

### Basic Usage

Display a random anime girl with a random programming language:
```bash
python waifetch.py fetch
# or if installed as package:
waifetch fetch
```

### Language-specific Display

Display an anime girl holding a specific programming language book:
```bash
python waifetch.py fetch --lang Python
python waifetch.py fetch -l Go
python waifetch.py fetch --lang "C++"
```

### List Available Languages

See all available programming languages:
```bash
python waifetch.py list
```

### Help

Get help and see all options:
```bash
python waifetch.py --help
```

## Examples

```bash
# Random image
python waifetch.py fetch

# List all available languages
python waifetch.py list

# Specific language
python waifetch.py fetch --lang Go
python waifetch.py fetch -l Rust
python waifetch.py fetch --lang JavaScript
```

## Environment Variables

- `GITHUB_TOKEN`: Optional GitHub personal access token for higher API rate limits

## Python Dependencies

- `requests>=2.31.0`: For HTTP requests to GitHub API
- `click>=8.1.0`: For command-line interface

## Architecture

The application follows clean architectural patterns:

- `Fetcher` class handles all API interactions and image operations
- Clean separation of concerns between CLI handling and core functionality
- Comprehensive error handling with custom exception types
- Proper resource management for temporary files
- Modular design for easy testing and maintenance

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) to get started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
