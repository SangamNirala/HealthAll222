import { useState, useCallback, useRef } from 'react';
import { medicalAPI } from '../services/medicalAPI';

export const useMedicalChat = () => {
  const [consultation, setConsultation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentStage, setCurrentStage] = useState('greeting');
  const [medicalContext, setMedicalContext] = useState({});
  const [emergencyDetected, setEmergencyDetected] = useState(false);
  
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
      
      // Add initial AI greeting with enhanced content
      const greetingMessage = {
        id: Date.now(),
        type: 'ai',
        content: `Hello! I'm Dr. AI, your personal medical assistant. I'm here to help you understand your health concerns and provide professional medical guidance.

I've successfully analyzed millions of medical cases and I'm trained on the latest medical literature. I can help you with:

• Symptom analysis and assessment
• Differential diagnosis with probabilities  
• Treatment recommendations
• When to seek immediate care
• Professional medical reports

**Important:** If this is a medical emergency, please call 911 immediately.

What brings you here today? Please describe any symptoms or health concerns you're experiencing.`,
        timestamp: new Date(),
        metadata: {
          stage: 'greeting',
          urgency: 'routine'
        }
      };
      
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

    try {
      // Send to medical AI service
      const response = await medicalAPI.processMessage({
        message: messageContent,
        consultation_id: consultation?.id,
        context: medicalContext,
        conversation_history: conversationHistory.current
      });

      // Handle emergency detection
      if (response.urgency === 'emergency') {
        setEmergencyDetected(true);
      }

      // Create AI response message
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
          recommendations: response.recommendations
        }
      };

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
      const response = await medicalAPI.generateMedicalReport({
        consultation_id: consultation.id,
        messages: messages,
        context: medicalContext
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
    
    return {
      consultation_id: consultation?.id,
      total_messages: messages.length,
      user_messages: userMessages.length,
      ai_responses: aiMessages.length,
      current_stage: currentStage,
      emergency_detected: emergencyDetected,
      medical_context: medicalContext,
      last_ai_response: aiMessages[aiMessages.length - 1]?.metadata
    };
  }, [consultation, messages, currentStage, emergencyDetected, medicalContext]);

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
    
    // Utils
    conversationHistory: conversationHistory.current
  };
};