import requests
from typing import Dict
from unifiedcatalogpy.models import Result
from unifiedcatalogpy.exceptions import APIError, AuthenticationError


class ApiClient:
    def __init__(self, base_url: str, credential: any):
        self.base_url = base_url
        self.credential = credential
        self.resource_scope = "73c2949e-da2d-457a-9607-fcc665198967/.default"

    def request(
        self, http_method: str, endpoint: str, params: Dict = None, data: Dict = None
    ) -> Result:
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
