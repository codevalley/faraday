# Fish completion script for Faraday CLI
# Install by copying to ~/.config/fish/completions/faraday.fish

# Global options
complete -c faraday -l config -d "Path to custom configuration file" -r
complete -c faraday -l api-url -d "Override API server URL" -r
complete -c faraday -l json -d "Output results in JSON format"
complete -c faraday -l verbose -s v -d "Enable verbose output for debugging"
complete -c faraday -l no-interactive -d "Disable automatic interactive mode"
complete -c faraday -l help -s h -d "Show help message"

# Main commands
complete -c faraday -f -n "__fish_use_subcommand" -a "auth" -d "Authentication commands"
complete -c faraday -f -n "__fish_use_subcommand" -a "config" -d "Configuration management commands"
complete -c faraday -f -n "__fish_use_subcommand" -a "thoughts" -d "Thought management commands"
complete -c faraday -f -n "__fish_use_subcommand" -a "search" -d "Search thoughts using natural language queries"
complete -c faraday -f -n "__fish_use_subcommand" -a "sync" -d "Cache synchronization commands"
complete -c faraday -f -n "__fish_use_subcommand" -a "help" -d "Help and tutorial commands"
complete -c faraday -f -n "__fish_use_subcommand" -a "interactive" -d "Start interactive mode"
complete -c faraday -f -n "__fish_use_subcommand" -a "version" -d "Show version information"

# Auth subcommands
complete -c faraday -f -n "__fish_seen_subcommand_from auth" -a "login" -d "Login to Faraday server"
complete -c faraday -f -n "__fish_seen_subcommand_from auth" -a "logout" -d "Logout from Faraday server"
complete -c faraday -f -n "__fish_seen_subcommand_from auth" -a "status" -d "Show authentication status"

# Config subcommands
complete -c faraday -f -n "__fish_seen_subcommand_from config" -a "get" -d "Get a configuration value"
complete -c faraday -f -n "__fish_seen_subcommand_from config" -a "set" -d "Set a configuration value"
complete -c faraday -f -n "__fish_seen_subcommand_from config" -a "show" -d "Show all configuration values"
complete -c faraday -f -n "__fish_seen_subcommand_from config" -a "reset" -d "Reset configuration to defaults"
complete -c faraday -f -n "__fish_seen_subcommand_from config" -a "path" -d "Show the path to the configuration file"

# Config keys for get/set commands
complete -c faraday -f -n "__fish_seen_subcommand_from config; and __fish_seen_subcommand_from get set" -a "api.url" -d "Faraday server URL"
complete -c faraday -f -n "__fish_seen_subcommand_from config; and __fish_seen_subcommand_from get set" -a "api.timeout" -d "Request timeout in seconds"
complete -c faraday -f -n "__fish_seen_subcommand_from config; and __fish_seen_subcommand_from get set" -a "auth.auto_login" -d "Automatically login when needed"
complete -c faraday -f -n "__fish_seen_subcommand_from config; and __fish_seen_subcommand_from get set" -a "auth.remember_token" -d "Remember authentication tokens"
complete -c faraday -f -n "__fish_seen_subcommand_from config; and __fish_seen_subcommand_from get set" -a "output.colors" -d "Enable colored output"
complete -c faraday -f -n "__fish_seen_subcommand_from config; and __fish_seen_subcommand_from get set" -a "output.pager" -d "Pager for long output"
complete -c faraday -f -n "__fish_seen_subcommand_from config; and __fish_seen_subcommand_from get set" -a "output.max_results" -d "Maximum results to show in lists"
complete -c faraday -f -n "__fish_seen_subcommand_from config; and __fish_seen_subcommand_from get set" -a "cache.enabled" -d "Enable local caching"
complete -c faraday -f -n "__fish_seen_subcommand_from config; and __fish_seen_subcommand_from get set" -a "cache.max_size_mb" -d "Maximum cache size in MB"
complete -c faraday -f -n "__fish_seen_subcommand_from config; and __fish_seen_subcommand_from get set" -a "cache.sync_interval" -d "Cache sync interval in seconds"
complete -c faraday -f -n "__fish_seen_subcommand_from config; and __fish_seen_subcommand_from get set" -a "ui.auto_interactive" -d "Enable automatic interactive mode"

