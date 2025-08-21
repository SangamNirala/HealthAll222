/**
 * 🎯 STEP 4.1 INTEGRATION: Enhanced Chatbot Modal
 * 
 * Enhanced chatbot modal that integrates Step 4.1 ConversationContext features
 * with the existing medical chat system for improved conversation management.
 */

import React, { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader } from './ui/dialog';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { X, Minimize2, Maximize2, AlertTriangle, Memory, Activity, Brain } from 'lucide-react';
import EnhancedMedicalChatInterface from './EnhancedMedicalChatInterface';
import { useEnhancedMedicalChat } from '../hooks/useEnhancedMedicalChat';

const EnhancedChatbotModal = ({ isOpen, onClose }) => {
  const [isMinimized, setIsMinimized] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [chatInitialized, setChatInitialized] = useState(false);
  
  const {
    consultation,
    messages,
    isLoading,
    currentStage,
    emergencyDetected,
    initializeConsultation,
    sendMessage,
    generateReport,
    // Step 4.1 Enhanced Features
    conversationContext,
    updatePatientInfo,
    getConversationInsights
  } = useEnhancedMedicalChat();

  useEffect(() => {
    if (isOpen && !chatInitialized) {
      initializeConsultation()
        .then(() => setChatInitialized(true))
        .catch(error => console.error('Failed to initialize enhanced consultation:', error));
    }
  }, [isOpen, chatInitialized, initializeConsultation]);

  const handleClose = () => {
    if (messages.length > 0) {
      // Enhanced confirmation with Step 4.1 context information
      const insights = getConversationInsights();
      const confirmMessage = `Are you sure you want to end this medical consultation?

Conversation Summary:
• ${insights.total_turns} conversation turns
• ${insights.symptoms_mentioned.length} symptoms tracked
• Current stage: ${currentStage}
• Context confidence: ${Math.round(insights.context_confidence * 100)}%

Your conversation history and context will be saved securely.`;

      if (window.confirm(confirmMessage)) {
        onClose();
      }
    } else {
      onClose();
    }
  };

  const getConversationStats = () => {
    if (!conversationContext) return null;
    
    return {
      turns: conversationContext.total_turns || 0,
      symptoms: conversationContext.symptom_history?.length || 0,
      confidence: Math.round((conversationContext.context_confidence_score || 0) * 100),
      stage: conversationContext.conversation_stage || 'initial'
    };
  };

  const stats = getConversationStats();

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50" />
      
      {/* Enhanced Modal */}
      <div className={`fixed z-50 transition-all duration-300 ${
        isFullscreen 
          ? 'inset-0' 
          : isMinimized 
          ? 'bottom-4 right-4 w-80 h-20'
          : 'top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[95vw] h-[90vh] max-w-7xl max-h-[850px]'
      }`}>
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden h-full flex flex-col">
          
          {/* Enhanced Header with Step 4.1 Information */}
          <div className="bg-gradient-to-r from-blue-600 to-teal-600 text-white px-6 py-4 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
                <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
              </div>
              <div>
                <h3 className="font-semibold text-lg flex items-center">
                  AI Medical Consultation
                  <Badge className="ml-2 bg-green-500/20 text-white border-green-300 text-xs">
                    Enhanced
                  </Badge>
                </h3>
                <p className="text-blue-100 text-sm flex items-center space-x-2">
                  <span>{chatInitialized ? 'Connected to Dr. AI Enhanced' : 'Initializing enhanced system...'}</span>
                  {chatInitialized && (
                    <Memory className="h-3 w-3 ml-1" title="Context Tracking Active" />
                  )}
                </p>
              </div>
            </div>
            
            {/* Step 4.1: Enhanced Stats Display */}
            {chatInitialized && stats && !isMinimized && (
              <div className="hidden md:flex items-center space-x-4 text-xs">
                <div className="flex items-center space-x-1 bg-white/10 rounded px-2 py-1">
                  <Activity className="h-3 w-3" />
                  <span>{stats.turns} turns</span>
                </div>
                <div className="flex items-center space-x-1 bg-white/10 rounded px-2 py-1">
                  <Memory className="h-3 w-3" />
                  <span>{stats.symptoms} symptoms</span>
                </div>
                <div className="flex items-center space-x-1 bg-white/10 rounded px-2 py-1">
                  <Brain className="h-3 w-3" />
                  <span>{stats.confidence}% confidence</span>
                </div>
              </div>
            )}
            
            <div className="flex items-center space-x-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsMinimized(!isMinimized)}
                className="text-white hover:bg-white/20 p-2"
              >
                <Minimize2 className="h-4 w-4" />
              </Button>
              
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsFullscreen(!isFullscreen)}
                className="text-white hover:bg-white/20 p-2"
              >
                <Maximize2 className="h-4 w-4" />
              </Button>
              
              <Button
                variant="ghost"
                size="sm"
                onClick={handleClose}
                className="text-white hover:bg-white/20 p-2"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Enhanced Emergency Notice */}
          {!isMinimized && (
            <div className="bg-gradient-to-r from-red-50 to-orange-50 border-l-4 border-red-400 px-4 py-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <AlertTriangle className="h-4 w-4 text-red-400 mr-2" />
                  <p className="text-sm text-red-800">
                    If this is a medical emergency, call 911 or your local emergency services immediately.
                  </p>
                </div>
                {emergencyDetected && (
                  <Badge variant="destructive" className="animate-pulse">
                    EMERGENCY DETECTED
                  </Badge>
                )}
              </div>
            </div>
          )}

          {/* Enhanced Chat Interface */}
          {!isMinimized && (
            <div className="flex-1 overflow-hidden">
              {chatInitialized ? (
                <EnhancedMedicalChatInterface
                  consultation={consultation}
                  messages={messages}
                  isLoading={isLoading}
                  onSendMessage={sendMessage}
                  onGenerateReport={generateReport}
                  isFullscreen={isFullscreen}
                  // Step 4.1 Enhanced Props
                  conversationContext={conversationContext}
                  conversationInsights={getConversationInsights}
                  onUpdatePatientInfo={updatePatientInfo}
                />
              ) : (
                <div className="flex items-center justify-center h-full">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">Initializing Enhanced AI Medical Assistant...</p>
                    <div className="text-sm text-gray-500 mt-2 space-y-1">
                      <p>✓ Loading medical knowledge base</p>
                      <p>✓ Initializing Step 4.1 conversation context</p>
                      <p>✓ Activating enhanced memory tracking</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Enhanced Minimized View with Step 4.1 Stats */}
          {isMinimized && (
            <div className="flex-1 flex items-center justify-between px-4">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium">Enhanced Medical Chat Active</span>
                <Memory className="h-3 w-3 text-blue-500" />
              </div>
              {stats && (
                <div className="flex items-center space-x-2 text-xs text-gray-500">
                  <Badge variant="outline" className="text-xs">
                    {stats.turns} turns
                  </Badge>
                  <Badge variant="outline" className="text-xs">
                    {stats.symptoms} symptoms
                  </Badge>
                  <Badge variant="outline" className="text-xs">
                    {stats.confidence}%
                  </Badge>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default EnhancedChatbotModal;