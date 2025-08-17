import React, { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader } from './ui/dialog';
import { Button } from './ui/button';
import { X, Minimize2, Maximize2, AlertTriangle } from 'lucide-react';
import MedicalChatInterface from './MedicalChatInterface';
import { useMedicalChat } from '../hooks/useMedicalChat';

const ChatbotModal = ({ isOpen, onClose }) => {
  const [isMinimized, setIsMinimized] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [chatInitialized, setChatInitialized] = useState(false);
  
  const {
    consultation,
    messages,
    isLoading,
    initializeConsultation,
    sendMessage,
    generateReport
  } = useMedicalChat();

  useEffect(() => {
    if (isOpen && !chatInitialized) {
      initializeConsultation()
        .then(() => setChatInitialized(true))
        .catch(error => console.error('Failed to initialize consultation:', error));
    }
  }, [isOpen, chatInitialized, initializeConsultation]);

  const handleClose = () => {
    if (messages.length > 0) {
      // Show confirmation dialog if there's an active consultation
      if (window.confirm('Are you sure you want to end this medical consultation? Your conversation will be saved.')) {
        onClose();
      }
    } else {
      onClose();
    }
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
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden h-full flex flex-col">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-4 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
                <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
              </div>
              <div>
                <h3 className="font-semibold text-lg">AI Medical Consultation</h3>
                <p className="text-blue-100 text-sm">
                  {chatInitialized ? 'Connected to Dr. AI' : 'Initializing...'}
                </p>
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

          {/* Emergency Notice */}
          {!isMinimized && (
            <div className="bg-red-50 border-l-4 border-red-400 px-4 py-2">
              <div className="flex items-center">
                <AlertTriangle className="h-4 w-4 text-red-400 mr-2" />
                <p className="text-sm text-red-800">
                  If this is a medical emergency, call 911 or your local emergency services immediately.
                </p>
              </div>
            </div>
          )}

          {/* Chat Interface */}
          {!isMinimized && (
            <div className="flex-1 overflow-hidden">
              {chatInitialized ? (
                <MedicalChatInterface
                  consultation={consultation}
                  messages={messages}
                  isLoading={isLoading}
                  onSendMessage={sendMessage}
                  onGenerateReport={generateReport}
                  isFullscreen={isFullscreen}
                />
              ) : (
                <div className="flex items-center justify-center h-full">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">Initializing AI Medical Assistant...</p>
                    <p className="text-sm text-gray-500 mt-2">Loading medical knowledge base</p>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Minimized View */}
          {isMinimized && (
            <div className="flex-1 flex items-center justify-between px-4">
              <div className="flex items-center space-x-2">
                <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                <span className="text-sm font-medium">Medical Chat Active</span>
              </div>
              {messages.length > 0 && (
                <div className="text-xs text-gray-500">
                  {messages.length} messages
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default ChatbotModal;