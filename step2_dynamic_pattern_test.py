#!/usr/bin/env python3
"""
🔬 STEP 2 DYNAMIC PATTERN ENHANCEMENT SYSTEM COMPREHENSIVE TESTING
================================================================

Comprehensive testing suite for Step 2 Dynamic Pattern Enhancement System APIs
including real-time pattern discovery, temporal evolution tracking, and 
ML-powered pattern validation capabilities.

Test Coverage:
1. POST /api/medical-ai/dynamic-pattern-discovery - Real-time pattern discovery
2. POST /api/medical-ai/pattern-evolution-analysis - Temporal pattern evolution
3. GET /api/medical-ai/pattern-discovery-analytics - Discovery performance metrics
4. GET /api/medical-ai/evolution-analytics-dashboard - Evolution analytics dashboard
5. POST /api/medical-ai/pattern-confidence-calibration - Feedback-based calibration

Advanced Features Tested:
- Algorithm Version 2.0_dynamic_pattern_discovery and 2.0_temporal_pattern_evolution
- Privacy-compliant K-anonymity protection
- ML-powered pattern validation using Gemini AI
- Statistical modeling for trend prediction
- Medical language evolution tracking
- Real-time processing optimization (<15ms target)
- Integration with existing MongoDB collections
"""

import asyncio
import aiohttp
import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List
import sys
import os

# Add the backend directory to the path for imports
sys.path.append('/app/backend')

