"""
Book routes - REST API endpoints for book management.
Includes CRUD operations, search, pagination, and sorting.
"""
from fastapi import APIRouter, HTTPException, status, Query
from beanie import PydanticObjectId
from beanie.operators import RegEx, And
from typing import Optional, Literal
import math

from app.models.book import Book
from app.schemas.book import (
    BookCreate,
    BookUpdate,
    BookResponse,
    BookListResponse,
    MessageResponse
)

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
    description="Add a new book to the digital library"
)
async def create_book(book_data: BookCreate) -> BookResponse:
    """
    Create a new book with the following information:
    - **title**: Book title (required)
    - **author**: Author name (required)
    - **description**: Book description (optional)
    - **published_year**: Year of publication (required, must be <= current year)
    - **price**: Book price (required, must be > 0)
    - **genre**: Book genre/category (optional)
    """
    try:
        # Create book document
        book = Book(**book_data.model_dump())
        
        # Save to database
        await book.insert()
        
        # Return response
        return BookResponse(
            _id=str(book.id),
            **book.model_dump(exclude={"id"})
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create book: {str(e)}"
        )


@router.get(
    "/",
    response_model=BookListResponse,
    summary="Get all books with pagination",
    description="Retrieve a paginated list of all books in the library"
)
async def get_all_books(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    sort_by: Optional[Literal["price", "published_year", "title", "created_at"]] = Query(
        None,
        description="Field to sort by"
    ),
    order: Literal["asc", "desc"] = Query("asc", description="Sort order")
) -> BookListResponse:
    """
    Get all books with pagination and optional sorting.
    
    - **page**: Page number (starts from 1)
    - **page_size**: Number of books per page (max 100)
    - **sort_by**: Sort by field (price, published_year, title, created_at)
    - **order**: Sort order (asc or desc)
    """
    try:
        # Calculate skip value
        skip = (page - 1) * page_size
        
        # Build query
        query = Book.find()
        
        # Apply sorting
        if sort_by:
            sort_field = f"{'-' if order == 'desc' else '+'}{sort_by}"
            query = query.sort(sort_field)
        
        # Get total count
        total = await query.count()
        
        # Get paginated results
        books = await query.skip(skip).limit(page_size).to_list()
        
        # Calculate total pages
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        
        # Convert to response format
        book_responses = [
            BookResponse(_id=str(book.id), **book.model_dump(exclude={"id"}))
            for book in books
        ]
        
        return BookListResponse(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            books=book_responses
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve books: {str(e)}"
        )


@router.get(
    "/search",
    response_model=BookListResponse,
    summary="Search books",
    description="Search books by title, author, or genre with pagination"
)
async def search_books(
    title: Optional[str] = Query(None, description="Search by title (case-insensitive)"),
    author: Optional[str] = Query(None, description="Search by author (case-insensitive)"),
    genre: Optional[str] = Query(None, description="Search by genre (case-insensitive)"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    min_year: Optional[int] = Query(None, ge=1000, description="Minimum publication year"),
    max_year: Optional[int] = Query(None, description="Maximum publication year"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    sort_by: Optional[Literal["price", "published_year", "title", "created_at"]] = Query(
        None,
        description="Field to sort by"
    ),
    order: Literal["asc", "desc"] = Query("asc", description="Sort order")
) -> BookListResponse:
    """
    Search books with multiple filters:
    
    - **title**: Search in book title (partial match, case-insensitive)
    - **author**: Search in author name (partial match, case-insensitive)
    - **genre**: Search in genre (partial match, case-insensitive)
    - **min_price/max_price**: Filter by price range
    - **min_year/max_year**: Filter by publication year range
    - **page**: Page number (starts from 1)
    - **page_size**: Number of books per page (max 100)
    - **sort_by**: Sort by field (price, published_year, title, created_at)
    - **order**: Sort order (asc or desc)
    """
    try:
        # Build filter conditions
        conditions = []
        
        if title:
            conditions.append(RegEx(Book.title, title, options="i"))
        
        if author:
            conditions.append(RegEx(Book.author, author, options="i"))
        
        if genre:
            conditions.append(RegEx(Book.genre, genre, options="i"))
        
        if min_price is not None:
            conditions.append(Book.price >= min_price)
        
        if max_price is not None:
            conditions.append(Book.price <= max_price)
        
        if min_year is not None:
            conditions.append(Book.published_year >= min_year)
        
        if max_year is not None:
            conditions.append(Book.published_year <= max_year)
        
        # Calculate skip value
        skip = (page - 1) * page_size
        
        # Build query
        if conditions:
            query = Book.find(And(*conditions))
        else:
            query = Book.find()
        
        # Apply sorting
        if sort_by:
            sort_field = f"{'-' if order == 'desc' else '+'}{sort_by}"
            query = query.sort(sort_field)
        
        # Get total count
        total = await query.count()
        
        # Get paginated results
        books = await query.skip(skip).limit(page_size).to_list()
        
        # Calculate total pages
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        
        # Convert to response format
        book_responses = [
            BookResponse(_id=str(book.id), **book.model_dump(exclude={"id"}))
            for book in books
        ]
        
        return BookListResponse(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            books=book_responses
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search books: {str(e)}"
        )


@router.get(
    "/{book_id}",
    response_model=BookResponse,
    summary="Get a book by ID",
    description="Retrieve detailed information about a specific book"
)
async def get_book_by_id(book_id: str) -> BookResponse:
    """
    Get a specific book by its unique ID.
    
    - **book_id**: MongoDB ObjectId of the book
    """
    try:
        # Validate and convert to ObjectId
        try:
            object_id = PydanticObjectId(book_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid book ID format"
            )
        
        # Find book
        book = await Book.get(object_id)
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )
        
        return BookResponse(
            _id=str(book.id),
            **book.model_dump(exclude={"id"})
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve book: {str(e)}"
        )


@router.put(
    "/{book_id}",
    response_model=BookResponse,
    summary="Update a book by ID",
    description="Update information for a specific book"
)
async def update_book(book_id: str, book_data: BookUpdate) -> BookResponse:
    """
    Update a book's information.
    Only provided fields will be updated.
    
    - **book_id**: MongoDB ObjectId of the book
    - **book_data**: Fields to update (all optional)
    """
    try:
        # Validate and convert to ObjectId
        try:
            object_id = PydanticObjectId(book_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid book ID format"
            )
        
        # Find book
        book = await Book.get(object_id)
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )
        
        # Get only non-None values for update
        update_data = book_data.model_dump(exclude_unset=True, exclude_none=True)
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update"
            )
        
        # Update book
        await book.set(update_data)
        
        # Reload to get updated document
        await book.sync()
        
        return BookResponse(
            _id=str(book.id),
            **book.model_dump(exclude={"id"})
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update book: {str(e)}"
        )


@router.delete(
    "/{book_id}",
    response_model=MessageResponse,
    summary="Delete a book by ID",
    description="Remove a book from the library"
)
async def delete_book(book_id: str) -> MessageResponse:
    """
    Delete a book from the library.
    
    - **book_id**: MongoDB ObjectId of the book
    """
    try:
        # Validate and convert to ObjectId
        try:
            object_id = PydanticObjectId(book_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid book ID format"
            )
        
        # Find book
        book = await Book.get(object_id)
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Book with ID {book_id} not found"
            )
        
        # Delete book
        await book.delete()
        
        return MessageResponse(
            message=f"Book '{book.title}' deleted successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete book: {str(e)}"
        )
