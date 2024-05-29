from pydantic import BaseModel
from typing import List, Generic, TypeVar

T = TypeVar("T")

class Page(Generic[T], BaseModel):
    total_elements: int
    page: int
    size: int
    items: List[T]