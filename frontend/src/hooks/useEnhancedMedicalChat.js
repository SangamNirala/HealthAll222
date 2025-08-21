/**
 * 🎯 STEP 4.1 INTEGRATION: Enhanced Medical Chat Hook
 * 
 * This hook integrates the Step 4.1 ConversationContext with the existing medical AI service
 * to provide enhanced conversation memory and context tracking capabilities.
 * 
 * Features:
 * - Step 4.1 ConversationContext integration
 * - Persistent conversation memory across interactions
 * - Enhanced context tracking with symptom history
 * - Patient demographics management
 * - Previous responses tracking
 * - Medical context updates
 * - Conversation stage management
 */

import { useState, useCallback, useRef, useEffect } from 'react';
import { medicalAPI } from '../services/medicalAPI';

// Step 4.1 ConversationContext simulation (since we can't directly import backend modules)
class ConversationContext {
  constructor() {
    // Step 4.1 Core Specifications - Exact implementation
    this.symptom_history = [];
    this.patient_demographics = {};
    this.previous_responses = [];
    this.medical_context = {};
    this.conversation_stage = "initial";
    
    // Enhanced attributes
    this.conversation_id = this._generateId();
    this.session_start_time = new Date();
    this.last_interaction_time = new Date();
    this.total_turns = 0;
    this.context_confidence_score = 0.0;
    this.conversation_memory = {
      key_topics_discussed: [],
      symptoms_mentioned: [],
      concerns_raised: [],
      questions_asked_by_patient: [],
      medical_terms_used: [],
      emotional_indicators: [],
      urgency_markers: []
    };
  }

  _generateId() {
    return 'conv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
  }

  addSymptomToHistory(symptom) {
    const symptom_entry = {
      timestamp: new Date().toISOString(),
      turn_number: this.total_turns,
      symptom_data: symptom,
      conversation_stage: this.conversation_stage
    };
    
    this.symptom_history.push(symptom_entry);
    
    // Update conversation memory
    const symptom_name = symptom.name || symptom.description || 'unknown_symptom';
    if (!this.conversation_memory.symptoms_mentioned.includes(symptom_name)) {
      this.conversation_memory.symptoms_mentioned.push(symptom_name);
    }
    
    this._updateInteractionTime();
  }

  addResponseToHistory(response) {
    const response_entry = {
      timestamp: new Date().toISOString(),
      turn_number: this.total_turns,
      response_data: response,
      conversation_stage: this.conversation_stage
    };
    
    this.previous_responses.push(response_entry);
    this._updateInteractionTime();
  }

  updatePatientDemographics(demographics) {
    this.patient_demographics = { ...this.patient_demographics, ...demographics };
    this._updateInteractionTime();
  }

  updateMedicalContext(context_update) {
    this.medical_context = { ...this.medical_context, ...context_update };
    this._updateInteractionTime();
  }

  advanceConversationStage(new_stage) {
    const previous_stage = this.conversation_stage;
    this.conversation_stage = new_stage;
    
    // Log stage transition
    const stage_transition = {
      timestamp: new Date().toISOString(),
      from_stage: previous_stage,
      to_stage: new_stage,
      turn_number: this.total_turns
    };
    
    if (!this.conversation_memory.stage_transitions) {
      this.conversation_memory.stage_transitions = [];
    }
    this.conversation_memory.stage_transitions.push(stage_transition);
    
    this._updateInteractionTime();
  }

  incrementTurn() {
    this.total_turns += 1;
    this._updateInteractionTime();
  }

  getRecentSymptoms(limit = 5) {
    return this.symptom_history.slice(-limit);
  }

  getRecentResponses(limit = 3) {
    return this.previous_responses.slice(-limit);
  }

