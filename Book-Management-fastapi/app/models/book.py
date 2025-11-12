"""
Book model - MongoDB document model using Beanie ODM.
Includes comprehensive validation rules.
"""
from beanie import Document
from pydantic import Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime, timezone


class Book(Document):
    """
    Book document model for MongoDB.
    Represents a book in the digital library.
    """
    
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Title of the book"
    )
    
    author: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the author"
    )
    
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Short summary of the book"
    )
    
    published_year: int = Field(
        ...,
        ge=1000,
        le=datetime.now(timezone.utc).year,
        description="Year of publication"
    )
    
    price: float = Field(
        ...,
        gt=0,
        description="Price of the book (must be positive)"
    )
    
    genre: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Category or type of book"
    )
    
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the book was added"
    )
    
    @field_validator('title', 'author')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        """Ensure title and author are not just whitespace."""
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or whitespace')
        return v.strip()
    
    @field_validator('genre', mode='before')
    @classmethod
    def validate_genre(cls, v: Optional[str]) -> Optional[str]:
        """Normalize genre to title case if provided."""
        if v and v.strip():
            return v.strip().title()
        return None
    
    @field_validator('price')
    @classmethod
    def validate_price_precision(cls, v: float) -> float:
        """Round price to 2 decimal places."""
        return round(v, 2)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Harry Potter and the Philosopher's Stone",
                "author": "J.K. Rowling",
                "description": "A young wizard begins his magical education",
                "published_year": 1997,
                "price": 19.99,
                "genre": "Fantasy"
            }
        }
    )
    
    class Settings:
        """Beanie document settings."""
        name = "books"  # Collection name
        indexes = [
            "title",
            "author",
            "genre",
            "published_year"
        ]