# Thoughts subcommands
complete -c faraday -f -n "__fish_seen_subcommand_from thoughts" -a "add" -d "Add a new thought"
complete -c faraday -f -n "__fish_seen_subcommand_from thoughts" -a "list" -d "List recent thoughts"
complete -c faraday -f -n "__fish_seen_subcommand_from thoughts" -a "show" -d "Show detailed information about a specific thought"
complete -c faraday -f -n "__fish_seen_subcommand_from thoughts" -a "delete" -d "Delete a thought by ID"

# Thoughts add options
complete -c faraday -n "__fish_seen_subcommand_from thoughts; and __fish_seen_subcommand_from add" -l mood -d "Mood associated with the thought" -r
complete -c faraday -n "__fish_seen_subcommand_from thoughts; and __fish_seen_subcommand_from add" -l tags -d "Comma-separated tags" -r
complete -c faraday -n "__fish_seen_subcommand_from thoughts; and __fish_seen_subcommand_from add" -l meta -d "Metadata in key=value format" -r

# Thoughts list options
complete -c faraday -n "__fish_seen_subcommand_from thoughts; and __fish_seen_subcommand_from list" -l limit -d "Maximum number of thoughts to show" -r
complete -c faraday -n "__fish_seen_subcommand_from thoughts; and __fish_seen_subcommand_from list" -l mood -d "Filter by mood" -r
complete -c faraday -n "__fish_seen_subcommand_from thoughts; and __fish_seen_subcommand_from list" -l tags -d "Filter by tags (comma-separated)" -r

# Search options
complete -c faraday -n "__fish_seen_subcommand_from search" -l limit -d "Maximum number of results to return" -r
complete -c faraday -n "__fish_seen_subcommand_from search" -l mood -d "Filter results by mood" -r
complete -c faraday -n "__fish_seen_subcommand_from search" -l tags -d "Filter results by tags (comma-separated)" -r
complete -c faraday -n "__fish_seen_subcommand_from search" -l since -d "Filter results since date" -r
complete -c faraday -n "__fish_seen_subcommand_from search" -l until -d "Filter results until date" -r
complete -c faraday -n "__fish_seen_subcommand_from search" -l min-score -d "Minimum relevance score (0.0-1.0)" -r
complete -c faraday -n "__fish_seen_subcommand_from search" -l sort -d "Sort results by" -xa "relevance date date-desc"

# Sync subcommands
complete -c faraday -f -n "__fish_seen_subcommand_from sync" -a "sync" -d "Synchronize with server"
complete -c faraday -f -n "__fish_seen_subcommand_from sync" -a "status" -d "Show sync status"

# Help subcommands
complete -c faraday -f -n "__fish_seen_subcommand_from help" -a "guide" -d "Show detailed help guides for specific topics"
complete -c faraday -f -n "__fish_seen_subcommand_from help" -a "tutorial" -d "Start an interactive tutorial for new users"
complete -c faraday -f -n "__fish_seen_subcommand_from help" -a "shortcuts" -d "Show keyboard shortcuts and quick commands"
complete -c faraday -f -n "__fish_seen_subcommand_from help" -a "workflows" -d "Show common workflows and usage patterns"

# Help guide topics
complete -c faraday -f -n "__fish_seen_subcommand_from help; and __fish_seen_subcommand_from guide" -a "getting-started" -d "First-time setup and basic usage"
complete -c faraday -f -n "__fish_seen_subcommand_from help; and __fish_seen_subcommand_from guide" -a "commands" -d "Complete command reference"
complete -c faraday -f -n "__fish_seen_subcommand_from help; and __fish_seen_subcommand_from guide" -a "interactive" -d "Interactive mode guide"
complete -c faraday -f -n "__fish_seen_subcommand_from help; and __fish_seen_subcommand_from guide" -a "configuration" -d "Configuration management"
complete -c faraday -f -n "__fish_seen_subcommand_from help; and __fish_seen_subcommand_from guide" -a "scripting" -d "Automation and scripting"
complete -c faraday -f -n "__fish_seen_subcommand_from help; and __fish_seen_subcommand_from guide" -a "troubleshooting" -d "Common issues and solutions"
complete -c faraday -f -n "__fish_seen_subcommand_from help; and __fish_seen_subcommand_from guide" -a "examples" -d "Real-world usage examples"

# Version options
complete -c faraday -n "__fish_seen_subcommand_from version" -l detailed -d "Show detailed version and system information"