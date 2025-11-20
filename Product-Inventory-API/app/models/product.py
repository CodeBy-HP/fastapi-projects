"""
Product Model for MongoDB using Beanie ODM.

This module defines the Product document model with validation,
computed fields, and database configuration.
"""

from beanie import Document
from pydantic import Field, computed_field, field_validator


class Product(Document):

    # === STORED FIELDS (Persisted in Database) ===
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

    # === COMPUTED FIELDS (Not stored in Database but included in api response)===

    @computed_field
    @property
    def in_stock(self) -> bool:
        return self.quantity > 0

    # === FIELD VALIDATORS ===
    @field_validator("name", "category")
    @classmethod
    def strip(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("Field cannot be emtpy or whitespace.")
        return v

    # === BEANIE DOCUMENT SETTINGS ===
    class Settings:
        name = "products"
        indexes = ["name", "category", "price"]


# === LOCAL TESTING ===
if __name__ == "__main__":
    #  First change the Document to BaseModel
    print("Running local tests...")

    tests = [
        {"name": "harsh", "category": "human", "price": 12, "quantity": 2},
        {"name": "   harsh   ", "category": "  human  ", "price": 12, "quantity": 2},
        {"name": " ", "category": "human", "price": 12, "quantity": 2},
        {"name": 123, "category": "human", "price": 12, "quantity": 2},
    ]

    for t in tests:
        try:
            p = Product(**t)
            print("OK:", p)
        except Exception as e:
            print("Error for input", t, "->", e)
