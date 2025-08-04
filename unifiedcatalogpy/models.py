from typing import List, Dict, Optional
from dataclasses import dataclass


class Result:
    def __init__(self, status_code: int, message: str = "", data: List[Dict] = None):
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else []


@dataclass
class PaginatedResult:
    """Represents a paginated API response."""
    items: List[Dict]
    total_count: Optional[int] = None
    page_size: int = 100
    continuation_token: Optional[str] = None
    has_more: bool = False
    
    @property
    def count(self) -> int:
        """Get the number of items in current page."""
        return len(self.items)


@dataclass
class PaginationOptions:
    """Options for paginated requests."""
    page_size: int = 100
    continuation_token: Optional[str] = None
    
    def __post_init__(self):
        if self.page_size <= 0:
            raise ValueError("page_size must be positive")
        if self.page_size > 1000:
            raise ValueError("page_size cannot exceed 1000")
