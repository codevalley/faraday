# Faraday CLI Configuration Guide

This guide covers all aspects of configuring the Faraday CLI for optimal use.

## Overview

The Faraday CLI uses TOML configuration files to store settings. Configuration is managed through the `faraday config` command group and provides platform-specific defaults.

## Configuration File Location

The CLI automatically determines the appropriate configuration file location based on your operating system:

### Platform-Specific Paths

| Platform | Configuration Path |
|----------|-------------------|
| **Windows** | `%APPDATA%\faraday\config.toml` |
| **macOS** | `~/Library/Application Support/faraday/config.toml` |
| **Linux/Unix** | `~/.config/faraday/config.toml` |

### Custom Configuration Path

You can override the default location using the `--config` flag:

```bash
faraday --config /path/to/custom/config.toml <command>
```

## Configuration Commands

### View Configuration

```bash
# Show all configuration settings
faraday config show

# Show configuration in JSON format
faraday --json config show

# Get specific configuration value
faraday config get api.url
faraday config get output.colors

# Show configuration file path
faraday config path
```

### Modify Configuration

```bash
# Set string values
faraday config set api.url "http://localhost:8001"
faraday config set output.pager "less"

# Set boolean values
faraday config set output.colors true
faraday config set auth.auto_login false

# Set numeric values
faraday config set api.timeout 60
faraday config set cache.max_size_mb 200
```

### Reset Configuration

```bash
# Reset all settings to defaults (with confirmation)
faraday config reset
```

## Configuration Sections

### API Configuration (`[api]`)

Controls how the CLI connects to your Faraday server.

```toml
[api]
url = "http://localhost:8001"
timeout = 30
```

#### Settings

- **`api.url`** (string, default: `"http://localhost:8001"`)
  - The base URL of your Faraday server
  - Examples: `"https://my-faraday.com"`, `"http://192.168.1.100:8001"`

- **`api.timeout`** (integer, default: `30`)
  - Request timeout in seconds
  - Range: 1-300 seconds

#### Examples

```bash
# Configure for production server
faraday config set api.url "https://faraday.mycompany.com"

# Increase timeout for slow connections
faraday config set api.timeout 60

# Configure for local development
faraday config set api.url "http://localhost:8001"
```

### Authentication Configuration (`[auth]`)

Controls authentication behavior and token management.

```toml
[auth]
auto_login = true
remember_token = true
```

#### Settings

- **`auth.auto_login`** (boolean, default: `true`)
  - Automatically attempt login when authentication is required
  - When `false`, you must manually run `faraday auth login`

- **`auth.remember_token`** (boolean, default: `true`)
  - Store authentication tokens for reuse
  - When `false`, you'll need to login for each session

#### Examples

```bash
# Disable automatic login for security
faraday config set auth.auto_login false

# Don't store tokens (login each time)
faraday config set auth.remember_token false

# Enable convenient authentication
faraday config set auth.auto_login true
faraday config set auth.remember_token true
```

### Output Configuration (`[output]`)

Controls how the CLI displays information.

```toml
[output]
colors = true
pager = "auto"
max_results = 20
```

#### Settings

- **`output.colors`** (boolean, default: `true`)
  - Enable colored terminal output
  - Disable for scripting or terminals that don't support colors

- **`output.pager`** (string, default: `"auto"`)
  - Pager to use for long output
  - Options: `"auto"`, `"less"`, `"more"`, `"none"`
  - `"auto"` automatically detects available pager

- **`output.max_results`** (integer, default: `20`)
  - Maximum number of results to display in list commands
  - Range: 1-1000

#### Examples

```bash
# Disable colors for scripting
faraday config set output.colors false

# Use specific pager
faraday config set output.pager "less"

# Show more results by default
faraday config set output.max_results 50

# Disable paging entirely
faraday config set output.pager "none"
```

### Cache Configuration (`[cache]`)

Controls local caching behavior for improved performance.

```toml
[cache]
enabled = true
max_size_mb = 100
sync_interval = 300
```

#### Settings

- **`cache.enabled`** (boolean, default: `true`)
  - Enable local caching of API responses
  - Improves performance for repeated queries

- **`cache.max_size_mb`** (integer, default: `100`)
  - Maximum cache size in megabytes
  - Range: 10-1000 MB

- **`cache.sync_interval`** (integer, default: `300`)
  - Cache synchronization interval in seconds
  - How often to check for updates from server
  - Range: 60-3600 seconds (1 minute to 1 hour)

#### Examples

```bash
# Disable caching
faraday config set cache.enabled false

# Increase cache size for better performance
faraday config set cache.max_size_mb 500

# Sync more frequently
faraday config set cache.sync_interval 120

# Sync less frequently to reduce server load
faraday config set cache.sync_interval 600
```

## Configuration Validation

The CLI validates all configuration values using Pydantic models. Invalid values are rejected with helpful error messages.

### Common Validation Errors

