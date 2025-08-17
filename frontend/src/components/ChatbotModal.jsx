import React, { useState, useEffect, useRef } from 'react';
import { Dialog, DialogContent, DialogHeader } from './ui/dialog';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { X, Minimize2, Maximize2, AlertTriangle, Send, User, Bot, Stethoscope } from 'lucide-react';
import { useMedicalChat } from '../hooks/useMedicalChat';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';

const ChatbotModal = ({ isOpen, onClose }) => {
  const [isMinimized, setIsMinimized] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef(null);
  
  const {
    consultation,
    messages,
    isLoading,
    emergencyDetected,
    currentStage,
    initializeConsultation,
    sendMessage,
    generateReport
  } = useMedicalChat();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && !consultation) {
      initializeConsultation().catch(error => {
        console.error('Failed to initialize consultation:', error);
      });
    }
  }, [isOpen, consultation, initializeConsultation]);

  const handleClose = () => {
    if (messages.length > 0) {
      const shouldClose = window.confirm(
        'Are you sure you want to end this medical consultation? Your conversation will be saved.'
      );
      if (shouldClose) {
        onClose();
      }
    } else {
      onClose();
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;
    
    const messageText = inputMessage;
    setInputMessage('');
    
    try {
      await sendMessage(messageText);
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const getUrgencyBadgeColor = (urgency) => {
    switch (urgency) {
      case 'emergency':
        return 'destructive';
      case 'urgent':
        return 'destructive';
      case 'routine':
      default:
        return 'secondary';
    }
  };

  const getStageName = (stage) => {
    const stageNames = {
      'greeting': 'Welcome',
      'chief_complaint': 'Describing Symptoms',
      'history_present_illness': 'Symptom Details', 
      'review_of_systems': 'Related Symptoms',
      'past_medical_history': 'Medical History',
      'medications_allergies': 'Medications & Allergies',
      'social_family_history': 'Background History',
      'differential_diagnosis': 'Analysis',
      'assessment_complete': 'Assessment Complete',
      'emergency_detected': 'Emergency Alert'
    };
    return stageNames[stage] || 'Consultation';
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50" />
      
      {/* Modal */}
      <div className={`fixed z-50 transition-all duration-300 ${
        isFullscreen 
          ? 'inset-0' 
          : isMinimized 
          ? 'bottom-4 right-4 w-80 h-16'
          : 'top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[95vw] h-[90vh] max-w-6xl max-h-[800px]'
      }`}>
        <Card className="h-full flex flex-col bg-white shadow-2xl">
          {/* Header */}
          <CardHeader className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-4 flex-shrink-0">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
                  <div className={`w-3 h-3 rounded-full animate-pulse ${
                    consultation ? 'bg-green-400' : 'bg-yellow-400'
                  }`}></div>
                </div>
                <div>
                  <h3 className="font-semibold text-lg flex items-center">
                    <Stethoscope className="w-5 h-5 mr-2" />
                    AI Medical Consultation
                  </h3>
                  <div className="flex items-center space-x-2">
                    <p className="text-blue-100 text-sm">
                      {consultation ? `Dr. AI • ${getStageName(currentStage)}` : 'Initializing...'}
                    </p>
                    {emergencyDetected && (
                      <Badge variant="destructive" className="text-xs">
                        Emergency Detected
                      </Badge>
                    )}
                  </div>
                </div>
              </div>
              
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
          </CardHeader>

          {/* Emergency Notice */}
          {!isMinimized && emergencyDetected && (
            <div className="bg-red-50 border-l-4 border-red-400 px-4 py-3 flex-shrink-0">
              <div className="flex items-center">
                <AlertTriangle className="h-5 w-5 text-red-400 mr-3" />
                <div>
                  <p className="text-sm text-red-800 font-semibold">
                    Medical Emergency Detected
                  </p>
                  <p className="text-sm text-red-700">
                    If this is a medical emergency, call 911 or your local emergency services immediately.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Chat Interface */}
          {!isMinimized && (
            <>
              {/* Messages Area */}
              <CardContent className="flex-1 overflow-hidden p-0">
                <div className="h-full flex flex-col">
                  <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {consultation ? (
                      messages.map((message, index) => (
                        <div
                          key={index}
                          className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                          <div className={`max-w-[80%] ${
                            message.type === 'user' 
                              ? 'bg-blue-600 text-white' 
                              : 'bg-gray-100 text-gray-900'
                          } rounded-lg p-3 shadow-sm`}>
                            <div className="flex items-start space-x-2">
                              <div className="flex-shrink-0">
                                {message.type === 'user' ? (
                                  <User className="w-4 h-4 mt-1" />
                                ) : (
                                  <Bot className="w-4 h-4 mt-1 text-blue-600" />
                                )}
                              </div>
                              <div className="flex-1">
                                <div className="text-sm whitespace-pre-wrap">
                                  {message.content}
                                </div>
                                {message.metadata?.urgency && (
                                  <Badge 
                                    variant={getUrgencyBadgeColor(message.metadata.urgency)}
                                    className="mt-2 text-xs"
                                  >
                                    {message.metadata.urgency}
                                  </Badge>
                                )}
                                <div className={`text-xs mt-1 opacity-75 ${
                                  message.type === 'user' ? 'text-blue-100' : 'text-gray-500'
                                }`}>
                                  {message.timestamp.toLocaleTimeString([], { 
                                    hour: '2-digit', 
                                    minute: '2-digit' 
                                  })}
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="flex items-center justify-center h-full">
                        <div className="text-center">
                          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                          <p className="text-gray-600">Initializing AI Medical Assistant...</p>
                          <p className="text-sm text-gray-500 mt-2">Loading medical knowledge base</p>
                        </div>
                      </div>
                    )}
                    
                    {isLoading && (
                      <div className="flex justify-start">
                        <div className="bg-gray-100 rounded-lg p-3 shadow-sm">
                          <div className="flex items-center space-x-2">
                            <Bot className="w-4 h-4 text-blue-600" />
                            <div className="flex space-x-1">
                              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
                              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                              <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                    <div ref={messagesEndRef} />
                  </div>

                  {/* Input Area */}
                  <div className="border-t border-gray-200 p-4 flex-shrink-0">
                    <div className="flex items-center space-x-3">
                      <Input
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Describe your symptoms or ask a medical question..."
                        disabled={isLoading || !consultation}
                        className="flex-1"
                      />
                      <Button
                        onClick={handleSendMessage}
                        disabled={isLoading || !inputMessage.trim() || !consultation}
                        className="bg-blue-600 hover:bg-blue-700"
                      >
                        <Send className="w-4 h-4" />
                      </Button>
                    </div>
                    <p className="text-xs text-gray-500 mt-2 text-center">
                      This is for informational purposes only. Call 911 for emergencies.
                    </p>
                  </div>
                </div>
              </CardContent>
            </>
          )}

          {/* Minimized View */}
          {isMinimized && (
            <CardContent className="flex-1 flex items-center justify-between px-4">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium">Medical Chat Active</span>
                {emergencyDetected && (
                  <AlertTriangle className="w-4 h-4 text-red-500" />
                )}
              </div>
              {messages.length > 0 && (
                <div className="text-xs text-gray-500">
                  {messages.length} messages
                </div>
              )}
            </CardContent>
          )}
        </Card>
      </div>
    </>
  );
};

export default ChatbotModal;