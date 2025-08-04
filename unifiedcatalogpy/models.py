"""Data models for API responses."""
from typing import Dict, List


class Result:
    """Represents an API response result."""
    def __init__(
        self, status_code: int, message: str = "", data: List[Dict] = None
    ):
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []
