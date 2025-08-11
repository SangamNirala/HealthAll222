import React, { useState, useEffect, useRef } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  Mic, 
  MicOff, 
  Volume2, 
  VolumeX, 
  CheckCircle, 
  AlertCircle, 
  Loader2,
  MessageSquare
} from 'lucide-react';
import geminiService from '../../services/geminiService';

// Custom hook for voice recognition
const useVoiceRecognition = () => {
  const [isSupported, setIsSupported] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState(null);
  const recognition = useRef(null);

  useEffect(() => {
    // Check if browser supports Speech Recognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (SpeechRecognition) {
      setIsSupported(true);
      recognition.current = new SpeechRecognition();
      
      // Configure recognition
      recognition.current.continuous = false;
      recognition.current.interimResults = true;
      recognition.current.lang = 'en-US';

      recognition.current.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';

        for (let i = 0; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }

        setTranscript(finalTranscript || interimTranscript);
      };

      recognition.current.onstart = () => {
        setIsListening(true);
        setError(null);
      };

      recognition.current.onend = () => {
        setIsListening(false);
      };

      recognition.current.onerror = (event) => {
        setError(event.error);
        setIsListening(false);
      };
    } else {
      setIsSupported(false);
      setError('Speech recognition is not supported in this browser');
    }

    return () => {
      if (recognition.current) {
        recognition.current.stop();
      }
    };
  }, []);

  const startListening = () => {
    if (recognition.current && !isListening) {
      setTranscript('');
      setError(null);
      recognition.current.start();
    }
  };

  const stopListening = () => {
    if (recognition.current && isListening) {
      recognition.current.stop();
    }
  };

  return {
    isSupported,
    isListening,
    transcript,
    error,
    startListening,
    stopListening
  };
};

