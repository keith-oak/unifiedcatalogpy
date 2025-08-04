---
applyTo: "**/test*.py"
---

# Test File Instructions

## Test Framework

- Use pytest as the primary testing framework
- Organize tests in a `tests/` directory structure
- Name test files with `test_` prefix or `_test` suffix
- Use descriptive test method names that explain what is being tested

## Test Structure

- Follow Arrange-Act-Assert pattern
- Use pytest fixtures for common setup and teardown
- Group related tests in test classes when appropriate
- Keep tests isolated and independent

## Mocking

- Mock external API calls using `unittest.mock` or `pytest-mock`
- Mock HTTP requests to Microsoft Purview API endpoints
- Create realistic mock responses based on actual Purview API responses
- Don't make real API calls in unit tests

## Test Coverage

- Aim for high test coverage (80%+) for business logic
- Test both success and error scenarios
- Include edge cases and boundary conditions
- Test authentication and authorization flows

## Assertions

- Use specific pytest assertions (`assert`, pytest.raises, etc.)
- Include meaningful assertion messages
- Test return values, exceptions, and side effects
- Verify mock calls and parameters when appropriate

## Test Data

- Use factory functions or fixtures for test data creation
- Create realistic test data that matches Purview entity structures
- Use parameterized tests for testing multiple scenarios
- Keep test data minimal but representative
