from datetime import datetime

from beanie import Document
from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductReview(Document):
    name: str
    product: str
    rating: float
    review: str
    date: datetime = datetime.now()

    class Settings:
        name = "product_review"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Abdulazeez",
                "product": "TestDriven TDD Course",
                "rating": 4.9,
                "review": "Excellent course!",
                "date": datetime.now()
            }
        }
    )


class UpdateProductReview(BaseModel):
    name: Optional[str] = None
    product: Optional[str] = None
    rating: Optional[float] = None
    review: Optional[str] = None
    date: Optional[datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Abdulazeez Abdulazeez",
                "product": "TestDriven TDD Course",
                "rating": 5.0,
                "review": "Excellent course!",
                "date": datetime.now()
            }
        }
    )
