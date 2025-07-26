"""CLI command modules."""

from faraday_cli.commands.auth import auth_group
from faraday_cli.commands.config import config_group
from faraday_cli.commands.thoughts import thoughts_group

# Import all command groups to register them
__all__ = ["auth_group", "config_group", "thoughts_group"]