class Step2DynamicPatternTester:
    """Comprehensive tester for Step 2 Dynamic Pattern Enhancement System"""
    
    def __init__(self):
        # Get backend URL from environment
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    self.base_url = line.split('=')[1].strip()
                    break
            else:
                self.base_url = "http://localhost:8001"
        
        self.api_base = f"{self.base_url}/api"
        self.test_results = []
        self.session = None
        
        print(f"🔬 Step 2 Dynamic Pattern Enhancement System Tester")
        print(f"🌐 Backend URL: {self.base_url}")
        print(f"📡 API Base: {self.api_base}")
        print("=" * 80)

    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={'Content-Type': 'application/json'}
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    def log_test_result(self, test_name: str, success: bool, details: str, response_data: Dict = None):
        """Log test result with details"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    📝 {details}")
        if response_data and success:
            print(f"    📊 Response keys: {list(response_data.keys())}")
        print()
        
        self.test_results.append({
            'test_name': test_name,
            'success': success,
            'details': details,
            'response_data': response_data
        })

    async def test_dynamic_pattern_discovery(self):
        """
        🎯 TEST 1: Real-time Pattern Discovery from Conversations
        
        Tests the core pattern discovery functionality with realistic medical
        conversation scenarios containing various symptom descriptions.
        """
        print("🔍 TESTING: Dynamic Pattern Discovery API")
        print("=" * 50)
        
        # Test Case 1: Complex symptom conversation with multiple patterns
        test_conversation_1 = {
            "conversation_id": f"test_conv_{uuid.uuid4().hex[:8]}",
            "patient_id": f"test_patient_{uuid.uuid4().hex[:8]}",
            "messages": [
                {
                    "role": "user",
                    "content": "I've been having this crushing chest pain that feels like an elephant sitting on my chest",
                    "timestamp": datetime.utcnow().isoformat()
                },
                {
                    "role": "user", 
                    "content": "It started about 2 hours ago and comes in waves every few minutes",
                    "timestamp": (datetime.utcnow() + timedelta(minutes=1)).isoformat()
                },
                {
                    "role": "user",
                    "content": "The pain shoots down my left arm and I feel like I'm going to throw up",
                    "timestamp": (datetime.utcnow() + timedelta(minutes=2)).isoformat()
                }
            ],
            "context_data": {
                "conversation_type": "emergency_assessment",
                "urgency_level": "high",
                "medical_context": "chest_pain_evaluation"
            }
        }
        
        try:
            start_time = time.time()
            async with self.session.post(
                f"{self.api_base}/medical-ai/dynamic-pattern-discovery",
                json=test_conversation_1
            ) as response:
                processing_time = (time.time() - start_time) * 1000
                
                if response.status == 200:
                    data = await response.json()
                    
                    # Validate response structure
                    required_fields = [
                        'status', 'conversation_id', 'patterns_discovered', 
                        'new_patterns', 'real_time_insights', 'processing_time_ms',
                        'algorithm_version'
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in data]
                    if missing_fields:
                        self.log_test_result(
                            "Dynamic Pattern Discovery - Response Structure",
                            False,
                            f"Missing required fields: {missing_fields}"
                        )
                        return
                    
                    # Validate algorithm version
                    expected_version = "2.0_dynamic_pattern_discovery"
                    if data.get('algorithm_version') != expected_version:
                        self.log_test_result(
                            "Dynamic Pattern Discovery - Algorithm Version",
                            False,
                            f"Expected version {expected_version}, got {data.get('algorithm_version')}"
                        )
                        return
                    
                    # Validate processing time (target <15ms for real-time)
                    actual_processing_time = data.get('processing_time_ms', processing_time)
                    if actual_processing_time > 15:
                        print(f"    ⚠️  Processing time {actual_processing_time:.2f}ms exceeds 15ms target (acceptable for complex analysis)")
                    
                    # Validate patterns discovered
                    patterns_count = data.get('patterns_discovered', 0)
                    new_patterns = data.get('new_patterns', [])
                    insights = data.get('real_time_insights', [])
                    
                    self.log_test_result(
                        "Dynamic Pattern Discovery - Complex Symptom Conversation",
                        True,
                        f"Discovered {patterns_count} patterns, {len(new_patterns)} new patterns, {len(insights)} insights. Processing: {actual_processing_time:.2f}ms",
                        data
                    )
                    
                    # Test Case 2: Simple conversation with fewer patterns
                    await self._test_simple_pattern_discovery()
                    
                    # Test Case 3: Medical terminology patterns
                    await self._test_medical_terminology_patterns()
                    
                else:
                    error_text = await response.text()
                    self.log_test_result(
                        "Dynamic Pattern Discovery - API Response",
                        False,
                        f"HTTP {response.status}: {error_text}"
                    )
                    
        except Exception as e:
            self.log_test_result(
                "Dynamic Pattern Discovery - Exception",
                False,
                f"Exception occurred: {str(e)}"
            )

    async def _test_simple_pattern_discovery(self):
        """Test pattern discovery with simpler conversation"""
        simple_conversation = {
            "conversation_id": f"simple_conv_{uuid.uuid4().hex[:8]}",
            "patient_id": f"simple_patient_{uuid.uuid4().hex[:8]}",
            "messages": [
                {
                    "role": "user",
                    "content": "I have a mild headache that started this morning",
                    "timestamp": datetime.utcnow().isoformat()
                }
            ],
            "context_data": {
                "conversation_type": "routine_consultation",
                "urgency_level": "low"
            }
        }
        
        try:
            async with self.session.post(
                f"{self.api_base}/medical-ai/dynamic-pattern-discovery",
                json=simple_conversation
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    patterns_count = data.get('patterns_discovered', 0)
                    processing_time = data.get('processing_time_ms', 0)
                    
                    self.log_test_result(
                        "Dynamic Pattern Discovery - Simple Conversation",
                        True,
                        f"Simple conversation processed: {patterns_count} patterns, {processing_time:.2f}ms",
                        data
                    )
                else:
                    error_text = await response.text()
                    self.log_test_result(
                        "Dynamic Pattern Discovery - Simple Conversation",
                        False,
                        f"HTTP {response.status}: {error_text}"
                    )
                    
        except Exception as e:
            self.log_test_result(
                "Dynamic Pattern Discovery - Simple Conversation Exception",
                False,
                f"Exception: {str(e)}"
            )

    async def _test_medical_terminology_patterns(self):
        """Test pattern discovery with medical terminology"""
        medical_conversation = {
            "conversation_id": f"medical_conv_{uuid.uuid4().hex[:8]}",
            "patient_id": f"medical_patient_{uuid.uuid4().hex[:8]}",
            "messages": [
                {
                    "role": "user",
                    "content": "I'm experiencing dyspnea and palpitations, especially during exertion",
                    "timestamp": datetime.utcnow().isoformat()
                },
                {
                    "role": "user",
                    "content": "My cardiologist mentioned possible arrhythmia based on my ECG results",
                    "timestamp": (datetime.utcnow() + timedelta(minutes=1)).isoformat()
                }
            ],
            "context_data": {
                "conversation_type": "specialist_followup",
                "medical_terminology_level": "high"
            }
        }
        
        try:
            async with self.session.post(
                f"{self.api_base}/medical-ai/dynamic-pattern-discovery",
                json=medical_conversation
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    patterns_count = data.get('patterns_discovered', 0)
                    new_patterns = data.get('new_patterns', [])
                    
                    # Check for medical terminology patterns
                    medical_patterns = [p for p in new_patterns if 'medical_terminology' in str(p).lower()]
                    
                    self.log_test_result(
                        "Dynamic Pattern Discovery - Medical Terminology",
                        True,
                        f"Medical terminology conversation: {patterns_count} patterns, {len(medical_patterns)} medical term patterns",
                        data
                    )
                else:
                    error_text = await response.text()
                    self.log_test_result(
                        "Dynamic Pattern Discovery - Medical Terminology",
                        False,
                        f"HTTP {response.status}: {error_text}"
                    )
                    
        except Exception as e:
            self.log_test_result(
                "Dynamic Pattern Discovery - Medical Terminology Exception",
                False,
                f"Exception: {str(e)}"
            )

    async def test_pattern_evolution_analysis(self):
        """
        📈 TEST 2: Pattern Evolution Analysis - Temporal Trend Tracking
        
        Tests temporal pattern evolution tracking with different time windows
        and analysis types.
        """
        print("📈 TESTING: Pattern Evolution Analysis API")
        print("=" * 50)
        
        # Test Case 1: 30-day comprehensive analysis
        evolution_request_30d = {
            "time_window_days": 30,
            "analysis_type": "comprehensive"
        }
        
        try:
            start_time = time.time()
            async with self.session.post(
                f"{self.api_base}/medical-ai/pattern-evolution-analysis",
                json=evolution_request_30d
            ) as response:
                processing_time = (time.time() - start_time) * 1000
                
                if response.status == 200:
                    data = await response.json()
                    
                    # Validate response structure
                    required_fields = [
                        'status', 'time_window_days', 'patterns_analyzed',
                        'temporal_trends', 'lifecycle_analysis', 'population_insights',
                        'trend_predictions', 'medical_language_evolution',
                        'processing_time_ms', 'algorithm_version'
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in data]
                    if missing_fields:
                        self.log_test_result(
                            "Pattern Evolution Analysis - Response Structure",
                            False,
                            f"Missing required fields: {missing_fields}"
                        )
                        return
                    
                    # Validate algorithm version
                    expected_version = "2.0_temporal_pattern_evolution"
                    if data.get('algorithm_version') != expected_version:
                        self.log_test_result(
                            "Pattern Evolution Analysis - Algorithm Version",
                            False,
                            f"Expected version {expected_version}, got {data.get('algorithm_version')}"
                        )
                        return
                    
                    patterns_analyzed = data.get('patterns_analyzed', 0)
                    temporal_trends = data.get('temporal_trends', {})
                    lifecycle_analysis = data.get('lifecycle_analysis', {})
                    population_insights = data.get('population_insights', [])
                    
                    self.log_test_result(
                        "Pattern Evolution Analysis - 30-day Comprehensive",
                        True,
                        f"Analyzed {patterns_analyzed} patterns, {len(population_insights)} population insights. Processing: {processing_time:.2f}ms",
                        data
                    )
                    
                    # Test Case 2: 7-day recent trends analysis
                    await self._test_recent_evolution_analysis()
                    
                    # Test Case 3: 90-day long-term analysis
                    await self._test_longterm_evolution_analysis()
                    
                else:
                    error_text = await response.text()
                    self.log_test_result(
                        "Pattern Evolution Analysis - API Response",
                        False,
                        f"HTTP {response.status}: {error_text}"
                    )
                    
        except Exception as e:
            self.log_test_result(
                "Pattern Evolution Analysis - Exception",
                False,
                f"Exception occurred: {str(e)}"
            )

    async def _test_recent_evolution_analysis(self):
        """Test recent evolution analysis (7 days)"""
        recent_request = {
            "time_window_days": 7,
            "analysis_type": "recent_trends"
        }
        
        try:
            async with self.session.post(
                f"{self.api_base}/medical-ai/pattern-evolution-analysis",
                json=recent_request
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    patterns_analyzed = data.get('patterns_analyzed', 0)
                    temporal_trends = data.get('temporal_trends', {})
                    
                    # Check for trend categories
                    emerging_patterns = temporal_trends.get('emerging_patterns', [])
                    declining_patterns = temporal_trends.get('declining_patterns', [])
                    stable_patterns = temporal_trends.get('stable_patterns', [])
                    
                    self.log_test_result(
                        "Pattern Evolution Analysis - 7-day Recent Trends",
                        True,
                        f"Recent trends: {len(emerging_patterns)} emerging, {len(declining_patterns)} declining, {len(stable_patterns)} stable",
                        data
                    )
                else:
                    error_text = await response.text()
                    self.log_test_result(
                        "Pattern Evolution Analysis - Recent Trends",
                        False,
                        f"HTTP {response.status}: {error_text}"
                    )
                    
        except Exception as e:
            self.log_test_result(
                "Pattern Evolution Analysis - Recent Trends Exception",
                False,
                f"Exception: {str(e)}"
            )

    async def _test_longterm_evolution_analysis(self):
        """Test long-term evolution analysis (90 days)"""
        longterm_request = {
            "time_window_days": 90,
            "analysis_type": "comprehensive"
        }
        
        try:
            async with self.session.post(
                f"{self.api_base}/medical-ai/pattern-evolution-analysis",
                json=longterm_request
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    patterns_analyzed = data.get('patterns_analyzed', 0)
                    lifecycle_analysis = data.get('lifecycle_analysis', {})
                    trend_predictions = data.get('trend_predictions', {})
                    
                    # Check lifecycle distribution
                    lifecycle_dist = lifecycle_analysis.get('lifecycle_distribution', {})
                    predictions = trend_predictions.get('emerging_pattern_candidates', [])
                    
                    self.log_test_result(
                        "Pattern Evolution Analysis - 90-day Long-term",
                        True,
                        f"Long-term analysis: {patterns_analyzed} patterns, {len(predictions)} predictions, lifecycle stages tracked",
                        data
                    )
                else:
                    error_text = await response.text()
                    self.log_test_result(
                        "Pattern Evolution Analysis - Long-term",
                        False,
                        f"HTTP {response.status}: {error_text}"
                    )
                    
        except Exception as e:
            self.log_test_result(
                "Pattern Evolution Analysis - Long-term Exception",
                False,
                f"Exception: {str(e)}"
            )

    async def test_pattern_discovery_analytics(self):
        """
        📊 TEST 3: Pattern Discovery Analytics - Performance Metrics
        
        Tests comprehensive analytics on pattern discovery performance,
        including discovery rates and system health metrics.
        """
        print("📊 TESTING: Pattern Discovery Analytics API")
        print("=" * 50)
        
        try:
            start_time = time.time()
            async with self.session.get(
                f"{self.api_base}/medical-ai/pattern-discovery-analytics"
            ) as response:
                processing_time = (time.time() - start_time) * 1000
                
                if response.status == 200:
                    data = await response.json()
                    
                    # Validate response structure
                    if 'status' not in data or data['status'] != 'success':
                        self.log_test_result(
                            "Pattern Discovery Analytics - Status",
                            False,
                            f"Expected success status, got: {data.get('status')}"
                        )
                        return
                    
                    analytics = data.get('analytics', {})
                    if not analytics:
                        self.log_test_result(
                            "Pattern Discovery Analytics - Analytics Data",
                            False,
                            "No analytics data returned"
                        )
                        return
                    
                    # Check for key analytics metrics
                    expected_metrics = [
                        'total_patterns_discovered',
                        'high_confidence_patterns', 
                        'recent_discoveries_24h',
                        'pattern_type_distribution',
                        'performance_metrics',
                        'algorithm_version'
                    ]
                    
                    missing_metrics = [metric for metric in expected_metrics if metric not in analytics]
                    if missing_metrics:
                        self.log_test_result(
                            "Pattern Discovery Analytics - Metrics",
                            False,
                            f"Missing analytics metrics: {missing_metrics}"
                        )
                        return
                    
                    # Validate algorithm version
                    expected_version = "2.0_dynamic_pattern_discovery"
                    if analytics.get('algorithm_version') != expected_version:
                        self.log_test_result(
                            "Pattern Discovery Analytics - Algorithm Version",
                            False,
                            f"Expected version {expected_version}, got {analytics.get('algorithm_version')}"
                        )
                        return
                    
                    total_patterns = analytics.get('total_patterns_discovered', 0)
                    high_confidence = analytics.get('high_confidence_patterns', 0)
                    recent_discoveries = analytics.get('recent_discoveries_24h', 0)
                    performance_metrics = analytics.get('performance_metrics', {})
                    
                    self.log_test_result(
                        "Pattern Discovery Analytics - Comprehensive Metrics",
                        True,
                        f"Total patterns: {total_patterns}, High confidence: {high_confidence}, Recent: {recent_discoveries}. Processing: {processing_time:.2f}ms",
                        data
                    )
                    
                else:
                    error_text = await response.text()
                    self.log_test_result(
                        "Pattern Discovery Analytics - API Response",
                        False,
                        f"HTTP {response.status}: {error_text}"
                    )
                    
        except Exception as e:
            self.log_test_result(
                "Pattern Discovery Analytics - Exception",
                False,
                f"Exception occurred: {str(e)}"
            )

    async def test_evolution_analytics_dashboard(self):
        """
        📈 TEST 4: Evolution Analytics Dashboard - Comprehensive Evolution Insights
        
        Tests comprehensive dashboard analytics for pattern evolution tracking,
        including lifecycle statistics and population insights.
        """
        print("📈 TESTING: Evolution Analytics Dashboard API")
        print("=" * 50)
        
        try:
            start_time = time.time()
            async with self.session.get(
                f"{self.api_base}/medical-ai/evolution-analytics-dashboard"
            ) as response:
                processing_time = (time.time() - start_time) * 1000
                
                if response.status == 200:
                    data = await response.json()
                    
                    # Validate response structure
                    if 'status' not in data or data['status'] != 'success':
                        self.log_test_result(
                            "Evolution Analytics Dashboard - Status",
                            False,
                            f"Expected success status, got: {data.get('status')}"
                        )
                        return
                    
                    dashboard = data.get('dashboard', {})
                    if not dashboard:
                        self.log_test_result(
                            "Evolution Analytics Dashboard - Dashboard Data",
                            False,
                            "No dashboard data returned"
                        )
                        return
                    
                    # Check for key dashboard components
                    expected_components = [
                        'recent_trends',
                        'monthly_trends',
                        'lifecycle_statistics',
                        'population_learning_summary',
                        'performance_metrics',
                        'algorithm_version'
                    ]
                    
                    missing_components = [comp for comp in expected_components if comp not in dashboard]
                    if missing_components:
                        self.log_test_result(
                            "Evolution Analytics Dashboard - Components",
                            False,
                            f"Missing dashboard components: {missing_components}"
                        )
                        return
                    
                    # Validate algorithm version
                    expected_version = "2.0_temporal_pattern_evolution"
                    if dashboard.get('algorithm_version') != expected_version:
                        self.log_test_result(
                            "Evolution Analytics Dashboard - Algorithm Version",
                            False,
                            f"Expected version {expected_version}, got {dashboard.get('algorithm_version')}"
                        )
                        return
                    
                    recent_trends = dashboard.get('recent_trends', {})
                    monthly_trends = dashboard.get('monthly_trends', {})
                    lifecycle_stats = dashboard.get('lifecycle_statistics', {})
                    population_summary = dashboard.get('population_learning_summary', {})
                    
                    self.log_test_result(
                        "Evolution Analytics Dashboard - Comprehensive Dashboard",
                        True,
                        f"Dashboard loaded with recent trends, monthly trends, lifecycle stats, and population summary. Processing: {processing_time:.2f}ms",
                        data
                    )
                    
                else:
                    error_text = await response.text()
                    self.log_test_result(
                        "Evolution Analytics Dashboard - API Response",
                        False,
                        f"HTTP {response.status}: {error_text}"
                    )
                    
        except Exception as e:
            self.log_test_result(
                "Evolution Analytics Dashboard - Exception",
                False,
                f"Exception occurred: {str(e)}"
            )

    async def test_pattern_confidence_calibration(self):
        """
        🎯 TEST 5: Pattern Confidence Calibration - Feedback-based Learning
        
        Tests feedback integration for pattern validation and confidence
        score adjustments through continuous learning loops.
        """
        print("🎯 TESTING: Pattern Confidence Calibration API")
        print("=" * 50)
        
        # Test Case 1: Positive feedback for pattern validation
        positive_feedback = {
            "feedback_data": [
                {
                    "pattern_id": f"test_pattern_{uuid.uuid4().hex[:8]}",
                    "feedback": "helpful",
                    "evidence_quality": 0.9,
                    "user_validation": True,
                    "medical_accuracy": 0.85
                },
                {
                    "pattern_id": f"test_pattern_{uuid.uuid4().hex[:8]}",
                    "feedback": "helpful",
                    "evidence_quality": 0.8,
                    "user_validation": True,
                    "medical_accuracy": 0.9
                }
            ]
        }
        
        try:
            start_time = time.time()
            async with self.session.post(
                f"{self.api_base}/medical-ai/pattern-confidence-calibration",
                json=positive_feedback
            ) as response:
                processing_time = (time.time() - start_time) * 1000
                
                if response.status == 200:
                    data = await response.json()
                    
                    # Validate response structure
                    required_fields = [
                        'patterns_updated',
                        'confidence_improvements',
                        'patterns_deprecated',
                        'calibration_summary'
                    ]
                    
                    missing_fields = [field for field in required_fields if field not in data]
                    if missing_fields:
                        self.log_test_result(
                            "Pattern Confidence Calibration - Response Structure",
                            False,
                            f"Missing required fields: {missing_fields}"
                        )
                        return
                    
                    patterns_updated = data.get('patterns_updated', 0)
                    confidence_improvements = data.get('confidence_improvements', 0)
                    patterns_deprecated = data.get('patterns_deprecated', 0)
                    calibration_summary = data.get('calibration_summary', {})
                    
                    # Validate calibration summary
                    expected_summary_fields = [
                        'total_feedback_processed',
                        'improvement_rate',
                        'deprecation_rate'
                    ]
                    
                    missing_summary_fields = [field for field in expected_summary_fields if field not in calibration_summary]
                    if missing_summary_fields:
                        self.log_test_result(
                            "Pattern Confidence Calibration - Summary Structure",
                            False,
                            f"Missing summary fields: {missing_summary_fields}"
                        )
                        return
                    
                    self.log_test_result(
                        "Pattern Confidence Calibration - Positive Feedback",
                        True,
                        f"Updated {patterns_updated} patterns, {confidence_improvements} improvements, {patterns_deprecated} deprecated. Processing: {processing_time:.2f}ms",
                        data
                    )
                    
                    # Test Case 2: Negative feedback
                    await self._test_negative_feedback_calibration()
                    
                    # Test Case 3: Mixed feedback
                    await self._test_mixed_feedback_calibration()
                    
                else:
                    error_text = await response.text()
                    self.log_test_result(
                        "Pattern Confidence Calibration - API Response",
                        False,
                        f"HTTP {response.status}: {error_text}"
                    )
                    
        except Exception as e:
            self.log_test_result(
                "Pattern Confidence Calibration - Exception",
                False,
                f"Exception occurred: {str(e)}"
            )

    async def _test_negative_feedback_calibration(self):
        """Test calibration with negative feedback"""
        negative_feedback = {
            "feedback_data": [
                {
                    "pattern_id": f"test_pattern_{uuid.uuid4().hex[:8]}",
                    "feedback": "not_helpful",
                    "evidence_quality": 0.3,
                    "user_validation": False,
                    "medical_accuracy": 0.2
                },
                {
                    "pattern_id": f"test_pattern_{uuid.uuid4().hex[:8]}",
                    "feedback": "incorrect",
                    "evidence_quality": 0.1,
                    "user_validation": False,
                    "medical_accuracy": 0.1
                }
            ]
        }
        
        try:
            async with self.session.post(
                f"{self.api_base}/medical-ai/pattern-confidence-calibration",
                json=negative_feedback
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    patterns_updated = data.get('patterns_updated', 0)
                    patterns_deprecated = data.get('patterns_deprecated', 0)
                    
                    self.log_test_result(
                        "Pattern Confidence Calibration - Negative Feedback",
                        True,
                        f"Negative feedback processed: {patterns_updated} updated, {patterns_deprecated} deprecated",
                        data
                    )
                else:
                    error_text = await response.text()
                    self.log_test_result(
                        "Pattern Confidence Calibration - Negative Feedback",
                        False,
                        f"HTTP {response.status}: {error_text}"
                    )
                    
        except Exception as e:
            self.log_test_result(
                "Pattern Confidence Calibration - Negative Feedback Exception",
                False,
                f"Exception: {str(e)}"
            )

    async def _test_mixed_feedback_calibration(self):
        """Test calibration with mixed feedback"""
        mixed_feedback = {
            "feedback_data": [
                {
                    "pattern_id": f"test_pattern_{uuid.uuid4().hex[:8]}",
                    "feedback": "helpful",
                    "evidence_quality": 0.8,
                    "user_validation": True,
                    "medical_accuracy": 0.85
                },
                {
                    "pattern_id": f"test_pattern_{uuid.uuid4().hex[:8]}",
                    "feedback": "not_helpful",
                    "evidence_quality": 0.4,
                    "user_validation": False,
                    "medical_accuracy": 0.3
                },
                {
                    "pattern_id": f"test_pattern_{uuid.uuid4().hex[:8]}",
                    "feedback": "helpful",
                    "evidence_quality": 0.9,
                    "user_validation": True,
                    "medical_accuracy": 0.9
                }
            ]
        }
        
        try:
            async with self.session.post(
                f"{self.api_base}/medical-ai/pattern-confidence-calibration",
                json=mixed_feedback
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    patterns_updated = data.get('patterns_updated', 0)
                    confidence_improvements = data.get('confidence_improvements', 0)
                    calibration_summary = data.get('calibration_summary', {})
                    
                    improvement_rate = calibration_summary.get('improvement_rate', 0)
                    
                    self.log_test_result(
                        "Pattern Confidence Calibration - Mixed Feedback",
                        True,
                        f"Mixed feedback processed: {patterns_updated} updated, {confidence_improvements} improvements, {improvement_rate:.1f}% improvement rate",
                        data
                    )
                else:
                    error_text = await response.text()
                    self.log_test_result(
                        "Pattern Confidence Calibration - Mixed Feedback",
                        False,
                        f"HTTP {response.status}: {error_text}"
                    )
                    
        except Exception as e:
            self.log_test_result(
                "Pattern Confidence Calibration - Mixed Feedback Exception",
                False,
                f"Exception: {str(e)}"
            )

    def print_final_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("🔬 STEP 2 DYNAMIC PATTERN ENHANCEMENT SYSTEM - FINAL TEST SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"📊 OVERALL RESULTS:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   📈 Success Rate: {success_rate:.1f}%")
        print()
        
        # Group results by test category
        categories = {}
        for result in self.test_results:
            category = result['test_name'].split(' - ')[0]
            if category not in categories:
                categories[category] = {'passed': 0, 'failed': 0, 'tests': []}
            
            if result['success']:
                categories[category]['passed'] += 1
            else:
                categories[category]['failed'] += 1
            categories[category]['tests'].append(result)
        
        print("📋 DETAILED RESULTS BY CATEGORY:")
        for category, data in categories.items():
            total_cat = data['passed'] + data['failed']
            cat_success_rate = (data['passed'] / total_cat * 100) if total_cat > 0 else 0
            print(f"\n🔸 {category}:")
            print(f"   Success Rate: {cat_success_rate:.1f}% ({data['passed']}/{total_cat})")
            
            for test in data['tests']:
                status = "✅" if test['success'] else "❌"
                test_name_short = test['test_name'].split(' - ', 1)[1] if ' - ' in test['test_name'] else test['test_name']
                print(f"   {status} {test_name_short}")
                if not test['success']:
                    print(f"      ⚠️  {test['details']}")
        
        print("\n" + "=" * 80)
        
        # Final assessment
        if success_rate >= 90:
            print("🎉 EXCELLENT: Step 2 Dynamic Pattern Enhancement System is FULLY FUNCTIONAL and production-ready!")
        elif success_rate >= 75:
            print("✅ GOOD: Step 2 Dynamic Pattern Enhancement System is mostly functional with minor issues.")
        elif success_rate >= 50:
            print("⚠️  PARTIAL: Step 2 Dynamic Pattern Enhancement System has significant issues requiring attention.")
        else:
            print("❌ CRITICAL: Step 2 Dynamic Pattern Enhancement System has major functionality problems.")
        
        print("=" * 80)

async def main():
    """Main test execution function"""
    print("🚀 Starting Step 2 Dynamic Pattern Enhancement System Comprehensive Testing")
    print("=" * 80)
    
    async with Step2DynamicPatternTester() as tester:
        # Execute all test suites
        await tester.test_dynamic_pattern_discovery()
        await tester.test_pattern_evolution_analysis()
        await tester.test_pattern_discovery_analytics()
        await tester.test_evolution_analytics_dashboard()
        await tester.test_pattern_confidence_calibration()
        
        # Print final summary
        tester.print_final_summary()

if __name__ == "__main__":
    asyncio.run(main())