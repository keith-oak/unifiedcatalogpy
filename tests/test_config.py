"""
Tests for configuration management.
"""

import pytest
import tempfile
import os
from pathlib import Path
import yaml
import json

from unifiedcatalogpy.config import (
    UnifiedCatalogConfig, ConfigManager, create_sample_config_file
)
from unifiedcatalogpy.exceptions import ValidationError


class TestUnifiedCatalogConfig:
    """Test UnifiedCatalogConfig class."""
    
    def test_default_config(self):
        """Test default configuration creation."""
        config = UnifiedCatalogConfig(account_id="test-account")
        assert config.account_id == "test-account"
        assert config.enable_retry is True
        assert config.max_retry_attempts == 3
        assert config.default_page_size == 100
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Valid config
        config = UnifiedCatalogConfig(account_id="test-account")
        config.validate()  # Should not raise
        
        # Invalid account_id
        with pytest.raises(ValidationError):
            config = UnifiedCatalogConfig(account_id="")
            config.validate()
        
        # Invalid page size
        with pytest.raises(ValidationError):
            config = UnifiedCatalogConfig(account_id="test", default_page_size=0)
            config.validate()
        
        # Page size exceeds max
        with pytest.raises(ValidationError):
            config = UnifiedCatalogConfig(
                account_id="test", 
                default_page_size=2000, 
                max_page_size=1000
            )
            config.validate()
    
    def test_retry_config_creation(self):
        """Test retry config creation."""
        config = UnifiedCatalogConfig(
            account_id="test",
            max_retry_attempts=5,
            retry_base_delay=2.0,
            retry_max_delay=120.0
        )
        
        retry_config = config.get_retry_config()
        assert retry_config.max_attempts == 5
        assert retry_config.base_delay == 2.0
        assert retry_config.max_delay == 120.0


class TestConfigManager:
    """Test ConfigManager class."""
    
    def test_from_dict(self):
        """Test config creation from dictionary."""
        data = {
            "account_id": "test-account",
            "tenant_id": "test-tenant",
            "enable_retry": False,
            "max_retry_attempts": 5
        }
        
        config = ConfigManager._create_config_from_dict(data)
        assert config.account_id == "test-account"
        assert config.tenant_id == "test-tenant"
        assert config.enable_retry is False
        assert config.max_retry_attempts == 5
    
    def test_from_yaml_file(self):
        """Test config loading from YAML file."""
        config_data = {
            "account_id": "yaml-test-account",
            "tenant_id": "yaml-test-tenant",
            "enable_retry": True,
            "max_retry_attempts": 4
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = ConfigManager.from_file(temp_path)
            assert config.account_id == "yaml-test-account"
            assert config.tenant_id == "yaml-test-tenant"
            assert config.enable_retry is True
            assert config.max_retry_attempts == 4
        finally:
            os.unlink(temp_path)
    
    def test_from_json_file(self):
        """Test config loading from JSON file."""
        config_data = {
            "account_id": "json-test-account",
            "tenant_id": "json-test-tenant",
            "enable_retry": False
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name
        
        try:
            config = ConfigManager.from_file(temp_path)
            assert config.account_id == "json-test-account"
            assert config.tenant_id == "json-test-tenant"
            assert config.enable_retry is False
        finally:
            os.unlink(temp_path)
    
    def test_from_env(self):
        """Test config loading from environment variables."""
        env_vars = {
            "PURVIEW_ACCOUNT_ID": "env-test-account",
            "AZURE_TENANT_ID": "env-test-tenant",
            "PURVIEW_ENABLE_RETRY": "false",
            "PURVIEW_MAX_RETRY_ATTEMPTS": "2"
        }
        
        # Set environment variables
        original_values = {}
        for key, value in env_vars.items():
            original_values[key] = os.environ.get(key)
            os.environ[key] = value
        
        try:
            config = ConfigManager.from_env()
            assert config.account_id == "env-test-account"
            assert config.tenant_id == "env-test-tenant"
            assert config.enable_retry is False
            assert config.max_retry_attempts == 2
        finally:
            # Restore original environment
            for key, original_value in original_values.items():
                if original_value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = original_value
    
    def test_from_connection_string(self):
        """Test config creation from connection string."""
        conn_str = "AccountId=conn-test-account;TenantId=conn-test-tenant;ClientId=test-client"
        
        config = ConfigManager.from_connection_string(conn_str)
        assert config.account_id == "conn-test-account"
        assert config.tenant_id == "conn-test-tenant"
        assert config.client_id == "test-client"
    
    def test_invalid_file_format(self):
        """Test handling of invalid file format."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("invalid content")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError, match="Unsupported configuration file format"):
                ConfigManager.from_file(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_file_not_found(self):
        """Test handling of missing configuration file."""
        with pytest.raises(FileNotFoundError):
            ConfigManager.from_file("nonexistent-config.yaml")


def test_create_sample_config_file():
    """Test sample config file creation."""
    with tempfile.TemporaryDirectory() as temp_dir:
        config_path = Path(temp_dir) / "test_config.yaml"
        
        create_sample_config_file(config_path)
        
        assert config_path.exists()
        
        # Verify the sample config can be loaded
        config = ConfigManager.from_file(config_path)
        assert config.account_id == "your-purview-account-id"  # placeholder value
        assert config.enable_retry is True