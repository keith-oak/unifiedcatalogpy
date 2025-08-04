import requests
from typing import Dict, Optional
from unifiedcatalogpy.models import Result, PaginatedResult, PaginationOptions
from unifiedcatalogpy.exceptions import APIError, AuthenticationError
from unifiedcatalogpy.retry import retry_on_failure, RetryConfig, CircuitBreaker


class ApiClient:
    def __init__(self, base_url: str, credential: any, retry_config: Optional[RetryConfig] = None, enable_circuit_breaker: bool = True):
        self.base_url = base_url
        self.credential = credential
        self.resource_scope = "73c2949e-da2d-457a-9607-fcc665198967/.default"
        self.retry_config = retry_config or RetryConfig()
        
        # Set up circuit breaker if enabled
        self.circuit_breaker = CircuitBreaker() if enable_circuit_breaker else None

    def request(
        self, http_method: str, endpoint: str, params: Dict = None, data: Dict = None
    ) -> Result:
        """Make HTTP request with retry and circuit breaker protection."""
        # Apply circuit breaker if enabled
        if self.circuit_breaker:
            return self.circuit_breaker.call(self._request_with_retry, http_method, endpoint, params, data)
        else:
            return self._request_with_retry(http_method, endpoint, params, data)
    
    @retry_on_failure()
    def _request_with_retry(
        self, http_method: str, endpoint: str, params: Dict = None, data: Dict = None
    ) -> Result:
        """Internal method that handles the actual HTTP request with retry logic."""
        full_url = self.base_url + endpoint
        
        try:
            token = self.credential.get_token(self.resource_scope).token
        except Exception as e:
            raise AuthenticationError("Failed to obtain authentication token") from e
        
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.request(
                method=http_method,
                url=full_url,
                headers=headers,
                params=params,
                json=data,
            )
        except requests.exceptions.RequestException as e:
            raise APIError("HTTP request failed") from e

        if response.status_code == 204:
            return Result(response.status_code, message=response.reason, data=[])

        try:
            data_out = response.json()
        except requests.exceptions.JSONDecodeError:
            data_out = []

        if 299 >= response.status_code >= 200:
            return Result(response.status_code, message=response.reason, data=data_out)
        
        # Handle specific error cases
        if response.status_code == 401:
            raise AuthenticationError(f"Authentication failed: {response.reason}")
        elif response.status_code == 403:
            raise APIError(f"Permission denied: {response.reason}", response.status_code, data_out)
        elif response.status_code == 404:
            raise APIError(f"Resource not found: {response.reason}", response.status_code, data_out)
        else:
            raise APIError(f"API request failed: {response.status_code} {response.reason}", response.status_code, data_out)

    def get(self, endpoint: str, params: Dict = None) -> Result:
        return self.request(http_method="GET", endpoint=endpoint, params=params)

    def post(self, endpoint: str, params: Dict = None, data: Dict = None) -> Result:
        return self.request(
            http_method="POST", endpoint=endpoint, params=params, data=data
        )

    def put(self, endpoint: str, params: Dict = None, data: Dict = None) -> Result:
        return self.request(
            http_method="PUT", endpoint=endpoint, params=params, data=data
        )

    def delete(self, endpoint: str, params: Dict = None, data: Dict = None) -> Result:
        return self.request(
            http_method="DELETE", endpoint=endpoint, params=params, data=data
        )

    def get_paginated(self, endpoint: str, pagination: Optional[PaginationOptions] = None, params: Dict = None) -> PaginatedResult:
        """
        Make a paginated GET request.
        
        :param endpoint: The API endpoint
        :param pagination: Pagination options
        :param params: Additional query parameters
        :return: PaginatedResult with items and pagination metadata
        """
        if pagination is None:
            pagination = PaginationOptions()
        
        # Merge pagination params with existing params
        all_params = params.copy() if params else {}
        all_params['$top'] = pagination.page_size
        
        if pagination.continuation_token:
            all_params['$skiptoken'] = pagination.continuation_token
        
        response = self.get(endpoint, params=all_params)
        
        # Extract pagination metadata from response
        items = response.data.get('value', []) if isinstance(response.data, dict) else response.data
        
        # Check for pagination metadata (common patterns in Microsoft APIs)
        continuation_token = None
        has_more = False
        total_count = None
        
        if isinstance(response.data, dict):
            # Try different common pagination metadata patterns
            continuation_token = response.data.get('@odata.nextLink') or response.data.get('continuationToken')
            total_count = response.data.get('@odata.count') or response.data.get('totalCount')
            has_more = continuation_token is not None or len(items) == pagination.page_size
        
        return PaginatedResult(
            items=items,
            total_count=total_count,
            page_size=pagination.page_size,
            continuation_token=continuation_token,
            has_more=has_more
        )
