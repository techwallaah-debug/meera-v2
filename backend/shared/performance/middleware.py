"""
Performance middleware - Response compression, caching headers
"""
from fastapi import Request, Response
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time
import gzip

class CompressionMiddleware(BaseHTTPMiddleware):
    """Compress responses"""
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Check if client accepts gzip
        accept_encoding = request.headers.get("Accept-Encoding", "")
        if "gzip" in accept_encoding:
            # Compress response body if it's text-based
            if response.headers.get("Content-Type", "").startswith(("text/", "application/json", "application/javascript")):
                body = b""
                async for chunk in response.body_iterator:
                    body += chunk
                
                compressed = gzip.compress(body)
                response = Response(
                    content=compressed,
                    status_code=response.status_code,
                    headers={
                        **dict(response.headers),
                        "Content-Encoding": "gzip",
                        "Content-Length": str(len(compressed))
                    },
                    media_type=response.media_type
                )
        
        return response

class CacheControlMiddleware(BaseHTTPMiddleware):
    """Add cache control headers"""
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add cache headers based on endpoint
        path = request.url.path
        
        if path.startswith("/static/") or path.startswith("/media/"):
            # Static assets - cache for 1 year
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        elif path.startswith("/api/products") or path.startswith("/api/posts"):
            # Product/post data - cache for 5 minutes
            response.headers["Cache-Control"] = "public, max-age=300"
        elif path.startswith("/api/users/me"):
            # User data - no cache
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        else:
            # Default - cache for 1 minute
            response.headers["Cache-Control"] = "public, max-age=60"
        
        return response

class TimingMiddleware(BaseHTTPMiddleware):
    """Add timing headers for performance monitoring"""
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Response-Time"] = f"{process_time:.3f}s"
        
        return response
