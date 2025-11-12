from beanie import Document
from pydantic import Field, field_validator
from datetime import datetime, timezone
from typing import Any, Optional


class Movie(Document):
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

    class Settings:
        name = "movies"
        indexes = [
            "title",
            "director",
            "genre",
            "release_year",
            [("title", 1), ("director", 1)],
        ]