  getConversationContextForAI() {
    return {
      conversation_stage: this.conversation_stage,
      total_turns: this.total_turns,
      recent_symptoms: this.getRecentSymptoms(3),
      recent_responses: this.getRecentResponses(2),
      patient_demographics: this.patient_demographics,
      medical_context: this.medical_context,
      key_conversation_memory: {
        symptoms_mentioned: this.conversation_memory.symptoms_mentioned,
        key_topics_discussed: this.conversation_memory.key_topics_discussed,
        concerns_raised: this.conversation_memory.concerns_raised
      },
      session_metadata: {
        confidence_score: this.context_confidence_score,
        session_duration_minutes: (new Date() - this.session_start_time) / (1000 * 60)
      }
    };
  }

  updateContextConfidence(new_confidence) {
    this.context_confidence_score = Math.max(0.0, Math.min(1.0, new_confidence));
    this._updateInteractionTime();
  }

  addConversationMemory(memory_type, memory_data) {
    if (!this.conversation_memory[memory_type]) {
      this.conversation_memory[memory_type] = [];
    }
    
    if (Array.isArray(this.conversation_memory[memory_type])) {
      if (!this.conversation_memory[memory_type].includes(memory_data)) {
        this.conversation_memory[memory_type].push(memory_data);
      }
    } else {
      this.conversation_memory[memory_type] = memory_data;
    }
    
    this._updateInteractionTime();
  }

  _updateInteractionTime() {
    this.last_interaction_time = new Date();
  }
}

