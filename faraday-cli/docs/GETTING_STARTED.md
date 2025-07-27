# Getting Started with Faraday CLI

Welcome to Faraday CLI! This guide will help you get up and running in just a few minutes.

## Quick Start

### 1. Installation

```bash
# Install from PyPI (when available)
pip install faraday-cli

# Or install from source
git clone <repository-url>
cd faraday-cli
pip install -e .
```

### 2. First-Time Setup

Configure your Faraday server:

```bash
faraday config set api.url http://localhost:8001
```

Login to your account:

```bash
faraday auth login
```

Verify everything is working:

```bash
faraday auth status
```

### 3. Your First Thought

Add your first thought:

```bash
faraday thoughts add "This is my first thought in Faraday!"
```

### 4. Try Interactive Mode

For a more natural experience:

```bash
faraday
```

This starts interactive mode where you can use commands like:
- `add: your thought here`
- `search: coffee meetings`
- `list 10`
- `help`

## Essential Commands

| Command | Description | Example |
|---------|-------------|---------|
| `faraday` | Start interactive mode | `faraday` |
| `faraday auth login` | Login to server | `faraday auth login` |
| `faraday thoughts add "text"` | Add a thought | `faraday thoughts add "Great meeting today"` |
| `faraday search "query"` | Search thoughts | `faraday search "coffee meetings"` |
| `faraday thoughts list` | List recent thoughts | `faraday thoughts list` |
| `faraday config show` | Show configuration | `faraday config show` |
| `faraday help guide` | Show help guides | `faraday help guide getting-started` |

## Interactive Mode

Interactive mode is perfect for daily use:

```bash
$ faraday
🧠 Welcome to Faraday Interactive Mode

faraday> add: Had a productive day working on the CLI
✓ Added thought: abc12345...

faraday> search: productive work
🔍 Found 3 thoughts matching "productive work":
1. [abc12345] Had a productive day working on the CLI
   ...

faraday> help
# Shows available commands

faraday> exit
👋 Thanks for using Faraday!
```

## Configuration

Faraday stores configuration in platform-specific locations:

- **Linux/Unix**: `~/.config/faraday/config.toml`
- **macOS**: `~/Library/Application Support/faraday/config.toml`
- **Windows**: `%APPDATA%\faraday\config.toml`

Key settings:

```bash
# Server configuration
faraday config set api.url "https://your-server.com"
faraday config set api.timeout 30

# Output preferences
faraday config set output.colors true
faraday config set output.max_results 20

# Caching
faraday config set cache.enabled true
faraday config set cache.max_size_mb 100
```

## Shell Integration

### Install Completions

Run the installation script to set up shell completions:

```bash
./scripts/install_completions.sh
```

This installs:
- Tab completion for your shell (Bash, Zsh, Fish)
- Man page (`man faraday`)
- Suggested aliases

### Useful Aliases

Add these to your shell config file:

```bash
alias ft='faraday thoughts'
alias fs='faraday search'
alias fc='faraday config'
alias fa='faraday auth'
alias fi='faraday interactive'
```

## Common Workflows

### Daily Journaling

```bash
# Start interactive mode
faraday

# Add thoughts throughout the day
faraday> add: Morning standup went well, discussed new features
faraday> add: Lunch with Sarah, great discussion about UX design
faraday> add: Afternoon coding session, implemented search filters

# Review your day
faraday> search: today insights
faraday> list 10
```

### Research and Note-Taking

```bash
# Capture research findings
faraday thoughts add "Paper: 'Attention Is All You Need' - transformer architecture breakthrough" --tags research,ml

# Link related concepts
faraday search "transformer architecture" --tags research

# Organize by topics
faraday thoughts add "Meeting notes: AI team discussion on model architecture" --tags meetings,ai
```

### Project Documentation

```bash
# Document project decisions
faraday thoughts add "Decision: Using FastAPI for the backend API" --tags project,backend

# Track progress
faraday thoughts add "Milestone: User authentication system completed" --tags project,milestone

# Review project history
faraday search "project decisions" --tags project
```

## Getting Help

Faraday has comprehensive help built-in:

```bash
# General help
faraday --help

# Command-specific help
faraday thoughts --help
faraday search --help

# Interactive tutorial
faraday help tutorial

# Detailed guides
faraday help guide getting-started
faraday help guide commands
faraday help guide interactive
faraday help guide configuration
faraday help guide scripting
faraday help guide troubleshooting
faraday help guide examples

# Quick reference
faraday help shortcuts
faraday help workflows
```

## Troubleshooting

### Common Issues

**Connection Problems:**
```bash
# Check configuration
faraday config get api.url

# Test with verbose output
faraday --verbose auth status

# Try different URL
faraday --api-url http://localhost:8001 auth status
```

**Authentication Issues:**
```bash
# Check login status
faraday auth status

# Re-login
faraday auth logout
faraday auth login
```

**Configuration Problems:**
```bash
# Show current config
faraday config show

# Reset to defaults
faraday config reset

# Check config file location
faraday config path
```

### Debug Mode

Use verbose output for troubleshooting:

```bash
faraday --verbose <command>
```

## Next Steps

1. **Explore Interactive Mode**: Run `faraday` and try the natural command syntax
2. **Set Up Shell Integration**: Run `./scripts/install_completions.sh`
3. **Read the Guides**: Check `faraday help guide` for detailed documentation
4. **Customize Configuration**: Adjust settings with `faraday config set`
5. **Try Scripting**: Use `--json` flag for automation

## Advanced Features

### JSON Output for Scripting

```bash
# Get structured data
faraday --json thoughts list | jq '.thoughts[].content'

# Process search results
faraday --json search "AI" | jq '.results[] | select(.score > 0.8)'
```

### Environment Variables

```bash
export FARADAY_API_URL="https://my-server.com"
export FARADAY_CONFIG="/path/to/config.toml"
export FARADAY_NO_INTERACTIVE=1
```

### Multiple Configurations

```bash
# Development config
faraday --config ~/.faraday/dev.toml thoughts list

# Production config
faraday --config ~/.faraday/prod.toml thoughts list
```

You're now ready to start building your personal knowledge base with Faraday CLI! 🚀

For more detailed information, check out the comprehensive guides:
- [CLI Usage Guide](CLI_USAGE.md)
- [Configuration Guide](CONFIGURATION.md)
- Built-in help: `faraday help guide`