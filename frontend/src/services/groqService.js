const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

class GroqService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async generateMealSuggestions(userData) {
    try {
      const response = await fetch(`${this.baseURL}/api/ai/meal-suggestions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userData,
          provider: 'groq'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        success: true,
        suggestions: data.suggestions || [],
        reasoning: data.reasoning || [],
        confidence: data.confidence || 0.8
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
          provider: 'groq'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        success: true,
        intent: data.intent || 'unknown',
        foods: data.foods || [],
        confidence: data.confidence || 0.8,
        clarifications: data.clarifications || []
      };
    } catch (error) {
      console.error('Voice command processing error:', error);
      return {
        success: false,
        error: error.message,
        intent: 'unknown',
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
          provider: 'groq'
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
        patterns: data.patterns || [],
        confidence: data.confidence || 0.8
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

  validateTextInput(text) {
    if (!text || typeof text !== 'string') {
      return { valid: false, error: 'Text input is required' };
    }

    const cleanText = text.trim();
    if (cleanText.length === 0) {
      return { valid: false, error: 'Text cannot be empty' };
    }

    if (cleanText.length > 1000) {
      return { valid: false, error: 'Text is too long (max 1000 characters)' };
    }

    return { valid: true };
  }
}

const groqService = new GroqService();
export default groqService;