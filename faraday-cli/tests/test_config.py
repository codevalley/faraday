"""Tests for configuration management."""

import pytest
import tempfile
from pathlib import Path

from faraday_cli.config import ConfigManager, CLIConfig


def test_config_manager_initialization():
    """Test ConfigManager initialization with default values."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "test_config.toml"
        config_manager = ConfigManager(str(config_path))
        
        assert config_manager.config_path == config_path
        assert isinstance(config_manager.config, CLIConfig)
        assert config_manager.config.api.url == "http://localhost:8001"


def test_config_get_set():
    """Test getting and setting configuration values."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "test_config.toml"
        config_manager = ConfigManager(str(config_path))
        
        # Test setting and getting a value
        config_manager.set("api.url", "http://example.com:8080")
        assert config_manager.get("api.url") == "http://example.com:8080"
        
        # Test getting non-existent key with default
        assert config_manager.get("nonexistent.key", "default") == "default"


def test_config_persistence():
    """Test that configuration persists across instances."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "test_config.toml"
        
        # Create first instance and set a value
        config1 = ConfigManager(str(config_path))
        config1.set("api.url", "http://persistent.com")
        
        # Create second instance and verify value persists
        config2 = ConfigManager(str(config_path))
        assert config2.get("api.url") == "http://persistent.com"


def test_config_reset():
    """Test configuration reset functionality."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "test_config.toml"
        config_manager = ConfigManager(str(config_path))
        
        # Change a value
        config_manager.set("api.url", "http://changed.com")
        assert config_manager.get("api.url") == "http://changed.com"
        
        # Reset and verify default is restored
        config_manager.reset()
        assert config_manager.get("api.url") == "http://localhost:8001"


def test_config_show():
    """Test showing all configuration values."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "test_config.toml"
        config_manager = ConfigManager(str(config_path))
        
        all_config = config_manager.show()
        assert isinstance(all_config, dict)
        assert "api" in all_config
        assert "auth" in all_config
        assert "output" in all_config
        assert "cache" in all_config