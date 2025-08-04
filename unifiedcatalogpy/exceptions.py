"""
Custom exceptions for UnifiedCatalogPy.
"""


class UnifiedCatalogError(Exception):
    """Base exception class for UnifiedCatalogPy."""
    pass


class AuthenticationError(UnifiedCatalogError):
    """Raised when authentication fails."""
    pass


class APIError(UnifiedCatalogError):
    """Raised when the API returns an error response."""
    
    def __init__(self, message: str, status_code: int = None, response_data=None):
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(message)


class ValidationError(UnifiedCatalogError):
    """Raised when input validation fails."""
    pass


class EntityNotFoundError(APIError):
    """Raised when a requested entity is not found."""
    pass


class RelationshipError(UnifiedCatalogError):
    """Raised when relationship operations fail."""
    pass


class PermissionError(APIError):
    """Raised when the user lacks permissions for an operation."""
    pass