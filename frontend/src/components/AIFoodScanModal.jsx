import React, { useState, useRef, useCallback } from 'react';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { 
  Camera, Upload, X, Brain, Sparkles, Target,
  CheckCircle2, AlertCircle, Zap, TrendingUp,
  Clock, Heart, Apple, Info
} from 'lucide-react';

const AIFoodScanModal = ({ isOpen, onClose, onFoodAnalyzed }) => {
  // Modal states
  const [step, setStep] = useState('capture'); // capture, analyze, results
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [analysisStage, setAnalysisStage] = useState('');
  const [analysisResults, setAnalysisResults] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

  // Camera states
  const [cameraActive, setCameraActive] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);

  // Reset modal state when opening/closing
  React.useEffect(() => {
    if (isOpen) {
      resetModal();
    } else {
      stopCamera();
    }
  }, [isOpen]);

  const resetModal = () => {
    setStep('capture');
    setImageFile(null);
    setImagePreview(null);
    setIsAnalyzing(false);
    setAnalysisProgress(0);
    setAnalysisResults(null);
    setErrorMessage('');
    setCameraActive(false);
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    setCameraActive(false);
  };

  // Camera functionality
  const startCamera = async () => {
    try {
      setErrorMessage('');
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { 
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'environment'
        }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
        setCameraActive(true);
      }
    } catch (error) {
      setErrorMessage('Camera access denied. Please try uploading an image instead.');
    }
  };

  const captureImage = () => {
    if (videoRef.current && canvasRef.current) {
      const canvas = canvasRef.current;
      const video = videoRef.current;
      
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      const ctx = canvas.getContext('2d');
      ctx.drawImage(video, 0, 0);
      
      canvas.toBlob((blob) => {
        const file = new File([blob], 'captured_food.jpg', { type: 'image/jpeg' });
        setImageFile(file);
        setImagePreview(canvas.toDataURL('image/jpeg', 0.8));
        stopCamera();
        setStep('analyze');
      }, 'image/jpeg', 0.8);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setImageFile(file);
      
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target.result);
        setStep('analyze');
      };
      reader.readAsDataURL(file);
    } else {
      setErrorMessage('Please select a valid image file');
    }
  };

  const analyzeFood = async () => {
    if (!imageFile) return;

    setIsAnalyzing(true);
    setAnalysisProgress(0);
    setErrorMessage('');

    try {
      // Convert to base64
      const base64Image = await convertImageToBase64(imageFile);

      // Simulate multi-stage processing
      setAnalysisStage('AI Vision Analysis...');
      setAnalysisProgress(25);
      await sleep(600);

      setAnalysisStage('Nutrition Calculation...');
      setAnalysisProgress(50);
      await sleep(600);

      setAnalysisStage('Database Validation...');
      setAnalysisProgress(75);
      await sleep(400);

      setAnalysisStage('Finding Alternatives...');
      setAnalysisProgress(90);
      await sleep(400);

      // Call API
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/ai/food-recognition-advanced`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image_base64: base64Image,
          user_preferences: {},
          dietary_restrictions: [],
          health_goals: []
        }),
      });

      if (response.ok) {
        const results = await response.json();
        setAnalysisProgress(100);
        setAnalysisStage('Complete!');
        
        setTimeout(() => {
          setAnalysisResults(results);
          setStep('results');
        }, 500);
      } else {
        throw new Error('Analysis failed');
      }

    } catch (error) {
      console.error('Analysis error:', error);
      setErrorMessage('Analysis failed. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const convertImageToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const base64 = reader.result.split(',')[1];
        resolve(base64);
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  };

  const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

  const getFoodScoreColor = (score) => {
    if (score >= 90) return 'text-green-600 bg-green-100';
    if (score >= 80) return 'text-blue-600 bg-blue-100';
    if (score >= 70) return 'text-yellow-600 bg-yellow-100';
    if (score >= 60) return 'text-orange-600 bg-orange-100';
    return 'text-red-600 bg-red-100';
  };

  const handleSaveToLog = () => {
    if (analysisResults && onFoodAnalyzed) {
      onFoodAnalyzed(analysisResults);
    }
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        
        {/* Modal Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center">
            <Brain className="w-6 h-6 mr-2 text-purple-600" />
            <h2 className="text-xl font-semibold">Quick AI Food Scan</h2>
          </div>
          <Button variant="ghost" size="sm" onClick={onClose}>
            <X className="w-5 h-5" />
          </Button>
        </div>

        {/* Modal Content */}
        <div className="p-6">
          
          {/* Step 1: Capture */}
          {step === 'capture' && (
            <div className="space-y-6">
              <div className="text-center">
                <h3 className="text-lg font-medium mb-2">Capture or Upload Food Image</h3>
                <p className="text-gray-600">Get instant AI-powered nutrition analysis and suggestions</p>
              </div>

              {/* Camera or Upload Options */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                {/* Camera */}
                <Card className="border-2 border-purple-200">
                  <CardHeader>
                    <CardTitle className="flex items-center text-base">
                      <Camera className="w-5 h-5 mr-2" />
                      Use Camera
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="relative bg-gray-100 rounded-lg overflow-hidden" style={{ aspectRatio: '4/3' }}>
                      {cameraActive ? (
                        <>
                          <video 
                            ref={videoRef} 
                            className="w-full h-full object-cover"
                            autoPlay 
                            playsInline 
                            muted
                          />
                          <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2">
                            <Button 
                              onClick={captureImage}
                              className="bg-purple-600 hover:bg-purple-700 rounded-full w-12 h-12"
                            >
                              <Camera className="w-5 h-5" />
                            </Button>
                          </div>
                        </>
                      ) : (
                        <div className="flex flex-col items-center justify-center h-full text-gray-500">
                          <Camera className="w-12 h-12 mb-3" />
                          <Button onClick={startCamera} size="sm">
                            Start Camera
                          </Button>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>

                {/* Upload */}
                <Card className="border-2 border-blue-200">
                  <CardHeader>
                    <CardTitle className="flex items-center text-base">
                      <Upload className="w-5 h-5 mr-2" />
                      Upload Image
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <Button 
                      onClick={() => fileInputRef.current?.click()}
                      className="w-full"
                      size="sm"
                    >
                      Choose from Gallery
                    </Button>
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="image/*"
                      onChange={handleFileUpload}
                      className="hidden"
                    />
                    
                    <div className="text-xs text-gray-500 space-y-1">
                      <p>• Good lighting helps accuracy</p>
                      <p>• Show the complete meal/food</p>
                      <p>• Avoid shadows and reflections</p>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {errorMessage && (
                <div className="flex items-center space-x-2 text-red-600 text-sm">
                  <AlertCircle className="w-4 h-4" />
                  <span>{errorMessage}</span>
                </div>
              )}
            </div>
          )}

          {/* Step 2: Analyze */}
          {step === 'analyze' && (
            <div className="space-y-6">
              
              {/* Image Preview */}
              <div className="text-center">
                <img 
                  src={imagePreview} 
                  alt="Food to analyze" 
                  className="max-w-xs max-h-48 rounded-lg shadow-lg mx-auto object-cover"
                />
              </div>

              {/* Analysis Progress */}
              {isAnalyzing ? (
                <Card className="bg-gradient-to-r from-purple-50 to-blue-50 border-purple-200">
                  <CardContent className="pt-6">
                    <div className="text-center space-y-4">
                      <div className="flex items-center justify-center space-x-2">
                        <div className="animate-spin rounded-full h-6 w-6 border-3 border-purple-600 border-t-transparent"></div>
                        <span className="font-medium text-purple-900">{analysisStage}</span>
                      </div>
                      
                      <Progress value={analysisProgress} className="w-full" />
                      
                      <div className="text-sm text-purple-700">
                        Processing with Gemini Vision + Groq + USDA database...
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ) : (
                <div className="text-center space-y-4">
                  <Button 
                    onClick={analyzeFood}
                    size="lg"
                    className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                  >
                    <Brain className="w-5 h-5 mr-2" />
                    Analyze with AI
                  </Button>
                  
                  <div className="flex justify-center space-x-4 text-xs text-gray-500">
                    <span className="flex items-center">
                      <Zap className="w-3 h-3 mr-1" />
                      Instant Results
                    </span>
                    <span className="flex items-center">
                      <Target className="w-3 h-3 mr-1" />
                      Accurate Scoring
                    </span>
                    <span className="flex items-center">
                      <Sparkles className="w-3 h-3 mr-1" />
                      Smart Suggestions
                    </span>
                  </div>
                </div>
              )}

              <div className="flex justify-center">
                <Button variant="outline" onClick={() => setStep('capture')}>
                  ← Back to Capture
                </Button>
              </div>
            </div>
          )}

          {/* Step 3: Results */}
          {step === 'results' && analysisResults && (
            <div className="space-y-6">
              
              {/* Summary */}
              <Card className="border-2 border-green-200 bg-green-50">
                <CardContent className="pt-4">
                  <div className="text-center">
                    <CheckCircle2 className="w-8 h-8 text-green-600 mx-auto mb-2" />
                    <h3 className="font-medium text-green-900">Analysis Complete!</h3>
                    <div className="grid grid-cols-3 gap-4 mt-4 text-sm">
                      <div>
                        <div className="font-bold text-green-600">{analysisResults.foods_detected?.length || 0}</div>
                        <div className="text-green-700">Foods Found</div>
                      </div>
                      <div>
                        <div className="font-bold text-green-600">{Math.round(analysisResults.confidence * 100)}%</div>
                        <div className="text-green-700">Confidence</div>
                      </div>
                      <div>
                        <div className="font-bold text-green-600">{analysisResults.processing_time}</div>
                        <div className="text-green-700">Processing</div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Foods & Scores */}
              <div className="space-y-3">
                <h4 className="font-medium flex items-center">
                  <Apple className="w-4 h-4 mr-2 text-orange-500" />
                  Detected Foods
                </h4>
                
                {analysisResults.foods_detected?.map((food, index) => (
                  <div key={index} className="border rounded-lg p-3">
                    <div className="flex items-center justify-between mb-2">
                      <div>
                        <h5 className="font-medium">{food.name}</h5>
                        <p className="text-xs text-gray-600">{food.portion_size}</p>
                      </div>
                      <Badge className={getFoodScoreColor(food.food_score?.score)}>
                        {food.food_score?.grade} ({food.food_score?.score}/100)
                      </Badge>
                    </div>
                    
                    <div className="grid grid-cols-4 gap-2 text-xs text-gray-600 mb-2">
                      <span>Cal: {food.nutrition?.calories}</span>
                      <span>Protein: {food.nutrition?.protein}</span>
                      <span>Carbs: {food.nutrition?.carbs}</span>
                      <span>Fat: {food.nutrition?.fat}</span>
                    </div>

                    {food.health_insights && food.health_insights[0] && (
                      <div className="flex items-start text-xs">
                        <Heart className="w-3 h-3 text-red-500 mr-1 mt-0.5 flex-shrink-0" />
                        <span className="text-gray-700">{food.health_insights[0]}</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Quick Alternatives */}
              {analysisResults.alternatives && analysisResults.alternatives.length > 0 && (
                <div className="space-y-3">
                  <h4 className="font-medium flex items-center">
                    <TrendingUp className="w-4 h-4 mr-2 text-green-500" />
                    Quick Improvements
                  </h4>
                  
                  {analysisResults.alternatives.slice(0, 2).map((altGroup, index) => (
                    <div key={index} className="bg-green-50 rounded-lg p-3 border border-green-200">
                      <div className="text-sm">
                        <div className="font-medium text-green-900 mb-1">
                          Try: {altGroup.alternatives?.[0]?.food}
                        </div>
                        <div className="text-green-700 text-xs">
                          {altGroup.alternatives?.[0]?.improvement}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex flex-col space-y-3">
                <Button 
                  onClick={handleSaveToLog}
                  className="w-full bg-green-600 hover:bg-green-700"
                >
                  <Heart className="w-4 h-4 mr-2" />
                  Save to Food Log
                </Button>
                
                <div className="grid grid-cols-2 gap-3">
                  <Button 
                    onClick={resetModal}
                    variant="outline"
                  >
                    Scan Another
                  </Button>
                  
                  <Button 
                    onClick={onClose}
                    variant="outline"
                  >
                    Close
                  </Button>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Hidden Canvas */}
        <canvas ref={canvasRef} style={{ display: 'none' }} />
      </div>
    </div>
  );
};

export default AIFoodScanModal;