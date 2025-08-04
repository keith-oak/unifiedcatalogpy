"""
Configuration management for UnifiedCatalogPy.
"""

import os
import yaml
import json
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path
from azure.identity import DefaultAzureCredential, ClientSecretCredential, InteractiveBrowserCredential
from .retry import RetryConfig
from .exceptions import ValidationError


@dataclass
class UnifiedCatalogConfig:
    """Configuration for UnifiedCatalogPy client."""
    
    # Required settings
    account_id: str
    
    # Optional authentication settings
    tenant_id: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    
    # API settings
    base_url: Optional[str] = None
    resource_scope: str = "73c2949e-da2d-457a-9607-fcc665198967/.default"
    
    # Reliability settings
    enable_retry: bool = True
    max_retry_attempts: int = 3
    retry_base_delay: float = 1.0
    retry_max_delay: float = 60.0
    enable_circuit_breaker: bool = True
    
    # Pagination settings
    default_page_size: int = 100
    max_page_size: int = 1000
    
    # Logging settings
    log_level: str = "INFO"
    log_requests: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return asdict(self)
    
    def get_retry_config(self) -> RetryConfig:
        """Get RetryConfig instance from current settings."""
        return RetryConfig(
            max_attempts=self.max_retry_attempts,
            base_delay=self.retry_base_delay,
            max_delay=self.retry_max_delay
        )
    
    def get_credential(self):
        """Get appropriate Azure credential based on configuration."""
        if self.client_id and self.client_secret and self.tenant_id:
            # Service principal authentication
            return ClientSecretCredential(
                tenant_id=self.tenant_id,
                client_id=self.client_id,
                client_secret=self.client_secret
            )
        elif self.tenant_id:
            # Interactive browser authentication with specific tenant
            return InteractiveBrowserCredential(tenant_id=self.tenant_id)
        else:
            # Default credential chain
            return DefaultAzureCredential()
    
    def validate(self):
        """Validate configuration settings."""
        if not self.account_id:
            raise ValidationError("account_id is required")
        
        if self.default_page_size <= 0:
            raise ValidationError("default_page_size must be positive")
        
        if self.default_page_size > self.max_page_size:
            raise ValidationError("default_page_size cannot exceed max_page_size")
        
        if self.max_retry_attempts < 0:
            raise ValidationError("max_retry_attempts cannot be negative")
        
        if self.retry_base_delay < 0:
            raise ValidationError("retry_base_delay cannot be negative")


