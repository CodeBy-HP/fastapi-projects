from typing import Literal, Optional
import math
from beanie import PydanticObjectId
from beanie.operators import RegEx, And
from fastapi import APIRouter, status, HTTPException, Query

from app.schemas.product import *
from app.core.logger import get_logger
from app.core.exceptions import ProductNotFoundException, InvalidProductIdException
from app.models.product import Product

router = APIRouter(prefix="/products", tags=["products"])

logger = get_logger(__name__)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    description="Add a new Product to the Product Inventory",
    summary="Create Product",
)
async def create_product(product_data: ProductCreate) -> ProductResponse:
    """
    Create a new product in the inventory.
    
    Args:
        product_data: Product information to create
        
    Returns:
        ProductResponse: Created product with ID
        
    Raises:
        HTTPException: If product creation fails
    """
    try:
        logger.info(
            f"Creating new product: {product_data.name}",
            extra={
                "product_name": product_data.name,
                "category": product_data.category,
                "price": product_data.price,
                "quantity": product_data.quantity,
            }
        )
        
        product = Product(**product_data.model_dump())
        await product.insert()
        
        logger.info(
            f"Product created successfully: {product.name} (ID: {product.id})",
            extra={
                "product_id": str(product.id),
                "product_name": product.name,
            }
        )

        return ProductResponse(
            _id=str(product.id), **product.model_dump(exclude={"id"})
        )

    except ValueError as e:
        logger.warning(
            f"Validation error while creating product: {str(e)}",
            extra={"error": str(e), "product_data": product_data.model_dump()}
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except Exception as e:
        logger.error(
            f"Failed to create product: {str(e)}",
            exc_info=True,
            extra={"product_data": product_data.model_dump()}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product",
        )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    description="Get a specific product by ID",
    summary="Get Product by ID",
)
async def get_product_by_id(product_id: str) -> ProductResponse:
    """
    Retrieve a product by its unique ID.
    
    Args:
        product_id: The product's unique identifier
        
    Returns:
        ProductResponse: The requested product
        
    Raises:
        HTTPException: If product not found or ID is invalid
    """
    try:
        logger.info(
            f"Fetching product by ID: {product_id}",
            extra={"product_id": product_id}
        )
        
        # Validate ObjectId format
        try:
            object_id = PydanticObjectId(product_id)
        except Exception as e:
            logger.warning(
                f"Invalid product ID format: {product_id}",
                extra={"product_id": product_id, "error": str(e)}
            )
            raise InvalidProductIdException(product_id)

        # Query database
        product = await Product.get(object_id)
        if not product:
            logger.info(
                f"Product not found: {product_id}",
                extra={"product_id": product_id}
            )
            raise ProductNotFoundException(product_id)

        logger.info(
            f"Product retrieved successfully: {product.name} (ID: {product_id})",
            extra={
                "product_id": product_id,
                "product_name": product.name,
            }
        )

        return ProductResponse(
            _id=str(product.id), **product.model_dump(exclude={"id"})
        )

    except (ProductNotFoundException, InvalidProductIdException):
        raise

    except Exception as e:
        logger.error(
            f"Unexpected error while fetching product {product_id}: {str(e)}",
            exc_info=True,
            extra={"product_id": product_id}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    description="Update information for a specific product",
    summary="Update Product",
)
async def update_product(
    product_id: str, product_data: ProductUpdate
) -> ProductResponse:
    """
    Update an existing product's information.
    
    Args:
        product_id: The product's unique identifier
        product_data: Fields to update
        
    Returns:
        ProductResponse: Updated product information
        
    Raises:
        HTTPException: If product not found, ID is invalid, or update fails
    """
    try:
        logger.info(
            f"Updating product: {product_id}",
            extra={
                "product_id": product_id,
                "update_data": product_data.model_dump(exclude_unset=True),
            }
        )
        
        # Validate product_id
        try:
            object_id = PydanticObjectId(product_id)
        except Exception as e:
            logger.warning(
                f"Invalid product ID format: {product_id}",
                extra={"product_id": product_id, "error": str(e)}
            )
            raise InvalidProductIdException(product_id)

        # Fetch product
        product = await Product.get(object_id)
        if not product:
            logger.info(
                f"Product not found for update: {product_id}",
                extra={"product_id": product_id}
            )
            raise ProductNotFoundException(product_id)

        # Prepare update fields
        update_data = product_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if not update_data:
            logger.warning(
                f"No fields provided to update for product: {product_id}",
                extra={"product_id": product_id}
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided to update",
            )

        # Log what's being updated
        logger.debug(
            f"Applying updates to product {product_id}",
            extra={
                "product_id": product_id,
                "fields_updated": list(update_data.keys()),
            }
        )

        # Apply update (set() automatically saves the changes)
        await product.set(update_data)
        
        logger.info(
            f"Product updated successfully: {product.name} (ID: {product_id})",
            extra={
                "product_id": product_id,
                "product_name": product.name,
                "updated_fields": list(update_data.keys()),
            }
        )

        return ProductResponse(
            _id=str(product.id), **product.model_dump(exclude={"id"})
        )

    except (ProductNotFoundException, InvalidProductIdException, HTTPException):
        raise

    except Exception as e:
        logger.error(
            f"Failed to update product {product_id}: {str(e)}",
            exc_info=True,
            extra={"product_id": product_id}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.delete(
    "/{product_id}",
    response_model=MessageResponse,
    description="Remove a product from the inventory",
    summary="Delete Product",
)
async def delete_product(product_id: str) -> MessageResponse:
    """
    Delete a product from the inventory.
    
    Args:
        product_id: The product's unique identifier
        
    Returns:
        MessageResponse: Confirmation message
        
    Raises:
        HTTPException: If product not found or ID is invalid
    """
    try:
        logger.info(
            f"Deleting product: {product_id}",
            extra={"product_id": product_id}
        )
        
        # Validate ID
        try:
            object_id = PydanticObjectId(product_id)
        except Exception as e:
            logger.warning(
                f"Invalid product ID format for deletion: {product_id}",
                extra={"product_id": product_id, "error": str(e)}
            )
            raise InvalidProductIdException(product_id)

        # Fetch product
        product = await Product.get(object_id)
        if not product:
            logger.info(
                f"Product not found for deletion: {product_id}",
                extra={"product_id": product_id}
            )
            raise ProductNotFoundException(product_id)

        # Store product name for logging
        product_name = product.name
        
        # Delete product
        await product.delete()
        
        logger.info(
            f"Product deleted successfully: {product_name} (ID: {product_id})",
            extra={
                "product_id": product_id,
                "product_name": product_name,
            }
        )

        return MessageResponse(
            message=f"Product '{product_name}' deleted successfully"
        )

    except (ProductNotFoundException, InvalidProductIdException):
        raise

    except Exception as e:
        logger.error(
            f"Failed to delete product {product_id}: {str(e)}",
            exc_info=True,
            extra={"product_id": product_id}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )


@router.get(
    "/",
    response_model=ProductListResponse,
    description="Retrieve a paginated list of all products in the inventory",
    summary="Get All Products",
)
async def get_all_products(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    sort_by: Optional[Literal["name", "category", "price"]] = Query(
        None, description="Field to sort by"
    ),
    order: Literal["asc", "desc"] = Query("asc", description="Sort order"),
) -> ProductListResponse:
    """
    Retrieve all products with pagination and optional sorting.
    
    Args:
        page: Page number (starts at 1)
        page_size: Number of items per page (max 100)
        sort_by: Field to sort results by
        order: Sort order (asc or desc)
        
    Returns:
        ProductListResponse: Paginated list of products
        
    Raises:
        HTTPException: If retrieval fails
    """
    try:
        logger.info(
            "Fetching all products",
            extra={
                "page": page,
                "page_size": page_size,
                "sort_by": sort_by,
                "order": order,
            }
        )
        
        skip = (page - 1) * page_size

        # Base query
        query = Product.find()

        # Count total products (before pagination)
        total = await query.count()
        logger.debug(f"Total products in database: {total}")

        # Apply sorting
        if sort_by:
            sort_field = f"{'-' if order == 'desc' else '+'}{sort_by}"
            query = query.sort(sort_field)
            logger.debug(f"Applied sorting: {sort_field}")

        # Fetch paginated products
        products = await query.skip(skip).limit(page_size).to_list()

        # Calculate total pages
        total_pages = max(1, math.ceil(total / page_size))

        # Build response
        product_response = [
            ProductResponse(_id=str(p.id), **p.model_dump(exclude={"id"}))
            for p in products
        ]
        
        logger.info(
            f"Retrieved {len(products)} products (page {page}/{total_pages})",
            extra={
                "total": total,
                "page": page,
                "total_pages": total_pages,
                "returned_count": len(products),
            }
        )

        return ProductListResponse(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            products=product_response,
        )

    except Exception as e:
        logger.error(
            f"Failed to retrieve products: {str(e)}",
            exc_info=True,
            extra={"page": page, "page_size": page_size}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve products",
        )


@router.get(
    "/search/",
    response_model=ProductListResponse,
    description="Search Products by name, category, or price range",
    summary="Search Products",
)
async def search_products(
    name: Optional[str] = Query(None, description="Search by name (case-insensitive)"),
    category: Optional[str] = Query(None, description="Search by category (case-insensitive)"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    sort_by: Optional[Literal["name", "category", "price"]] = Query(
        None, description="Sort by field [name, category, price]"
    ),
    order: Literal["asc", "desc"] = Query("asc", description="Sort order"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
) -> ProductListResponse:
    """
    Search and filter products with pagination and sorting.
    
    Args:
        name: Product name to search for (partial match)
        category: Product category to filter by
        min_price: Minimum price filter
        max_price: Maximum price filter
        sort_by: Field to sort results by
        order: Sort order (asc or desc)
        page: Page number for pagination
        page_size: Number of items per page
        
    Returns:
        ProductListResponse: Paginated list of matching products
        
    Raises:
        HTTPException: If search fails
    """
    try:
        logger.info(
            "Searching products",
            extra={
                "search_name": name,
                "search_category": category,
                "min_price": min_price,
                "max_price": max_price,
                "sort_by": sort_by,
                "order": order,
                "page": page,
                "page_size": page_size,
            }
        )
        
        conditions = []

        # Build search conditions
        if name:
            conditions.append(RegEx(Product.name, name, options="i"))
            logger.debug(f"Added name filter: {name}")

        if category:
            conditions.append(RegEx(Product.category, category, options="i"))
            logger.debug(f"Added category filter: {category}")

        if min_price is not None:
            conditions.append(Product.price >= min_price)
            logger.debug(f"Added min_price filter: {min_price}")

        if max_price is not None:
            if min_price is not None and max_price < min_price:
                logger.warning(
                    f"Invalid price range: max_price ({max_price}) < min_price ({min_price})"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="max_price cannot be less than min_price"
                )
            conditions.append(Product.price <= max_price)
            logger.debug(f"Added max_price filter: {max_price}")

        # Calculate pagination
        skip = (page - 1) * page_size

        # Build query
        if conditions:
            query = Product.find(And(*conditions))
        else:
            query = Product.find()

        # Get total count
        total = await query.count()
        logger.debug(f"Found {total} matching products")

        # Apply sorting
        if sort_by:
            sort_field = f"{'-' if order == 'desc' else '+'}{sort_by}"
            query = query.sort(sort_field)
            logger.debug(f"Applied sorting: {sort_field}")

        # Fetch paginated results
        products = await query.skip(skip).limit(page_size).to_list()

        # Calculate total pages
        total_pages = math.ceil(total / page_size) if total > 0 else 1

        # Build response
        product_response = [
            ProductResponse(_id=str(p.id), **p.model_dump(exclude={"id"}))
            for p in products
        ]
        
        logger.info(
            f"Search completed: returned {len(products)} products (page {page}/{total_pages})",
            extra={
                "total": total,
                "page": page,
                "total_pages": total_pages,
                "returned_count": len(products),
            }
        )

        return ProductListResponse(
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            products=product_response,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Failed to search products: {str(e)}",
            exc_info=True,
            extra={
                "search_name": name,
                "search_category": category,
                "min_price": min_price,
                "max_price": max_price,
            }
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search products",
        )
