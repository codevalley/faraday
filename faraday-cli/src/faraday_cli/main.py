"""Main CLI entry point using Click framework."""

import click
from rich.console import Console
from typing import Optional

from faraday_cli.config import ConfigManager
from faraday_cli.api import APIClient
from faraday_cli.auth import AuthManager
from faraday_cli.output import OutputFormatter
from faraday_cli.commands.auth import auth_group
from faraday_cli.commands.config import config_group
from faraday_cli.commands.thoughts import thoughts_group
from faraday_cli.commands.search import search_command


@click.group()
@click.option("--config", help="Config file path")
@click.option("--api-url", help="API server URL")
@click.option("--json", "json_output", is_flag=True, help="Output JSON")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
@click.pass_context
def cli(
    ctx: click.Context,
    config: Optional[str],
    api_url: Optional[str],
    json_output: bool,
    verbose: bool,
) -> None:
    """Faraday Personal Semantic Engine CLI

    A command-line interface for managing thoughts, performing semantic searches,
    and analyzing your personal knowledge base.
    """
    # Ensure context object exists
    ctx.ensure_object(dict)

    # Initialize core components
    console = Console()
    config_manager = ConfigManager(config)
    auth_manager = AuthManager(config_manager.config_dir)

    # Use provided API URL or fall back to config
    effective_api_url = api_url or config_manager.get(
        "api.url", "http://localhost:8001"
    )
    api_client = APIClient(effective_api_url, auth_manager)

    output_formatter = OutputFormatter(console, json_output)

    # Store in context for subcommands
    ctx.obj["config"] = config_manager
    ctx.obj["api_client"] = api_client
    ctx.obj["auth_manager"] = auth_manager
    ctx.obj["output"] = output_formatter
    ctx.obj["console"] = console
    ctx.obj["verbose"] = verbose


# Register command groups
cli.add_command(auth_group)
cli.add_command(config_group)
cli.add_command(thoughts_group)
cli.add_command(search_command, name="search")


@cli.command()
@click.pass_context
def version(ctx: click.Context) -> None:
    """Show version information."""
    from faraday_cli import __version__

    output = ctx.obj["output"]
    if output.json_mode:
        click.echo(f'{{"version": "{__version__}"}}')
    else:
        output.console.print(f"Faraday CLI version {__version__}")


if __name__ == "__main__":
    cli()
