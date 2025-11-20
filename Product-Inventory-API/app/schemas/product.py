from typing import Optional, Union
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductCreate(BaseModel):
    """Defines the shape of data we serve through APIs, should not contain business logic (ex. computed field -> it belongs in documents)"""

    name: str = Field(
        ..., min_length=1, max_length=150, description="Name of the product"
    )

    category: str = Field(
        ..., min_length=1, max_length=150, description="Category of the product"
    )

    price: float = Field(
        ..., gt=0, description="Price of the product (must be positive)"
    )

    quantity: int = Field(..., ge=0, description="Current stock quantity")

    # === FIELD VALIDATORS ===
    @field_validator("name", "category")
    @classmethod
    def strip(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("Field cannot be emtpy or whitespace.")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Iphone13",
                "category": "Electronics",
                "price": 120000,
                "quantity": 12,
            }
        }
    )


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=150, description="Name of the product"
    )

    category: Optional[str] = Field(
        None, min_length=1, max_length=150, description="Category of the product"
    )

    price: Optional[float] = Field(
        None, gt=0, description="Price of the product (must be positive)"
    )

    quantity: Optional[int] = Field(None, ge=0, description="Current stock quantity")

    # === FIELD VALIDATORS ===
    @field_validator("name", "category")
    @classmethod
    def strip(cls, v: Union[None, str]) -> Union[str, None]:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Field cannot be emtpy or whitespace.")
            return v
        return None

    model_config = ConfigDict(
        json_schema_extra={"example": {"name": "Iphone12", "price": 130000}}
    )


class ProductResponse(BaseModel):
    """Schemas for Movie response"""

    id: str = Field(alias="_id")
    name: str
    category: str
    price: float
    quantity: int
    in_stock: bool

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "name": "Iphone11",
                "category": "Electronics",
                "price": 120000,
                "quantity": 0,
                "in_stock": False,
            }
        },
    )


class ProductListResponse(BaseModel):
    "Schemas for pagination Product list response"

    total: int = Field(..., description="Total number of books matching the query")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    products: list[ProductResponse] = Field(..., description="List of products")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total": 100,
                "page": 1,
                "page_size": 10,
                "total_pages": 10,
                "products": [],
            }
        }
    )


class MessageResponse(BaseModel):
    """Generic message reponse"""

    message: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"message": "Product deleted sucdessfully"}}
    )
