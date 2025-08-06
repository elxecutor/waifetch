#!/usr/bin/env python3
"""
waifetch - Display anime girls holding programming books in your terminal uWu
A fun CLI that displays random anime girls holding programming books directly
in your terminal using Python.
"""

import sys
import argparse
from src.commands import fetch, list as list_cmd
from src.display import WaifetchError

__version__ = "1.0.0"


def main():
    """Main entry point for the application"""
    parser = argparse.ArgumentParser(
        prog="waifetch",
        description="Display anime girls holding programming books in your terminal uWu",
        epilog="Fetch random anime girl images or list available programming languages"
    )
    
    parser.add_argument('--version', action='version', version=f'waifetch {__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Fetch command (default behavior)
    fetch_parser = subparsers.add_parser('fetch', help='Fetch and display a random anime girl image')
    fetch_parser.add_argument(
        '-l', '--lang',
        help='Specify programming language (e.g., C, Go, Rust)',
        metavar='LANGUAGE'
    )
    fetch_parser.set_defaults(func=fetch.handle_fetch)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all available programming languages')
    list_parser.set_defaults(func=list_cmd.handle_list)
    
    # Parse arguments
    args = parser.parse_args()
    
    try:
        if args.command is None:
            # Default behavior: fetch a random image
            fetch.handle_fetch()
        elif hasattr(args, 'func'):
            if args.command == 'fetch':
                args.func(args.lang if hasattr(args, 'lang') else None)
            else:
                args.func()
        else:
            parser.print_help()
            
    except WaifetchError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
