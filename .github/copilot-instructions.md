# GitHub Copilot Instructions for UnifiedCatalogPy

## Project Overview
UnifiedCatalogPy is an unofficial Python wrapper for Microsoft Purview Data Governance's Unified Catalog API. The library provides a simple interface for managing data governance elements including domains, glossary terms, data products, OKRs, and critical data elements.

> **Note**: This repository uses file-specific instructions in `.github/instructions/` for targeted guidance. This file contains general project-wide instructions.

## Code Style and Conventions
- Always use Python 3.9+ compatible syntax
- Follow PEP 8 style guidelines with snake_case for functions and variables
- Use type hints for all function parameters and return values when possible
- Use double quotes for strings consistently
- Include docstrings for all public methods and classes
- Keep line length under 88 characters (Black formatter standard)

## Project Structure
- `unifiedcatalogpy/` - Main package directory
  - `client.py` - Main UnifiedCatalogClient class
  - `api_client.py` - Low-level API client for HTTP requests
  - `models.py` - Data models and type definitions
  - `utils.py` - Utility functions
  - `__init__.py` - Package initialization

## Dependencies and Libraries
- Use `requests` for HTTP requests (already included)
- Authentication should use `azure-identity` library (user dependency)
- Prefer standard library modules when possible
- When adding new dependencies, update pyproject.toml accordingly

## API Design Patterns
- All client methods should follow the naming pattern: `create_*`, `get_*`, `update_*`, `delete_*`
- Return proper response objects or raise meaningful exceptions
- Use consistent parameter naming across similar methods
- Always include `governance_domain_id` parameter where applicable
- Handle HTTP errors gracefully with informative error messages

## Authentication and Security
- Never hardcode credentials or API keys
- Always use credential objects from azure-identity
- Respect Microsoft Purview's authentication requirements
- Include proper error handling for authentication failures

## Error Handling
- Raise specific exceptions for different error types
- Include helpful error messages that guide users to solutions
- Log important events and errors appropriately
- Handle network timeouts and connection errors gracefully

## Documentation
- All public methods must have comprehensive docstrings
- Include parameter types and descriptions
- Provide usage examples in docstrings when helpful
- Document any Microsoft Purview-specific concepts or limitations

## Testing Considerations
- Write code that can be easily unit tested
- Consider mocking HTTP requests in tests
- Include edge case handling
- Test authentication scenarios

## Microsoft Purview Specifics
- Use proper Purview entity IDs and object references
- Respect Purview's data governance concepts and terminology
- Handle Purview-specific status values (Draft, Active, etc.)
- Include proper owner object structures with Entra ID references
- Support rich text descriptions using HTML div tags when appropriate

## File Naming and Organization
- Always specify the full file path when suggesting code changes
- Keep related functionality grouped in appropriate modules
- Use descriptive variable names that reflect Purview concepts