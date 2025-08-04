"""
Tests for models and response models.
"""

import pytest
from datetime import datetime

from unifiedcatalogpy.models import Result, PaginatedResult, PaginationOptions
from unifiedcatalogpy.response_models import (
    GovernanceDomain, Term, DataProduct, Contact, Resource,
    EntityStatus, GovernanceDomainType, DataProductType
)


class TestPaginationOptions:
    """Test PaginationOptions class."""
    
    def test_default_options(self):
        """Test default pagination options."""
        options = PaginationOptions()
        assert options.page_size == 100
        assert options.continuation_token is None
    
    def test_custom_options(self):
        """Test custom pagination options."""
        options = PaginationOptions(page_size=50, continuation_token="token123")
        assert options.page_size == 50
        assert options.continuation_token == "token123"
    
    def test_validation(self):
        """Test pagination options validation."""
        # Valid options
        PaginationOptions(page_size=1)  # Should not raise
        PaginationOptions(page_size=1000)  # Should not raise
        
        # Invalid options
        with pytest.raises(ValueError):
            PaginationOptions(page_size=0)
        
        with pytest.raises(ValueError):
            PaginationOptions(page_size=-1)
        
        with pytest.raises(ValueError):
            PaginationOptions(page_size=1001)


class TestPaginatedResult:
    """Test PaginatedResult class."""
    
    def test_basic_properties(self):
        """Test basic paginated result properties."""
        items = [{"id": "1"}, {"id": "2"}]
        result = PaginatedResult(
            items=items,
            total_count=100,
            page_size=50,
            continuation_token="next_token",
            has_more=True
        )
        
        assert result.items == items
        assert result.count == 2
        assert result.total_count == 100
        assert result.page_size == 50
        assert result.continuation_token == "next_token"
        assert result.has_more is True
    
    def test_empty_result(self):
        """Test empty paginated result."""
        result = PaginatedResult(items=[])
        assert result.count == 0
        assert result.has_more is False
        assert result.continuation_token is None


class TestResponseModels:
    """Test response model classes."""
    
    def test_contact_from_dict(self):
        """Test Contact model creation from dictionary."""
        data = {"id": "user123", "description": "Data Owner"}
        contact = Contact.from_dict(data)
        
        assert contact.id == "user123"
        assert contact.description == "Data Owner"
    
    def test_resource_from_dict(self):
        """Test Resource model creation from dictionary."""
        data = {"name": "Documentation", "url": "https://example.com/docs"}
        resource = Resource.from_dict(data)
        
        assert resource.name == "Documentation"
        assert resource.url == "https://example.com/docs"
    
    def test_governance_domain_from_dict(self):
        """Test GovernanceDomain model creation from dictionary."""
        data = {
            "id": "domain123",
            "name": "Test Domain",
            "description": "A test governance domain",
            "type": "FunctionalUnit",
            "status": "Draft",
            "parent_id": "parent123",
            "contacts": {
                "owner": [
                    {"id": "user123", "description": "Domain Owner"}
                ]
            },
            "createdAt": "2024-01-01T00:00:00Z",
            "updatedAt": "2024-01-02T00:00:00Z"
        }
        
        domain = GovernanceDomain.from_dict(data)
        
        assert domain.id == "domain123"
        assert domain.name == "Test Domain"
        assert domain.description == "A test governance domain"
        assert domain.type == GovernanceDomainType.FUNCTIONAL_UNIT
        assert domain.status == EntityStatus.DRAFT
        assert domain.parent_id == "parent123"
        assert len(domain.owners) == 1
        assert domain.owners[0].id == "user123"
        assert domain.owners[0].description == "Domain Owner"
        assert isinstance(domain.created_at, datetime)
        assert isinstance(domain.updated_at, datetime)
    
    def test_term_from_dict(self):
        """Test Term model creation from dictionary."""
        data = {
            "id": "term123",
            "name": "Test Term",
            "description": "A test term",
            "status": "Published",
            "domain": "domain123",
            "parent_id": None,
            "contacts": {
                "owner": [{"id": "user123"}]
            },
            "acronyms": ["TT", "TEST"],
            "resources": [
                {"name": "Wiki", "url": "https://wiki.example.com"}
            ]
        }
        
        term = Term.from_dict(data)
        
        assert term.id == "term123"
        assert term.name == "Test Term"
        assert term.description == "A test term"
        assert term.status == EntityStatus.PUBLISHED
        assert term.domain_id == "domain123"
        assert term.parent_id is None
        assert len(term.owners) == 1
        assert term.owners[0].id == "user123"
        assert term.acronyms == ["TT", "TEST"]
        assert len(term.resources) == 1
        assert term.resources[0].name == "Wiki"
    
    def test_data_product_from_dict(self):
        """Test DataProduct model creation from dictionary."""
        data = {
            "id": "dp123",
            "name": "Test Data Product",
            "description": "A test data product",
            "type": "Dataset",
            "status": "Draft",
            "domain": "domain123",
            "businessUse": "Analytics and reporting",
            "contacts": {
                "owner": [{"id": "user123", "description": "Product Owner"}]
            },
            "audience": ["Analysts", "Data Scientists"],
            "termsOfUse": ["Internal use only"],
            "documentation": ["User guide available"],
            "updateFrequency": "Weekly",
            "endorsed": True
        }
        
        product = DataProduct.from_dict(data)
        
        assert product.id == "dp123"
        assert product.name == "Test Data Product"
        assert product.type == DataProductType.DATASET
        assert product.status == EntityStatus.DRAFT
        assert product.domain_id == "domain123"
        assert product.business_use == "Analytics and reporting"
        assert len(product.owners) == 1
        assert product.owners[0].description == "Product Owner"
        assert product.audience == ["Analysts", "Data Scientists"]
        assert product.terms_of_use == ["Internal use only"]
        assert product.endorsed is True
    
    def test_datetime_parsing(self):
        """Test datetime parsing in models."""
        # Test valid ISO datetime
        data = {
            "id": "test",
            "name": "Test",
            "description": "Test",
            "type": "FunctionalUnit",
            "status": "Draft",
            "createdAt": "2024-01-01T12:30:45Z"
        }
        
        domain = GovernanceDomain.from_dict(data)
        assert isinstance(domain.created_at, datetime)
        assert domain.created_at.year == 2024
        assert domain.created_at.month == 1
        assert domain.created_at.day == 1
        
        # Test invalid datetime
        data["createdAt"] = "invalid-date"
        domain = GovernanceDomain.from_dict(data)
        assert domain.created_at is None
        
        # Test None datetime
        data["createdAt"] = None
        domain = GovernanceDomain.from_dict(data)
        assert domain.created_at is None


class TestResult:
    """Test Result class."""
    
    def test_basic_result(self):
        """Test basic result creation."""
        result = Result(200, "OK", [{"id": "1"}])
        
        assert result.status_code == 200
        assert result.message == "OK"
        assert result.data == [{"id": "1"}]
    
    def test_result_defaults(self):
        """Test result with default values."""
        result = Result(404)
        
        assert result.status_code == 404
        assert result.message == ""
        assert result.data == []