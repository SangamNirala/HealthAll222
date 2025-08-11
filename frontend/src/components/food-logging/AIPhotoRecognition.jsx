import React, { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  Camera, 
  Upload, 
  RotateCcw, 
  Sparkles, 
  CheckCircle, 
  AlertCircle,
  Loader2
} from 'lucide-react';
import geminiService from '../../services/geminiService';

const AIPhotoRecognition = ({ userId, onFoodRecognized }) => {
  const [isWebcamActive, setIsWebcamActive] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const [uploadedImage, setUploadedImage] = useState(null);
  const [recognitionResults, setRecognitionResults] = useState([]);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const [confidence, setConfidence] = useState(0);
  
  const webcamRef = useRef(null);
  const fileInputRef = useRef(null);

  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "user"
  };

  const capturePhoto = useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      setCapturedImage(imageSrc);
      setIsWebcamActive(false);
      analyzeImage(imageSrc);
    }
  }, [webcamRef]);

  const handleFileUpload = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file
    const validation = geminiService.validateImageFile(file);
    if (!validation.valid) {
      setError(validation.error);
      return;
    }

    // Read and display the file
    const reader = new FileReader();
    reader.onload = (e) => {
      const imageSrc = e.target?.result;
      setUploadedImage(imageSrc);
      setCapturedImage(null);
      analyzeImage(imageSrc);
    };
    reader.readAsDataURL(file);
  };

  const analyzeImage = async (imageSrc) => {
    setIsAnalyzing(true);
    setError(null);
    setRecognitionResults([]);

    try {
      // Convert image to blob if needed
      let imageFile;
      if (typeof imageSrc === 'string' && imageSrc.startsWith('data:')) {
        // Convert base64 to blob
        const response = await fetch(imageSrc);
        imageFile = await response.blob();
      } else {
        imageFile = imageSrc;
      }

      // Use Gemini service to analyze the image
      const result = await geminiService.analyzeFoodImage(imageFile);

      if (result.success) {
        setRecognitionResults(result.foods || []);
        setConfidence(result.confidence || 0);
        
        if (result.foods.length === 0) {
          setError('No food items detected in the image. Please try a clearer photo.');
        }
      } else {
        setError(result.error || 'Failed to analyze image');
      }
    } catch (error) {
      console.error('Image analysis error:', error);
      setError('An error occurred while analyzing the image');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleFoodSelect = (food) => {
    if (onFoodRecognized) {
      onFoodRecognized({
        name: food.name,
        brand: food.brand || '',
        nutrition: {
          calories: food.calories || 0,
          protein: food.protein || 0,
          carbs: food.carbs || 0,
          fat: food.fat || 0,
          fiber: food.fiber || 0,
          sodium: food.sodium || 0,
          servingSize: food.serving_size || food.portion || '1 serving'
        },
        source: 'ai_photo_recognition',
        confidence: confidence
      });
    }
  };

  const resetCapture = () => {
    setCapturedImage(null);
    setUploadedImage(null);
    setRecognitionResults([]);
    setError(null);
    setConfidence(0);
    setIsWebcamActive(false);
    // Clear file input
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

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
            <Sparkles className="h-5 w-5" />
            AI Food Recognition
          </CardTitle>
          <p className="text-sm text-gray-600">
            Take a photo or upload an image to automatically identify food items and their nutrition
          </p>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-3">
            <Button
              onClick={() => setIsWebcamActive(!isWebcamActive)}
              disabled={isAnalyzing}
              className="flex-1"
            >
              <Camera className="h-4 w-4 mr-2" />
              {isWebcamActive ? 'Hide Camera' : 'Open Camera'}
            </Button>
            
            <Button
              onClick={() => fileInputRef.current?.click()}
              disabled={isAnalyzing}
              variant="outline"
              className="flex-1"
            >
              <Upload className="h-4 w-4 mr-2" />
              Upload Photo
            </Button>

            <Button
              onClick={resetCapture}
              disabled={isAnalyzing}
              variant="outline"
              size="sm"
            >
              <RotateCcw className="h-4 w-4" />
            </Button>
          </div>

          {/* Hidden file input */}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileUpload}
            className="hidden"
          />

          {/* Error Display */}
          {error && (
            <div className="flex items-center gap-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-800">
              <AlertCircle className="h-5 w-5" />
              <span className="text-sm">{error}</span>
            </div>
          )}

          {/* Webcam */}
          {isWebcamActive && (
            <div className="relative">
              <Webcam
                ref={webcamRef}
                audio={false}
                height={360}
                screenshotFormat="image/jpeg"
                width="100%"
                videoConstraints={videoConstraints}
                className="rounded-lg"
              />
              <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2">
                <Button onClick={capturePhoto} disabled={isAnalyzing}>
                  <Camera className="h-4 w-4 mr-2" />
                  Capture
                </Button>
              </div>
            </div>
          )}

          {/* Captured/Uploaded Image */}
          {(capturedImage || uploadedImage) && (
            <div className="space-y-4">
              <div className="relative">
                <img
                  src={capturedImage || uploadedImage}
                  alt="Captured food"
                  className="w-full h-64 object-cover rounded-lg"
                />
                {isAnalyzing && (
                  <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center rounded-lg">
                    <div className="flex items-center gap-2 text-white">
                      <Loader2 className="h-5 w-5 animate-spin" />
                      <span>Analyzing image...</span>
                    </div>
                  </div>
                )}
              </div>

              {/* Confidence Score */}
              {confidence > 0 && !isAnalyzing && (
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Recognition Confidence:</span>
                  <Badge className={getConfidenceColor(confidence)}>
                    {getConfidenceText(confidence)} ({Math.round(confidence * 100)}%)
                  </Badge>
                </div>
              )}
            </div>
          )}

          {/* Recognition Results */}
          {recognitionResults.length > 0 && !isAnalyzing && (
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-green-600" />
                <h4 className="font-medium">Detected Food Items</h4>
              </div>

              {recognitionResults.map((food, index) => (
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
                        {food.portion && (
                          <p className="text-xs text-green-600 mt-1">
                            Estimated portion: {food.portion}
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

          {/* Tips */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-medium text-blue-900 mb-2">Tips for better recognition:</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• Ensure good lighting and clear focus</li>
              <li>• Include the entire food item in the frame</li>
              <li>• Avoid cluttered backgrounds</li>
              <li>• Take photos from above for best results</li>
              <li>• Multiple food items can be detected in one image</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default AIPhotoRecognition;