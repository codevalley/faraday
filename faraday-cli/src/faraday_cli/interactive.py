"""Interactive shell for Faraday CLI using Click's prompt utilities."""

import asyncio
import shlex
import sys
from typing import Dict, List, Optional, Callable, Any
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt

from faraday_cli.config import ConfigManager
from faraday_cli.cached_api import CachedAPIClient
from faraday_cli.output import OutputFormatter
from faraday_cli.auth import AuthManager


class InteractiveSession:
    """Interactive shell session for Faraday CLI."""
    
    def __init__(
        self,
        config: ConfigManager,
        cached_api: CachedAPIClient,
        output: OutputFormatter,
        auth_manager: AuthManager,
        console: Console,
    ):
        self.config = config
        self.cached_api = cached_api
        self.output = output
        self.auth_manager = auth_manager
        self.console = console
        self.history: List[str] = []
        self.running = True
        
        # Command registry
        self.commands: Dict[str, Callable] = {
            "add": self._handle_add,
            "search": self._handle_search,
            "list": self._handle_list,
            "show": self._handle_show,
            "delete": self._handle_delete,
            "sync": self._handle_sync,
            "stats": self._handle_stats,
            "config": self._handle_config,
            "help": self._handle_help,
            "history": self._handle_history,
            "clear": self._handle_clear,
            "exit": self._handle_exit,
            "quit": self._handle_exit,
        }
        
        # Command aliases
        self.aliases = {
            "h": "help",
            "q": "quit",
            "ls": "list",
            "rm": "delete",
            "?": "help",
        }
    
    def start(self) -> None:
        """Start the interactive session."""
        self._show_welcome()
        
        try:
            while self.running:
                try:
                    # Get user input
                    prompt_text = self._get_prompt()
                    user_input = Prompt.ask(prompt_text, console=self.console)
                    
                    if not user_input.strip():
                        continue
                    
                    # Add to history
                    self.history.append(user_input)
                    
                    # Parse and execute command
                    asyncio.run(self._execute_command(user_input))
                    
                except KeyboardInterrupt:
                    self.console.print("\n[yellow]Use 'exit' or 'quit' to leave the session[/yellow]")
                    continue
                except EOFError:
                    break
                    
        except Exception as e:
            self.console.print(f"[red]Session error: {e}[/red]")
        finally:
            self._show_goodbye()
    
    def _show_welcome(self) -> None:
        """Display welcome message."""
        welcome_text = Text()
        welcome_text.append("🧠 ", style="blue")
        welcome_text.append("Welcome to Faraday Interactive Mode", style="bold blue")
        
        panel = Panel(
            welcome_text,
            subtitle="Type 'help' for available commands or 'exit' to quit",
            border_style="blue",
        )
        self.console.print(panel)
        self.console.print()
    
    def _show_goodbye(self) -> None:
        """Display goodbye message."""
        self.console.print("\n[blue]👋 Thanks for using Faraday! Your thoughts are safe.[/blue]")
    
    def _get_prompt(self) -> str:
        """Get the command prompt string."""
        if self.auth_manager.is_authenticated():
            return "[bold green]faraday>[/bold green]"
        else:
            return "[bold yellow]faraday (not logged in)>[/bold yellow]"
    
    async def _execute_command(self, user_input: str) -> None:
        """Parse and execute a command."""
        try:
            # Parse command and arguments
            parts = shlex.split(user_input)
            if not parts:
                return
            
            command = parts[0].lower()
            args = parts[1:]
            
            # Handle aliases
            command = self.aliases.get(command, command)
            
            # Handle colon syntax (e.g., "add: my thought")
            if ":" in user_input:
                colon_index = user_input.find(":")
                potential_command = user_input[:colon_index].strip().lower()
                if potential_command in ["add", "search"]:
                    command = potential_command
                    content = user_input[colon_index + 1:].strip()
                    args = [content] if content else []
            
            # Execute command
            if command in self.commands:
                await self.commands[command](args)
            else:
                self.console.print(f"[red]Unknown command: {command}[/red]")
                self.console.print("Type 'help' to see available commands.")
                
        except Exception as e:
            self.console.print(f"[red]Error executing command: {e}[/red]")
    
    async def _handle_add(self, args: List[str]) -> None:
        """Handle add command."""
        if not args:
            content = Prompt.ask("Enter thought content", console=self.console)
        else:
            content = " ".join(args)
        
        if not content.strip():
            self.console.print("[yellow]Cannot add empty thought[/yellow]")
            return
        
        try:
            # Check authentication
            if not self.auth_manager.is_authenticated():
                self.console.print("[yellow]You need to login first. Use the main CLI: faraday auth login[/yellow]")
                return
            
            # Create thought
            thought = await self.cached_api.create_thought(content)
            thought_id = thought.id if hasattr(thought, 'id') else thought.get('id', 'unknown')
            self.console.print(f"[green]✓[/green] Added thought: {thought_id[:8]}...")
            
        except Exception as e:
            self.console.print(f"[red]Failed to add thought: {e}[/red]")
    
    async def _handle_search(self, args: List[str]) -> None:
        """Handle search command."""
        if not args:
            query = Prompt.ask("Enter search query", console=self.console)
        else:
            query = " ".join(args)
        
        if not query.strip():
            self.console.print("[yellow]Cannot search with empty query[/yellow]")
            return
        
        try:
            # Check authentication
            if not self.auth_manager.is_authenticated():
                self.console.print("[yellow]You need to login first. Use the main CLI: faraday auth login[/yellow]")
                return
            
            # Perform search
            results = await self.cached_api.search_thoughts(query, limit=5)
            
            # Handle both SearchResult objects and dictionaries
            if hasattr(results, 'thoughts'):
                thoughts = results.thoughts
            else:
                thoughts = results.get("results", [])
            
            if not thoughts:
                self.console.print("[yellow]No results found[/yellow]")
                return
            
            # Display results
            self.output.format_search_results(results)
            
        except Exception as e:
            self.console.print(f"[red]Search failed: {e}[/red]")
    
    async def _handle_list(self, args: List[str]) -> None:
        """Handle list command."""
        try:
            # Check authentication
            if not self.auth_manager.is_authenticated():
                self.console.print("[yellow]You need to login first. Use the main CLI: faraday auth login[/yellow]")
                return
            
            # Parse limit
            limit = 10
            if args and args[0].isdigit():
                limit = int(args[0])
            
            # Get thoughts
            thoughts = await self.cached_api.get_thoughts(limit=limit)
            
            if not thoughts:
                self.console.print("[yellow]No thoughts found[/yellow]")
                return
            
            # Display thoughts
            self.output.format_thoughts_list(thoughts)
            
        except Exception as e:
            self.console.print(f"[red]Failed to list thoughts: {e}[/red]")
    
    async def _handle_show(self, args: List[str]) -> None:
        """Handle show command."""
        if not args:
            thought_id = Prompt.ask("Enter thought ID", console=self.console)
        else:
            thought_id = args[0]
        
        if not thought_id.strip():
            self.console.print("[yellow]Please provide a thought ID[/yellow]")
            return
        
        try:
            # Check authentication
            if not self.auth_manager.is_authenticated():
                self.console.print("[yellow]You need to login first. Use the main CLI: faraday auth login[/yellow]")
                return
            
            # Get thought
            thought = await self.cached_api.get_thought(thought_id)
            
            if not thought:
                self.console.print(f"[red]Thought {thought_id} not found[/red]")
                return
            
            # Display thought
            self.output.format_thought_detail(thought)
            
        except Exception as e:
            self.console.print(f"[red]Failed to show thought: {e}[/red]")
    
    async def _handle_delete(self, args: List[str]) -> None:
        """Handle delete command."""
        if not args:
            thought_id = Prompt.ask("Enter thought ID", console=self.console)
        else:
            thought_id = args[0]
        
        if not thought_id.strip():
            self.console.print("[yellow]Please provide a thought ID[/yellow]")
            return
        
        # Confirm deletion
        confirm = Prompt.ask(
            f"Are you sure you want to delete thought {thought_id}?",
            choices=["y", "n"],
            default="n",
            console=self.console
        )
        
        if confirm.lower() != "y":
            self.console.print("[yellow]Deletion cancelled[/yellow]")
            return
        
        try:
            # Check authentication
            if not self.auth_manager.is_authenticated():
                self.console.print("[yellow]You need to login first. Use the main CLI: faraday auth login[/yellow]")
                return
            
            # Delete thought
            await self.cached_api.delete_thought(thought_id)
            self.console.print(f"[green]✓[/green] Deleted thought {thought_id}")
            
        except Exception as e:
            self.console.print(f"[red]Failed to delete thought: {e}[/red]")
    
    async def _handle_sync(self, args: List[str]) -> None:
        """Handle sync command."""
        try:
            # Check authentication
            if not self.auth_manager.is_authenticated():
                self.console.print("[yellow]You need to login first. Use the main CLI: faraday auth login[/yellow]")
                return
            
            self.console.print("[blue]Syncing with server...[/blue]")
            await self.cached_api.sync()
            self.console.print("[green]✓[/green] Sync completed")
            
        except Exception as e:
            self.console.print(f"[red]Sync failed: {e}[/red]")
    
    async def _handle_stats(self, args: List[str]) -> None:
        """Handle stats command."""
        try:
            # Check authentication
            if not self.auth_manager.is_authenticated():
                self.console.print("[yellow]You need to login first. Use the main CLI: faraday auth login[/yellow]")
                return
            
            # Get basic stats from cache
            stats = await self.cached_api.get_stats()
            
            # Display stats
            table = Table(title="Thought Statistics")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Total Thoughts", str(stats.get("total_thoughts", 0)))
            table.add_row("Cached Thoughts", str(stats.get("cached_thoughts", 0)))
            table.add_row("Pending Sync", str(stats.get("pending_sync", 0)))
            
            self.console.print(table)
            
        except Exception as e:
            self.console.print(f"[red]Failed to get stats: {e}[/red]")
    
    async def _handle_config(self, args: List[str]) -> None:
        """Handle config command."""
        if not args:
            # Show current config
            config_data = {
                "API URL": str(self.config.get("api.url", "http://localhost:8001")),
                "Cache Enabled": str(self.config.get("cache.enabled", True)),
                "Output Colors": str(self.config.get("output.colors", True)),
            }
            
            table = Table(title="Configuration")
            table.add_column("Setting", style="cyan")
            table.add_column("Value", style="green")
            
            for key, value in config_data.items():
                table.add_row(key, value)
            
            self.console.print(table)
        else:
            self.console.print("[yellow]Config modification not supported in interactive mode.[/yellow]")
            self.console.print("Use the main CLI: faraday config set <key> <value>")
    
    async def _handle_help(self, args: List[str]) -> None:
        """Handle help command."""
        help_table = Table(title="Available Commands")
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description", style="white")
        help_table.add_column("Example", style="dim")
        
        commands_help = [
            ("add <content>", "Add a new thought", "add: Had a great idea"),
            ("search <query>", "Search thoughts", "search: coffee meetings"),
            ("list [limit]", "List recent thoughts", "list 5"),
            ("show <id>", "Show thought details", "show abc123"),
            ("delete <id>", "Delete a thought", "delete abc123"),
            ("sync", "Sync with server", "sync"),
            ("stats", "Show statistics", "stats"),
            ("config", "Show configuration", "config"),
            ("history", "Show command history", "history"),
            ("clear", "Clear screen", "clear"),
            ("help", "Show this help", "help"),
            ("exit/quit", "Exit interactive mode", "exit"),
        ]
        
        for cmd, desc, example in commands_help:
            help_table.add_row(cmd, desc, example)
        
        self.console.print(help_table)
        self.console.print("\n[dim]Tips:[/dim]")
        self.console.print("• Use colon syntax: 'add: your thought here'")
        self.console.print("• Press Ctrl+C to cancel current input")
        self.console.print("• Commands are case-insensitive")
    
    async def _handle_history(self, args: List[str]) -> None:
        """Handle history command."""
        if not self.history:
            self.console.print("[yellow]No command history[/yellow]")
            return
        
        # Show last 10 commands by default
        limit = 10
        if args and args[0].isdigit():
            limit = int(args[0])
        
        recent_history = self.history[-limit:]
        
        table = Table(title="Command History")
        table.add_column("#", style="dim")
        table.add_column("Command", style="white")
        
        for i, cmd in enumerate(recent_history, 1):
            table.add_row(str(i), cmd)
        
        self.console.print(table)
    
    async def _handle_clear(self, args: List[str]) -> None:
        """Handle clear command."""
        # Clear screen
        self.console.clear()
        self._show_welcome()
    
    async def _handle_exit(self, args: List[str]) -> None:
        """Handle exit command."""
        self.running = False


@click.command()
@click.pass_context
def interactive(ctx: click.Context) -> None:
    """Start interactive mode for conversational thought management.
    
    Interactive mode provides a REPL-style interface where you can:
    - Add thoughts with natural syntax: "add: your thought here"
    - Search your knowledge base: "search: coffee meetings"
    - Manage thoughts with simple commands
    - Get help and command completion
    
    Type 'help' in interactive mode to see all available commands.
    """
    # Get components from context
    config = ctx.obj["config"]
    cached_api = ctx.obj["cached_api"]
    output = ctx.obj["output"]
    auth_manager = ctx.obj["auth_manager"]
    console = ctx.obj["console"]
    
    # Create and start interactive session
    session = InteractiveSession(config, cached_api, output, auth_manager, console)
    session.start()