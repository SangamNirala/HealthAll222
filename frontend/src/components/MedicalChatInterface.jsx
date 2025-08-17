import React, { useState, useEffect, useRef } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Badge } from './ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { 
  Send, User, Bot, Stethoscope, AlertTriangle, FileText, 
  Download, Clock, Activity, Heart, Brain, Shield, Zap
} from 'lucide-react';
import '../styles/medical-grade.css';

const MedicalChatInterface = ({ 
  consultation, 
  messages, 
  isLoading, 
  onSendMessage, 
  onGenerateReport, 
  isFullscreen 
}) => {
  const [inputMessage, setInputMessage] = useState('');
  const [emergencyDetected, setEmergencyDetected] = useState(false);
  const [currentStage, setCurrentStage] = useState('greeting');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Update emergency status based on latest messages
    const latestMessage = messages[messages.length - 1];
    if (latestMessage?.metadata?.urgency === 'emergency') {
      setEmergencyDetected(true);
    }
    if (latestMessage?.metadata?.stage) {
      setCurrentStage(latestMessage.metadata.stage);
    }
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;
    
    const messageText = inputMessage;
    setInputMessage('');
    
    try {
      await onSendMessage(messageText);
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

  const getStageDisplay = (stage) => {
    const stageMap = {
      greeting: 'Initial Consultation',
      chief_complaint: 'Chief Complaint',
      history_present_illness: 'Medical History',
      review_of_systems: 'Symptom Review',
      past_medical_history: 'Past Medical History',
      medications_allergies: 'Medications & Allergies',
      social_family_history: 'Social & Family History',
      risk_assessment: 'Risk Assessment',
      differential_diagnosis: 'Diagnosis Analysis',
      recommendations: 'Treatment Plan',
      completed: 'Consultation Complete'
    };
    return stageMap[stage] || 'Medical Assessment';
  };

  const formatMessageContent = (content) => {
    // Enhanced formatting for medical content
    const formattedContent = content
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/• /g, '• ')
      .replace(/\n/g, '<br />')
      .replace(/(Call 911|Emergency|EMERGENCY|911)/gi, '<span class="medical-text-emergency">$1</span>');
    
    return { __html: formattedContent };
  };

  return (
    <div className="medical-interface flex flex-col h-full bg-gradient-to-br from-blue-50 to-white">
      
      {/* Medical Header */}
      <div className="medical-card-header flex items-center justify-between p-4 bg-gradient-to-r from-blue-600 to-blue-700 text-white">
        <div className="flex items-center space-x-3">
          <div className="medical-status medical-status-online bg-white/20 text-white">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
            <span className="medical-text-sm">Dr. AI Online</span>
          </div>
          <div className="text-blue-100 text-sm">
            Stage: {getStageDisplay(currentStage)}
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {consultation && (
            <div className="medical-badge medical-badge-info bg-white/20 text-white">
              ID: {consultation.id?.slice(-8) || 'Unknown'}
            </div>
          )}
          
          {messages.length > 5 && (
            <Button
              onClick={onGenerateReport}
              className="medical-btn medical-btn-secondary bg-white/20 hover:bg-white/30 text-white border-white/30"
              size="sm"
            >
              <FileText className="h-4 w-4 mr-2" />
              Generate Report
            </Button>
          )}
        </div>
      </div>

      {/* Emergency Alert */}
      {emergencyDetected && (
        <div className="medical-alert medical-alert-emergency m-4 animate-pulse">
          <AlertTriangle className="h-5 w-5 flex-shrink-0" />
          <div>
            <h4 className="font-semibold">🚨 Medical Emergency Detected</h4>
            <p className="text-sm mt-1">
              Critical symptoms identified. If you haven't already, please call 911 or seek immediate medical attention.
            </p>
          </div>
        </div>
      )}

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={message.id || index}
            className={`flex items-start space-x-3 ${
              message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''
            }`}
          >
            {/* Avatar */}
            <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
              message.type === 'user' 
                ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white' 
                : 'bg-gradient-to-br from-teal-500 to-teal-600 text-white'
            }`}>
              {message.type === 'user' ? (
                <User className="h-5 w-5" />
              ) : (
                <Stethoscope className="h-5 w-5" />
              )}
            </div>

            {/* Message Content */}
            <div className={`flex-1 max-w-3xl ${
              message.type === 'user' ? 'text-right' : 'text-left'
            }`}>
              
              {/* Message Bubble */}
              <div className={`medical-card inline-block p-4 rounded-lg ${
                message.type === 'user'
                  ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white ml-auto'
                  : 'bg-white border border-gray-200 medical-shadow-sm'
              }`}>
                
                {message.type === 'ai' && (
                  <div className="flex items-center space-x-2 mb-2 text-sm text-gray-600">
                    <Bot className="h-4 w-4 text-teal-500" />
                    <span className="font-medium">Dr. AI</span>
                    {message.metadata?.urgency && (
                      <span className={`medical-badge ${
                        message.metadata.urgency === 'emergency' ? 'medical-badge-critical' :
                        message.metadata.urgency === 'urgent' ? 'medical-badge-urgent' :
                        'medical-badge-routine'
                      }`}>
                        {message.metadata.urgency}
                      </span>
                    )}
                  </div>
                )}
                
                <div 
                  className={`medical-text-sm leading-relaxed ${
                    message.type === 'user' ? 'text-white' : 'text-gray-800'
                  }`}
                  dangerouslySetInnerHTML={formatMessageContent(message.content)}
                />
                
                {/* Medical Metadata */}
                {message.metadata && message.type === 'ai' && (
                  <div className="mt-3 pt-3 border-t border-gray-100">
                    
                    {/* Confidence Score */}
                    {message.metadata.confidence && (
                      <div className="flex items-center space-x-2 text-xs text-gray-500 mb-2">
                        <Brain className="h-3 w-3" />
                        <span>AI Confidence: {Math.round(message.metadata.confidence * 100)}%</span>
                        <div className="medical-progress flex-1 max-w-16">
                          <div 
                            className="medical-progress-bar"
                            style={{ width: `${message.metadata.confidence * 100}%` }}
                          />
                        </div>
                      </div>
                    )}
                    
                    {/* Differential Diagnoses Preview */}
                    {message.metadata.differential_diagnoses && message.metadata.differential_diagnoses.length > 0 && (
                      <div className="mt-2 p-2 bg-blue-50 rounded-md">
                        <div className="text-xs font-medium text-blue-800 mb-1 flex items-center">
                          <Activity className="h-3 w-3 mr-1" />
                          Likely Conditions:
                        </div>
                        <div className="space-y-1">
                          {message.metadata.differential_diagnoses.slice(0, 2).map((diagnosis, idx) => (
                            <div key={idx} className="text-xs text-blue-700 flex justify-between">
                              <span>{diagnosis.condition}</span>
                              <span className="medical-badge medical-badge-info">
                                {diagnosis.probability}%
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Timestamp */}
              <div className={`text-xs text-gray-500 mt-1 flex items-center ${
                message.type === 'user' ? 'justify-end' : 'justify-start'
              }`}>
                <Clock className="h-3 w-3 mr-1" />
                {message.timestamp ? new Date(message.timestamp).toLocaleTimeString() : 'Now'}
              </div>
            </div>
          </div>
        ))}

        {/* Typing Indicator */}
        {isLoading && (
          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-teal-500 to-teal-600 text-white flex items-center justify-center">
              <Stethoscope className="h-5 w-5" />
            </div>
            <div className="medical-card bg-white p-4 rounded-lg border border-gray-200">
              <div className="flex items-center space-x-2 text-gray-600">
                <div className="medical-spinner"></div>
                <span className="medical-text-sm">Dr. AI is analyzing...</span>
              </div>
              <div className="text-xs text-gray-500 mt-2 flex items-center">
                <Brain className="h-3 w-3 mr-1" />
                Processing medical information
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-white p-4">
        <div className="flex items-end space-x-3">
          <div className="flex-1">
            <div className="relative">
              <Input
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Describe your symptoms or ask a medical question..."
                disabled={isLoading}
                className="medical-input pr-12 min-h-[44px] resize-none"
              />
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2 flex items-center space-x-1">
                {emergencyDetected && (
                  <AlertTriangle className="h-4 w-4 text-red-500" />
                )}
                <Shield className="h-4 w-4 text-gray-400" title="HIPAA Compliant" />
              </div>
            </div>
            
            {/* Quick Actions */}
            <div className="flex items-center justify-between mt-2 text-xs text-gray-500">
              <div className="flex items-center space-x-4">
                <span className="flex items-center">
                  <Heart className="h-3 w-3 mr-1 text-red-400" />
                  Emergency? Call 911 first
                </span>
                <span className="flex items-center">
                  <Shield className="h-3 w-3 mr-1 text-green-400" />
                  Anonymous & Private
                </span>
              </div>
              <span className="text-gray-400">Press Enter to send</span>
            </div>
          </div>
          
          <Button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="medical-btn medical-btn-primary h-11 px-6"
          >
            {isLoading ? (
              <div className="medical-spinner border-white"></div>
            ) : (
              <>
                <Send className="h-4 w-4 mr-2" />
                Send
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default MedicalChatInterface;