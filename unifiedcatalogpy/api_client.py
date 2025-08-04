"""API client module for making HTTP requests."""
from typing import Dict

import requests

from unifiedcatalogpy.models import Result


class ApiClient:
    """HTTP client for making requests to the Unified Catalog API."""
    def __init__(self, base_url: str, credential: any):
        self.base_url = base_url
        self.credential = credential
        self.resource_scope = "73c2949e-da2d-457a-9607-fcc665198967/.default"

    def request(
        self,
        http_method: str,
        endpoint: str,
        params: Dict = None,
        data: Dict = None,
    ) -> Result:
        """Make HTTP request to API endpoint."""
        full_url = self.base_url + endpoint
        token = self.credential.get_token(self.resource_scope).token
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
            raise Exception("Request failed") from e

        if response.status_code == 204:
            return Result(
                response.status_code, message=response.reason, data=[]
            )

        try:
            data_out = response.json()
        except requests.exceptions.JSONDecodeError:
            data_out = []

        if 299 >= response.status_code >= 200:
            return Result(
                response.status_code, message=response.reason, data=data_out
            )
        raise Exception(f"{response.status_code}: {response.reason}")

    def get(self, endpoint: str, params: Dict = None) -> Result:
        """Make GET request."""
        return self.request(
            http_method="GET", endpoint=endpoint, params=params
        )

    def post(
        self, endpoint: str, params: Dict = None, data: Dict = None
    ) -> Result:
        """Make POST request."""
        return self.request(
            http_method="POST", endpoint=endpoint, params=params, data=data
        )

    def put(
        self, endpoint: str, params: Dict = None, data: Dict = None
    ) -> Result:
        """Make PUT request."""
        return self.request(
            http_method="PUT", endpoint=endpoint, params=params, data=data
        )

    def delete(
        self, endpoint: str, params: Dict = None, data: Dict = None
    ) -> Result:
        """Make DELETE request."""
        return self.request(
            http_method="DELETE", endpoint=endpoint, params=params, data=data
        )
