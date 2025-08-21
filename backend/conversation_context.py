"""
🎯 STEP 4.1: CONVERSATION MEMORY AND CONTEXT TRACKING IMPLEMENTATION
Enhanced conversation memory system for sophisticated medical chatbot interactions
Part of the comprehensive Medical Chatbot NLP Enhancement Project

This module implements the ConversationContext class as specified in Step 4.1
for tracking conversation memory and context across multiple interaction turns.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import uuid


class ConversationStage(Enum):
    """Enumeration of conversation stages for medical interactions"""
    INITIAL = "initial"
    GREETING = "greeting"
    SYMPTOM_GATHERING = "symptom_gathering"
    DETAILED_ASSESSMENT = "detailed_assessment"
    MEDICAL_HISTORY = "medical_history"
    DIFFERENTIAL_DIAGNOSIS = "differential_diagnosis"
    RECOMMENDATIONS = "recommendations"
    FOLLOW_UP = "follow_up"
    COMPLETED = "completed"


@dataclass
class ConversationContext:
    """
    🧠 STEP 4.1: CONVERSATION MEMORY AND CONTEXT TRACKING CLASS 🧠
    
    Enhanced conversation context system for maintaining sophisticated medical 
    conversation state across multiple interactions. Provides comprehensive
    memory management for symptom progression, patient context, and conversational
    intelligence.
    
    This class implements the exact specification from Step 4.1:
    - symptom_history: []
    - patient_demographics: {}
    - previous_responses: []
    - medical_context: {}
    - conversation_stage: "initial"
    
    Enhanced with additional functionality for production medical chatbot usage.
    """
    
    # Core Step 4.1 Specifications - Exact implementation as requested
    symptom_history: List[Dict[str, Any]] = field(default_factory=list)
    patient_demographics: Dict[str, Any] = field(default_factory=dict)
    previous_responses: List[Dict[str, Any]] = field(default_factory=list)
    medical_context: Dict[str, Any] = field(default_factory=dict)
    conversation_stage: str = "initial"
    
    # Enhanced conversation management attributes
    conversation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: Optional[str] = None
    session_start_time: datetime = field(default_factory=datetime.utcnow)
    last_interaction_time: datetime = field(default_factory=datetime.utcnow)
    total_turns: int = 0
    
    # Advanced memory management
    conversation_memory: Dict[str, Any] = field(default_factory=dict)
    context_confidence_score: float = 0.0
    memory_retention_minutes: int = 60  # How long to retain conversation context
    
    def __post_init__(self):
        """Initialize conversation context with default values"""
        # Ensure conversation_stage is properly set as string
        if isinstance(self.conversation_stage, ConversationStage):
            self.conversation_stage = self.conversation_stage.value
        
        # Initialize conversation memory structure
        if not self.conversation_memory:
            self.conversation_memory = {
                "key_topics_discussed": [],
                "symptoms_mentioned": [],
                "concerns_raised": [],
                "questions_asked_by_patient": [],
                "medical_terms_used": [],
                "emotional_indicators": [],
                "urgency_markers": []
            }
    
    def add_symptom_to_history(self, symptom: Dict[str, Any]) -> None:
        """
        Add a new symptom to the conversation history
        
        Args:
            symptom: Dictionary containing symptom information
                Expected keys: 'name', 'description', 'severity', 'onset', 'duration'
        """
        symptom_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "turn_number": self.total_turns,
            "symptom_data": symptom,
            "conversation_stage": self.conversation_stage
        }
        
        self.symptom_history.append(symptom_entry)
        
        # Update conversation memory
        symptom_name = symptom.get('name', 'unknown_symptom')
        if symptom_name not in self.conversation_memory["symptoms_mentioned"]:
            self.conversation_memory["symptoms_mentioned"].append(symptom_name)
        
        self._update_interaction_time()
    
    def add_response_to_history(self, response: Dict[str, Any]) -> None:
        """
        Add an AI response to the conversation history
        
        Args:
            response: Dictionary containing response information
                Expected keys: 'content', 'type', 'confidence', 'reasoning'
        """
        response_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "turn_number": self.total_turns,
            "response_data": response,
            "conversation_stage": self.conversation_stage
        }
        
        self.previous_responses.append(response_entry)
        self._update_interaction_time()
    
    def update_patient_demographics(self, demographics: Dict[str, Any]) -> None:
        """
        Update patient demographic information
        
        Args:
            demographics: Dictionary with demographic information
                Expected keys: 'age', 'gender', 'medical_history', 'allergies', etc.
        """
        self.patient_demographics.update(demographics)
        self._update_interaction_time()
    
    def update_medical_context(self, context_update: Dict[str, Any]) -> None:
        """
        Update medical context information
        
        Args:
            context_update: Dictionary with medical context updates
                Expected keys: 'chief_complaint', 'current_medications', 'risk_factors', etc.
        """
        self.medical_context.update(context_update)
        self._update_interaction_time()
    
    def advance_conversation_stage(self, new_stage: str) -> None:
        """
        Advance the conversation to a new stage
        
        Args:
            new_stage: New conversation stage as string
        """
        previous_stage = self.conversation_stage
        self.conversation_stage = new_stage
        
        # Log stage transition
        stage_transition = {
            "timestamp": datetime.utcnow().isoformat(),
            "from_stage": previous_stage,
            "to_stage": new_stage,
            "turn_number": self.total_turns
        }
        
        if "stage_transitions" not in self.conversation_memory:
            self.conversation_memory["stage_transitions"] = []
        self.conversation_memory["stage_transitions"].append(stage_transition)
        
        self._update_interaction_time()
    
    def increment_turn(self) -> None:
        """Increment conversation turn counter"""
        self.total_turns += 1
        self._update_interaction_time()
    
    def get_recent_symptoms(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get the most recent symptoms from conversation history
        
        Args:
            limit: Maximum number of recent symptoms to return
            
        Returns:
            List of recent symptom entries
        """
        return self.symptom_history[-limit:] if self.symptom_history else []
    
    def get_recent_responses(self, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Get the most recent AI responses from conversation history
        
        Args:
            limit: Maximum number of recent responses to return
            
        Returns:
            List of recent response entries
        """
        return self.previous_responses[-limit:] if self.previous_responses else []
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """
        Generate a comprehensive conversation summary
        
        Returns:
            Dictionary containing conversation summary statistics and key information
        """
        duration_minutes = (self.last_interaction_time - self.session_start_time).total_seconds() / 60
        
        return {
            "conversation_id": self.conversation_id,
            "patient_id": self.patient_id,
            "current_stage": self.conversation_stage,
            "total_turns": self.total_turns,
            "session_duration_minutes": round(duration_minutes, 2),
            "symptoms_discussed": len(self.symptom_history),
            "responses_generated": len(self.previous_responses),
            "key_topics": self.conversation_memory.get("key_topics_discussed", []),
            "symptoms_mentioned": self.conversation_memory.get("symptoms_mentioned", []),
            "confidence_score": self.context_confidence_score,
            "last_interaction": self.last_interaction_time.isoformat(),
            "session_start": self.session_start_time.isoformat()
        }
    
    def is_session_expired(self) -> bool:
        """
        Check if the conversation session has expired based on inactivity
        
        Returns:
            True if session has expired, False otherwise
        """
        time_since_last_interaction = datetime.utcnow() - self.last_interaction_time
        return time_since_last_interaction > timedelta(minutes=self.memory_retention_minutes)
    
    def search_conversation_history(self, query: str) -> List[Dict[str, Any]]:
        """
        Search through conversation history for specific terms or patterns
        
        Args:
            query: Search query string
            
        Returns:
            List of matching entries from symptom_history and previous_responses
        """
        query_lower = query.lower()
        matching_entries = []
        
        # Search through symptom history
        for entry in self.symptom_history:
            symptom_data = entry.get("symptom_data", {})
            searchable_text = " ".join([
                str(symptom_data.get("name", "")),
                str(symptom_data.get("description", "")),
                str(symptom_data.get("location", ""))
            ]).lower()
            
            if query_lower in searchable_text:
                matching_entries.append({
                    "type": "symptom",
                    "entry": entry,
                    "match_score": self._calculate_match_score(query_lower, searchable_text)
                })
        
        # Search through response history
        for entry in self.previous_responses:
            response_data = entry.get("response_data", {})
            searchable_text = str(response_data.get("content", "")).lower()
            
            if query_lower in searchable_text:
                matching_entries.append({
                    "type": "response",
                    "entry": entry,
                    "match_score": self._calculate_match_score(query_lower, searchable_text)
                })
        
        # Sort by match score (highest first)
        matching_entries.sort(key=lambda x: x["match_score"], reverse=True)
        
        return matching_entries
    
    def update_context_confidence(self, new_confidence: float) -> None:
        """
        Update the confidence score for the conversation context
        
        Args:
            new_confidence: New confidence score (0.0 to 1.0)
        """
        self.context_confidence_score = max(0.0, min(1.0, new_confidence))
        self._update_interaction_time()
    
    def add_conversation_memory(self, memory_type: str, memory_data: Any) -> None:
        """
        Add specific information to conversation memory
        
        Args:
            memory_type: Type of memory to add (e.g., 'key_topics_discussed')
            memory_data: Data to add to memory
        """
        if memory_type not in self.conversation_memory:
            self.conversation_memory[memory_type] = []
        
        if isinstance(self.conversation_memory[memory_type], list):
            if memory_data not in self.conversation_memory[memory_type]:
                self.conversation_memory[memory_type].append(memory_data)
        else:
            self.conversation_memory[memory_type] = memory_data
        
        self._update_interaction_time()
    
    def get_conversation_context_for_ai(self) -> Dict[str, Any]:
        """
        Generate conversation context specifically formatted for AI processing
        
        Returns:
            Dictionary with conversation context optimized for AI consumption
        """
        return {
            "conversation_stage": self.conversation_stage,
            "total_turns": self.total_turns,
            "recent_symptoms": self.get_recent_symptoms(3),
            "recent_responses": self.get_recent_responses(2),
            "patient_demographics": self.patient_demographics,
            "medical_context": self.medical_context,
            "key_conversation_memory": {
                "symptoms_mentioned": self.conversation_memory.get("symptoms_mentioned", []),
                "key_topics_discussed": self.conversation_memory.get("key_topics_discussed", []),
                "concerns_raised": self.conversation_memory.get("concerns_raised", [])
            },
            "session_metadata": {
                "confidence_score": self.context_confidence_score,
                "session_duration_minutes": (datetime.utcnow() - self.session_start_time).total_seconds() / 60
            }
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert ConversationContext to dictionary for serialization
        
        Returns:
            Dictionary representation of the conversation context
        """
        return {
            "conversation_id": self.conversation_id,
            "patient_id": self.patient_id,
            "symptom_history": self.symptom_history,
            "patient_demographics": self.patient_demographics,
            "previous_responses": self.previous_responses,
            "medical_context": self.medical_context,
            "conversation_stage": self.conversation_stage,
            "session_start_time": self.session_start_time.isoformat(),
            "last_interaction_time": self.last_interaction_time.isoformat(),
            "total_turns": self.total_turns,
            "conversation_memory": self.conversation_memory,
            "context_confidence_score": self.context_confidence_score,
            "memory_retention_minutes": self.memory_retention_minutes
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationContext':
        """
        Create ConversationContext from dictionary
        
        Args:
            data: Dictionary containing conversation context data
            
        Returns:
            ConversationContext instance
        """
        # Parse datetime fields
        session_start_time = datetime.fromisoformat(data.get("session_start_time", datetime.utcnow().isoformat()))
        last_interaction_time = datetime.fromisoformat(data.get("last_interaction_time", datetime.utcnow().isoformat()))
        
        return cls(
            conversation_id=data.get("conversation_id", str(uuid.uuid4())),
            patient_id=data.get("patient_id"),
            symptom_history=data.get("symptom_history", []),
            patient_demographics=data.get("patient_demographics", {}),
            previous_responses=data.get("previous_responses", []),
            medical_context=data.get("medical_context", {}),
            conversation_stage=data.get("conversation_stage", "initial"),
            session_start_time=session_start_time,
            last_interaction_time=last_interaction_time,
            total_turns=data.get("total_turns", 0),
            conversation_memory=data.get("conversation_memory", {}),
            context_confidence_score=data.get("context_confidence_score", 0.0),
            memory_retention_minutes=data.get("memory_retention_minutes", 60)
        )
    
    def _update_interaction_time(self) -> None:
        """Update the last interaction timestamp"""
        self.last_interaction_time = datetime.utcnow()
    
    def _calculate_match_score(self, query: str, text: str) -> float:
        """
        Calculate match score for search functionality
        
        Args:
            query: Search query
            text: Text to search in
            
        Returns:
            Match score between 0.0 and 1.0
        """
        if not query or not text:
            return 0.0
        
        # Simple scoring based on frequency and position of matches
        query_words = query.split()
        text_words = text.split()
        
        matches = sum(1 for word in query_words if word in text)
        position_bonus = 0.1 if query in text[:100] else 0.0  # Bonus for early matches
        
        score = (matches / len(query_words)) + position_bonus
        return min(1.0, score)


# Conversation Context Manager for handling multiple conversations
class ConversationContextManager:
    """
    Manager class for handling multiple conversation contexts
    Provides storage and retrieval of conversation contexts for different patients/sessions
    """
    
    def __init__(self):
        self.active_contexts: Dict[str, ConversationContext] = {}
        self.max_active_contexts = 100  # Limit memory usage
    
    def create_context(self, patient_id: str = None) -> ConversationContext:
        """
        Create a new conversation context
        
        Args:
            patient_id: Optional patient identifier
            
        Returns:
            New ConversationContext instance
        """
        context = ConversationContext(patient_id=patient_id)
        self.active_contexts[context.conversation_id] = context
        
        # Clean up old contexts if we have too many
        self._cleanup_expired_contexts()
        
        return context
    
    def get_context(self, conversation_id: str) -> Optional[ConversationContext]:
        """
        Retrieve a conversation context by ID
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            ConversationContext if found, None otherwise
        """
        return self.active_contexts.get(conversation_id)
    
    def update_context(self, conversation_id: str, context: ConversationContext) -> None:
        """
        Update a stored conversation context
        
        Args:
            conversation_id: Conversation identifier
            context: Updated ConversationContext
        """
        self.active_contexts[conversation_id] = context
    
    def remove_context(self, conversation_id: str) -> bool:
        """
        Remove a conversation context
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            True if context was removed, False if not found
        """
        if conversation_id in self.active_contexts:
            del self.active_contexts[conversation_id]
            return True
        return False
    
    def get_contexts_by_patient(self, patient_id: str) -> List[ConversationContext]:
        """
        Get all conversation contexts for a specific patient
        
        Args:
            patient_id: Patient identifier
            
        Returns:
            List of ConversationContext instances for the patient
        """
        return [
            context for context in self.active_contexts.values()
            if context.patient_id == patient_id
        ]
    
    def _cleanup_expired_contexts(self) -> None:
        """Remove expired conversation contexts to manage memory"""
        expired_contexts = [
            conv_id for conv_id, context in self.active_contexts.items()
            if context.is_session_expired()
        ]
        
        for conv_id in expired_contexts:
            del self.active_contexts[conv_id]
        
        # If still too many contexts, remove oldest ones
        if len(self.active_contexts) > self.max_active_contexts:
            sorted_contexts = sorted(
                self.active_contexts.items(),
                key=lambda x: x[1].last_interaction_time
            )
            
            contexts_to_remove = len(self.active_contexts) - self.max_active_contexts
            for conv_id, _ in sorted_contexts[:contexts_to_remove]:
                del self.active_contexts[conv_id]


# Global conversation context manager instance
conversation_manager = ConversationContextManager()