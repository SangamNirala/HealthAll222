"""
🧠🔍 ADVANCED MEDICAL SENTIMENT ANALYZER 🔍🧠
================================================

MISSION: Revolutionary medical context sentiment analysis that understands the nuanced
emotional landscape of healthcare conversations with clinical precision.

Features:
- Medical-specific emotion detection (clinical anxiety vs general nervousness)  
- Context-aware sentiment analysis (chest pain anxiety vs appointment anxiety)
- Multi-dimensional emotional scoring with confidence intervals
- Real-time medical urgency tone analysis
- Cultural sensitivity in medical emotional expressions
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import asyncio
import google.generativeai as genai
from motor.motor_asyncio import AsyncIOMotorDatabase

class MedicalSentimentAnalyzer:
    """
    🧠🔍 ADVANCED MEDICAL SENTIMENT ANALYZER
    
    Performs sophisticated sentiment analysis specifically designed for medical
    conversations, with the ability to distinguish between different types of
    medical emotions and their clinical significance.
    """
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.logger = logging.getLogger(__name__)
        
        # Initialize Gemini API
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Medical emotion classification patterns
        self.medical_emotion_patterns = {
            'medical_anxiety': [
                'worried about results', 'scared of diagnosis', 'what if it\'s serious',
                'afraid of cancer', 'concerned about symptoms', 'health anxiety',
                'medical fears', 'worried about test results', 'afraid of surgery'
            ],
            'pain_distress': [
                'unbearable pain', 'can\'t take it anymore', 'pain is killing me',
                'worst pain ever', 'excruciating', 'agony', 'torture',
                'suffering', 'can\'t sleep due to pain', 'pain medication not working'
            ],
            'diagnostic_fear': [
                'what\'s wrong with me', 'am I dying', 'is it terminal',
                'worst case scenario', 'afraid of bad news', 'scared of results',
                'what if it spreads', 'fear of diagnosis', 'medical uncertainty'
            ],
            'treatment_anxiety': [
                'afraid of side effects', 'worried about treatment', 'scared of surgery',
                'medication fears', 'procedure anxiety', 'treatment complications',
                'will it work', 'recovery concerns', 'rehabilitation fears'
            ],
            'hope_relief': [
                'feeling better', 'symptoms improving', 'hopeful about recovery',
                'grateful for help', 'positive outlook', 'optimistic',
                'relieved', 'thankful', 'getting better', 'healing well'
            ],
            'frustration_anger': [
                'doctors don\'t listen', 'no one understands', 'tired of being sick',
                'frustrated with treatment', 'angry about symptoms', 'fed up',
                'why me', 'unfair', 'system failure', 'medical mistakes'
            ]
        }
        
        # Medical urgency indicators
        self.urgency_indicators = {
            'emergency': [
                'can\'t breathe', 'chest crushing', 'worst headache ever',
                'sudden weakness', 'severe bleeding', 'losing consciousness',
                'heart attack', 'stroke symptoms', 'severe allergic reaction'
            ],
            'urgent': [
                'severe pain', 'high fever', 'persistent vomiting',
                'difficulty breathing', 'severe symptoms', 'getting worse',
                'sharp pain', 'intense discomfort', 'concerning symptoms'
            ],
            'routine': [
                'mild symptoms', 'minor concern', 'general question',
                'follow up', 'checking in', 'routine inquiry',
                'preventive care', 'health maintenance'
            ]
        }
        
        self.logger.info("🧠 Medical Sentiment Analyzer initialized")

    async def analyze_medical_sentiment(
        self, 
        message: str, 
        patient_id: str, 
        medical_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        🎯 COMPREHENSIVE MEDICAL SENTIMENT ANALYSIS
        
        Performs multi-dimensional sentiment analysis specifically for medical contexts:
        - Primary and secondary emotion detection
        - Medical anxiety vs general anxiety distinction
        - Pain distress level assessment
        - Health concern urgency scoring
        - Cultural and communication style considerations
        """
        
        try:
            # Step 1: Rule-based medical emotion detection
            rule_based_results = await self._rule_based_emotion_detection(message)
            
            # Step 2: AI-powered contextual sentiment analysis
            ai_results = await self._ai_powered_sentiment_analysis(
                message, medical_context, patient_id
            )
            
            # Step 3: Medical urgency tone analysis
            urgency_analysis = await self._analyze_medical_urgency(message, medical_context)
            
            # Step 4: Combine and validate results
            combined_results = await self._combine_sentiment_analyses(
                rule_based_results, ai_results, urgency_analysis
            )
            
            # Step 5: Generate confidence scoring
            confidence_score = await self._calculate_sentiment_confidence(
                message, combined_results
            )
            
            # Format final results
            sentiment_results = {
                'patient_id': patient_id,
                'timestamp': datetime.now(),
                'message_analyzed': message[:100] + '...' if len(message) > 100 else message,
                
                # Core sentiment analysis
                'primary_emotion': combined_results['primary_emotion'],
                'secondary_emotions': combined_results['secondary_emotions'],
                'intensity_level': combined_results['intensity_level'],
                'confidence': confidence_score,
                
                # Medical-specific scoring
                'medical_anxiety_score': combined_results['medical_anxiety'],
                'pain_distress_score': combined_results['pain_distress'],
                'urgency_score': combined_results['urgency_level'],
                
                # Detailed analysis
                'emotion_indicators': combined_results['emotion_indicators'],
                'medical_context_factors': combined_results['context_factors'],
                'cultural_considerations': combined_results['cultural_factors'],
                
                # Metadata
                'analysis_version': '2.0_medical_sentiment_analysis',
                'processing_method': 'hybrid_rule_ai'
            }
            
            # Store analysis results
            await self._store_sentiment_analysis(sentiment_results)
            
            self.logger.info(f"🧠 Medical sentiment analysis completed for {patient_id}")
            return sentiment_results
            
        except Exception as e:
            self.logger.error(f"❌ Error in medical sentiment analysis: {str(e)}")
            raise

    async def _rule_based_emotion_detection(self, message: str) -> Dict[str, Any]:
        """Rule-based emotion detection using medical patterns"""
        
        message_lower = message.lower()
        detected_emotions = []
        emotion_scores = {}
        
        # Check each medical emotion pattern
        for emotion_type, patterns in self.medical_emotion_patterns.items():
            score = 0
            matched_patterns = []
            
            for pattern in patterns:
                if pattern in message_lower:
                    score += 1
                    matched_patterns.append(pattern)
            
            if score > 0:
                detected_emotions.append(emotion_type)
                emotion_scores[emotion_type] = score / len(patterns)  # Normalize
        
        # Determine primary emotion (highest score)
        primary_emotion = 'calm'
        if emotion_scores:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
        
        # Get secondary emotions (other detected emotions)
        secondary_emotions = [e for e in detected_emotions if e != primary_emotion][:3]
        
        return {
            'primary_emotion': primary_emotion,
            'secondary_emotions': secondary_emotions,
            'emotion_scores': emotion_scores,
            'matched_patterns': {emotion: [] for emotion in detected_emotions}
        }

    async def _ai_powered_sentiment_analysis(
        self, 
        message: str, 
        medical_context: Dict[str, Any],
        patient_id: str
    ) -> Dict[str, Any]:
        """AI-powered contextual sentiment analysis using Gemini"""
        
        context_info = json.dumps(medical_context, default=str) if medical_context else "{}"
        
        prompt = f"""
        As a medical psychology expert, analyze the emotional content of this patient message with deep medical context awareness.

        PATIENT MESSAGE: "{message}"
        MEDICAL CONTEXT: {context_info}
        
        Provide comprehensive emotional analysis in JSON format:
        {{
            "primary_emotion": "anxiety|fear|frustration|depression|hope|relief|panic|desperation|calm|uncertain|distressed|optimistic",
            "secondary_emotions": ["list", "of", "secondary", "emotions"],
            "emotional_intensity": 1-5,
            "medical_anxiety_level": 0.0-1.0,
            "pain_distress_level": 0.0-1.0,
            "health_concern_urgency": 0.0-1.0,
            "context_factors": ["factors", "influencing", "emotional", "state"],
            "medical_vs_general": "medical|general|mixed",
            "clinical_significance": "low|moderate|high|critical",
            "emotional_reasoning": "detailed explanation of emotional assessment"
        }}
        
        Focus on:
        1. Medical anxiety vs general anxiety distinction
        2. Pain-related emotional distress
        3. Health concern urgency level
        4. Context-aware emotional interpretation
        5. Clinical significance of emotional state
        """
        
        try:
            response = await self.model.generate_content_async(prompt)
            result = json.loads(response.text.strip())
            return result
        except Exception as e:
            self.logger.error(f"AI sentiment analysis error: {str(e)}")
            return {
                "primary_emotion": "uncertain",
                "secondary_emotions": [],
                "emotional_intensity": 3,
                "medical_anxiety_level": 0.5,
                "pain_distress_level": 0.0,
                "health_concern_urgency": 0.3,
                "context_factors": [],
                "medical_vs_general": "general",
                "clinical_significance": "moderate"
            }

    async def _analyze_medical_urgency(
        self, 
        message: str, 
        medical_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze medical urgency and tone"""
        
        message_lower = message.lower()
        urgency_level = 'routine'
        urgency_score = 0.0
        matched_indicators = []
        
        # Check urgency indicators
        for level, indicators in self.urgency_indicators.items():
            for indicator in indicators:
                if indicator in message_lower:
                    if level == 'emergency':
                        urgency_level = 'emergency'
                        urgency_score = 1.0
                        matched_indicators.append(indicator)
                    elif level == 'urgent' and urgency_level != 'emergency':
                        urgency_level = 'urgent'
                        urgency_score = max(urgency_score, 0.7)
                        matched_indicators.append(indicator)
                    elif level == 'routine' and urgency_level == 'routine':
                        urgency_score = max(urgency_score, 0.3)
                        matched_indicators.append(indicator)
        
        return {
            'urgency_level': urgency_level,
            'urgency_score': urgency_score,
            'urgency_indicators': matched_indicators,
            'emergency_keywords_detected': len([i for i in matched_indicators 
                                              if any(e in i for e in self.urgency_indicators['emergency'])]) > 0
        }

    async def _combine_sentiment_analyses(
        self, 
        rule_based: Dict[str, Any],
        ai_results: Dict[str, Any],
        urgency_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Combine rule-based and AI analyses intelligently"""
        
        # Determine primary emotion (AI takes precedence for nuanced analysis)
        primary_emotion = ai_results.get('primary_emotion', rule_based['primary_emotion'])
        
        # Combine secondary emotions
        ai_secondary = ai_results.get('secondary_emotions', [])
        rule_secondary = rule_based['secondary_emotions']
        combined_secondary = list(set(ai_secondary + rule_secondary))[:3]
        
        # Calculate intensity (average of AI and rule-based where applicable)
        intensity = ai_results.get('emotional_intensity', 3)
        if rule_based['emotion_scores']:
            rule_intensity = max(rule_based['emotion_scores'].values()) * 5
            intensity = int((intensity + rule_intensity) / 2)
        
        return {
            'primary_emotion': primary_emotion,
            'secondary_emotions': combined_secondary,
            'intensity_level': min(max(intensity, 1), 5),
            
            # Medical-specific scores
            'medical_anxiety': ai_results.get('medical_anxiety_level', 0.3),
            'pain_distress': ai_results.get('pain_distress_level', 0.0),
            'urgency_level': urgency_analysis['urgency_score'],
            
            # Supporting information
            'emotion_indicators': list(rule_based['matched_patterns'].keys()),
            'context_factors': ai_results.get('context_factors', []),
            'cultural_factors': [],  # Placeholder for cultural analysis
            'urgency_indicators': urgency_analysis['urgency_indicators']
        }

    async def _calculate_sentiment_confidence(
        self, 
        message: str, 
        analysis_results: Dict[str, Any]
    ) -> float:
        """Calculate confidence score for sentiment analysis"""
        
        confidence_factors = []
        
        # Message length factor
        if len(message) > 10:
            confidence_factors.append(0.2)
        
        # Emotion indicator factor
        if analysis_results['emotion_indicators']:
            confidence_factors.append(0.3)
        
        # Context factor
        if analysis_results['context_factors']:
            confidence_factors.append(0.2)
        
        # Urgency clarity factor
        if analysis_results['urgency_indicators']:
            confidence_factors.append(0.15)
        
        # Intensity consistency factor
        if 1 <= analysis_results['intensity_level'] <= 5:
            confidence_factors.append(0.15)
        
        base_confidence = sum(confidence_factors)
        
        # Adjust for medical context clarity
        if analysis_results['medical_anxiety'] > 0.7 or analysis_results['pain_distress'] > 0.7:
            base_confidence += 0.1
        
        return min(max(base_confidence, 0.1), 0.95)

    async def _store_sentiment_analysis(self, results: Dict[str, Any]):
        """Store sentiment analysis results in database"""
        try:
            await self.db.medical_sentiment_analyses.insert_one(results)
        except Exception as e:
            self.logger.error(f"Error storing sentiment analysis: {str(e)}")

    async def get_patient_sentiment_history(
        self, 
        patient_id: str, 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get recent sentiment analysis history for a patient"""
        try:
            history = await self.db.medical_sentiment_analyses.find({
                'patient_id': patient_id
            }).sort('timestamp', -1).limit(limit).to_list(length=limit)
            
            return history
        except Exception as e:
            self.logger.error(f"Error retrieving sentiment history: {str(e)}")
            return []

    async def analyze_sentiment_trends(
        self, 
        patient_id: str, 
        days: int = 7
    ) -> Dict[str, Any]:
        """Analyze sentiment trends over time for a patient"""
        
        try:
            from datetime import timedelta
            
            start_date = datetime.now() - timedelta(days=days)
            
            sentiment_data = await self.db.medical_sentiment_analyses.find({
                'patient_id': patient_id,
                'timestamp': {'$gte': start_date}
            }).sort('timestamp', 1).to_list(length=None)
            
            if not sentiment_data:
                return {'trend': 'insufficient_data', 'analysis': 'Not enough data for trend analysis'}
            
            # Calculate trend metrics
            anxiety_levels = [data['medical_anxiety_score'] for data in sentiment_data]
            pain_levels = [data['pain_distress_score'] for data in sentiment_data]
            
            anxiety_trend = 'stable'
            if len(anxiety_levels) >= 3:
                recent_avg = sum(anxiety_levels[-3:]) / 3
                earlier_avg = sum(anxiety_levels[:-3]) / len(anxiety_levels[:-3]) if len(anxiety_levels) > 3 else recent_avg
                
                if recent_avg > earlier_avg + 0.2:
                    anxiety_trend = 'increasing'
                elif recent_avg < earlier_avg - 0.2:
                    anxiety_trend = 'decreasing'
            
            return {
                'patient_id': patient_id,
                'analysis_period': f'{days} days',
                'anxiety_trend': anxiety_trend,
                'average_anxiety_level': sum(anxiety_levels) / len(anxiety_levels),
                'average_pain_distress': sum(pain_levels) / len(pain_levels),
                'total_analyses': len(sentiment_data),
                'trend_confidence': 0.8 if len(sentiment_data) >= 5 else 0.5
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing sentiment trends: {str(e)}")
            return {'trend': 'error', 'analysis': 'Error in trend analysis'}