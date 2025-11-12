from typing import Literal, Optional
from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Query
import math
from app.models.movie import Movie
from app.schemas.movie import (
    MovieCreate,
    MovieUpdate,
    MovieResponse,
    MovieListResponse,
    MessageResponse,
)
from beanie.operators import RegEx, And

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.post(
    "/",
    response_model=MovieResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Movie",
    description="Add a new Movie to the Movie Collection",
)
async def create_movie(movie_data: MovieCreate) -> MovieResponse:
    try:
        movie = Movie(**movie_data.model_dump())

        await movie.insert()

        return MovieResponse(_id=str(movie.id), **movie.model_dump(exclude={"id"}))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create movie: {str(e)}",
        )


@router.get(
    "/",
    response_model=MovieListResponse,
    summary="Get all Movies with pagination",
    description="Retrieve a pagination list of all movies in the collection",
)
async def get_all_movies(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    sort_by: Optional[Literal["title", "release_year", "rating"]] = Query(
        None, description="Field[title,release_year,rating] to sort by"
    ),
    order: Literal["asc", "desc"] = Query("asc", description="Sort order"),
) -> MovieListResponse:
    try:
        # Calculate skip value
        skip = (page - 1) * page_size

        # Built query
        query = Movie.find()

        # Apply sorting
        if sort_by:
            sort_field = f"{'-' if order == 'desc' else '+'}{sort_by}"
            query = query.sort(sort_field)

        # Get total count
        total = await query.count()

        # Get pagination result
        movies = await query.skip(skip).limit(page_size).to_list()

        # Calculate total pages
        total_pages = math.ceil(total / page_size) if total > 0 else 1

        # Convert to response format
        movie_response = [
            MovieResponse(_id=str(movie.id), **movie.model_dump(exclude={"id"}))
            for movie in movies
        ]

        return MovieListResponse(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            movies=movie_response,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrive movies: {str(e)}",
        )


@router.get(
    "/search",
    response_model=MovieListResponse,
    summary="Search Movies",
    description="Search Movies by title,director,genre,release_year,is_favorite",
)
async def search_movies(
    title: Optional[str] = Query(
        None, description="Search by title (case-insensitive)"
    ),
    director: Optional[str] = Query(
        None, description="Search by director (case-insensitive)"
    ),
    genre: Optional[str] = Query(
        None, description="Search by genre (case-insensitive)"
    ),
    min_year: Optional[int] = Query(None, ge=1000, description="Minimum release_year"),
    max_year: Optional[int] = Query(None, ge=1000, description="Maximum release_year"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    sort_by: Optional[Literal["title", "director", "genre", "release_year"]] = Query(
        None, description="Field to sort by"
    ),
    order: Literal["asc", "desc"] = Query("asc", description="Sort order"),
) -> MovieListResponse:
    try:
        conditions = []

        if title:
            conditions.append(RegEx(Movie.title, title, options="i"))

        if director:
            conditions.append(RegEx(Movie.director, director, options="i"))

        if genre:
            conditions.append(Regex(Movie.genre, genre, options="i"))

        if min_year is not None:
            conditions.append(Movie.release_year >= min_year)

        if max_year is not None:
            conditions.append(Movie.release_year <= max_year)

        skip = (page - 1) * page_size

        if conditions:
            query = Movie.find(And(*conditions))
        else:
            query = Movie.find()

        if sort_by:
            sort_field = f"{'-' if order == 'desc' else '+'}{sort_by}"
            query = query.sort(sort_field)

        total = await query.count()

        movies = await query.skip(skip).limit(page_size).to_list()

        total_pages = math.ceil(total / page_size) if total > 0 else 1

        movie_responses = [
            MovieResponse(_id=str(movie.id), **movie.model_dump(exclude={"id"}))
            for movie in movies
        ]

        return MovieListResponse(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            movies=movie_responses,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search movies: {str(e)}",
        )


@router.get(
    "/{movie_id}",
    response_model=MovieResponse,
    summary="Get a Movie by ID",
    description="Retrieve detailed information about specific movie",
)
async def get_movie_by_id(movie_id: str) -> MovieResponse:
    try:
        # Validate and convert to ObjectId
        try:
            object_id = PydanticObjectId(movie_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book ID format"
            )

        movie = await Movie.get(object_id)

        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with Id {movie_id} not found",
            )

        return MovieResponse(_id=str(movie.id), **movie.model_dump(exclude={"id"}))

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve movie: {str(e)}",
        )


@router.put(
    "/{movie_id}",
    response_model=MovieResponse,
    summary="Update a movie by ID",
    description="Update information for a specific movie",
)
async def update_movie(movie_id: str, movie_data: MovieUpdate) -> MovieResponse:
    try:
        # Validate and convert to ObjectId
        try:
            object_id = PydanticObjectId(movie_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid movie ID format",
            )

        movie = await Movie.get(object_id)

        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {movie_id} not found",
            )

        update_data = movie_data.model_dump(exclude_unset=True, exclude_none=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update",
            )

        # Update book
        await movie.set(update_data)

        await movie.sync()

        return MovieResponse(_id=str(movie.id), **movie.model_dump(exclude={"id"}))

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update movie: {str(e)}",
        )


@router.delete(
    "/{movie_id}",
    response_model=MessageResponse,
    summary="Delete a movie by ID",
    description="Remove a movie from the collection",
)
async def delete_movie(movie_id: str) -> MessageResponse:
    try:
        # Validate and convert to ObjectId
        try:
            object_id = PydanticObjectId(movie_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid movie ID format",
            )

        # Find
        movie = await Movie.get(object_id)

        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with ID {movie_id} not found",
            )

        # Delete
        await movie.delete()

        return MessageResponse(message=f"Movie '{movie.title}' deleted successfully")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete movie: {str(e)}",
        )
