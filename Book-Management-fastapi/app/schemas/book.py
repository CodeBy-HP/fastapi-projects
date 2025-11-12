"""
Pydantic schemas for request/response models.
Separate from database models for better API design.
"""
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime


class BookCreate(BaseModel):
    """Schema for creating a new book."""
    
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=2000)
    published_year: int = Field(..., ge=1000, le=datetime.now().year)
    price: float = Field(..., gt=0)
    genre: Optional[str] = Field(default=None, max_length=50)
    
    @field_validator('title', 'author')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        """Ensure title and author are not just whitespace."""
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or whitespace')
        return v.strip()
    
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


class BookUpdate(BaseModel):
    """Schema for updating an existing book. All fields are optional."""
    
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    author: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=2000)
    published_year: Optional[int] = Field(default=None, ge=1000, le=datetime.now().year)
    price: Optional[float] = Field(default=None, gt=0)
    genre: Optional[str] = Field(default=None, max_length=50)
    
    @field_validator('title', 'author')
    @classmethod
    def validate_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Ensure title and author are not just whitespace if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError('Field cannot be empty or whitespace')
        return v.strip() if v else None
    
    @field_validator('price')
    @classmethod
    def validate_price_precision(cls, v: Optional[float]) -> Optional[float]:
        """Round price to 2 decimal places if provided."""
        return round(v, 2) if v is not None else None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Harry Potter and the Chamber of Secrets",
                "price": 21.99
            }
        }
    )


class BookResponse(BaseModel):
    """Schema for book response."""
    
    id: str = Field(alias="_id")
    title: str
    author: str
    description: Optional[str] = None
    published_year: int
    price: float
    genre: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "title": "Harry Potter and the Philosopher's Stone",
                "author": "J.K. Rowling",
                "description": "A young wizard begins his magical education",
                "published_year": 1997,
                "price": 19.99,
                "genre": "Fantasy",
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
    )


class BookListResponse(BaseModel):
    """Schema for paginated book list response."""
    
    total: int = Field(..., description="Total number of books matching the query")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    books: list[BookResponse] = Field(..., description="List of books")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total": 100,
                "page": 1,
                "page_size": 10,
                "total_pages": 10,
                "books": []
            }
        }
    )


class MessageResponse(BaseModel):
    """Generic message response."""
    
    message: str
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "Book deleted successfully"
            }
        }
    )
