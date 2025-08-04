---
applyTo: "**/*.py"
---

# Python Code Instructions

## Code Style

- Use Python 3.9+ features and syntax
- Follow PEP 8 with 88-character line limit (Black formatter)
- Use snake_case for functions, variables, and module names
- Use PascalCase for class names
- Use UPPER_CASE for constants
- Always use double quotes for strings

## Type Hints

- Include type hints for all function parameters and return values
- Use `from __future__ import annotations` for forward references
- Import types from `typing` module when needed
- Use `Optional[T]` for nullable parameters

## Error Handling

- Raise specific exceptions with descriptive messages
- Use custom exception classes when appropriate
- Handle HTTP errors with meaningful user-facing messages
- Include error context (status codes, response details)

## Documentation

- Write comprehensive docstrings for all public methods
- Use Google-style docstrings format
- Include parameter descriptions and return value details
- Add usage examples for complex methods

## Imports

- Group imports: standard library, third-party, local imports
- Use absolute imports within the package
- Sort imports alphabetically within groups
