"""
Pytest configuration and fixtures for UnifiedCatalogPy tests.
"""

import pytest
from unittest.mock import Mock
from unifiedcatalogpy.config import UnifiedCatalogConfig


@pytest.fixture
def sample_config():
    """Fixture providing a sample configuration for testing."""
    return UnifiedCatalogConfig(
        account_id="test-account-id",
        tenant_id="test-tenant-id",
        client_id="test-client-id",
        client_secret="test-secret",
        enable_retry=True,
        max_retry_attempts=3,
        default_page_size=50
    )


@pytest.fixture
def mock_credential():
    """Fixture providing a mock Azure credential."""
    mock_cred = Mock()
    mock_token = Mock()
    mock_token.token = "mock-access-token"
    mock_cred.get_token.return_value = mock_token
    return mock_cred


@pytest.fixture
def sample_governance_domain_data():
    """Fixture providing sample governance domain data."""
    return {
        "id": "domain-123",
        "name": "Test Domain",
        "description": "A test governance domain",
        "type": "FunctionalUnit",
        "status": "Draft",
        "parent_id": None,
        "contacts": {
            "owner": [
                {"id": "user-123", "description": "Domain Owner"}
            ]
        },
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-02T00:00:00Z"
    }


@pytest.fixture
def sample_term_data():
    """Fixture providing sample term data."""
    return {
        "id": "term-123",
        "name": "Test Term",
        "description": "A test glossary term",
        "status": "Published",
        "domain": "domain-123",
        "parent_id": None,
        "contacts": {
            "owner": [{"id": "user-123", "description": "Term Owner"}]
        },
        "acronyms": ["TT", "TEST"],
        "resources": [
            {"name": "Documentation", "url": "https://example.com/docs"}
        ],
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-02T00:00:00Z"
    }


@pytest.fixture
def sample_paginated_response():
    """Fixture providing sample paginated API response."""
    return {
        "value": [
            {"id": "1", "name": "Item 1"},
            {"id": "2", "name": "Item 2"},
            {"id": "3", "name": "Item 3"}
        ],
        "@odata.nextLink": "next-page-token",
        "@odata.count": 100
    }