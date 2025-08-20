"""
🗃️ MONGODB-BASED DISTRIBUTED CACHING SYSTEM
Advanced persistent caching using MongoDB with TTL support

This module provides a complete replacement for Redis caching using MongoDB,
offering persistent, distributed caching with automatic expiration and 
high-performance retrieval capabilities.

Features:
- TTL (Time To Live) support with automatic cleanup
- High-performance indexing for fast retrieval
- JSON-compatible data storage
- Connection pooling and error handling
- Cache statistics and monitoring
- LRU cache management with MongoDB persistence

Algorithm Version: mongodb_caching_v1.0
"""

import asyncio
import hashlib
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from collections import deque

import motor.motor_asyncio
from pymongo import IndexModel, ASCENDING
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError

logger = logging.getLogger(__name__)


class MongoDBCachingSystem:
    """
    🗃️ ADVANCED MONGODB-BASED CACHING SYSTEM
    
    Complete replacement for Redis caching using MongoDB with:
    - Persistent storage with TTL support
    - High-performance indexing
    - Automatic cleanup of expired entries
    - Cache statistics and monitoring
    - Error handling and connection resilience
    """
    
    def __init__(self, db_name: str = None, collection_name: str = "medical_ai_cache"):
        """Initialize MongoDB caching system"""
        
        # Database configuration
        self.db_name = db_name or os.environ.get('MONGO_DB_NAME', 'symptom_analyzer')
        self.collection_name = collection_name
        self.mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
        
        # Connection objects
        self.client = None
        self.database = None
        self.cache_collection = None
        self.statistics_collection = None
        
        # Cache statistics
        self.cache_stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "mongodb_hits": 0,
            "memory_hits": 0,
            "pattern_hits": 0,
            "storage_operations": 0,
            "cleanup_operations": 0
        }
        
        # In-memory LRU cache for ultra-fast access
        self.memory_cache = {}
        self.pattern_cache = {}
        self.cache_access_order = deque()
        self.max_memory_cache_size = 5000
        
        # Connection status
        self.is_connected = False
        self.last_connection_attempt = None
        
        logger.info("MongoDB Caching System initialized")
    
    async def initialize_mongodb_cache(self) -> bool:
        """Initialize MongoDB connection and create indexes"""
        try:
            # Create MongoDB client with connection pooling
            self.client = motor.motor_asyncio.AsyncIOMotorClient(
                self.mongo_url,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                maxPoolSize=50,
                minPoolSize=5
            )
            
            # Test connection
            await self.client.admin.command('ping')
            
            # Get database and collections
            self.database = self.client[self.db_name]
            self.cache_collection = self.database[self.collection_name]
            self.statistics_collection = self.database[f"{self.collection_name}_stats"]
            
            # Create essential indexes
            await self._create_cache_indexes()
            
            # Initialize cache statistics
            await self._initialize_statistics()
            
            self.is_connected = True
            self.last_connection_attempt = datetime.now()
            
            logger.info(f"MongoDB caching initialized successfully on database: {self.db_name}")
            return True
            
        except Exception as e:
            logger.error(f"MongoDB caching initialization failed: {e}")
            self.is_connected = False
            return False
    
    async def _create_cache_indexes(self):
        """Create optimized indexes for cache performance"""
        
        # Primary cache collection indexes
        cache_indexes = [
            # Primary cache key index
            IndexModel([("cache_key", ASCENDING)], unique=True),
            
            # TTL index for automatic expiration
            IndexModel([("expires_at", ASCENDING)], expireAfterSeconds=0),
            
            # Performance indexes
            IndexModel([("created_at", ASCENDING)]),
            IndexModel([("cache_type", ASCENDING)]),
            IndexModel([("last_accessed", ASCENDING)]),
            
            # Compound indexes for complex queries
            IndexModel([
                ("cache_type", ASCENDING),
                ("created_at", ASCENDING)
            ]),
            IndexModel([
                ("expires_at", ASCENDING),
                ("last_accessed", ASCENDING)
            ])
        ]
        
        # Create indexes
        await self.cache_collection.create_indexes(cache_indexes)
        
        # Statistics collection indexes
        stats_indexes = [
            IndexModel([("date", ASCENDING)], unique=True),
            IndexModel([("timestamp", ASCENDING)])
        ]
        
        await self.statistics_collection.create_indexes(stats_indexes)
        
        logger.info("MongoDB cache indexes created successfully")
    
    async def _initialize_statistics(self):
        """Initialize cache statistics tracking"""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        try:
            # Create today's statistics document if it doesn't exist
            await self.statistics_collection.update_one(
                {"date": today},
                {
                    "$setOnInsert": {
                        "date": today,
                        "timestamp": datetime.now(),
                        "total_requests": 0,
                        "cache_hits": 0,
                        "cache_misses": 0,
                        "mongodb_operations": 0,
                        "cleanup_operations": 0
                    }
                },
                upsert=True
            )
            
        except Exception as e:
            logger.warning(f"Could not initialize statistics: {e}")
    
    def _generate_cache_key(self, text: str, context: Optional[Dict] = None) -> str:
        """Generate unique cache key for text and context"""
        # Normalize text for consistent caching
        normalized_text = text.lower().strip()
        
        # Include relevant context in cache key
        context_key = ""
        if context:
            relevant_context = {
                "stage": context.get("stage"),
                "patient_type": context.get("patient_type"),
                "urgency": context.get("urgency"),
                "intent_category": context.get("intent_category")
            }
            # Remove None values
            relevant_context = {k: v for k, v in relevant_context.items() if v is not None}
            context_key = json.dumps(relevant_context, sort_keys=True)
        
        # Generate SHA-256 hash for consistent key
        combined = f"{normalized_text}|{context_key}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    async def get_cached_result(
        self, 
        text: str, 
        context: Optional[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """Get cached result with multi-tier lookup"""
        cache_key = self._generate_cache_key(text, context)
        self.cache_stats["total_requests"] += 1
        
        # TIER 1: Memory cache (fastest)
        memory_result = await self._get_from_memory_cache(cache_key)
        if memory_result:
            self.cache_stats["cache_hits"] += 1
            self.cache_stats["memory_hits"] += 1
            self._update_memory_access_order(cache_key)
            logger.debug(f"Memory cache hit for key: {cache_key}")
            return memory_result
        
        # TIER 2: Pattern cache (smart matching)
        pattern_result = await self._check_pattern_cache(text)
        if pattern_result:
            self.cache_stats["cache_hits"] += 1
            self.cache_stats["pattern_hits"] += 1
            # Store in memory cache for future access
            await self._store_in_memory_cache(cache_key, pattern_result)
            logger.debug(f"Pattern cache hit for text: {text[:50]}...")
            return pattern_result
        
        # TIER 3: MongoDB persistent cache
        mongodb_result = await self._get_from_mongodb_cache(cache_key)
        if mongodb_result:
            self.cache_stats["cache_hits"] += 1
            self.cache_stats["mongodb_hits"] += 1
            # Store in memory cache for future access
            await self._store_in_memory_cache(cache_key, mongodb_result)
            logger.debug(f"MongoDB cache hit for key: {cache_key}")
            return mongodb_result
        
        # Cache miss
        self.cache_stats["cache_misses"] += 1
        logger.debug(f"Cache miss for text: {text[:50]}...")
        return None
    
    async def _get_from_memory_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get result from in-memory cache"""
        return self.memory_cache.get(cache_key)
    
    async def _check_pattern_cache(self, text: str) -> Optional[Dict[str, Any]]:
        """Check pattern cache for similar texts"""
        # Simple pattern matching - could be enhanced with fuzzy matching
        text_lower = text.lower().strip()
        
        # Check for exact pattern matches
        for pattern, result in self.pattern_cache.items():
            if pattern in text_lower or text_lower in pattern:
                return result
        
        return None
    
    async def _get_from_mongodb_cache(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Get result from MongoDB cache"""
        if not self.is_connected:
            return None
        
        try:
            # Find cache entry that hasn't expired
            cache_doc = await self.cache_collection.find_one({
                "cache_key": cache_key,
                "expires_at": {"$gt": datetime.now()}
            })
            
            if cache_doc:
                # Update last accessed time
                await self.cache_collection.update_one(
                    {"_id": cache_doc["_id"]},
                    {"$set": {"last_accessed": datetime.now()}}
                )
                
                # Return cached data
                return cache_doc.get("cached_data")
            
        except Exception as e:
            logger.error(f"MongoDB cache retrieval failed: {e}")
        
        return None
    
    async def store_cached_result(
        self,
        text: str,
        context: Optional[Dict],
        result: Dict[str, Any],
        ttl: int = 3600
    ):
        """Store result in multi-tier cache with TTL"""
        cache_key = self._generate_cache_key(text, context)
        self.cache_stats["storage_operations"] += 1
        
        # TIER 1: Store in memory cache
        await self._store_in_memory_cache(cache_key, result)
        
        # TIER 2: Store in pattern cache
        await self._store_in_pattern_cache(text, result)
        
        # TIER 3: Store in MongoDB persistent cache
        await self._store_in_mongodb_cache(cache_key, text, context, result, ttl)
        
        # Manage cache sizes
        await self._manage_cache_sizes()
    
    async def _store_in_memory_cache(self, cache_key: str, result: Dict[str, Any]):
        """Store result in memory cache"""
        self.memory_cache[cache_key] = result
        self._update_memory_access_order(cache_key)
    
    async def _store_in_pattern_cache(self, text: str, result: Dict[str, Any]):
        """Store pattern for future similarity matching"""
        text_pattern = text.lower().strip()[:100]  # First 100 chars as pattern
        self.pattern_cache[text_pattern] = result
    
    async def _store_in_mongodb_cache(
        self,
        cache_key: str,
        text: str,
        context: Optional[Dict],
        result: Dict[str, Any],
        ttl: int
    ):
        """Store result in MongoDB cache"""
        if not self.is_connected:
            return
        
        try:
            expires_at = datetime.now() + timedelta(seconds=ttl)
            
            cache_doc = {
                "cache_key": cache_key,
                "original_text": text[:500],  # Store first 500 chars for debugging
                "context": context,
                "cached_data": result,
                "cache_type": "intent_classification",
                "created_at": datetime.now(),
                "last_accessed": datetime.now(),
                "expires_at": expires_at,
                "ttl_seconds": ttl
            }
            
            # Upsert cache document
            await self.cache_collection.update_one(
                {"cache_key": cache_key},
                {"$set": cache_doc},
                upsert=True
            )
            
        except Exception as e:
            logger.error(f"MongoDB cache storage failed: {e}")
    
    def _update_memory_access_order(self, cache_key: str):
        """Update LRU access order for memory cache"""
        # Remove from current position if exists
        if cache_key in self.cache_access_order:
            self.cache_access_order.remove(cache_key)
        
        # Add to end (most recent)
        self.cache_access_order.append(cache_key)
    
    async def _manage_cache_sizes(self):
        """Manage memory cache size using LRU eviction"""
        # Memory cache LRU management
        while len(self.memory_cache) > self.max_memory_cache_size:
            # Remove least recently used item
            if self.cache_access_order:
                lru_key = self.cache_access_order.popleft()
                self.memory_cache.pop(lru_key, None)
        
        # Pattern cache size management
        if len(self.pattern_cache) > 1000:
            # Remove oldest 20% of pattern cache
            items_to_remove = len(self.pattern_cache) // 5
            keys_to_remove = list(self.pattern_cache.keys())[:items_to_remove]
            for key in keys_to_remove:
                self.pattern_cache.pop(key, None)
    
    async def get_cache_statistics(self) -> Dict[str, Any]:
        """Get comprehensive cache statistics"""
        total_requests = max(self.cache_stats["total_requests"], 1)
        cache_hit_rate = (self.cache_stats["cache_hits"] / total_requests) * 100
        
        # Get MongoDB collection statistics
        mongodb_stats = 0
        mongodb_available = self.is_connected
        
        if self.is_connected:
            try:
                mongodb_stats = await self.cache_collection.estimated_document_count()
                # Test connection is still active
                await self.client.admin.command('ping')
                mongodb_available = True
            except Exception as e:
                logger.warning(f"MongoDB connection test failed: {e}")
                mongodb_available = False
                self.is_connected = False
        
        return {
            "cache_type": "mongodb_distributed",
            "total_requests": self.cache_stats["total_requests"],
            "cache_hits": self.cache_stats["cache_hits"],
            "cache_hit_rate_percentage": round(cache_hit_rate, 2),
            "memory_hits": self.cache_stats["memory_hits"],
            "pattern_hits": self.cache_stats["pattern_hits"],
            "mongodb_hits": self.cache_stats["mongodb_hits"],
            "cache_misses": self.cache_stats["cache_misses"],
            "memory_cache_size": len(self.memory_cache),
            "pattern_cache_size": len(self.pattern_cache),
            "mongodb_cache_size": mongodb_stats,
            "mongodb_connected": mongodb_available,
            "mongodb_available": mongodb_available,  # Ensure both keys are present
            "storage_operations": self.cache_stats["storage_operations"],
            "cleanup_operations": self.cache_stats["cleanup_operations"],
            "last_updated": datetime.now().isoformat()
        }
    
    async def cleanup_expired_cache(self) -> int:
        """Clean up expired cache entries (MongoDB handles this automatically with TTL)"""
        if not self.is_connected:
            return 0
        
        try:
            # MongoDB TTL indexes handle automatic cleanup, but we can manually clean if needed
            result = await self.cache_collection.delete_many({
                "expires_at": {"$lt": datetime.now()}
            })
            
            self.cache_stats["cleanup_operations"] += 1
            cleaned_count = result.deleted_count
            
            if cleaned_count > 0:
                logger.info(f"Manually cleaned up {cleaned_count} expired cache entries")
            
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Cache cleanup failed: {e}")
            return 0
    
    async def clear_all_cache(self):
        """Clear all cache data (for testing/maintenance)"""
        # Clear memory caches
        self.memory_cache.clear()
        self.pattern_cache.clear()
        self.cache_access_order.clear()
        
        # Clear MongoDB cache
        if self.is_connected:
            try:
                await self.cache_collection.delete_many({})
                logger.info("All MongoDB cache data cleared")
            except Exception as e:
                logger.error(f"Failed to clear MongoDB cache: {e}")
        
        # Reset statistics
        for key in self.cache_stats:
            self.cache_stats[key] = 0
    
    async def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            self.is_connected = False
            logger.info("MongoDB caching connection closed")


# Export the main class
__all__ = ["MongoDBCachingSystem"]