"""List command implementation for waifetch."""

import click
from ..github_client import GitHubClient
from ..display import WaifetchError


def handle_list():
    """Handle the list command to show available languages."""
    try:
        client = GitHubClient()
        languages = client.get_language_folders()
        
        click.echo("Available programming languages:")
        
        # Display in columns like the Go version
        for i, language in enumerate(languages):
            if i > 0 and i % 6 == 0:
                click.echo()
            click.echo(f"{language:<20}", nl=False)
        click.echo()  # Final newline
        
    except WaifetchError as e:
        raise click.ClickException(str(e))
