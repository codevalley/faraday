# Faraday CLI Documentation

Welcome to the Faraday CLI documentation! This directory contains comprehensive guides for using the Faraday command-line interface.

## Documentation Index

### 📖 [CLI Usage Guide](CLI_USAGE.md)
Complete guide to using all Faraday CLI commands, including:
- Getting started and first-time setup
- All command groups (config, auth, thoughts)
- Output formats and global options
- Advanced usage patterns and scripting
- Troubleshooting common issues

### ⚙️ [Configuration Guide](CONFIGURATION.md)
Detailed configuration management documentation:
- Platform-specific configuration paths
- All configuration options and their meanings
- Configuration validation and error handling
- Environment-specific setups
- Security considerations

## Quick Reference

### Essential Commands

```bash
# Setup
faraday config set api.url http://localhost:8001
faraday auth login

# Daily usage
faraday thoughts add "Your thought here"
faraday thoughts search "search query"
faraday thoughts list

# Configuration
faraday config show
faraday config set key value
faraday config reset
```

### Global Options

```bash
--config PATH     # Use custom config file
--api-url URL     # Override API URL
--json           # JSON output format
--verbose        # Verbose output
```

## Getting Help

- **Command help**: `faraday --help` or `faraday <command> --help`
- **Configuration**: `faraday config --help`
- **Version info**: `faraday version`

## Additional Resources

- **Main README**: [../README.md](../README.md) - Project overview and installation
- **Contributing**: See main repository for contribution guidelines
- **Issues**: Report bugs and feature requests in the main repository

## Documentation Structure

```
docs/
├── README.md           # This file - documentation index
├── CLI_USAGE.md        # Complete CLI usage guide
└── CONFIGURATION.md    # Configuration management guide
```

Each guide is self-contained and can be read independently, though they cross-reference each other where relevant.