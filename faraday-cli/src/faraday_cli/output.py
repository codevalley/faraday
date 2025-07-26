"""Output formatting using Rich library for beautiful terminal display."""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, TextColumn

from faraday_cli.api import ThoughtData, SearchResult, UserStats


class OutputFormatter:
    """Handles formatted output for CLI commands using Rich library."""
    
    def __init__(self, console: Console, json_mode: bool = False):
        """Initialize output formatter.
        
        Args:
            console: Rich console instance
            json_mode: If True, output raw JSON instead of formatted text
        """
        self.console = console
        self.json_mode = json_mode
    
    def format_thought(self, thought: ThoughtData, show_full: bool = True) -> None:
        """Format and display a single thought.
        
        Args:
            thought: Thought data to display
            show_full: If True, show full details; if False, show summary
        """
        if self.json_mode:
            self.console.print(thought.json(indent=2))
            return
        
        # Create thought panel
        if show_full:
            # Full thought display with metadata
            content_text = Text(thought.content, style="white")
            
            # Build metadata info
            metadata_parts = []
            metadata_parts.append(f"📅 {thought.timestamp.strftime('%Y-%m-%d %H:%M')}")
            
            if thought.metadata:
                if "mood" in thought.metadata:
                    mood_emoji = self._get_mood_emoji(thought.metadata["mood"])
                    metadata_parts.append(f"{mood_emoji} {thought.metadata['mood']}")
                
                if "tags" in thought.metadata and thought.metadata["tags"]:
                    tags = ", ".join(thought.metadata["tags"])
                    metadata_parts.append(f"🏷️  {tags}")
            
            metadata_text = " • ".join(metadata_parts)
            
            # Create panel with thought content and metadata
            panel_content = f"{content_text}\n\n{metadata_text}"
            panel = Panel(
                panel_content,
                title=f"Thought #{thought.id[:8]}",
                title_align="left",
                border_style="blue"
            )
            
        else:
            # Summary display for lists
            timestamp_str = thought.timestamp.strftime('%m/%d %H:%M')
            content_preview = thought.content[:80] + "..." if len(thought.content) > 80 else thought.content
            
            panel = Panel(
                f"{content_preview}\n[dim]{timestamp_str} • ID: {thought.id[:8]}[/dim]",
                border_style="dim blue"
            )
        
        self.console.print(panel)
    
    def format_thought_list(self, thoughts: List[ThoughtData], title: str = "Thoughts") -> None:
        """Format and display a list of thoughts.
        
        Args:
            thoughts: List of thoughts to display
            title: Title for the thought list
        """
        if self.json_mode:
            thoughts_data = [json.loads(thought.json()) for thought in thoughts]
            self.console.print(json.dumps(thoughts_data, indent=2, default=str))
            return
        
        if not thoughts:
            self.console.print(f"[dim]No {title.lower()} found.[/dim]")
            return
        
        self.console.print(f"\n[bold blue]{title}[/bold blue] ({len(thoughts)} found)\n")
        
        for thought in thoughts:
            self.format_thought(thought, show_full=False)
            self.console.print()  # Add spacing between thoughts
    
    def format_search_results(self, results: SearchResult) -> None:
        """Format and display search results.
        
        Args:
            results: Search results to display
        """
        if self.json_mode:
            self.console.print(results.json(indent=2))
            return
        
        # Search header
        self.console.print(f"\n🔍 Search: [bold]'{results.query}'[/bold] "
                          f"({results.total} results in {results.execution_time:.2f}s)\n")
        
        if not results.thoughts:
            self.console.print("[dim]No matching thoughts found.[/dim]")
            return
        
        # Display each result with relevance info
        for i, thought in enumerate(results.thoughts, 1):
            # For now, we'll show a mock relevance score
            # In a real implementation, this would come from the search API
            relevance = max(95 - (i * 5), 60)  # Mock decreasing relevance
            
            content_preview = thought.content[:100] + "..." if len(thought.content) > 100 else thought.content
            timestamp_str = thought.timestamp.strftime('%Y-%m-%d')
            
            # Create result panel with relevance indicator
            panel_title = f"{relevance}% Match • Thought #{thought.id[:8]}"
            panel_content = f"{content_preview}\n[dim]{timestamp_str}[/dim]"
            
            if thought.metadata:
                metadata_parts = []
                if "tags" in thought.metadata and thought.metadata["tags"]:
                    tags = ", ".join(thought.metadata["tags"])
                    metadata_parts.append(f"🏷️ {tags}")
                if "mood" in thought.metadata:
                    mood_emoji = self._get_mood_emoji(thought.metadata["mood"])
                    metadata_parts.append(f"{mood_emoji} {thought.metadata['mood']}")
                
                if metadata_parts:
                    panel_content += f" • {' • '.join(metadata_parts)}"
            
            panel = Panel(
                panel_content,
                title=panel_title,
                title_align="left",
                border_style="green" if relevance >= 80 else "yellow" if relevance >= 60 else "red"
            )
            
            self.console.print(panel)
            self.console.print()
    
    def format_stats(self, stats: UserStats) -> None:
        """Format and display user statistics.
        
        Args:
            stats: User statistics to display
        """
        if self.json_mode:
            self.console.print(stats.json(indent=2))
            return
        
        # Create stats table
        table = Table(title="📊 Your Faraday Statistics", show_header=False)
        table.add_column("Metric", style="cyan", width=20)
        table.add_column("Value", style="white")
        
        table.add_row("Total Thoughts", str(stats.total_thoughts))
        table.add_row("This Week", str(stats.thoughts_this_week))
        
        if stats.most_common_tags:
            tags_str = ", ".join(stats.most_common_tags[:5])  # Show top 5 tags
            table.add_row("Top Tags", tags_str)
        
        self.console.print(table)
        
        # Mood distribution chart (simple text-based)
        if stats.mood_distribution:
            self.console.print("\n[bold]Mood Distribution:[/bold]")
            total_moods = sum(stats.mood_distribution.values())
            
            for mood, count in stats.mood_distribution.items():
                percentage = (count / total_moods) * 100 if total_moods > 0 else 0
                emoji = self._get_mood_emoji(mood)
                bar_length = int(percentage / 5)  # Scale bar to fit terminal
                bar = "█" * bar_length + "░" * (20 - bar_length)
                
                self.console.print(f"{emoji} {mood:10} {bar} {percentage:5.1f}% ({count})")
    
    def format_table(self, data: List[Dict[str, Any]], headers: List[str], 
                    title: Optional[str] = None) -> None:
        """Format and display data as a table.
        
        Args:
            data: List of dictionaries containing row data
            headers: List of column headers
            title: Optional table title
        """
        if self.json_mode:
            self.console.print(json.dumps(data, indent=2, default=str))
            return
        
        if not data:
            self.console.print("[dim]No data to display.[/dim]")
            return
        
        table = Table(title=title)
        
        # Add columns
        for header in headers:
            table.add_column(header, style="cyan")
        
        # Add rows
        for row in data:
            row_values = [str(row.get(header, "")) for header in headers]
            table.add_row(*row_values)
        
        self.console.print(table)
    
    def format_error(self, error: str, error_type: str = "Error") -> None:
        """Format and display an error message.
        
        Args:
            error: Error message to display
            error_type: Type of error (for styling)
        """
        if self.json_mode:
            error_data = {"error": error, "type": error_type}
            self.console.print(json.dumps(error_data, indent=2))
            return
        
        # Choose emoji and color based on error type
        if "network" in error_type.lower():
            emoji = "🌐"
            style = "red"
        elif "auth" in error_type.lower():
            emoji = "🔐"
            style = "yellow"
        elif "validation" in error_type.lower():
            emoji = "❌"
            style = "orange3"
        else:
            emoji = "💥"
            style = "red"
        
        panel = Panel(
            f"{emoji} {error}",
            title=f"[{style}]{error_type}[/{style}]",
            border_style=style
        )
        
        self.console.print(panel)
    
    def format_success(self, message: str, title: str = "Success") -> None:
        """Format and display a success message.
        
        Args:
            message: Success message to display
            title: Title for the success panel
        """
        if self.json_mode:
            success_data = {"success": True, "message": message}
            self.console.print(json.dumps(success_data, indent=2))
            return
        
        panel = Panel(
            f"✅ {message}",
            title=f"[green]{title}[/green]",
            border_style="green"
        )
        
        self.console.print(panel)
    
    def create_progress(self, description: str = "Processing...") -> Progress:
        """Create a progress indicator for long-running operations.
        
        Args:
            description: Description of the operation
            
        Returns:
            Rich Progress instance
        """
        return Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        )
    
    def _get_mood_emoji(self, mood: str) -> str:
        """Get emoji representation for a mood.
        
        Args:
            mood: Mood string
            
        Returns:
            Appropriate emoji for the mood
        """
        mood_emojis = {
            "happy": "😊",
            "excited": "🤩",
            "sad": "😢",
            "angry": "😠",
            "neutral": "😐",
            "anxious": "😰",
            "calm": "😌",
            "confused": "😕",
            "grateful": "🙏",
            "frustrated": "😤"
        }
        
        return mood_emojis.get(mood.lower(), "💭")