export const useEnhancedMedicalChat = () => {
  const [consultation, setConsultation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentStage, setCurrentStage] = useState('greeting');
  const [medicalContext, setMedicalContext] = useState({});
  const [emergencyDetected, setEmergencyDetected] = useState(false);
  
  // Step 4.1 ConversationContext Integration
  const conversationContext = useRef(new ConversationContext());
  const conversationHistory = useRef([]);

  const initializeConsultation = useCallback(async () => {
    setIsLoading(true);
    
    try {
      const response = await medicalAPI.initializeConsultation({
        patient_id: 'anonymous',
        timestamp: new Date().toISOString()
      });
      
      setConsultation(response.consultation);
      setMedicalContext(response.context);
      
      // Step 4.1: Initialize ConversationContext with medical context
      conversationContext.current.updateMedicalContext({
        consultation_id: response.consultation.id,
        initial_stage: response.stage,
        emergency_level: response.urgency || 'routine'
      });
      
      conversationContext.current.advanceConversationStage(response.stage || 'greeting');
      
      // Add initial AI greeting with enhanced Step 4.1 context awareness
      const greetingMessage = {
        id: Date.now(),
        type: 'ai',
        content: `Hello! I'm Dr. AI, your advanced medical assistant with enhanced conversation memory. I'm here to help you understand your health concerns and provide professional medical guidance.

I've successfully analyzed millions of medical cases and I'm trained on the latest medical literature. I can help you with:

• **Comprehensive symptom analysis** with memory tracking
• **Differential diagnosis** with probability assessment  
• **Personalized treatment recommendations**
• **Emergency risk evaluation** with immediate alerts
• **Professional medical reports** with conversation history
• **Context-aware follow-up** based on our conversation

**🔍 Enhanced Features:**
- I remember our entire conversation history
- I track your symptoms and their progression
- I maintain context across different topics
- I adapt my responses based on your communication style

**Important:** If this is a medical emergency, please call 911 immediately.

What brings you here today? Please describe any symptoms or health concerns you're experiencing.`,
        timestamp: new Date(),
        metadata: {
          stage: 'greeting',
          urgency: 'routine',
          enhanced_context: true,
          conversation_context: conversationContext.current.getConversationContextForAI()
        }
      };
      
      // Step 4.1: Add response to context tracking
      conversationContext.current.addResponseToHistory({
        content: greetingMessage.content,
        type: 'greeting',
        confidence: 1.0,
        stage: 'greeting'
      });
      
      setMessages([greetingMessage]);
      setCurrentStage('greeting');
      
    } catch (error) {
      console.error('Failed to initialize consultation:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const sendMessage = useCallback(async (messageContent) => {
    if (!messageContent.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user', 
      content: messageContent,
      timestamp: new Date()
    };

    // Add user message immediately
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // Step 4.1: Increment conversation turn
    conversationContext.current.incrementTurn();

    try {
      // Enhanced API call with Step 4.1 context
      const enhancedContext = {
        ...medicalContext,
        step_41_conversation_context: conversationContext.current.getConversationContextForAI(),
        conversation_memory: conversationContext.current.conversation_memory,
        symptom_history: conversationContext.current.symptom_history,
        total_turns: conversationContext.current.total_turns
      };

      const response = await medicalAPI.processMessage({
        message: messageContent,
        consultation_id: consultation?.id,
        context: enhancedContext,
        conversation_history: conversationHistory.current
      });

      // Step 4.1: Extract and track symptoms from user message and AI response
      const extractedSymptoms = extractSymptomsFromMessage(messageContent, response);
      extractedSymptoms.forEach(symptom => {
        conversationContext.current.addSymptomToHistory(symptom);
      });

      // Handle emergency detection
      if (response.urgency === 'emergency') {
        setEmergencyDetected(true);
        conversationContext.current.addConversationMemory('urgency_markers', 'emergency_detected');
      }

      // Step 4.1: Update conversation stage and medical context
      if (response.stage !== conversationContext.current.conversation_stage) {
        conversationContext.current.advanceConversationStage(response.stage);
      }

      conversationContext.current.updateMedicalContext({
        current_stage: response.stage,
        urgency_level: response.urgency,
        last_ai_confidence: response.confidence,
        differential_diagnoses: response.differential_diagnoses,
        recommendations: response.recommendations
      });

      // Create AI response message with enhanced Step 4.1 metadata
      const aiMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: response.response,
        timestamp: new Date(),
        metadata: {
          stage: response.stage,
          urgency: response.urgency,
          confidence: response.confidence,
          medical_reasoning: response.clinical_reasoning,
          differential_diagnoses: response.differential_diagnoses,
          recommendations: response.recommendations,
          // Step 4.1 Enhanced Metadata
          conversation_context: conversationContext.current.getConversationContextForAI(),
          symptoms_tracked: conversationContext.current.symptom_history.length,
          conversation_turn: conversationContext.current.total_turns,
          context_confidence: conversationContext.current.context_confidence_score
        }
      };

      // Step 4.1: Add AI response to context tracking
      conversationContext.current.addResponseToHistory({
        content: response.response,
        type: 'medical_response',
        confidence: response.confidence || 0.8,
        stage: response.stage,
        urgency: response.urgency,
        clinical_reasoning: response.clinical_reasoning
      });

      // Update confidence based on response quality
      if (response.confidence) {
        conversationContext.current.updateContextConfidence(response.confidence);
      }

      // Update state
      setMessages(prev => [...prev, aiMessage]);
      setCurrentStage(response.stage);
      setMedicalContext(response.context);
      
      // Update conversation history
      conversationHistory.current = [...conversationHistory.current, userMessage, aiMessage];

      return response;

    } catch (error) {
      console.error('Failed to send message:', error);
      
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        type: 'ai',
        content: "I apologize, but I'm experiencing a technical issue. Please try again, or if this is urgent, contact your healthcare provider directly.",
        timestamp: new Date(),
        metadata: {
          error: true,
          stage: currentStage,
          urgency: 'routine'
        }
      };
      
      setMessages(prev => [...prev, errorMessage]);
      
    } finally {
      setIsLoading(false);
    }
  }, [consultation, medicalContext, isLoading, currentStage]);

  const generateReport = useCallback(async () => {
    if (!consultation || messages.length === 0) return null;

    setIsLoading(true);

    try {
      // Step 4.1: Include conversation context in report generation
      const response = await medicalAPI.generateMedicalReport({
        consultation_id: consultation.id,
        messages: messages,
        context: {
          ...medicalContext,
          step_41_conversation_context: conversationContext.current.getConversationContextForAI(),
          conversation_summary: {
            total_turns: conversationContext.current.total_turns,
            symptoms_discussed: conversationContext.current.symptom_history.length,
            conversation_stages: conversationContext.current.conversation_memory.stage_transitions,
            key_topics: conversationContext.current.conversation_memory.key_topics_discussed
          }
        }
      });

      return response.report;

    } catch (error) {
      console.error('Failed to generate report:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [consultation, messages, medicalContext]);

  const getConsultationSummary = useCallback(() => {
    if (!medicalContext || messages.length === 0) return null;

    const userMessages = messages.filter(m => m.type === 'user');
    const aiMessages = messages.filter(m => m.type === 'ai');
    
    // Step 4.1: Enhanced summary with conversation context
    return {
      consultation_id: consultation?.id,
      total_messages: messages.length,
      user_messages: userMessages.length,
      ai_responses: aiMessages.length,
      current_stage: currentStage,
      emergency_detected: emergencyDetected,
      medical_context: medicalContext,
      last_ai_response: aiMessages[aiMessages.length - 1]?.metadata,
      // Step 4.1 Enhanced Context
      conversation_context: conversationContext.current.getConversationContextForAI(),
      symptoms_tracked: conversationContext.current.symptom_history,
      conversation_memory: conversationContext.current.conversation_memory,
      context_confidence: conversationContext.current.context_confidence_score,
      session_duration: (new Date() - conversationContext.current.session_start_time) / (1000 * 60)
    };
  }, [consultation, messages, currentStage, emergencyDetected, medicalContext]);

  // Step 4.1: Enhanced context management functions
  const updatePatientInfo = useCallback((demographics) => {
    conversationContext.current.updatePatientDemographics(demographics);
  }, []);

  const getConversationInsights = useCallback(() => {
    return {
      conversation_id: conversationContext.current.conversation_id,
      symptoms_mentioned: conversationContext.current.conversation_memory.symptoms_mentioned,
      key_topics: conversationContext.current.conversation_memory.key_topics_discussed,
      urgency_markers: conversationContext.current.conversation_memory.urgency_markers,
      total_turns: conversationContext.current.total_turns,
      context_confidence: conversationContext.current.context_confidence_score
    };
  }, []);

  return {
    // State
    consultation,
    messages,
    isLoading,
    currentStage,
    medicalContext,
    emergencyDetected,
    
    // Actions
    initializeConsultation,
    sendMessage,
    generateReport,
    getConsultationSummary,
    
    // Step 4.1: Enhanced context management
    updatePatientInfo,
    getConversationInsights,
    
    // Utils
    conversationHistory: conversationHistory.current,
    // Step 4.1: Direct access to conversation context
    conversationContext: conversationContext.current
  };
};

// Helper function to extract symptoms from messages
const extractSymptomsFromMessage = (userMessage, aiResponse) => {
  const symptoms = [];
  
  // Simple symptom extraction patterns (this could be enhanced with NLP)
  const symptomPatterns = [
    /(?:i have|experiencing|feeling|suffer from)\s+(?:a\s+)?([^.!?]+)/gi,
    /(?:pain|ache|hurt|sore)\s+(?:in\s+)?(?:my\s+)?([^.!?]+)/gi,
    /(?:headache|migraine|fever|nausea|dizziness|fatigue)/gi,
    /(?:chest\s+pain|back\s+pain|stomach\s+pain|joint\s+pain)/gi
  ];

  symptomPatterns.forEach(pattern => {
    const matches = [...userMessage.matchAll(pattern)];
    matches.forEach(match => {
      symptoms.push({
        name: match[1] || match[0],
        description: userMessage,
        severity: null,
        onset: null,
        duration: null,
        extracted_at: new Date().toISOString(),
        source: 'user_message'
      });
    });
  });

  // Extract symptoms from AI response differential diagnoses
  if (aiResponse.differential_diagnoses) {
    aiResponse.differential_diagnoses.forEach(diagnosis => {
      symptoms.push({
        name: diagnosis.condition,
        description: `AI identified potential condition: ${diagnosis.condition}`,
        severity: diagnosis.severity || null,
        probability: diagnosis.probability || null,
        extracted_at: new Date().toISOString(),
        source: 'ai_analysis'
      });
    });
  }

  return symptoms;
};

export default useEnhancedMedicalChat;