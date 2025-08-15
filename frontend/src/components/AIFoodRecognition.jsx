import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Camera, Upload, Scan, Sparkles, Zap, Target, 
  Award, TrendingUp, ChefHat, Clock, Info,
  AlertCircle, CheckCircle2, Star, Brain,
  Lightbulb, BarChart3, Heart, Apple,
  ShoppingCart, BookOpen, Users, Flame
} from 'lucide-react';

const AIFoodRecognition = () => {
  const { switchRole } = useRole();
  
  // Camera and image states
  const [cameraActive, setCameraActive] = useState(false);
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [captureMethod, setCaptureMethod] = useState('camera'); // camera, upload, drag
  
  // Analysis states
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [analysisStage, setAnalysisStage] = useState('');
  const [analysisResults, setAnalysisResults] = useState(null);
  
  // User preferences
  const [userPreferences, setUserPreferences] = useState({
    dietary_restrictions: [],
    health_goals: [],
    cuisine_preferences: []
  });
  
  // UI states
  const [activeTab, setActiveTab] = useState('scan');
  const [showProcessingAnimation, setShowProcessingAnimation] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Refs
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    switchRole('guest');
    return () => {
      stopCamera();
    };
  }, [switchRole]);

  // Camera functionality
  const startCamera = async () => {
    try {
      setErrorMessage('');
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { 
          width: { ideal: 1920 },
          height: { ideal: 1080 },
          facingMode: 'environment' // Use back camera on mobile
        }
      });
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
        setCameraActive(true);
      }
    } catch (error) {
      console.error('Camera access error:', error);
      setErrorMessage('Camera access denied. Please enable camera permissions or try uploading an image.');
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    setCameraActive(false);
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
        setActiveTab('analyze');
      }, 'image/jpeg', 0.8);
    }
  };

  // File upload functionality
  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setImageFile(file);
      
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target.result);
        setActiveTab('analyze');
      };
      reader.readAsDataURL(file);
    } else {
      setErrorMessage('Please select a valid image file (JPG, PNG, etc.)');
    }
  };

  // Drag and drop functionality
  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setImageFile(file);
      
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target.result);
        setActiveTab('analyze');
      };
      reader.readAsDataURL(file);
    }
  };

  // AI Analysis functionality
  const analyzeFood = async () => {
    if (!imageFile) {
      setErrorMessage('Please capture or upload an image first');
      return;
    }

    setIsAnalyzing(true);
    setShowProcessingAnimation(true);
    setAnalysisProgress(0);
    setErrorMessage('');

    try {
      // Convert image to base64
      const base64Image = await convertImageToBase64(imageFile);

      // Stage 1: Gemini Vision Analysis
      setAnalysisStage('Analyzing food with AI vision...');
      setAnalysisProgress(25);
      await sleep(800);

      // Stage 2: Nutrition Analysis
      setAnalysisStage('Calculating nutrition and scoring...');
      setAnalysisProgress(50);
      await sleep(800);

      // Stage 3: Database Validation
      setAnalysisStage('Validating with nutrition databases...');
      setAnalysisProgress(75);
      await sleep(600);

      // Stage 4: Generating Alternatives
      setAnalysisStage('Finding healthier alternatives...');
      setAnalysisProgress(90);
      await sleep(400);

      // Call comprehensive food recognition API
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/ai/food-recognition-advanced`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image_base64: base64Image,
          user_preferences: userPreferences,
          dietary_restrictions: userPreferences.dietary_restrictions,
          health_goals: userPreferences.health_goals
        }),
      });

      if (response.ok) {
        const results = await response.json();
        setAnalysisProgress(100);
        setAnalysisStage('Analysis complete!');
        
        setTimeout(() => {
          setAnalysisResults(results);
          setActiveTab('results');
          setShowProcessingAnimation(false);
        }, 500);
      } else {
        throw new Error('Analysis failed');
      }

    } catch (error) {
      console.error('Food analysis error:', error);
      setErrorMessage('Analysis failed. Please try again or check your connection.');
      setShowProcessingAnimation(false);
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Helper functions
  const convertImageToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const base64 = reader.result.split(',')[1]; // Remove data:image/jpeg;base64, prefix
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

  const getGradeEmoji = (grade) => {
    const gradeEmojis = { 'A': '🌟', 'B': '👍', 'C': '👌', 'D': '⚠️', 'F': '❌' };
    return gradeEmojis[grade] || '📊';
  };

  // Add user preferences functionality
  const updatePreferences = (category, value) => {
    setUserPreferences(prev => ({
      ...prev,
      [category]: prev[category].includes(value) 
        ? prev[category].filter(item => item !== value)
        : [...prev[category], value]
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-violet-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            <Brain className="w-10 h-10 inline mr-3 text-purple-600" />
            AI Food Recognition
          </h1>
          <p className="text-xl text-gray-600 mb-2">
            Snap, Analyze & Transform Your Nutrition with AI
          </p>
          <div className="flex justify-center space-x-4 text-sm text-purple-600">
            <span className="flex items-center">
              <Zap className="w-4 h-4 mr-1" />
              Instant Recognition
            </span>
            <span className="flex items-center">
              <Target className="w-4 h-4 mr-1" />
              Smart Scoring
            </span>
            <span className="flex items-center">
              <Sparkles className="w-4 h-4 mr-1" />
              Healthier Alternatives
            </span>
          </div>
        </div>

        {/* Main Interface */}
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-4 mb-8">
            <TabsTrigger value="scan" className="flex items-center">
              <Camera className="w-4 h-4 mr-2" />
              Scan Food
            </TabsTrigger>
            <TabsTrigger value="analyze" className="flex items-center">
              <Brain className="w-4 h-4 mr-2" />
              Analyze
            </TabsTrigger>
            <TabsTrigger value="results" className="flex items-center">
              <BarChart3 className="w-4 h-4 mr-2" />
              Results
            </TabsTrigger>
            <TabsTrigger value="settings" className="flex items-center">
              <Target className="w-4 h-4 mr-2" />
              Preferences
            </TabsTrigger>
          </TabsList>

          {/* Scan Tab */}
          <TabsContent value="scan">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Camera Interface */}
              <Card className="border-2 border-purple-200">
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Camera className="w-6 h-6 mr-2 text-purple-600" />
                    Live Camera Feed
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
                        {/* Food Detection Overlay */}
                        <div className="absolute top-4 left-4 right-4">
                          <div className="bg-black bg-opacity-50 rounded-lg p-2 text-white text-sm">
                            <div className="flex items-center justify-between">
                              <span>🎯 Position food in center</span>
                              <span className="animate-pulse">● REC</span>
                            </div>
                          </div>
                        </div>
                        {/* Capture Button */}
                        <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2">
                          <Button 
                            onClick={captureImage}
                            size="lg"
                            className="bg-purple-600 hover:bg-purple-700 rounded-full w-16 h-16"
                          >
                            <Camera className="w-6 h-6" />
                          </Button>
                        </div>
                      </>
                    ) : (
                      <div className="flex flex-col items-center justify-center h-full text-gray-500">
                        <Camera className="w-16 h-16 mb-4" />
                        <p className="text-lg font-medium mb-2">Camera Not Active</p>
                        <p className="text-sm mb-4">Enable camera to capture food images</p>
                        <Button onClick={startCamera} className="bg-purple-600 hover:bg-purple-700">
                          <Camera className="w-4 h-4 mr-2" />
                          Start Camera
                        </Button>
                      </div>
                    )}
                  </div>
                  
                  {cameraActive && (
                    <div className="mt-4 flex justify-between">
                      <Button variant="outline" onClick={stopCamera}>
                        Stop Camera
                      </Button>
                      <div className="text-sm text-gray-500 flex items-center">
                        <Info className="w-4 h-4 mr-1" />
                        Position food clearly in frame
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Upload Options */}
              <Card className="border-2 border-blue-200">
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Upload className="w-6 h-6 mr-2 text-blue-600" />
                    Upload Options
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-6">
                  {/* File Upload */}
                  <div>
                    <Button 
                      onClick={() => fileInputRef.current?.click()}
                      className="w-full bg-blue-600 hover:bg-blue-700"
                      size="lg"
                    >
                      <Upload className="w-5 h-5 mr-2" />
                      Choose Image from Gallery
                    </Button>
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="image/*"
                      onChange={handleFileUpload}
                      className="hidden"
                    />
                  </div>

                  {/* Drag and Drop */}
                  <div
                    onDragOver={handleDragOver}
                    onDrop={handleDrop}
                    className="border-2 border-dashed border-blue-300 rounded-lg p-8 text-center hover:border-blue-500 transition-colors cursor-pointer"
                  >
                    <Upload className="w-12 h-12 mx-auto text-blue-400 mb-4" />
                    <p className="text-lg font-medium text-gray-700 mb-2">
                      Drag & Drop Image Here
                    </p>
                    <p className="text-sm text-gray-500">
                      Supports JPG, PNG, WebP formats
                    </p>
                  </div>

                  {/* Tips */}
                  <Card className="bg-gradient-to-r from-green-50 to-blue-50 border-green-200">
                    <CardContent className="pt-4">
                      <div className="flex items-start space-x-2">
                        <Lightbulb className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                        <div>
                          <h4 className="font-medium text-green-900 mb-2">Photo Tips for Best Results</h4>
                          <ul className="text-sm text-green-800 space-y-1">
                            <li>• Ensure good lighting</li>
                            <li>• Show the full meal/food item</li>
                            <li>• Avoid shadows and reflections</li>
                            <li>• Include reference objects for portion size</li>
                          </ul>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Analyze Tab */}
          <TabsContent value="analyze">
            <div className="max-w-4xl mx-auto">
              <Card className="border-2 border-yellow-200">
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Brain className="w-6 h-6 mr-2 text-yellow-600" />
                    AI Analysis Center
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {imagePreview ? (
                    <div className="space-y-6">
                      {/* Image Preview */}
                      <div className="flex justify-center">
                        <div className="relative">
                          <img 
                            src={imagePreview} 
                            alt="Food to analyze" 
                            className="max-w-md max-h-80 rounded-lg shadow-lg object-cover"
                          />
                          <Badge className="absolute top-2 right-2 bg-green-100 text-green-800">
                            <CheckCircle2 className="w-3 h-3 mr-1" />
                            Ready to Analyze
                          </Badge>
                        </div>
                      </div>

                      {/* Analysis Button or Progress */}
                      {showProcessingAnimation ? (
                        <Card className="bg-gradient-to-r from-purple-100 to-blue-100 border-purple-200">
                          <CardContent className="pt-6">
                            <div className="text-center space-y-4">
                              <div className="flex items-center justify-center space-x-2">
                                <div className="animate-spin rounded-full h-8 w-8 border-4 border-purple-600 border-t-transparent"></div>
                                <span className="text-lg font-medium text-purple-900">
                                  {analysisStage}
                                </span>
                              </div>
                              
                              <Progress value={analysisProgress} className="w-full" />
                              
                              <div className="text-sm text-purple-700">
                                Processing with multiple AI models for comprehensive analysis...
                              </div>
                              
                              {/* Processing Steps Indicator */}
                              <div className="grid grid-cols-4 gap-4 mt-6">
                                <div className={`text-center p-2 rounded-lg ${analysisProgress >= 25 ? 'bg-purple-200' : 'bg-gray-100'}`}>
                                  <Scan className="w-6 h-6 mx-auto mb-1" />
                                  <div className="text-xs">Vision AI</div>
                                </div>
                                <div className={`text-center p-2 rounded-lg ${analysisProgress >= 50 ? 'bg-purple-200' : 'bg-gray-100'}`}>
                                  <BarChart3 className="w-6 h-6 mx-auto mb-1" />
                                  <div className="text-xs">Nutrition</div>
                                </div>
                                <div className={`text-center p-2 rounded-lg ${analysisProgress >= 75 ? 'bg-purple-200' : 'bg-gray-100'}`}>
                                  <BookOpen className="w-6 h-6 mx-auto mb-1" />
                                  <div className="text-xs">Database</div>
                                </div>
                                <div className={`text-center p-2 rounded-lg ${analysisProgress >= 90 ? 'bg-purple-200' : 'bg-gray-100'}`}>
                                  <Sparkles className="w-6 h-6 mx-auto mb-1" />
                                  <div className="text-xs">Alternatives</div>
                                </div>
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      ) : (
                        <div className="text-center space-y-4">
                          <Button 
                            onClick={analyzeFood}
                            disabled={isAnalyzing}
                            size="lg"
                            className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                          >
                            <Brain className="w-5 h-5 mr-2" />
                            Analyze with AI
                          </Button>
                          
                          <div className="text-sm text-gray-500">
                            Analysis uses Gemini Vision + Groq + USDA database for comprehensive results
                          </div>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="text-center py-12">
                      <Brain className="w-16 h-16 mx-auto text-gray-300 mb-4" />
                      <h3 className="text-lg font-medium text-gray-500 mb-2">No Image Selected</h3>
                      <p className="text-gray-400 mb-4">Please capture or upload a food image first</p>
                      <Button onClick={() => setActiveTab('scan')} variant="outline">
                        <Camera className="w-4 h-4 mr-2" />
                        Go Back to Camera
                      </Button>
                    </div>
                  )}

                  {errorMessage && (
                    <Card className="bg-red-50 border-red-200">
                      <CardContent className="pt-4">
                        <div className="flex items-center space-x-2 text-red-800">
                          <AlertCircle className="w-5 h-5" />
                          <span>{errorMessage}</span>
                        </div>
                      </CardContent>
                    </Card>
                  )}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Results Tab */}
          <TabsContent value="results">
            {analysisResults ? (
              <div className="space-y-6">
                {/* Analysis Summary */}
                <Card className="border-2 border-green-200 bg-gradient-to-r from-green-50 to-blue-50">
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span className="flex items-center">
                        <Sparkles className="w-6 h-6 mr-2 text-green-600" />
                        Analysis Complete
                      </span>
                      <Badge className="bg-green-100 text-green-800">
                        {analysisResults.processing_time} • {analysisResults.api_sources?.length} AI Models
                      </Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">{analysisResults.foods_detected?.length || 0}</div>
                        <div className="text-sm text-gray-600">Foods Detected</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-blue-600">{Math.round(analysisResults.confidence * 100)}%</div>
                        <div className="text-sm text-gray-600">Confidence</div>
                      </div>
                      <div className="text-center">
                        <div className="text-2xl font-bold text-purple-600">{analysisResults.alternatives?.length || 0}</div>
                        <div className="text-sm text-gray-600">Alternatives Found</div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Foods Detected */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center">
                        <Apple className="w-5 h-5 mr-2 text-orange-500" />
                        Detected Foods & Scores
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      {analysisResults.foods_detected?.map((food, index) => (
                        <div key={index} className="border rounded-lg p-4">
                          <div className="flex items-start justify-between mb-3">
                            <div>
                              <h3 className="font-semibold text-lg">{food.name}</h3>
                              <p className="text-sm text-gray-600">
                                {food.portion_size} • {food.cooking_method}
                              </p>
                            </div>
                            <div className="text-right">
                              <Badge className={`${getFoodScoreColor(food.food_score?.score)} text-lg px-3 py-1`}>
                                {getGradeEmoji(food.food_score?.grade)} {food.food_score?.grade}
                              </Badge>
                              <div className="text-sm text-gray-500 mt-1">
                                {food.food_score?.score}/100
                              </div>
                            </div>
                          </div>

                          {/* Nutrition Info */}
                          <div className="grid grid-cols-2 gap-2 text-sm bg-gray-50 rounded p-3 mb-3">
                            <div>Calories: <span className="font-medium">{food.nutrition?.calories}</span></div>
                            <div>Protein: <span className="font-medium">{food.nutrition?.protein}</span></div>
                            <div>Carbs: <span className="font-medium">{food.nutrition?.carbs}</span></div>
                            <div>Fat: <span className="font-medium">{food.nutrition?.fat}</span></div>
                          </div>

                          {/* Health Insights */}
                          <div className="space-y-1">
                            {food.health_insights?.slice(0, 2).map((insight, i) => (
                              <div key={i} className="flex items-start text-sm">
                                <Heart className="w-3 h-3 text-red-500 mr-2 mt-0.5 flex-shrink-0" />
                                <span className="text-gray-700">{insight}</span>
                              </div>
                            ))}
                          </div>

                          {/* Dietary Tags */}
                          {food.dietary_tags && food.dietary_tags.length > 0 && (
                            <div className="flex flex-wrap gap-1 mt-3">
                              {food.dietary_tags.map((tag, i) => (
                                <Badge key={i} variant="secondary" className="text-xs">
                                  {tag.replace('_', ' ')}
                                </Badge>
                              ))}
                            </div>
                          )}
                        </div>
                      ))}
                    </CardContent>
                  </Card>

                  {/* Healthier Alternatives */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center">
                        <TrendingUp className="w-5 h-5 mr-2 text-green-500" />
                        Healthier Alternatives
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      {analysisResults.alternatives?.map((altGroup, index) => (
                        <div key={index} className="border rounded-lg p-4">
                          <div className="mb-3">
                            <h4 className="font-medium text-gray-900">Instead of: {altGroup.original_food}</h4>
                            <p className="text-sm text-gray-500">Current score: {altGroup.original_score}</p>
                          </div>

                          <div className="space-y-3">
                            {altGroup.alternatives?.map((alt, altIndex) => (
                              <div key={altIndex} className="bg-green-50 rounded-lg p-3 border border-green-200">
                                <div className="flex items-start justify-between mb-2">
                                  <h5 className="font-medium text-green-900">{alt.food}</h5>
                                  <Badge className="bg-green-600 text-white">
                                    {alt.score}
                                  </Badge>
                                </div>
                                
                                <p className="text-sm text-green-800 mb-2">
                                  <strong>Improvement:</strong> {alt.improvement}
                                </p>
                                
                                <p className="text-sm text-green-700 mb-2">
                                  {alt.why_better}
                                </p>

                                {alt.prep_time && (
                                  <div className="flex items-center text-xs text-green-600">
                                    <Clock className="w-3 h-3 mr-1" />
                                    Prep time: {alt.prep_time}
                                  </div>
                                )}

                                {alt.swapping_tips && (
                                  <div className="mt-2 p-2 bg-yellow-50 rounded border border-yellow-200">
                                    <div className="flex items-start text-xs text-yellow-800">
                                      <Lightbulb className="w-3 h-3 mr-1 mt-0.5 flex-shrink-0" />
                                      <span>{alt.swapping_tips}</span>
                                    </div>
                                  </div>
                                )}
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}

                      {(!analysisResults.alternatives || analysisResults.alternatives.length === 0) && (
                        <div className="text-center py-8 text-gray-500">
                          <ChefHat className="w-12 h-12 mx-auto mb-3 opacity-50" />
                          <p>No alternatives needed - your food choices look great!</p>
                        </div>
                      )}
                    </CardContent>
                  </Card>
                </div>

                {/* Session Insights */}
                {analysisResults.session_insights && (
                  <Card className="border-2 border-blue-200 bg-blue-50">
                    <CardHeader>
                      <CardTitle className="flex items-center">
                        <Info className="w-5 h-5 mr-2 text-blue-600" />
                        Personalized Insights
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-2">
                        {analysisResults.session_insights.map((insight, index) => (
                          <div key={index} className="flex items-start">
                            <Sparkles className="w-4 h-4 text-blue-600 mr-2 mt-0.5 flex-shrink-0" />
                            <span className="text-blue-900">{insight}</span>
                          </div>
                        ))}
                      </div>
                    </CardContent>
                  </Card>
                )}

                {/* Action Buttons */}
                <div className="flex flex-wrap gap-4 justify-center">
                  <Button 
                    onClick={() => {
                      setImageFile(null);
                      setImagePreview(null);
                      setAnalysisResults(null);
                      setActiveTab('scan');
                    }}
                    className="bg-purple-600 hover:bg-purple-700"
                  >
                    <Camera className="w-4 h-4 mr-2" />
                    Scan Another Food
                  </Button>
                  
                  <Button variant="outline">
                    <Heart className="w-4 h-4 mr-2" />
                    Save to Food Log
                  </Button>
                  
                  <Button variant="outline">
                    <Users className="w-4 h-4 mr-2" />
                    Share Results
                  </Button>
                  
                  <Button variant="outline">
                    <ShoppingCart className="w-4 h-4 mr-2" />
                    Shopping List
                  </Button>
                </div>
              </div>
            ) : (
              <div className="text-center py-16">
                <BarChart3 className="w-20 h-20 mx-auto text-gray-300 mb-6" />
                <h3 className="text-xl font-medium text-gray-500 mb-2">No Analysis Results</h3>
                <p className="text-gray-400 mb-6">Capture and analyze a food image to see detailed results</p>
                <Button onClick={() => setActiveTab('scan')}>
                  <Camera className="w-4 h-4 mr-2" />
                  Start Food Recognition
                </Button>
              </div>
            )}
          </TabsContent>

          {/* Settings/Preferences Tab */}
          <TabsContent value="settings">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Target className="w-5 h-5 mr-2 text-purple-600" />
                  Personal Preferences
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Dietary Restrictions */}
                <div>
                  <h3 className="font-medium text-gray-900 mb-3">Dietary Restrictions</h3>
                  <div className="flex flex-wrap gap-2">
                    {[
                      'Vegetarian', 'Vegan', 'Gluten-Free', 'Dairy-Free', 
                      'Nut-Free', 'Keto', 'Paleo', 'Low-Sodium'
                    ].map(restriction => (
                      <Button
                        key={restriction}
                        variant={userPreferences.dietary_restrictions.includes(restriction.toLowerCase().replace('-', '_')) ? "default" : "outline"}
                        size="sm"
                        onClick={() => updatePreferences('dietary_restrictions', restriction.toLowerCase().replace('-', '_'))}
                      >
                        {restriction}
                      </Button>
                    ))}
                  </div>
                </div>

                {/* Health Goals */}
                <div>
                  <h3 className="font-medium text-gray-900 mb-3">Health Goals</h3>
                  <div className="flex flex-wrap gap-2">
                    {[
                      'Weight Loss', 'Muscle Gain', 'Maintain Weight', 
                      'Better Energy', 'Heart Health', 'Diabetes Management'
                    ].map(goal => (
                      <Button
                        key={goal}
                        variant={userPreferences.health_goals.includes(goal.toLowerCase().replace(' ', '_')) ? "default" : "outline"}
                        size="sm"
                        onClick={() => updatePreferences('health_goals', goal.toLowerCase().replace(' ', '_'))}
                      >
                        {goal}
                      </Button>
                    ))}
                  </div>
                </div>

                {/* Cuisine Preferences */}
                <div>
                  <h3 className="font-medium text-gray-900 mb-3">Favorite Cuisines</h3>
                  <div className="flex flex-wrap gap-2">
                    {[
                      'Mediterranean', 'Asian', 'Mexican', 'Italian', 
                      'Indian', 'American', 'Middle Eastern', 'Thai'
                    ].map(cuisine => (
                      <Button
                        key={cuisine}
                        variant={userPreferences.cuisine_preferences.includes(cuisine.toLowerCase()) ? "default" : "outline"}
                        size="sm"
                        onClick={() => updatePreferences('cuisine_preferences', cuisine.toLowerCase())}
                      >
                        {cuisine}
                      </Button>
                    ))}
                  </div>
                </div>

                <Card className="bg-gradient-to-r from-purple-50 to-blue-50 border-purple-200">
                  <CardContent className="pt-4">
                    <div className="flex items-start space-x-2">
                      <Info className="w-5 h-5 text-purple-600 mt-0.5 flex-shrink-0" />
                      <div>
                        <h4 className="font-medium text-purple-900 mb-1">How Preferences Work</h4>
                        <p className="text-sm text-purple-700">
                          Your preferences help our AI provide more personalized food recommendations 
                          and alternative suggestions that fit your lifestyle and goals.
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Hidden Canvas for Image Processing */}
        <canvas ref={canvasRef} style={{ display: 'none' }} />
      </div>
    </div>
  );
};

export default AIFoodRecognition;