const VoiceLogging = ({ userId, onFoodLogged }) => {
  const [processedFoods, setProcessedFoods] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingError, setProcessingError] = useState(null);
  const [confidence, setConfidence] = useState(0);
  const [audioEnabled, setAudioEnabled] = useState(true);
  
  const {
    isSupported,
    isListening,
    transcript,
    error: voiceError,
    startListening,
    stopListening
  } = useVoiceRecognition();

  const audioRef = useRef(null);

  useEffect(() => {
    // Process transcript when voice recognition stops
    if (transcript && !isListening && !isProcessing) {
      processVoiceCommand(transcript);
    }
  }, [transcript, isListening, isProcessing]);

  const processVoiceCommand = async (voiceTranscript) => {
    if (!voiceTranscript.trim()) return;

    setIsProcessing(true);
    setProcessingError(null);
    setProcessedFoods([]);

    try {
      const result = await geminiService.processVoiceCommand(voiceTranscript);

      if (result.success) {
        setProcessedFoods(result.foodItems || []);
        setConfidence(result.confidence || 0);
        
        if (result.foodItems.length === 0) {
          setProcessingError('No food items identified in your voice command. Please try again with more specific details.');
        }

        // Play confirmation sound if enabled
        if (audioEnabled && result.foodItems.length > 0) {
          playConfirmationSound();
        }
      } else {
        setProcessingError(result.error || 'Failed to process voice command');
      }
    } catch (error) {
      console.error('Voice command processing error:', error);
      setProcessingError('An error occurred while processing your voice command');
    } finally {
      setIsProcessing(false);
    }
  };

  const playConfirmationSound = () => {
    // Create a simple confirmation beep
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = 800;
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.3);
  };

  const handleFoodSelect = (food) => {
    if (onFoodLogged) {
      onFoodLogged({
        name: food.name,
        brand: food.brand || '',
        nutrition: {
          calories: food.calories || 0,
          protein: food.protein || 0,
          carbs: food.carbs || 0,
          fat: food.fat || 0,
          fiber: food.fiber || 0,
          sodium: food.sodium || 0,
          servingSize: food.quantity || food.serving_size || '1 serving'
        },
        source: 'voice_recognition',
        confidence: confidence
      });
    }
  };

  const clearResults = () => {
    setProcessedFoods([]);
    setProcessingError(null);
    setConfidence(0);
  };

  if (!isSupported) {
    return (
      <Card>
        <CardContent className="p-6 text-center">
          <MicOff className="h-12 w-12 mx-auto mb-4 text-gray-400" />
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Voice Recognition Not Supported
          </h3>
          <p className="text-gray-600">
            Your browser doesn't support voice recognition. Please try using Chrome, Edge, or Safari.
          </p>
        </CardContent>
      </Card>
    );
  }

  const getConfidenceColor = (conf) => {
    if (conf >= 0.8) return 'bg-green-100 text-green-800';
    if (conf >= 0.6) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  const getConfidenceText = (conf) => {
    if (conf >= 0.8) return 'High';
    if (conf >= 0.6) return 'Medium';
    return 'Low';
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MessageSquare className="h-5 w-5" />
            Voice Food Logging
          </CardTitle>
          <p className="text-sm text-gray-600">
            Speak naturally to log your food. Say things like "I had a grilled chicken salad with olive oil dressing"
          </p>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Voice Control Panel */}
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center gap-3">
              <Button
                onClick={isListening ? stopListening : startListening}
                disabled={isProcessing}
                className={`${isListening ? 'bg-red-500 hover:bg-red-600' : 'bg-blue-500 hover:bg-blue-600'}`}
              >
                {isListening ? (
                  <>
                    <MicOff className="h-4 w-4 mr-2" />
                    Stop Listening
                  </>
                ) : (
                  <>
                    <Mic className="h-4 w-4 mr-2" />
                    Start Speaking
                  </>
                )}
              </Button>
              
              <Button
                variant="outline"
                size="sm"
                onClick={() => setAudioEnabled(!audioEnabled)}
              >
                {audioEnabled ? (
                  <Volume2 className="h-4 w-4" />
                ) : (
                  <VolumeX className="h-4 w-4" />
                )}
              </Button>
            </div>

            {/* Status Indicator */}
            <div className="flex items-center gap-2">
              {isListening && (
                <Badge className="bg-red-100 text-red-800 animate-pulse">
                  🎤 Listening...
                </Badge>
              )}
              {isProcessing && (
                <Badge className="bg-blue-100 text-blue-800">
                  <Loader2 className="h-3 w-3 mr-1 animate-spin" />
                  Processing...
                </Badge>
              )}
              {confidence > 0 && !isProcessing && (
                <Badge className={getConfidenceColor(confidence)}>
                  {getConfidenceText(confidence)} Confidence
                </Badge>
              )}
            </div>
          </div>

          {/* Transcript Display */}
          {transcript && (
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="font-medium text-blue-900 mb-2">What you said:</h4>
              <p className="text-blue-800 italic">"{transcript}"</p>
            </div>
          )}

          {/* Errors */}
          {(voiceError || processingError) && (
            <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-800">
              <AlertCircle className="h-5 w-5" />
              <span className="text-sm">{voiceError || processingError}</span>
            </div>
          )}

          {/* Processing Results */}
          {processedFoods.length > 0 && (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-green-600" />
                  <h4 className="font-medium">Identified Food Items</h4>
                </div>
                <Button variant="outline" size="sm" onClick={clearResults}>
                  Clear Results
                </Button>
              </div>

              {processedFoods.map((food, index) => (
                <Card key={index} className="border-green-200 bg-green-50">
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h5 className="font-medium text-green-900">{food.name}</h5>
                        {food.brand && (
                          <p className="text-sm text-green-700">{food.brand}</p>
                        )}
                        <div className="grid grid-cols-2 gap-2 mt-2 text-sm text-green-800">
                          <span>Calories: {food.calories || 0}</span>
                          <span>Protein: {food.protein || 0}g</span>
                          <span>Carbs: {food.carbs || 0}g</span>
                          <span>Fat: {food.fat || 0}g</span>
                        </div>
                        {food.quantity && (
                          <p className="text-xs text-green-600 mt-1">
                            Estimated quantity: {food.quantity}
                          </p>
                        )}
                        {food.notes && (
                          <p className="text-xs text-green-600 mt-1">
                            Notes: {food.notes}
                          </p>
                        )}
                      </div>
                      <div className="flex flex-col gap-2 items-end">
                        {food.confidence && (
                          <Badge className={getConfidenceColor(food.confidence)}>
                            {Math.round(food.confidence * 100)}%
                          </Badge>
                        )}
                        <Button
                          size="sm"
                          onClick={() => handleFoodSelect(food)}
                        >
                          Add to Log
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}

          {/* Voice Command Examples */}
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <h4 className="font-medium text-yellow-900 mb-2">Example Voice Commands:</h4>
            <ul className="text-sm text-yellow-800 space-y-1">
              <li>• "I ate a grilled chicken breast with steamed broccoli"</li>
              <li>• "Log two slices of whole wheat toast with peanut butter"</li>
              <li>• "I had a large Caesar salad for lunch"</li>
              <li>• "Add one medium apple and a handful of almonds"</li>
              <li>• "I drank a protein shake after my workout"</li>
            </ul>
          </div>

          {/* Voice Recognition Tips */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-medium text-blue-900 mb-2">Tips for best results:</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Speak clearly and at a normal pace</li>
              <li>• Include quantities when possible (e.g., "one cup", "medium size")</li>
              <li>• Mention cooking methods (e.g., "grilled", "baked", "fried")</li>
              <li>• Be specific about brands if important for nutrition accuracy</li>
              <li>• Use a quiet environment for better recognition</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default VoiceLogging;