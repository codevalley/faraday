# Faraday CLI

A powerful command-line interface for the Faraday Personal Semantic Engine that enables you to manage your thoughts, perform semantic searches, and analyze your personal knowledge base from the terminal.

## Features

- 🧠 **Thought Management**: Add, search, and organize your thoughts
- 🔍 **Semantic Search**: Find thoughts using natural language queries
- ⚙️ **Configuration Management**: Flexible configuration with platform-specific defaults
- 🔐 **Authentication**: Secure login and token management
- 📊 **Multiple Output Formats**: Human-readable and JSON output modes
- 🎨 **Rich Terminal UI**: Beautiful, colorized output with Rich library
- 🌐 **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### From PyPI (when published)
```bash
pip install faraday-cli
```

### Development Installation
```bash
git clone <repository-url>
cd faraday-cli
poetry install
```

## Quick Start

1. **Configure your Faraday instance**:
   ```bash
   faraday config set api.url http://localhost:8001
   ```

2. **Login to your account**:
   ```bash
   faraday login
   ```

3. **Add your first thought**:
   ```bash
   faraday thoughts add "Had an amazing coffee meeting with Sarah today"
   ```

4. **Search your thoughts**:
   ```bash
   faraday thoughts search "coffee meetings"
   ```

## Commands Overview

### Configuration Commands

The `faraday config` command group manages CLI configuration:

```bash
# Show all configuration
faraday config show

# Get specific configuration value
faraday config get api.url

# Set configuration values
faraday config set api.url http://localhost:8001
faraday config set output.colors true
faraday config set api.timeout 60

# Reset to defaults
faraday config reset

# Show config file location
faraday config path
```

### Authentication Commands

```bash
# Login to your Faraday instance
faraday auth login

# Check login status
faraday auth status

# Logout
faraday auth logout
```

### Thought Management Commands

```bash
# Add a new thought
faraday thoughts add "Your thought content here"

# Search thoughts
faraday thoughts search "search query"

# List recent thoughts
faraday thoughts list

# Get specific thought by ID
faraday thoughts get <thought-id>
```

### Global Options

All commands support these global options:

```bash
# Use custom config file
faraday --config /path/to/config.toml <command>

# Override API URL
faraday --api-url http://custom-server:8001 <command>

# JSON output mode
faraday --json <command>

# Verbose output
faraday --verbose <command>
```

## Configuration

### Configuration File Locations

The CLI stores configuration in platform-specific locations:

- **Windows**: `%APPDATA%\faraday\config.toml`
- **macOS**: `~/Library/Application Support/faraday/config.toml`
- **Linux**: `~/.config/faraday/config.toml`

### Configuration Structure

```toml
[api]
url = "http://localhost:8001"
timeout = 30

[auth]
auto_login = true
remember_token = true

[output]
colors = true
pager = "auto"
max_results = 20

[cache]
enabled = true
max_size_mb = 100
sync_interval = 300
```

### Configuration Options

#### API Settings
- `api.url`: Faraday server URL (default: `http://localhost:8001`)
- `api.timeout`: Request timeout in seconds (default: `30`)

#### Authentication Settings
- `auth.auto_login`: Automatically attempt login when needed (default: `true`)
- `auth.remember_token`: Remember authentication tokens (default: `true`)

#### Output Settings
- `output.colors`: Enable colored output (default: `true`)
- `output.pager`: Pager for long output (`auto`, `less`, `more`, `none`) (default: `auto`)
- `output.max_results`: Maximum results to display (default: `20`)

#### Cache Settings
- `cache.enabled`: Enable local caching (default: `true`)
- `cache.max_size_mb`: Maximum cache size in MB (default: `100`)
- `cache.sync_interval`: Cache sync interval in seconds (default: `300`)

## Examples

### Basic Usage

```bash
# Configure your server
faraday config set api.url https://my-faraday-server.com

# Login
faraday auth login

# Add some thoughts
faraday thoughts add "Learning about semantic search today"
faraday thoughts add "Great book recommendation: 'Thinking, Fast and Slow'"
faraday thoughts add "Coffee shop idea: AI-powered menu recommendations"

# Search for thoughts
faraday thoughts search "book recommendations"
faraday thoughts search "AI ideas"

# List recent thoughts
faraday thoughts list --limit 10
```

### JSON Output Mode

```bash
# Get configuration as JSON
faraday --json config show

# Search with JSON output
faraday --json thoughts search "coffee" | jq '.results[].content'

# Get thought details as JSON
faraday --json thoughts get abc123 | jq '.timestamp'
```

### Advanced Configuration

```bash
# Set up for development environment
faraday config set api.url http://localhost:8001
faraday config set api.timeout 60
faraday config set output.max_results 50

# Disable colors for scripting
faraday config set output.colors false

# Configure caching
faraday config set cache.max_size_mb 200
faraday config set cache.sync_interval 600
```

## Error Handling

The CLI provides helpful error messages for common issues:

```bash
# Invalid configuration values
$ faraday config set api.timeout "not_a_number"
💥 Invalid configuration: Invalid configuration value for 'api.timeout': 
   Input should be a valid integer

# Missing configuration keys
$ faraday config get nonexistent.key
💥 Configuration key 'nonexistent.key' not found

# Connection issues
$ faraday thoughts list
💥 Connection Error: Could not connect to Faraday server at http://localhost:8001
   Please check your configuration and server status.
```

## Troubleshooting

### Common Issues

1. **Configuration file not found**:
   ```bash
   # Check config file location
   faraday config path
   
   # Reset to defaults if corrupted
   faraday config reset
   ```

2. **Connection refused**:
   ```bash
   # Check server URL
   faraday config get api.url
   
   # Update if needed
   faraday config set api.url http://correct-server:8001
   ```

3. **Authentication issues**:
   ```bash
   # Check login status
   faraday auth status
   
   # Re-login if needed
   faraday auth logout
   faraday auth login
   ```

### Debug Mode

Enable verbose output for debugging:

```bash
faraday --verbose thoughts search "debug query"
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone <repository-url>
cd faraday-cli

# Install dependencies
poetry install

# Run CLI in development
poetry run faraday --help

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=faraday_cli

# Format code
poetry run black .
poetry run isort .

# Type checking
poetry run mypy src/
```

### Project Structure

```
faraday-cli/
├── src/faraday_cli/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── config.py            # Configuration management
│   ├── api.py               # API client
│   ├── auth.py              # Authentication
│   ├── output.py            # Output formatting
│   └── commands/
│       ├── __init__.py
│       ├── auth.py          # Auth commands
│       ├── config.py        # Config commands
│       └── thoughts.py      # Thought commands
├── tests/
│   ├── test_config.py
│   ├── test_main.py
│   └── ...
├── pyproject.toml
└── README.md
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_config.py

# Run with verbose output
poetry run pytest -v

# Run with coverage
poetry run pytest --cov=faraday_cli --cov-report=html
```

### Code Quality

The project follows strict code quality standards:

```bash
# Format code
poetry run black .

# Sort imports
poetry run isort .

# Type checking
poetry run mypy src/

# All quality checks
poetry run black . && poetry run isort . && poetry run mypy src/ && poetry run pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and quality checks
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- 📖 Documentation: [Link to docs]
- 🐛 Bug Reports: [Link to issues]
- 💬 Discussions: [Link to discussions]
- 📧 Email: team@faraday.dev