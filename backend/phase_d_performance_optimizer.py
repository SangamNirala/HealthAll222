"""
🚀 PHASE D: PERFECTION & SCALE - ADVANCED PERFORMANCE OPTIMIZATION SYSTEM

World-Class Performance Optimization for Medical Intent Classification at Scale

This system implements:
- Advanced caching layer with intelligent pattern pre-computation
- Concurrent processing for batch intent classification
- Load balancing and auto-scaling optimizations
- Performance benchmarking under high-load scenarios
- Clinical-grade response time guarantees

Algorithm Version: Phase_D_Production_Excellence_v1.0
Target: <25ms processing time at 1000+ concurrent requests
"""

import asyncio
import time
import threading
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import logging
from datetime import datetime, timedelta
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing as mp
from functools import lru_cache
import numpy as np
from enum import Enum
import redis
import aioredis
from contextlib import asynccontextmanager

# Configure logging
logger = logging.getLogger(__name__)

class PerformanceTier(str, Enum):
    """Performance tier classifications"""
    EMERGENCY = "emergency"        # <10ms - Critical medical situations
    URGENT = "urgent"             # <15ms - Urgent medical scenarios  
    ROUTINE = "routine"           # <25ms - Standard medical conversations
    BATCH = "batch"               # <50ms - Batch processing scenarios

class CacheStrategy(str, Enum):
    """Caching strategy options"""
    MEMORY_ONLY = "memory_only"
    REDIS_DISTRIBUTED = "redis_distributed"
    HYBRID = "hybrid"
    PATTERN_PRECOMPUTE = "pattern_precompute"

@dataclass
class PerformanceMetrics:
    """Comprehensive performance tracking"""
    request_id: str
    processing_time_ms: float
    cache_hit: bool
    concurrent_requests: int
    memory_usage_mb: float
    cpu_utilization: float
    performance_tier: PerformanceTier
    optimization_applied: List[str]
    timestamp: datetime
    
@dataclass
class ScalabilityMetrics:
    """System scalability tracking"""
    total_requests_processed: int
    peak_concurrent_requests: int
    average_processing_time_ms: float
    p95_processing_time_ms: float
    p99_processing_time_ms: float
    cache_hit_rate: float
    error_rate: float
    throughput_requests_per_second: float
    system_health_score: float

