from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime, timezone
from typing import Optional, Any


class MovieCreate(BaseModel):
    """Schema for creating a new Movie"""

    title: str = Field(
        ..., min_length=1, max_length=200, description="Title of the Movie"
    )

    director: str = Field(..., min_length=1, max_length=50, description="Director Name")

    genre: str = Field(
        ..., min_length=1, max_length=50, description="Genre of the Movie"
    )

    release_year: int = Field(
        ..., ge=1000, le=datetime.now(timezone.utc).year, description="Year of release"
    )

    rating: float = Field(..., ge=0, le=10, description="Rating of Movie")

    is_favorite: Optional[bool] = Field(
        ..., default=False, description="Is Marked Favorite my Session User"
    )

    @field_validator("title", "director", "genre")
    @classmethod
    def strip_and_capitalize(cls, v: str):
        v = v.strip()
        if not v:
            raise ValueError("Field cannot be empty or whitespace.")
        return v.title()

    @field_validator("release_year")
    @classmethod
    def validate_realease_year(cls, v: int):
        current_year = datetime.now(timezone.utc).year
        if v > current_year:
            raise ValueError(f"the release year cannot be in future{v}")
        if v < 1888:
            raise ValueError("the release year seems invalid(<1888)")
        return v

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v: float):
        if not (0 <= v <= 10):
            raise ValueError("the rating must be between 0 and 10.")
        return round(v, 1)

    @field_validator("is_favorite", mode="before")
    @classmethod
    def validate_is_favorite(cls, v: Any):
        if isinstance(v, str):
            v = v.lower() in {"true", "1", "yes"}
        return bool(v)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Fight Club",
                "director": "Nolan",
                "genre": "Philosophical",
                "release_year": 2004,
                "rating": 9.8,
                "is_favorite": True,
            }
        }
    )


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(
        None, min_length=1, max_length=200, description="Title of the Movie"
    )
    director: Optional[str] = Field(
        None, min_length=1, max_length=50, description="Director Name"
    )
    genre: Optional[str] = Field(
        None, min_length=1, max_length=50, description="Genre of the Movie"
    )
    release_year: Optional[int] = Field(
        None, ge=1000, le=datetime.now(timezone.utc).year, description="Year of release"
    )
    rating: Optional[float] = Field(None, ge=0, le=10, description="Rating of Movie")
    is_favorite: Optional[bool] = Field(
        None, description="Is Marked Favorite by Session User"
    )

    @field_validator("title", "director", "genre")
    @classmethod
    def strip_and_capitalize(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError("Field cannot be empty or whitespace.")
            return v.strip().title()
        return None

    @field_validator("release_year")
    @classmethod
    def validate_release_year(cls, v: Optional[int]) -> Optional[int]:
        if v is None:
            return None
        current_year = datetime.now(timezone.utc).year
        if v > current_year:
            raise ValueError(f"The release year cannot be in the future ({v})")
        if v < 1888:
            raise ValueError("The release year seems invalid (<1888)")
        return v

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v: Optional[float]) -> Optional[float]:
        if v is None:
            return None
        if not (0 <= v <= 10):
            raise ValueError("The rating must be between 0 and 10.")
        return round(v, 1)

    @field_validator("is_favorite", mode="before")
    @classmethod
    def validate_is_favorite(cls, v: Any):
        if isinstance(v, str):
            v = v.lower() in {"true", "1", "yes"}
        return bool(v) if v is not None else None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Oblivision",
                "rating": 7.8,
            }
        }
    )


class MovieResponse(BaseModel):
    """Schema for Movie response"""

    id: str = Field(alias="_id")
    title: str
    director: str
    genre: str
    release_year: int
    rating: float
    is_favorite: Optional[bool]

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "title": "Fight Club",
                "director": "Nolan",
                "genre": 2008,
                "rating": 9.8,
                "is_favorite": True,
            }
        },
    )


class MovieListResponse(BaseModel):
    """schema for pagination Movie list response"""

    total: int = Field(..., description="Total number of books matching the query")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")
    movies: list[MovieResponse] = Field(..., description="List of movies")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total": 100,
                "page": 1,
                "page_size": 10,
                "total_pages": 10,
                "movies": [],
            }
        }
    )


class MessageResponse(BaseModel):
    """Generic message response."""

    message: str

    model_config = ConfigDict(
        json_schema_extra={"example": {"message": "Movie deleted successfully"}}
    )
