"""Configuration management for Faraday CLI."""

import toml
from pathlib import Path
from typing import Any, Optional, Dict
from pydantic import BaseModel


class CLIConfig(BaseModel):
    """Configuration model for CLI settings."""
    
    class APIConfig(BaseModel):
        url: str = "http://localhost:8001"
        timeout: int = 30
    
    class AuthConfig(BaseModel):
        auto_login: bool = True
        remember_token: bool = True
    
    class OutputConfig(BaseModel):
        colors: bool = True
        pager: str = "auto"
        max_results: int = 20
    
    class CacheConfig(BaseModel):
        enabled: bool = True
        max_size_mb: int = 100
        sync_interval: int = 300
    
    api: APIConfig = APIConfig()
    auth: AuthConfig = AuthConfig()
    output: OutputConfig = OutputConfig()
    cache: CacheConfig = CacheConfig()


class ConfigManager:
    """Manages CLI configuration using TOML files."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Optional path to config file. If None, uses default location.
        """
        if config_path:
            self.config_path = Path(config_path)
        else:
            # Default config location
            self.config_path = Path.home() / ".config" / "faraday" / "config.toml"
        
        self.config_dir = self.config_path.parent
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self._config_data = self._load_config()
        self.config = CLIConfig(**self._config_data)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return toml.load(f)
            except Exception as e:
                # If config is corrupted, create new one
                print(f"Warning: Could not load config file: {e}")
                return {}
        else:
            # Create default config
            default_config = CLIConfig()
            self._save_config(default_config.model_dump())
            return default_config.model_dump()
    
    def _save_config(self, config_data: Dict[str, Any]) -> None:
        """Save configuration to file."""
        with open(self.config_path, 'w') as f:
            toml.dump(config_data, f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation.
        
        Args:
            key: Configuration key in dot notation (e.g., 'api.url')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation.
        
        Args:
            key: Configuration key in dot notation (e.g., 'api.url')
            value: Value to set
        """
        keys = key.split('.')
        config_data = self._config_data.copy()
        
        # Navigate to the parent of the target key
        current = config_data
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Set the value
        current[keys[-1]] = value
        
        # Update internal state and save
        self._config_data = config_data
        self.config = CLIConfig(**config_data)
        self._save_config(config_data)
    
    def show(self) -> Dict[str, Any]:
        """Get all configuration values."""
        return self._config_data.copy()
    
    def reset(self) -> None:
        """Reset configuration to defaults."""
        default_config = CLIConfig()
        self._config_data = default_config.model_dump()
        self.config = default_config
        self._save_config(self._config_data)