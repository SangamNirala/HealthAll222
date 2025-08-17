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

  const handleGenerateReport = async () => {
    try {
      await onGenerateReport();
    } catch (error) {
      console.error('Failed to generate report:', error);
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

  const getStageIcon = (stage) => {
    const stageIcons = {
      'greeting': Stethoscope,
      'chief_complaint': AlertTriangle,
      'history_present_illness': Activity,
      'review_of_systems': Heart,
      'past_medical_history': Clock,
      'medications_allergies': FileText,
      'social_family_history': User,
      'differential_diagnosis': Brain,
      'assessment_complete': FileText,
      'emergency_detected': AlertTriangle
    };
    return stageIcons[stage] || Stethoscope;
  };

  const StageIcon = getStageIcon(currentStage);

  return (
    <div className="h-full flex flex-col">
      {/* Medical Status Bar */}
      <div className="bg-gray-50 border-b border-gray-200 px-4 py-3 flex items-center justify-between flex-shrink-0">
        <div className="flex items-center space-x-3">
          <StageIcon className={`w-4 h-4 ${emergencyDetected ? 'text-red-500' : 'text-blue-600'}`} />
          <span className="text-sm font-medium text-gray-700">
            Current Stage: {getStageName(currentStage)}
          </span>
          {emergencyDetected && (
            <Badge variant="destructive" className="text-xs">
              Emergency Protocol Active
            </Badge>
          )}
        </div>
        
        <div className="flex items-center space-x-2">
          {messages.length > 5 && (
            <Button
              variant="outline"
              size="sm"
              onClick={handleGenerateReport}
              className="text-xs"
            >
              <FileText className="w-3 h-3 mr-1" />
              Generate Report
            </Button>
          )}
          <div className="text-xs text-gray-500">
            {messages.length} messages
          </div>
        </div>
      </div>

      {/* Emergency Alert Banner */}
      {emergencyDetected && (
        <div className="bg-red-50 border-l-4 border-red-400 px-4 py-3 flex-shrink-0">
          <div className="flex items-start space-x-3">
            <AlertTriangle className="h-5 w-5 text-red-400 mt-0.5 flex-shrink-0" />
            <div className="flex-1">
              <h4 className="text-sm font-semibold text-red-800">
                Medical Emergency Detected
              </h4>
              <p className="text-sm text-red-700 mt-1">
                If this is a medical emergency, call 911 or go to your nearest emergency room immediately.
              </p>
              <div className="mt-2 flex flex-wrap gap-2 text-xs text-red-700">
                <span>🇺🇸 Emergency: 911</span>
                <span>🇺🇸 Poison Control: 1-800-222-1222</span>
                <span>🇺🇸 Crisis Line: 988</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Messages Area */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full flex flex-col">
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.length > 0 ? (
              messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[85%] ${
                    message.type === 'user' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-100 text-gray-900 border border-gray-200'
                  } rounded-lg p-3 shadow-sm`}>
                    <div className="flex items-start space-x-2">
                      <div className="flex-shrink-0">
                        {message.type === 'user' ? (
                          <User className="w-4 h-4 mt-1" />
                        ) : (
                          <Bot className="w-4 h-4 mt-1 text-blue-600" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="text-sm whitespace-pre-wrap break-words">
                          {message.content}
                        </div>
                        
                        {/* Message Metadata */}
                        <div className="flex items-center justify-between mt-2">
                          <div className="flex items-center space-x-2">
                            {message.metadata?.urgency && (
                              <Badge 
                                variant={getUrgencyBadgeColor(message.metadata.urgency)}
                                className="text-xs"
                              >
                                {message.metadata.urgency}
                              </Badge>
                            )}
                            {message.metadata?.stage && message.type === 'ai' && (
                              <Badge variant="outline" className="text-xs">
                                {getStageName(message.metadata.stage)}
                              </Badge>
                            )}
                          </div>
                          
                          <div className={`text-xs opacity-75 ${
                            message.type === 'user' ? 'text-blue-100' : 'text-gray-500'
                          }`}>
                            {message.timestamp.toLocaleTimeString([], { 
                              hour: '2-digit', 
                              minute: '2-digit' 
                            })}
                          </div>
                        </div>

                        {/* AI Response Metadata */}
                        {message.type === 'ai' && message.metadata && (
                          <div className="mt-2 pt-2 border-t border-gray-300">
                            {message.metadata.differential_diagnoses && (
                              <div className="text-xs text-gray-600">
                                <strong>Diagnostic Considerations:</strong> {message.metadata.differential_diagnoses.length} conditions assessed
                              </div>
                            )}
                            {message.metadata.recommendations && (
                              <div className="text-xs text-gray-600 mt-1">
                                <strong>Recommendations:</strong> {message.metadata.recommendations.length} items
                              </div>
                            )}
                          </div>
                        )}
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
            
            {/* Loading Indicator */}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 border border-gray-200 rounded-lg p-3 shadow-sm">
                  <div className="flex items-center space-x-2">
                    <Bot className="w-4 h-4 text-blue-600" />
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                    <span className="text-xs text-gray-600">Dr. AI is analyzing...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Medical Input Area */}
          <div className="border-t border-gray-200 bg-white flex-shrink-0">
            {/* Quick Response Suggestions */}
            {messages.length > 0 && !isLoading && (
              <div className="px-4 py-2 border-b border-gray-100">
                <div className="flex flex-wrap gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setInputMessage("Can you explain that in simpler terms?")}
                    className="text-xs"
                  >
                    Explain Simply
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setInputMessage("What should I do next?")}
                    className="text-xs"
                  >
                    Next Steps
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setInputMessage("How serious is this?")}
                    className="text-xs"
                  >
                    Severity
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setInputMessage("When should I see a doctor?")}
                    className="text-xs"
                  >
                    Doctor Visit
                  </Button>
                </div>
              </div>
            )}

            {/* Main Input */}
            <div className="p-4">
              <div className="flex items-end space-x-3">
                <div className="flex-1">
                  <Input
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Describe your symptoms, ask questions, or request clarification..."
                    disabled={isLoading}
                    className="min-h-[40px] resize-none"
                  />
                </div>
                <Button
                  onClick={handleSendMessage}
                  disabled={isLoading || !inputMessage.trim()}
                  className="bg-blue-600 hover:bg-blue-700 px-4 py-2"
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
              
              {/* Medical Disclaimer */}
              <p className="text-xs text-gray-500 mt-2 text-center">
                This AI assistant provides information only. For emergencies, call 911. 
                Always consult healthcare professionals for medical decisions.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Medical Context Panel (for fullscreen mode) */}
      {isFullscreen && messages.length > 3 && (
        <div className="w-80 border-l border-gray-200 bg-gray-50 flex-shrink-0">
          <div className="p-4">
            <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
              <FileText className="w-4 h-4 mr-2" />
              Consultation Summary
            </h3>
            
            <div className="space-y-3">
              <Card className="p-3">
                <div className="text-xs text-gray-600 uppercase tracking-wide mb-1">
                  Conversation Stage
                </div>
                <div className="font-medium text-sm">{getStageName(currentStage)}</div>
              </Card>
              
              <Card className="p-3">
                <div className="text-xs text-gray-600 uppercase tracking-wide mb-1">
                  Message Count
                </div>
                <div className="font-medium text-sm">{messages.length} exchanges</div>
              </Card>

              <Card className="p-3">
                <div className="text-xs text-gray-600 uppercase tracking-wide mb-1">
                  Status
                </div>
                <div className={`font-medium text-sm ${
                  emergencyDetected ? 'text-red-600' : 'text-green-600'
                }`}>
                  {emergencyDetected ? 'Emergency Detected' : 'Routine Consultation'}
                </div>
              </Card>

              {messages.length > 5 && (
                <Button
                  onClick={handleGenerateReport}
                  className="w-full mt-4"
                  variant="outline"
                >
                  <Download className="w-4 h-4 mr-2" />
                  Generate Medical Report
                </Button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MedicalChatInterface;