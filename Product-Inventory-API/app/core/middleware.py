"""
Custom Middleware for Production-Ready FastAPI Application

This module provides middleware for request logging, timing, and error tracking.
"""

import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log all incoming requests with timing information.
    
    Logs:
    - Request method, path, and query parameters
    - Client IP address
    - Request processing time
    - Response status code
    - Unique request ID for tracing
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and log relevant information.
        
        Args:
            request: The incoming request
            call_next: The next middleware or route handler
            
        Returns:
            Response from the route handler
        """
        # Generate unique request ID for tracking
        request_id = str(uuid.uuid4())
        
        # Extract request information
        method = request.method
        path = request.url.path
        query_params = str(request.url.query) if request.url.query else None
        client_host = request.client.host if request.client else "unknown"
        
        # Start timing
        start_time = time.time()
        
        # Log incoming request
        logger.info(
            f"Incoming request: {method} {path}",
            extra={
                "request_id": request_id,
                "method": method,
                "path": path,
                "query_params": query_params,
                "client_host": client_host,
            }
        )
        
        # Add request_id to request state for use in route handlers
        request.state.request_id = request_id
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"Request completed: {method} {path} - Status: {response.status_code} - Time: {process_time:.3f}s",
                extra={
                    "request_id": request_id,
                    "method": method,
                    "path": path,
                    "status_code": response.status_code,
                    "process_time": process_time,
                    "client_host": client_host,
                }
            )
            
            # Add custom headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time:.3f}"
            
            return response
            
        except Exception as e:
            # Calculate processing time even for errors
            process_time = time.time() - start_time
            
            # Log error
            logger.error(
                f"Request failed: {method} {path} - Error: {str(e)} - Time: {process_time:.3f}s",
                exc_info=True,
                extra={
                    "request_id": request_id,
                    "method": method,
                    "path": path,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "process_time": process_time,
                    "client_host": client_host,
                }
            )
            
            # Re-raise the exception to be handled by exception handlers
            raise


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses.
    
    Adds common security headers to protect against various attacks.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Add security headers to the response.
        
        Args:
            request: The incoming request
            call_next: The next middleware or route handler
            
        Returns:
            Response with added security headers
        """
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response
