const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

class GeminiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async recognizeFood(imageBase64) {
    try {
      const response = await fetch(`${this.baseURL}/api/ai/food-recognition`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: imageBase64,
          provider: 'gemini'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        success: true,
        foods: data.foods || [],
        confidence: data.confidence || 0.8,
        insights: data.insights || []
      };
    } catch (error) {
      console.error('Food recognition error:', error);
      return {
        success: false,
        error: error.message,
        foods: []
      };
    }
  }

  async generateHealthInsights(healthData) {
    try {
      const response = await fetch(`${this.baseURL}/api/ai/health-insights`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          healthData,
          provider: 'gemini',
          analysis_type: 'comprehensive'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        success: true,
        insights: data.insights || [],
        recommendations: data.recommendations || [],
        patterns: data.patterns || {},
        confidence: data.confidence || 0.85
      };
    } catch (error) {
      console.error('Health insights error:', error);
      return {
        success: false,
        error: error.message,
        insights: []
      };
    }
  }

  async analyzeFoodImage(imageFile) {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = async (e) => {
        const base64Image = e.target.result.split(',')[1]; // Remove data:image/jpeg;base64, prefix
        const result = await this.recognizeFood(base64Image);
        resolve(result);
      };
      reader.onerror = () => {
        resolve({
          success: false,
          error: 'Failed to read image file',
          foods: []
        });
      };
      reader.readAsDataURL(imageFile);
    });
  }

  async generateMealSuggestions(nutritionHistory, preferences = {}) {
    try {
      const response = await fetch(`${this.baseURL}/api/ai/meal-suggestions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nutritionHistory,
          preferences,
          provider: 'gemini'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        success: true,
        suggestions: data.suggestions || [],
        reasoning: data.reasoning || '',
        nutritionalBenefits: data.nutritionalBenefits || []
      };
    } catch (error) {
      console.error('Meal suggestions error:', error);
      return {
        success: false,
        error: error.message,
        suggestions: []
      };
    }
  }

  async processVoiceCommand(transcript) {
    try {
      const response = await fetch(`${this.baseURL}/api/ai/voice-command`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          transcript,
          provider: 'gemini',
          command_type: 'food_logging'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        success: true,
        foodItems: data.foodItems || [],
        intent: data.intent || 'log_food',
        confidence: data.confidence || 0.8,
        clarifications: data.clarifications || []
      };
    } catch (error) {
      console.error('Voice command processing error:', error);
      return {
        success: false,
        error: error.message,
        foodItems: []
      };
    }
  }

  // Utility method to validate image file
  validateImageFile(file) {
    const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
    const maxSize = 10 * 1024 * 1024; // 10MB

    if (!validTypes.includes(file.type)) {
      return {
        valid: false,
        error: 'Please upload a JPEG, PNG, or WebP image file'
      };
    }

    if (file.size > maxSize) {
      return {
        valid: false,
        error: 'Image file size must be less than 10MB'
      };
    }

    return { valid: true };
  }

  // Format nutrition data for AI analysis
  formatNutritionData(rawData) {
    return {
      dailyIntake: rawData.calories || 0,
      macros: {
        protein: rawData.protein || 0,
        carbs: rawData.carbs || 0,
        fat: rawData.fat || 0
      },
      micronutrients: rawData.micronutrients || {},
      mealTiming: rawData.mealTiming || [],
      exerciseData: rawData.exercise || {},
      healthMetrics: rawData.healthMetrics || {}
    };
  }
}

export default new GeminiService();