from pydantic import BaseModel, Field
from typing import Optional


class Item(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
