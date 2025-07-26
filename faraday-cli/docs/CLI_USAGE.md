# Faraday CLI Usage Guide

Complete guide to using the Faraday CLI for managing your personal semantic engine.

## Table of Contents

- [Getting Started](#getting-started)
- [Global Options](#global-options)
- [Configuration Commands](#configuration-commands)
- [Authentication Commands](#authentication-commands)
- [Thought Management Commands](#thought-management-commands)
- [Output Formats](#output-formats)
- [Advanced Usage](#advanced-usage)
- [Scripting and Automation](#scripting-and-automation)
- [Troubleshooting](#troubleshooting)

## Getting Started

### First-Time Setup

1. **Install the CLI** (when available on PyPI):
   ```bash
   pip install faraday-cli
   ```

2. **Configure your server**:
   ```bash
   faraday config set api.url http://localhost:8001
   ```

3. **Login to your account**:
   ```bash
   faraday auth login
   ```

4. **Verify setup**:
   ```bash
   faraday auth status
   ```

### Quick Commands Reference

```bash
# Configuration
faraday config show                    # View all settings
faraday config set api.url <url>       # Set server URL
faraday config reset                   # Reset to defaults

# Authentication  
faraday auth login                     # Login to server
faraday auth status                    # Check login status
faraday auth logout                    # Logout

# Thoughts
faraday thoughts add "content"         # Add new thought
faraday thoughts search "query"        # Search thoughts
faraday thoughts list                  # List recent thoughts
faraday thoughts get <id>              # Get specific thought

# Utility
faraday version                        # Show version
faraday --help                         # Show help
```

## Global Options

These options can be used with any command:

### `--config PATH`

Use a custom configuration file:

```bash
# Use development config
faraday --config ~/dev-config.toml thoughts list

# Use production config
faraday --config /etc/faraday/prod.toml auth status
```

### `--api-url URL`

Override the configured API URL:

```bash
# Connect to different server temporarily
faraday --api-url http://staging.example.com:8001 thoughts list

# Test against local development server
faraday --api-url http://localhost:3000 auth status
```

### `--json`

Output results in JSON format:

```bash
# Get configuration as JSON
faraday --json config show

# Search with JSON output for processing
faraday --json thoughts search "coffee" | jq '.results[].content'

# Get structured data for scripts
faraday --json thoughts list | jq '.thoughts | length'
```

### `--verbose`

Enable verbose output for debugging:

```bash
# Debug connection issues
faraday --verbose thoughts list

# See detailed API requests
faraday --verbose auth login
```

## Configuration Commands

The `faraday config` command group manages CLI settings.

### `faraday config show`

Display all configuration settings in a readable format:

```bash
$ faraday config show
Current Configuration:

api:
  api.url = http://localhost:8001
  api.timeout = 30
auth:
  auth.auto_login = True
  auth.remember_token = True
output:
  output.colors = True
  output.pager = auto
  output.max_results = 20
cache:
  cache.enabled = True
  cache.max_size_mb = 100
  cache.sync_interval = 300
```

### `faraday config get [KEY]`

Get specific configuration value or all values:

```bash
# Get specific value
$ faraday config get api.url
api.url = http://localhost:8001

# Get all values (same as 'show')
$ faraday config get
# ... shows all configuration
```

### `faraday config set KEY VALUE`

Set configuration values with automatic type detection:

```bash
# String values
faraday config set api.url "https://my-server.com"

# Boolean values (JSON parsing)
faraday config set output.colors true
faraday config set auth.auto_login false

# Numeric values
faraday config set api.timeout 60
faraday config set cache.max_size_mb 200

# Complex values (JSON)
faraday config set custom.list '[1, 2, 3]'
```

### `faraday config reset`

Reset all configuration to defaults with confirmation:

```bash
$ faraday config reset
Are you sure you want to reset all configuration to defaults? [y/N]: y
✅ Configuration reset to defaults
```

### `faraday config path`

Show the location of the configuration file:

```bash
$ faraday config path
Configuration file: /Users/username/Library/Application Support/faraday/config.toml
✓ File exists
```

## Authentication Commands

The `faraday auth` command group manages authentication.

### `faraday auth login`

Login to your Faraday server:

```bash
$ faraday auth login
Username: john@example.com
Password: [hidden]
✅ Successfully logged in as john@example.com
```

**Interactive prompts**:
- Username/email
- Password (hidden input)
- Optional: Remember credentials

### `faraday auth status`

Check current authentication status:

```bash
$ faraday auth status
✅ Logged in as john@example.com
Server: http://localhost:8001
Token expires: 2024-01-15 14:30:00 UTC
```

### `faraday auth logout`

Logout and clear stored tokens:

```bash
$ faraday auth logout
✅ Successfully logged out
```

## Thought Management Commands

The `faraday thoughts` command group manages your thoughts.

### `faraday thoughts add CONTENT`

Add a new thought:

```bash
# Simple thought
faraday thoughts add "Had a great meeting with the design team today"

# Thought with quotes
faraday thoughts add "Einstein said: 'Imagination is more important than knowledge'"

# Multi-line thought (use quotes)
faraday thoughts add "Project ideas:
1. AI-powered note taking
2. Semantic search for documents
3. Personal knowledge graph"
```

**Response**:
```bash
✅ Thought added successfully
ID: abc123def456
Content: Had a great meeting with the design team today
```

### `faraday thoughts search QUERY`

Search your thoughts using natural language:

```bash
# Simple search
faraday thoughts search "design meetings"

# Complex queries
faraday thoughts search "AI projects and machine learning"
faraday thoughts search "book recommendations fiction"

# Search with filters (if supported)
faraday thoughts search "coffee" --limit 10
```

**Response**:
```bash
Found 3 thoughts matching "design meetings":

1. [abc123] Had a great meeting with the design team today
   Similarity: 0.95 | Created: 2024-01-10 14:30

2. [def456] Design review went well, team loved the new mockups  
   Similarity: 0.87 | Created: 2024-01-08 10:15

3. [ghi789] Planning next design sprint meeting for Friday
   Similarity: 0.82 | Created: 2024-01-05 16:45
```

### `faraday thoughts list`

List recent thoughts:

```bash
# List default number of thoughts
faraday thoughts list

# List specific number
faraday thoughts list --limit 50

# List with different sorting
faraday thoughts list --sort created_desc
faraday thoughts list --sort relevance
```

**Response**:
```bash
Recent thoughts (20 most recent):

1. [abc123] Had a great meeting with the design team today
   Created: 2024-01-10 14:30

2. [def456] Learning about vector databases and embeddings
   Created: 2024-01-10 09:15

3. [ghi789] Coffee shop idea: AI-powered menu recommendations
   Created: 2024-01-09 16:20
```

### `faraday thoughts get ID`

Get a specific thought by ID:

```bash
faraday thoughts get abc123def456
```

**Response**:
```bash
Thought Details:

ID: abc123def456
Content: Had a great meeting with the design team today
Created: 2024-01-10 14:30:00 UTC
Updated: 2024-01-10 14:30:00 UTC
Tags: meeting, design, team
Related: 3 similar thoughts found
```

## Output Formats

### Human-Readable Output (Default)

Designed for terminal use with colors, formatting, and visual elements:

```bash
$ faraday thoughts search "coffee"
Found 2 thoughts matching "coffee":

☕ [abc123] Great coffee shop downtown with amazing wifi
   Similarity: 0.92 | Created: 2024-01-10 14:30

☕ [def456] Coffee meeting with Sarah went really well  
   Similarity: 0.85 | Created: 2024-01-08 10:15
```

### JSON Output

Structured data perfect for scripting and processing:

```bash
$ faraday --json thoughts search "coffee"
{
  "query": "coffee",
  "results": [
    {
      "id": "abc123",
      "content": "Great coffee shop downtown with amazing wifi",
      "similarity": 0.92,
      "created_at": "2024-01-10T14:30:00Z",
      "tags": ["coffee", "location", "wifi"]
    },
    {
      "id": "def456", 
      "content": "Coffee meeting with Sarah went really well",
      "similarity": 0.85,
      "created_at": "2024-01-08T10:15:00Z",
      "tags": ["coffee", "meeting", "sarah"]
    }
  ],
  "total": 2,
  "query_time": 0.045
}
```

## Advanced Usage

### Combining Commands with Pipes

```bash
# Search and get details of first result
faraday --json thoughts search "AI" | jq -r '.results[0].id' | xargs faraday thoughts get

# Count thoughts by tag
faraday --json thoughts list --limit 1000 | jq '.thoughts[].tags[]' | sort | uniq -c

# Export all thoughts to file
faraday --json thoughts list --limit 10000 > my_thoughts_backup.json
```

### Environment Variables

Set environment variables for common configurations:

```bash
# Set default API URL
export FARADAY_API_URL="https://my-server.com"

# Set default config file
export FARADAY_CONFIG="$HOME/.config/faraday/prod.toml"

# Use in commands
faraday thoughts list
```

### Aliases and Shortcuts

Create shell aliases for common operations:

```bash
# Add to your ~/.bashrc or ~/.zshrc
alias ft="faraday thoughts"
alias fc="faraday config"
alias fa="faraday auth"

# Usage
ft add "Quick thought"
ft search "important"
fc show
fa status
```

### Configuration Profiles

Manage multiple environments:

```bash
# Development profile
alias faraday-dev="faraday --config ~/.config/faraday/dev.toml"

# Production profile  
alias faraday-prod="faraday --config ~/.config/faraday/prod.toml"

# Staging profile
alias faraday-staging="faraday --config ~/.config/faraday/staging.toml"

# Usage
faraday-dev thoughts add "Development note"
faraday-prod thoughts search "production issues"
```

## Scripting and Automation

### Bash Scripts

```bash
#!/bin/bash
# daily_thoughts.sh - Add daily standup notes

echo "Adding daily standup thoughts..."

# Add thoughts from command line arguments
for thought in "$@"; do
    echo "Adding: $thought"
    faraday thoughts add "$thought"
done

# Search for today's thoughts
echo "Today's thoughts:"
faraday thoughts search "$(date +%Y-%m-%d)"
```

### Python Integration

```python
#!/usr/bin/env python3
import subprocess
import json
import sys

def search_thoughts(query):
    """Search thoughts and return JSON results."""
    result = subprocess.run([
        'faraday', '--json', 'thoughts', 'search', query
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return None

def add_thought(content):
    """Add a new thought."""
    result = subprocess.run([
        'faraday', 'thoughts', 'add', content
    ], capture_output=True, text=True)
    
    return result.returncode == 0

# Usage
if __name__ == "__main__":
    # Search for thoughts
    results = search_thoughts("machine learning")
    if results:
        print(f"Found {len(results['results'])} thoughts")
        
    # Add new thought
    if add_thought("Automated thought from Python script"):
        print("Thought added successfully")
```

### Cron Jobs

```bash
# Add to crontab (crontab -e)

# Daily backup of thoughts
0 2 * * * faraday --json thoughts list --limit 10000 > ~/backups/thoughts_$(date +\%Y\%m\%d).json

# Weekly summary
0 9 * * 1 faraday thoughts search "weekly goals" | mail -s "Weekly Goals" user@example.com
```

## Troubleshooting

### Common Issues

#### Connection Problems

```bash
# Check configuration
faraday config get api.url

# Test connection with verbose output
faraday --verbose auth status

# Try different URL
faraday --api-url http://localhost:8001 auth status
```

#### Authentication Issues

```bash
# Check login status
faraday auth status

# Clear and re-login
faraday auth logout
faraday auth login

# Check server connectivity
curl -I $(faraday config get api.url)
```

#### Configuration Problems

```bash
# Check config file location and contents
faraday config path
faraday config show

# Reset corrupted configuration
faraday config reset

# Use temporary config
faraday --config /tmp/test-config.toml config show
```

### Debug Mode

Enable verbose output for detailed debugging:

```bash
# See all HTTP requests and responses
faraday --verbose thoughts search "debug"

# Check configuration loading
faraday --verbose config show

# Debug authentication flow
faraday --verbose auth login
```

### Error Messages

Common error messages and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `Connection refused` | Server not running | Check server status and URL |
| `Authentication failed` | Invalid credentials | Re-login with correct credentials |
| `Configuration key not found` | Typo in key name | Check available keys with `config show` |
| `Invalid configuration value` | Wrong data type | Check value format and type |
| `Permission denied` | File permissions | Fix config file permissions |

### Getting Help

```bash
# General help
faraday --help

# Command-specific help
faraday config --help
faraday thoughts --help
faraday auth --help

# Subcommand help
faraday thoughts add --help
faraday config set --help
```

### Reporting Issues

When reporting issues, include:

1. **CLI version**: `faraday version`
2. **Configuration**: `faraday --json config show` (remove sensitive data)
3. **Error output**: Full error message with `--verbose` flag
4. **Environment**: OS, terminal, shell version
5. **Steps to reproduce**: Exact commands that cause the issue

This comprehensive usage guide should help users effectively use all aspects of the Faraday CLI.