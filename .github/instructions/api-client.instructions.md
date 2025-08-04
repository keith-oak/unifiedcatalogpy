---
applyTo: "**/api_client.py"
---

# API Client Instructions

## HTTP Requests

- Use the `requests` library for all HTTP operations
- Always include proper headers (Authorization, Content-Type, Accept)
- Set reasonable timeouts for all requests (default: 30 seconds)
- Handle connection errors, timeouts, and HTTP status codes gracefully

## Authentication

- Use Azure credential objects, never hardcode credentials
- Refresh tokens when necessary using azure-identity patterns
- Include proper error handling for authentication failures
- Support both user and service principal authentication

## Microsoft Purview Specifics

- Base URL format: `https://{account_id}-api.purview-service.microsoft.com`
- Always include API version in requests where required
- Use proper Purview entity IDs and references
- Handle Purview-specific error responses and status codes

## Response Handling

- Parse JSON responses with proper error handling
- Return structured data objects or raise meaningful exceptions
- Log important API interactions for debugging
- Handle pagination when supported by endpoints

## URL Construction

- Use proper URL encoding for parameters
- Build URLs programmatically, don't use string concatenation
- Validate required parameters before making requests
- Support query parameters for filtering and pagination

## Rate Limiting

- Implement retry logic with exponential backoff
- Respect any rate limiting headers from Purview API
- Use appropriate delays between bulk operations