```bash
# Invalid data type
$ faraday config set api.timeout "not_a_number"
💥 Invalid configuration: Invalid configuration value for 'api.timeout': 
   Input should be a valid integer

# Out of range value
$ faraday config set cache.max_size_mb 5000
💥 Invalid configuration: Invalid configuration value for 'cache.max_size_mb': 
   Value must be between 10 and 1000

# Invalid boolean value
$ faraday config set output.colors "maybe"
💥 Invalid configuration: Invalid configuration value for 'output.colors': 
   Input should be a valid boolean
```

### Valid Value Formats

| Type | Valid Examples | Invalid Examples |
|------|----------------|------------------|
| **String** | `"hello"`, `"http://example.com"` | (none - all strings accepted) |
| **Integer** | `30`, `100`, `0` | `"30"`, `3.14`, `"abc"` |
| **Boolean** | `true`, `false` | `"true"`, `1`, `0`, `"yes"` |

**Note**: The CLI automatically parses JSON values, so you can use JSON syntax:

```bash
# These are equivalent
faraday config set output.colors true
faraday config set output.colors "true"  # Parsed as JSON boolean

# These are equivalent  
faraday config set api.timeout 60
faraday config set api.timeout "60"      # Parsed as JSON number
```

## Environment-Specific Configurations

### Development Environment

```bash
# Local development setup
faraday config set api.url "http://localhost:8001"
faraday config set api.timeout 60
faraday config set output.max_results 50
faraday config set cache.sync_interval 120
```

### Production Environment

```bash
# Production setup
faraday config set api.url "https://faraday.mycompany.com"
faraday config set api.timeout 30
faraday config set auth.auto_login false
faraday config set cache.max_size_mb 200
```

### CI/CD Environment

```bash
# Scripting/automation setup
faraday config set output.colors false
faraday config set output.pager "none"
faraday config set auth.auto_login false
faraday config set cache.enabled false
```

## Configuration File Format

The configuration file uses TOML format. Here's a complete example:

```toml
# Faraday CLI Configuration File
# Generated automatically - you can edit manually if needed

[api]
# Faraday server URL
url = "http://localhost:8001"
# Request timeout in seconds
timeout = 30

[auth]
# Automatically login when needed
auto_login = true
# Remember authentication tokens
remember_token = true

[output]
# Enable colored output
colors = true
# Pager for long output (auto, less, more, none)
pager = "auto"
# Maximum results to show in lists
max_results = 20

[cache]
# Enable local caching
enabled = true
# Maximum cache size in MB
max_size_mb = 100
# Cache sync interval in seconds
sync_interval = 300
```

## Troubleshooting Configuration

### Configuration File Issues

```bash
# Check if config file exists and location
faraday config path

# View current configuration
faraday config show

# Reset corrupted configuration
faraday config reset
```

### Permission Issues

If you encounter permission errors:

1. **Check file permissions**:
   ```bash
   # On Unix-like systems
   ls -la "$(faraday config path | grep -o '/.*')"
   ```

2. **Fix permissions**:
   ```bash
   # Make config directory writable
   chmod 755 ~/.config/faraday/
   chmod 644 ~/.config/faraday/config.toml
   ```

3. **Use custom location**:
   ```bash
   # Use a writable location
   faraday --config ~/my-faraday-config.toml config show
   ```

### Network Configuration

For corporate environments or special network setups:

```bash
# Configure proxy (if your HTTP client supports it)
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# Use custom CA certificates
export REQUESTS_CA_BUNDLE=/path/to/ca-bundle.crt

# Increase timeout for slow networks
faraday config set api.timeout 120
```

## Advanced Configuration

### Multiple Configurations

You can maintain multiple configuration files for different environments:

```bash
# Development config
faraday --config ~/.config/faraday/dev.toml config show

# Production config  
faraday --config ~/.config/faraday/prod.toml config show

# Create environment-specific aliases
alias faraday-dev="faraday --config ~/.config/faraday/dev.toml"
alias faraday-prod="faraday --config ~/.config/faraday/prod.toml"
```

### Configuration Templates

Create template configurations for team sharing:

```toml
# team-template.toml
[api]
url = "https://faraday.ourcompany.com"
timeout = 45

[auth]
auto_login = true
remember_token = true

[output]
colors = true
pager = "less"
max_results = 25

[cache]
enabled = true
max_size_mb = 150
sync_interval = 300
```

Team members can copy and customize:

```bash
cp team-template.toml ~/.config/faraday/config.toml
faraday config set api.url "https://faraday-staging.ourcompany.com"
```

## Security Considerations

### Sensitive Information

- Configuration files may contain server URLs but not passwords
- Authentication tokens are stored separately in the auth directory
- Use appropriate file permissions (600 or 644) for config files

### Best Practices

1. **Don't commit config files** to version control
2. **Use environment variables** for sensitive settings in CI/CD
3. **Regularly rotate** authentication tokens
4. **Use HTTPS** for production API URLs
5. **Disable token storage** in shared environments

```bash
# Secure configuration for shared systems
faraday config set auth.remember_token false
faraday config set auth.auto_login false
```

This comprehensive configuration guide should help users understand and effectively use the Faraday CLI configuration system.