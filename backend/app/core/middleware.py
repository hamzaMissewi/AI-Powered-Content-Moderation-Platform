# backend/app/core/middleware.py
import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.core.config import settings
from app.core.exceptions import RateLimitExceeded

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all requests and responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path}",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else None,
            }
        )
        
        # Process request
        response = await call_next(request)
        
        # Calculate process time
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log response
        logger.info(
            f"Response: {response.status_code} - {process_time:.3f}s",
            extra={
                "status_code": response.status_code,
                "process_time": process_time,
            }
        )
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting middleware."""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.rate_limit_store: dict = {}
        self.cleanup_interval = 60  # Clean up old entries every 60 seconds
        self.last_cleanup = time.time()
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)
        
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/api/docs", "/api/redoc", "/api/v1/openapi.json"]:
            return await call_next(request)
        
        # Get client identifier
        client_id = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Cleanup old entries periodically
        if current_time - self.last_cleanup > self.cleanup_interval:
            self._cleanup_old_entries(current_time)
            self.last_cleanup = current_time
        
        # Check rate limit
        if client_id in self.rate_limit_store:
            requests = self.rate_limit_store[client_id]
            # Remove requests older than 1 minute
            requests = [req_time for req_time in requests if current_time - req_time < 60]
            
            if len(requests) >= settings.RATE_LIMIT_PER_MINUTE:
                logger.warning(f"Rate limit exceeded for {client_id}")
                raise RateLimitExceeded()
            
            requests.append(current_time)
            self.rate_limit_store[client_id] = requests
        else:
            self.rate_limit_store[client_id] = [current_time]
        
        return await call_next(request)
    
    def _cleanup_old_entries(self, current_time: float) -> None:
        """Remove entries older than 1 minute."""
        for client_id in list(self.rate_limit_store.keys()):
            requests = [req_time for req_time in self.rate_limit_store[client_id] 
                       if current_time - req_time < 60]
            if requests:
                self.rate_limit_store[client_id] = requests
            else:
                del self.rate_limit_store[client_id]