class ConfigManager:
    """Manages configuration loading and validation."""
    
    DEFAULT_CONFIG_PATHS = [
        "purview_config.yaml",
        "purview_config.yml",
        "purview_config.json",
        "~/.purview/config.yaml",
        "~/.purview/config.yml",
        "~/.purview/config.json",
    ]
    
    ENV_VAR_MAPPING = {
        "account_id": "PURVIEW_ACCOUNT_ID",
        "tenant_id": "AZURE_TENANT_ID",
        "client_id": "AZURE_CLIENT_ID",
        "client_secret": "AZURE_CLIENT_SECRET",
        "base_url": "PURVIEW_BASE_URL",
        "resource_scope": "PURVIEW_RESOURCE_SCOPE",
        "enable_retry": "PURVIEW_ENABLE_RETRY",
        "max_retry_attempts": "PURVIEW_MAX_RETRY_ATTEMPTS",
        "retry_base_delay": "PURVIEW_RETRY_BASE_DELAY",
        "retry_max_delay": "PURVIEW_RETRY_MAX_DELAY",
        "enable_circuit_breaker": "PURVIEW_ENABLE_CIRCUIT_BREAKER",
        "default_page_size": "PURVIEW_DEFAULT_PAGE_SIZE",
        "max_page_size": "PURVIEW_MAX_PAGE_SIZE",
        "log_level": "PURVIEW_LOG_LEVEL",
        "log_requests": "PURVIEW_LOG_REQUESTS",
    }
    
    @classmethod
    def from_file(cls, config_path: Union[str, Path]) -> UnifiedCatalogConfig:
        """
        Load configuration from file.
        
        :param config_path: Path to configuration file
        :return: UnifiedCatalogConfig instance
        """
        config_path = Path(config_path).expanduser()
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            if config_path.suffix.lower() in ['.yaml', '.yml']:
                data = yaml.safe_load(f)
            elif config_path.suffix.lower() == '.json':
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported configuration file format: {config_path.suffix}")
        
        return cls._create_config_from_dict(data)
    
    @classmethod
    def from_env(cls) -> UnifiedCatalogConfig:
        """
        Load configuration from environment variables.
        
        :return: UnifiedCatalogConfig instance
        """
        data = {}
        
        for config_key, env_var in cls.ENV_VAR_MAPPING.items():
            value = os.getenv(env_var)
            if value is not None:
                # Type conversion based on expected type
                if config_key in ['enable_retry', 'enable_circuit_breaker', 'log_requests']:
                    value = value.lower() in ('true', '1', 'yes', 'on')
                elif config_key in ['max_retry_attempts', 'default_page_size', 'max_page_size']:
                    value = int(value)
                elif config_key in ['retry_base_delay', 'retry_max_delay']:
                    value = float(value)
                
                data[config_key] = value
        
        return cls._create_config_from_dict(data)
    
    @classmethod
    def find_config_file(cls) -> Optional[Path]:
        """
        Find configuration file in default locations.
        
        :return: Path to config file if found, None otherwise
        """
        for config_path in cls.DEFAULT_CONFIG_PATHS:
            path = Path(config_path).expanduser()
            if path.exists():
                return path
        return None
    
    @classmethod
    def load_default(cls) -> UnifiedCatalogConfig:
        """
        Load configuration using default strategy:
        1. Look for config file in default locations
        2. Fall back to environment variables
        3. Use defaults for missing values
        
        :return: UnifiedCatalogConfig instance
        """
        config_data = {}
        
        # Try to load from file first
        config_file = cls.find_config_file()
        if config_file:
            try:
                file_config = cls.from_file(config_file)
                config_data.update(file_config.to_dict())
            except Exception:
                pass  # Ignore file loading errors, fall back to env vars
        
        # Override with environment variables
        env_config = cls.from_env()
        config_data.update({k: v for k, v in env_config.to_dict().items() if v is not None})
        
        return cls._create_config_from_dict(config_data)
    
    @classmethod
    def from_connection_string(cls, connection_string: str) -> UnifiedCatalogConfig:
        """
        Parse configuration from connection string.
        
        Format: "AccountId=<id>;TenantId=<tenant>;ClientId=<client>;ClientSecret=<secret>"
        
        :param connection_string: Connection string
        :return: UnifiedCatalogConfig instance
        """
        if not connection_string:
            raise ValidationError("Connection string cannot be empty")
        
        parts = connection_string.split(';')
        data = {}
        
        for part in parts:
            if '=' not in part:
                continue
            key, value = part.split('=', 1)
            key = key.strip().lower()
            value = value.strip()
            
            # Map connection string keys to config keys
            key_mapping = {
                'accountid': 'account_id',
                'tenantid': 'tenant_id',
                'clientid': 'client_id',
                'clientsecret': 'client_secret',
                'baseurl': 'base_url',
            }
            
            config_key = key_mapping.get(key)
            if config_key:
                data[config_key] = value
        
        return cls._create_config_from_dict(data)
    
    @classmethod
    def _create_config_from_dict(cls, data: Dict[str, Any]) -> UnifiedCatalogConfig:
        """Create config instance from dictionary, handling missing values."""
        # Filter out None values and unknown keys
        valid_keys = {f.name for f in UnifiedCatalogConfig.__dataclass_fields__.values()}
        filtered_data = {k: v for k, v in data.items() if k in valid_keys and v is not None}
        
        config = UnifiedCatalogConfig(**filtered_data)
        config.validate()
        return config


def create_sample_config_file(path: Union[str, Path] = "purview_config.yaml"):
    """
    Create a sample configuration file.
    
    :param path: Path where to create the sample config file
    """
    path = Path(path)
    
    sample_config = {
        "account_id": "your-purview-account-id",
        "tenant_id": "your-azure-tenant-id",
        "client_id": "your-service-principal-client-id",
        "client_secret": "your-service-principal-secret",
        "enable_retry": True,
        "max_retry_attempts": 3,
        "retry_base_delay": 1.0,
        "retry_max_delay": 60.0,
        "enable_circuit_breaker": True,
        "default_page_size": 100,
        "max_page_size": 1000,
        "log_level": "INFO",
        "log_requests": False,
    }
    
    with open(path, 'w') as f:
        yaml.dump(sample_config, f, default_flow_style=False, indent=2)
    
    # Configuration file created at: {path}