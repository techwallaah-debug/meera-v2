"""
Advanced Redis caching utilities
"""
import redis
import json
import pickle
from typing import Optional, Any, Callable
from functools import wraps
import os
from datetime import timedelta

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0,
    decode_responses=False  # For pickle support
)

class CacheManager:
    """Advanced cache manager with TTL, invalidation, and patterns"""
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            data = redis_client.get(key)
            if data:
                return pickle.loads(data)
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    @staticmethod
    def set(key: str, value: Any, ttl: int = 3600):
        """Set value in cache with TTL"""
        try:
            data = pickle.dumps(value)
            redis_client.setex(key, ttl, data)
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    @staticmethod
    def delete(key: str):
        """Delete key from cache"""
        try:
            redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    @staticmethod
    def delete_pattern(pattern: str):
        """Delete all keys matching pattern"""
        try:
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
            return len(keys)
        except Exception as e:
            print(f"Cache delete pattern error: {e}")
            return 0
    
    @staticmethod
    def invalidate_user_cache(user_id: int):
        """Invalidate all cache entries for a user"""
        patterns = [
            f"user:{user_id}:*",
            f"feed:{user_id}:*",
            f"cart:{user_id}:*",
        ]
        total_deleted = 0
        for pattern in patterns:
            total_deleted += CacheManager.delete_pattern(pattern)
        return total_deleted
    
    @staticmethod
    def cache_result(key_prefix: str, ttl: int = 3600):
        """Decorator to cache function results"""
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key from function args
                cache_key = f"{key_prefix}:{hash(str(args) + str(kwargs))}"
                
                # Try to get from cache
                cached = CacheManager.get(cache_key)
                if cached is not None:
                    return cached
                
                # Execute function
                result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
                
                # Store in cache
                CacheManager.set(cache_key, result, ttl)
                
                return result
            return wrapper
        return decorator

# Feed caching
class FeedCache:
    """Specialized cache for feed data"""
    
    @staticmethod
    def get_feed(user_id: int, feed_type: str = "main", skip: int = 0, limit: int = 20):
        """Get cached feed"""
        key = f"feed:{user_id}:{feed_type}:{skip}:{limit}"
        return CacheManager.get(key)
    
    @staticmethod
    def set_feed(user_id: int, feed_data: list, feed_type: str = "main", 
                 skip: int = 0, limit: int = 20, ttl: int = 300):
        """Cache feed data (5 minutes TTL)"""
        key = f"feed:{user_id}:{feed_type}:{skip}:{limit}"
        return CacheManager.set(key, feed_data, ttl)
    
    @staticmethod
    def invalidate_user_feed(user_id: int):
        """Invalidate user's feed cache"""
        return CacheManager.delete_pattern(f"feed:{user_id}:*")

# Product cache
class ProductCache:
    """Specialized cache for product data"""
    
    @staticmethod
    def get_product(product_id: int):
        """Get cached product"""
        key = f"product:{product_id}"
        return CacheManager.get(key)
    
    @staticmethod
    def set_product(product_id: int, product_data: dict, ttl: int = 3600):
        """Cache product (1 hour TTL)"""
        key = f"product:{product_id}"
        return CacheManager.set(key, product_data, ttl)
    
    @staticmethod
    def invalidate_product(product_id: int):
        """Invalidate product cache"""
        return CacheManager.delete(f"product:{product_id}")

# Session cache
class SessionCache:
    """Session management with Redis"""
    
    @staticmethod
    def get_session(session_id: str):
        """Get session data"""
        key = f"session:{session_id}"
        return CacheManager.get(key)
    
    @staticmethod
    def set_session(session_id: str, session_data: dict, ttl: int = 86400):
        """Set session (24 hours TTL)"""
        key = f"session:{session_id}"
        return CacheManager.set(key, session_data, ttl)
    
    @staticmethod
    def delete_session(session_id: str):
        """Delete session"""
        key = f"session:{session_id}"
        return CacheManager.delete(key)

import asyncio
