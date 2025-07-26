# Faraday CLI

Command-line interface for the Faraday Personal Semantic Engine.

## Installation

```bash
pip install faraday-cli
```

## Usage

```bash
# Login to your Faraday instance
faraday login

# Add a new thought
faraday add "Had an amazing coffee meeting with Sarah today"

# Search your thoughts
faraday search "coffee meetings"

# List recent thoughts
faraday list

# Interactive mode
faraday interactive
```

## Configuration

The CLI can be configured using:

```bash
faraday config set api-url http://localhost:8001
faraday config show
```

## Development

```bash
# Install dependencies
poetry install

# Run CLI in development
poetry run faraday --help

# Run tests
poetry run pytest

# Format code
poetry run black .
poetry run isort .
```