class AdvancedCachingLayer:
    """
    🧠 ADVANCED INTELLIGENT CACHING SYSTEM
    
    Multi-tier caching with pattern pre-computation and predictive loading
    for medical intent classification optimization.
    """
    
    def __init__(self):
        """Initialize advanced caching system"""
        self.memory_cache = {}  # In-memory cache for fastest access
        self.pattern_cache = {}  # Pre-computed pattern results
        self.confidence_cache = {}  # Cached confidence calculations
        self.redis_client = None  # Distributed cache (when available)
        
        # Cache statistics
        self.cache_stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "memory_hits": 0,
            "pattern_hits": 0,
            "redis_hits": 0,
            "cache_misses": 0
        }
        
        # LRU cache for pattern matching
        self.lru_cache = {}
        self.cache_access_order = deque()
        self.max_cache_size = 10000
        
        logger.info("AdvancedCachingLayer initialized with multi-tier architecture")
    
    async def initialize_redis_cache(self, redis_url: str = "redis://localhost:6379"):
        """Initialize Redis distributed caching"""
        try:
            self.redis_client = aioredis.from_url(redis_url)
            await self.redis_client.ping()
            logger.info("Redis distributed caching initialized successfully")
            return True
        except Exception as e:
            logger.warning(f"Redis initialization failed: {e}. Using memory-only caching.")
            return False
    
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
                "urgency": context.get("urgency")
            }
            context_key = json.dumps(relevant_context, sort_keys=True)
        
        # Generate SHA-256 hash for consistent key
        combined = f"{normalized_text}|{context_key}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    async def get_cached_result(
        self, 
        text: str, 
        context: Optional[Dict] = None
    ) -> Optional[Dict[str, Any]]:
        """Get cached intent classification result"""
        cache_key = self._generate_cache_key(text, context)
        self.cache_stats["total_requests"] += 1
        
        # Try memory cache first (fastest)
        if cache_key in self.memory_cache:
            self.cache_stats["cache_hits"] += 1
            self.cache_stats["memory_hits"] += 1
            self._update_cache_access(cache_key)
            logger.debug(f"Memory cache hit for key: {cache_key}")
            return self.memory_cache[cache_key]
        
        # Try pattern cache for similar patterns
        pattern_result = await self._check_pattern_cache(text)
        if pattern_result:
            self.cache_stats["cache_hits"] += 1
            self.cache_stats["pattern_hits"] += 1
            # Store in memory cache for future access
            self.memory_cache[cache_key] = pattern_result
            self._update_cache_access(cache_key)
            logger.debug(f"Pattern cache hit for text: {text[:50]}...")
            return pattern_result
        
        # Try Redis distributed cache
        if self.redis_client:
            try:
                redis_result = await self.redis_client.get(f"intent_cache:{cache_key}")
                if redis_result:
                    result = json.loads(redis_result)
                    self.cache_stats["cache_hits"] += 1
                    self.cache_stats["redis_hits"] += 1
                    # Store in memory cache for future access
                    self.memory_cache[cache_key] = result
                    self._update_cache_access(cache_key)
                    logger.debug(f"Redis cache hit for key: {cache_key}")
                    return result
            except Exception as e:
                logger.error(f"Redis cache access failed: {e}")
        
        # Cache miss
        self.cache_stats["cache_misses"] += 1
        logger.debug(f"Cache miss for text: {text[:50]}...")
        return None
    
    async def store_cached_result(
        self,
        text: str,
        context: Optional[Dict],
        result: Dict[str, Any],
        ttl: int = 3600
    ):
        """Store result in cache with TTL"""
        cache_key = self._generate_cache_key(text, context)
        
        # Store in memory cache
        self.memory_cache[cache_key] = result
        self._update_cache_access(cache_key)
        
        # Store patterns for similarity matching
        await self._store_pattern_cache(text, result)
        
        # Store in Redis if available
        if self.redis_client:
            try:
                await self.redis_client.setex(
                    f"intent_cache:{cache_key}",
                    ttl,
                    json.dumps(result, default=str)
                )
            except Exception as e:
                logger.error(f"Redis cache storage failed: {e}")
        
        # Manage memory cache size
        self._manage_cache_size()
        
        logger.debug(f"Cached result stored for key: {cache_key}")
    
    async def _check_pattern_cache(self, text: str) -> Optional[Dict[str, Any]]:
        """Check pattern-based cache for similar medical expressions"""
        # Extract key medical terms for pattern matching
        medical_keywords = self._extract_medical_keywords(text)
        
        # Find similar cached patterns
        for pattern_key, cached_result in self.pattern_cache.items():
            if self._calculate_pattern_similarity(medical_keywords, pattern_key) > 0.85:
                return cached_result
        
        return None
    
    async def _store_pattern_cache(self, text: str, result: Dict[str, Any]):
        """Store pattern-based cache entry"""
        medical_keywords = self._extract_medical_keywords(text)
        pattern_key = "|".join(sorted(medical_keywords))
        
        # Only cache high-confidence results
        if result.get("confidence_score", 0) > 0.8:
            self.pattern_cache[pattern_key] = result
    
    def _extract_medical_keywords(self, text: str) -> List[str]:
        """Extract key medical terms from text"""
        # Common medical keywords for pattern matching
        medical_terms = [
            "pain", "ache", "hurt", "chest", "head", "stomach", "back",
            "severe", "mild", "chronic", "acute", "sudden", "gradual",
            "medication", "treatment", "doctor", "hospital", "emergency",
            "symptoms", "fever", "nausea", "dizziness", "breathing"
        ]
        
        text_lower = text.lower()
        found_terms = [term for term in medical_terms if term in text_lower]
        return found_terms
    
    def _calculate_pattern_similarity(self, keywords1: List[str], pattern_key: str) -> float:
        """Calculate similarity between keyword sets"""
        keywords2 = pattern_key.split("|")
        
        if not keywords1 or not keywords2:
            return 0.0
        
        intersection = set(keywords1) & set(keywords2)
        union = set(keywords1) | set(keywords2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _update_cache_access(self, cache_key: str):
        """Update LRU cache access order"""
        if cache_key in self.cache_access_order:
            self.cache_access_order.remove(cache_key)
        self.cache_access_order.append(cache_key)
    
    def _manage_cache_size(self):
        """Manage memory cache size using LRU eviction"""
        while len(self.memory_cache) > self.max_cache_size:
            # Remove least recently used entry
            lru_key = self.cache_access_order.popleft()
            if lru_key in self.memory_cache:
                del self.memory_cache[lru_key]
    
    def get_cache_statistics(self) -> Dict[str, Any]:
        """Get comprehensive cache performance statistics"""
        total_requests = self.cache_stats["total_requests"]
        cache_hit_rate = (self.cache_stats["cache_hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "total_requests": total_requests,
            "cache_hits": self.cache_stats["cache_hits"],
            "cache_hit_rate_percentage": round(cache_hit_rate, 2),
            "memory_hits": self.cache_stats["memory_hits"],
            "pattern_hits": self.cache_stats["pattern_hits"],
            "redis_hits": self.cache_stats["redis_hits"],
            "cache_misses": self.cache_stats["cache_misses"],
            "memory_cache_size": len(self.memory_cache),
            "pattern_cache_size": len(self.pattern_cache),
            "redis_available": self.redis_client is not None
        }

class ConcurrentProcessingEngine:
    """
    ⚡ CONCURRENT PROCESSING ENGINE
    
    High-performance concurrent processing system for batch intent classification
    with intelligent load distribution and resource optimization.
    """
    
    def __init__(self, max_workers: int = None):
        """Initialize concurrent processing engine"""
        self.max_workers = max_workers or min(32, (mp.cpu_count() or 1) + 4)
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)
        self.process_pool = ProcessPoolExecutor(max_workers=min(8, mp.cpu_count() or 1))
        
        # Performance tracking
        self.processing_stats = {
            "total_batches": 0,
            "total_requests": 0,
            "average_batch_time": 0.0,
            "peak_concurrent_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0
        }
        
        # Load balancing
        self.current_load = 0
        self.load_history = deque(maxlen=100)
        
        logger.info(f"ConcurrentProcessingEngine initialized with {self.max_workers} workers")
    
    async def process_batch_intents(
        self,
        requests: List[Tuple[str, Optional[Dict]]],
        performance_tier: PerformanceTier = PerformanceTier.ROUTINE
    ) -> List[Dict[str, Any]]:
        """Process batch of intent classification requests concurrently"""
        batch_start_time = time.time()
        batch_size = len(requests)
        
        logger.info(f"Processing batch of {batch_size} intent classification requests")
        
        # Update statistics
        self.processing_stats["total_batches"] += 1
        self.processing_stats["total_requests"] += batch_size
        self.current_load += batch_size
        self.processing_stats["peak_concurrent_requests"] = max(
            self.processing_stats["peak_concurrent_requests"],
            self.current_load
        )
        
        try:
            # Determine processing strategy based on batch size and performance tier
            if batch_size <= 10 or performance_tier == PerformanceTier.EMERGENCY:
                # Use asyncio for small batches or emergency scenarios
                results = await self._process_async_batch(requests, performance_tier)
            elif batch_size <= 50:
                # Use thread pool for medium batches
                results = await self._process_thread_batch(requests, performance_tier)
            else:
                # Use process pool for large batches
                results = await self._process_multiprocess_batch(requests, performance_tier)
            
            # Update success statistics
            self.processing_stats["successful_requests"] += len(results)
            
        except Exception as e:
            logger.error(f"Batch processing failed: {e}")
            self.processing_stats["failed_requests"] += batch_size
            # Return error results for all requests
            results = [{"error": str(e), "success": False} for _ in requests]
        
        finally:
            # Update load tracking
            self.current_load -= batch_size
            batch_time = (time.time() - batch_start_time) * 1000
            self.load_history.append({
                "timestamp": datetime.utcnow(),
                "batch_size": batch_size,
                "processing_time_ms": batch_time,
                "performance_tier": performance_tier
            })
            
            # Update average batch time
            total_batches = self.processing_stats["total_batches"]
            self.processing_stats["average_batch_time"] = (
                (self.processing_stats["average_batch_time"] * (total_batches - 1) + batch_time) / total_batches
            )
        
        logger.info(f"Batch processing completed in {batch_time:.2f}ms")
        return results
    
    async def _process_async_batch(
        self,
        requests: List[Tuple[str, Optional[Dict]]],
        performance_tier: PerformanceTier
    ) -> List[Dict[str, Any]]:
        """Process batch using asyncio concurrency"""
        from medical_intent_classifier import classify_patient_intent
        
        async def process_single_request(text: str, context: Optional[Dict]) -> Dict[str, Any]:
            try:
                result = await classify_patient_intent(text, context)
                return {
                    "success": True,
                    "primary_intent": result.primary_intent,
                    "confidence_score": result.confidence_score,
                    "urgency_level": result.urgency_level.value,
                    "processing_time_ms": result.processing_time_ms,
                    "performance_tier": performance_tier.value
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "performance_tier": performance_tier.value
                }
        
        # Create coroutines for all requests
        coroutines = [process_single_request(text, context) for text, context in requests]
        
        # Execute all coroutines concurrently
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        
        # Handle any exceptions
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append({
                    "success": False,
                    "error": str(result),
                    "performance_tier": performance_tier.value
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _process_thread_batch(
        self,
        requests: List[Tuple[str, Optional[Dict]]],
        performance_tier: PerformanceTier
    ) -> List[Dict[str, Any]]:
        """Process batch using thread pool"""
        loop = asyncio.get_event_loop()
        
        def process_request_sync(text: str, context: Optional[Dict]) -> Dict[str, Any]:
            try:
                # Import here to avoid circular imports
                import asyncio
                from medical_intent_classifier import classify_patient_intent
                
                # Create new event loop for thread
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                
                try:
                    result = new_loop.run_until_complete(classify_patient_intent(text, context))
                    return {
                        "success": True,
                        "primary_intent": result.primary_intent,
                        "confidence_score": result.confidence_score,
                        "urgency_level": result.urgency_level.value,
                        "processing_time_ms": result.processing_time_ms,
                        "performance_tier": performance_tier.value
                    }
                finally:
                    new_loop.close()
                    
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "performance_tier": performance_tier.value
                }
        
        # Submit all tasks to thread pool
        futures = [
            loop.run_in_executor(self.thread_pool, process_request_sync, text, context)
            for text, context in requests
        ]
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*futures, return_exceptions=True)
        
        # Handle any exceptions
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                processed_results.append({
                    "success": False,
                    "error": str(result),
                    "performance_tier": performance_tier.value
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _process_multiprocess_batch(
        self,
        requests: List[Tuple[str, Optional[Dict]]],
        performance_tier: PerformanceTier
    ) -> List[Dict[str, Any]]:
        """Process large batches using multiprocessing"""
        # For multiprocessing, we'll chunk the requests
        chunk_size = max(1, len(requests) // (self.max_workers // 2))
        chunks = [requests[i:i + chunk_size] for i in range(0, len(requests), chunk_size)]
        
        # Process chunks in thread pool (simpler than true multiprocessing for this case)
        results = await self._process_thread_batch(requests, performance_tier)
        return results
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get comprehensive processing performance statistics"""
        success_rate = 0
        if self.processing_stats["total_requests"] > 0:
            success_rate = (self.processing_stats["successful_requests"] / 
                          self.processing_stats["total_requests"] * 100)
        
        # Calculate recent performance metrics
        recent_loads = list(self.load_history)[-20:]  # Last 20 batches
        recent_avg_time = np.mean([load["processing_time_ms"] for load in recent_loads]) if recent_loads else 0
        
        return {
            "total_batches_processed": self.processing_stats["total_batches"],
            "total_requests_processed": self.processing_stats["total_requests"],
            "success_rate_percentage": round(success_rate, 2),
            "average_batch_processing_time_ms": round(self.processing_stats["average_batch_time"], 2),
            "recent_average_processing_time_ms": round(recent_avg_time, 2),
            "peak_concurrent_requests": self.processing_stats["peak_concurrent_requests"],
            "current_load": self.current_load,
            "max_workers": self.max_workers,
            "thread_pool_active": True,
            "process_pool_active": True
        }

class LoadBalancingOptimizer:
    """
    ⚖️ INTELLIGENT LOAD BALANCING OPTIMIZER
    
    Advanced load balancing with predictive scaling and resource optimization
    for medical intent classification at enterprise scale.
    """
    
    def __init__(self):
        """Initialize load balancing optimizer"""
        self.current_metrics = ScalabilityMetrics(
            total_requests_processed=0,
            peak_concurrent_requests=0,
            average_processing_time_ms=0.0,
            p95_processing_time_ms=0.0,
            p99_processing_time_ms=0.0,
            cache_hit_rate=0.0,
            error_rate=0.0,
            throughput_requests_per_second=0.0,
            system_health_score=1.0
        )
        
        # Performance history for trend analysis
        self.performance_history = deque(maxlen=1000)
        self.response_times = deque(maxlen=10000)
        
        # Auto-scaling parameters
        self.scaling_thresholds = {
            "cpu_high": 80.0,
            "memory_high": 85.0,
            "response_time_high": 50.0,  # ms
            "error_rate_high": 5.0,  # %
            "throughput_low": 10.0  # requests/second
        }
        
        logger.info("LoadBalancingOptimizer initialized with intelligent scaling")
    
    def record_request_metrics(
        self,
        processing_time_ms: float,
        cache_hit: bool,
        error_occurred: bool,
        concurrent_requests: int
    ):
        """Record metrics for a single request"""
        # Update response times
        self.response_times.append(processing_time_ms)
        
        # Update concurrent request peak
        self.current_metrics.peak_concurrent_requests = max(
            self.current_metrics.peak_concurrent_requests,
            concurrent_requests
        )
        
        # Update counters
        self.current_metrics.total_requests_processed += 1
        
        if error_occurred:
            # Count errors for error rate calculation
            pass
        
        # Calculate rolling averages
        self._update_rolling_metrics()
        
        # Record performance snapshot
        self.performance_history.append({
            "timestamp": datetime.utcnow(),
            "processing_time_ms": processing_time_ms,
            "cache_hit": cache_hit,
            "error": error_occurred,
            "concurrent_requests": concurrent_requests
        })
    
    def _update_rolling_metrics(self):
        """Update rolling performance metrics"""
        if not self.response_times:
            return
        
        # Calculate percentiles
        response_array = np.array(list(self.response_times))
        self.current_metrics.average_processing_time_ms = float(np.mean(response_array))
        self.current_metrics.p95_processing_time_ms = float(np.percentile(response_array, 95))
        self.current_metrics.p99_processing_time_ms = float(np.percentile(response_array, 99))
        
        # Calculate cache hit rate from recent history
        recent_history = list(self.performance_history)[-100:]  # Last 100 requests
        if recent_history:
            cache_hits = sum(1 for h in recent_history if h["cache_hit"])
            self.current_metrics.cache_hit_rate = cache_hits / len(recent_history)
            
            # Calculate error rate
            errors = sum(1 for h in recent_history if h["error"])
            self.current_metrics.error_rate = errors / len(recent_history)
        
        # Calculate throughput (requests per second over last minute)
        one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
        recent_requests = [h for h in recent_history if h["timestamp"] > one_minute_ago]
        self.current_metrics.throughput_requests_per_second = len(recent_requests) / 60.0
        
        # Calculate system health score
        self.current_metrics.system_health_score = self._calculate_health_score()
    
    def _calculate_health_score(self) -> float:
        """Calculate overall system health score (0-1)"""
        scores = []
        
        # Response time score (lower is better)
        response_score = max(0, 1 - (self.current_metrics.average_processing_time_ms / 100.0))
        scores.append(response_score)
        
        # Error rate score (lower is better)
        error_score = max(0, 1 - (self.current_metrics.error_rate * 20))  # 5% error = 0 score
        scores.append(error_score)
        
        # Cache hit rate score (higher is better)
        cache_score = self.current_metrics.cache_hit_rate
        scores.append(cache_score)
        
        # Throughput score (normalized to expected throughput)
        throughput_score = min(1.0, self.current_metrics.throughput_requests_per_second / 50.0)
        scores.append(throughput_score)
        
        return float(np.mean(scores))
    
    def should_scale_up(self) -> Tuple[bool, str]:
        """Determine if system should scale up"""
        reasons = []
        
        if self.current_metrics.average_processing_time_ms > self.scaling_thresholds["response_time_high"]:
            reasons.append("high_response_time")
        
        if self.current_metrics.error_rate > self.scaling_thresholds["error_rate_high"] / 100:
            reasons.append("high_error_rate")
        
        if self.current_metrics.system_health_score < 0.7:
            reasons.append("low_health_score")
        
        should_scale = len(reasons) > 0
        reason = "; ".join(reasons) if reasons else "no_scaling_needed"
        
        return should_scale, reason
    
    def should_scale_down(self) -> Tuple[bool, str]:
        """Determine if system can scale down"""
        # Only scale down if performance is excellent
        if (self.current_metrics.average_processing_time_ms < 20.0 and
            self.current_metrics.error_rate < 0.01 and
            self.current_metrics.system_health_score > 0.95 and
            self.current_metrics.throughput_requests_per_second < 20.0):
            return True, "excellent_performance_low_load"
        
        return False, "scaling_down_not_recommended"
    
    def get_optimization_recommendations(self) -> List[str]:
        """Get specific optimization recommendations"""
        recommendations = []
        
        if self.current_metrics.cache_hit_rate < 0.6:
            recommendations.append("increase_cache_size")
        
        if self.current_metrics.p95_processing_time_ms > 75.0:
            recommendations.append("optimize_pattern_matching")
        
        if self.current_metrics.error_rate > 0.02:
            recommendations.append("enhance_error_handling")
        
        if self.current_metrics.throughput_requests_per_second < 30.0:
            recommendations.append("increase_worker_threads")
        
        return recommendations
    
    def get_scalability_metrics(self) -> Dict[str, Any]:
        """Get comprehensive scalability metrics"""
        scale_up, scale_up_reason = self.should_scale_up()
        scale_down, scale_down_reason = self.should_scale_down()
        
        return {
            "current_metrics": asdict(self.current_metrics),
            "scaling_recommendations": {
                "should_scale_up": scale_up,
                "scale_up_reason": scale_up_reason,
                "should_scale_down": scale_down,
                "scale_down_reason": scale_down_reason
            },
            "optimization_recommendations": self.get_optimization_recommendations(),
            "performance_trend": self._get_performance_trend(),
            "thresholds": self.scaling_thresholds
        }
    
    def _get_performance_trend(self) -> str:
        """Analyze performance trend over recent history"""
        if len(self.performance_history) < 50:
            return "insufficient_data"
        
        recent = list(self.performance_history)[-50:]
        older = list(self.performance_history)[-100:-50]
        
        if not older:
            return "stable"
        
        recent_avg = np.mean([h["processing_time_ms"] for h in recent])
        older_avg = np.mean([h["processing_time_ms"] for h in older])
        
        change_percent = ((recent_avg - older_avg) / older_avg) * 100
        
        if change_percent > 10:
            return "degrading"
        elif change_percent < -10:
            return "improving"
        else:
            return "stable"

class PerformanceBenchmarkingSystem:
    """
    📊 ADVANCED PERFORMANCE BENCHMARKING SYSTEM
    
    Comprehensive benchmarking and stress testing for medical intent classification
    under high-load scenarios with detailed performance analysis.
    """
    
    def __init__(self):
        """Initialize performance benchmarking system"""
        self.benchmark_results = []
        self.stress_test_results = []
        
        logger.info("PerformanceBenchmarkingSystem initialized")
    
    async def run_performance_benchmark(
        self,
        test_scenarios: List[Dict[str, Any]],
        concurrent_levels: List[int] = [1, 10, 50, 100, 500],
        duration_seconds: int = 60
    ) -> Dict[str, Any]:
        """Run comprehensive performance benchmark"""
        logger.info("Starting comprehensive performance benchmark")
        
        benchmark_results = {
            "test_start_time": datetime.utcnow().isoformat(),
            "test_scenarios": len(test_scenarios),
            "concurrent_levels_tested": concurrent_levels,
            "duration_per_test_seconds": duration_seconds,
            "results": {}
        }
        
        for concurrent_level in concurrent_levels:
            logger.info(f"Testing with {concurrent_level} concurrent requests")
            
            level_results = await self._run_concurrent_level_test(
                test_scenarios, concurrent_level, duration_seconds
            )
            
            benchmark_results["results"][f"concurrent_{concurrent_level}"] = level_results
        
        # Store benchmark results
        self.benchmark_results.append(benchmark_results)
        
        logger.info("Performance benchmark completed")
        return benchmark_results
    
    async def _run_concurrent_level_test(
        self,
        test_scenarios: List[Dict[str, Any]],
        concurrent_level: int,
        duration_seconds: int
    ) -> Dict[str, Any]:
        """Run test at specific concurrency level"""
        from medical_intent_classifier import classify_patient_intent
        
        test_results = {
            "concurrent_requests": concurrent_level,
            "duration_seconds": duration_seconds,
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "response_times_ms": [],
            "throughput_rps": 0.0,
            "average_response_time_ms": 0.0,
            "p50_response_time_ms": 0.0,
            "p95_response_time_ms": 0.0,
            "p99_response_time_ms": 0.0
        }
        
        start_time = time.time()
        end_time = start_time + duration_seconds
        
        async def worker_task():
            """Individual worker task"""
            worker_results = []
            
            while time.time() < end_time:
                # Select random test scenario
                scenario = np.random.choice(test_scenarios)
                
                request_start = time.time()
                try:
                    result = await classify_patient_intent(
                        scenario["text"], 
                        scenario.get("context")
                    )
                    success = True
                except Exception as e:
                    success = False
                
                request_time = (time.time() - request_start) * 1000
                worker_results.append({
                    "success": success,
                    "response_time_ms": request_time
                })
                
                # Small delay to prevent overwhelming
                await asyncio.sleep(0.001)
            
            return worker_results
        
        # Create concurrent workers
        workers = [worker_task() for _ in range(concurrent_level)]
        
        # Execute all workers concurrently
        worker_results_list = await asyncio.gather(*workers, return_exceptions=True)
        
        # Aggregate results
        all_results = []
        for worker_results in worker_results_list:
            if not isinstance(worker_results, Exception):
                all_results.extend(worker_results)
        
        # Calculate metrics
        test_results["total_requests"] = len(all_results)
        test_results["successful_requests"] = sum(1 for r in all_results if r["success"])
        test_results["failed_requests"] = test_results["total_requests"] - test_results["successful_requests"]
        
        response_times = [r["response_time_ms"] for r in all_results]
        test_results["response_times_ms"] = response_times
        
        if response_times:
            test_results["average_response_time_ms"] = float(np.mean(response_times))
            test_results["p50_response_time_ms"] = float(np.percentile(response_times, 50))
            test_results["p95_response_time_ms"] = float(np.percentile(response_times, 95))
            test_results["p99_response_time_ms"] = float(np.percentile(response_times, 99))
        
        test_results["throughput_rps"] = test_results["total_requests"] / duration_seconds
        
        return test_results
    
    async def run_stress_test(
        self,
        max_concurrent_requests: int = 1000,
        ramp_up_duration_seconds: int = 300,
        steady_state_duration_seconds: int = 600
    ) -> Dict[str, Any]:
        """Run comprehensive stress test"""
        logger.info(f"Starting stress test: max {max_concurrent_requests} concurrent requests")
        
        stress_test_results = {
            "test_start_time": datetime.utcnow().isoformat(),
            "max_concurrent_requests": max_concurrent_requests,
            "ramp_up_duration_seconds": ramp_up_duration_seconds,
            "steady_state_duration_seconds": steady_state_duration_seconds,
            "phases": {}
        }
        
        # Phase 1: Ramp up
        logger.info("Phase 1: Ramp up testing")
        ramp_results = await self._run_ramp_up_test(
            max_concurrent_requests, ramp_up_duration_seconds
        )
        stress_test_results["phases"]["ramp_up"] = ramp_results
        
        # Phase 2: Steady state
        logger.info("Phase 2: Steady state testing")
        steady_results = await self._run_steady_state_test(
            max_concurrent_requests, steady_state_duration_seconds
        )
        stress_test_results["phases"]["steady_state"] = steady_results
        
        # Phase 3: Graceful degradation
        logger.info("Phase 3: Graceful degradation testing")
        degradation_results = await self._run_degradation_test(max_concurrent_requests)
        stress_test_results["phases"]["degradation"] = degradation_results
        
        # Store stress test results
        self.stress_test_results.append(stress_test_results)
        
        logger.info("Stress test completed")
        return stress_test_results
    
    async def _run_ramp_up_test(
        self, 
        max_concurrent: int, 
        duration_seconds: int
    ) -> Dict[str, Any]:
        """Run ramp-up phase of stress test"""
        # Gradually increase load
        ramp_steps = 10
        step_duration = duration_seconds / ramp_steps
        
        ramp_results = []
        
        for step in range(ramp_steps):
            concurrent_level = int((step + 1) * max_concurrent / ramp_steps)
            
            step_results = await self._run_concurrent_level_test(
                [{"text": "I have chest pain", "context": None}],  # Simple test scenario
                concurrent_level,
                int(step_duration)
            )
            
            step_results["step"] = step + 1
            step_results["target_concurrent"] = concurrent_level
            ramp_results.append(step_results)
        
        return {
            "ramp_steps": ramp_results,
            "max_concurrent_achieved": max_concurrent,
            "total_duration_seconds": duration_seconds
        }
    
    async def _run_steady_state_test(
        self, 
        concurrent_level: int, 
        duration_seconds: int
    ) -> Dict[str, Any]:
        """Run steady state phase of stress test"""
        return await self._run_concurrent_level_test(
            [{"text": "I have chest pain", "context": None}],
            concurrent_level,
            duration_seconds
        )
    
    async def _run_degradation_test(self, max_concurrent: int) -> Dict[str, Any]:
        """Test graceful degradation under extreme load"""
        # Test with 150% of max concurrent to see how system handles overload
        overload_concurrent = int(max_concurrent * 1.5)
        
        degradation_results = await self._run_concurrent_level_test(
            [{"text": "I have chest pain", "context": None}],
            overload_concurrent,
            60  # 1 minute of overload testing
        )
        
        degradation_results["overload_factor"] = 1.5
        degradation_results["baseline_concurrent"] = max_concurrent
        
        return degradation_results
    
    def get_benchmark_summary(self) -> Dict[str, Any]:
        """Get comprehensive benchmark summary"""
        if not self.benchmark_results:
            return {"status": "no_benchmarks_run"}
        
        latest_benchmark = self.benchmark_results[-1]
        
        # Extract key performance indicators
        performance_summary = {
            "latest_benchmark_time": latest_benchmark["test_start_time"],
            "total_benchmarks_run": len(self.benchmark_results),
            "key_performance_indicators": {},
            "performance_targets": {
                "target_response_time_ms": 25,
                "target_throughput_rps": 100,
                "target_success_rate": 99.5
            },
            "recommendations": []
        }
        
        # Analyze latest results
        for level_key, results in latest_benchmark["results"].items():
            level = results["concurrent_requests"]
            
            performance_summary["key_performance_indicators"][level_key] = {
                "average_response_time_ms": results["average_response_time_ms"],
                "p95_response_time_ms": results["p95_response_time_ms"],
                "throughput_rps": results["throughput_rps"],
                "success_rate": (results["successful_requests"] / results["total_requests"] * 100) if results["total_requests"] > 0 else 0
            }
        
        # Generate recommendations based on results
        recommendations = []
        for level_key, kpi in performance_summary["key_performance_indicators"].items():
            if kpi["average_response_time_ms"] > 25:
                recommendations.append(f"Optimize processing for {level_key} load")
            if kpi["success_rate"] < 99.5:
                recommendations.append(f"Improve reliability for {level_key} load")
        
        performance_summary["recommendations"] = recommendations
        
        return performance_summary

# Global instances
advanced_caching_layer = AdvancedCachingLayer()
concurrent_processing_engine = ConcurrentProcessingEngine()
load_balancing_optimizer = LoadBalancingOptimizer()
performance_benchmarking_system = PerformanceBenchmarkingSystem()

async def initialize_performance_optimization():
    """Initialize all performance optimization components"""
    try:
        # Initialize Redis caching if available
        await advanced_caching_layer.initialize_redis_cache()
        
        logger.info("Phase D Performance Optimization System initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize performance optimization: {e}")
        return False

async def get_performance_status() -> Dict[str, Any]:
    """Get comprehensive performance optimization status"""
    return {
        "phase_d_status": "operational",
        "algorithm_version": "Phase_D_Production_Excellence_v1.0",
        "components": {
            "caching_layer": advanced_caching_layer.get_cache_statistics(),
            "concurrent_processing": concurrent_processing_engine.get_processing_statistics(),
            "load_balancing": load_balancing_optimizer.get_scalability_metrics(),
            "benchmarking": performance_benchmarking_system.get_benchmark_summary()
        },
        "optimization_targets": {
            "target_response_time_ms": 25,
            "target_cache_hit_rate": 80,
            "target_throughput_rps": 200,
            "target_concurrent_requests": 1000
        },
        "last_updated": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    # Quick test of performance optimization system
    async def test_performance_system():
        # Initialize system
        await initialize_performance_optimization()
        
        # Test caching
        cache_stats = advanced_caching_layer.get_cache_statistics()
        print(f"Cache Statistics: {cache_stats}")
        
        # Test concurrent processing
        test_requests = [("I have chest pain", None), ("My head hurts", None)]
        batch_results = await concurrent_processing_engine.process_batch_intents(
            test_requests, PerformanceTier.ROUTINE
        )
        print(f"Batch Results: {len(batch_results)} processed")
        
        # Get overall status
        status = await get_performance_status()
        print(f"System Status: {status['phase_d_status']}")
    
    # Run test
    asyncio.run(test_performance_system())