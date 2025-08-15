/**
 * Predictive Analytics Service
 * Integrates with backend ML models for health predictions and insights
 */

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

class PredictiveAnalyticsService {
  constructor() {
    this.cache = new Map();
    this.cacheExpiry = 5 * 60 * 1000; // 5 minutes
  }

  /**
   * Predict daily energy levels based on food intake and lifestyle factors
   */
  async predictEnergy(intakeData) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/ai/energy-prediction`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          intake_data: intakeData
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        success: true,
        data: {
          predicted_energy: data.predicted_energy,
          confidence: data.confidence,
          factors: data.factors,
          recommendations: data.recommendations,
          model_accuracy: data.model_accuracy
        }
      };
    } catch (error) {
      console.error('Error predicting energy:', error);
      return {
        success: false,
        error: error.message,
        data: this._getDefaultEnergyPrediction()
      };
    }
  }

  /**
   * Analyze mood-food correlations
   */
  async analyzeMoodFoodCorrelation(userId, timeframeDays = 30) {
    const cacheKey = `mood-correlation-${userId}-${timeframeDays}`;
    
    // Check cache first
    if (this._getCachedData(cacheKey)) {
      return this._getCachedData(cacheKey);
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/ai/mood-food-correlation`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          timeframe_days: timeframeDays
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const result = {
        success: true,
        data: {
          correlations: data.correlations,
          trigger_foods: data.trigger_foods,
          mood_predictors: data.mood_predictors,
          recommendations: data.recommendations,
          confidence: data.confidence
        }
      };

      this._setCachedData(cacheKey, result);
      return result;
    } catch (error) {
      console.error('Error analyzing mood-food correlation:', error);
      return {
        success: false,
        error: error.message,
        data: this._getDefaultMoodCorrelation()
      };
    }
  }

  /**
   * Analyze sleep impact based on daily choices
   */
  async analyzeSleepImpact(dailyChoices) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/ai/sleep-impact-analysis`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          daily_choices: dailyChoices
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        success: true,
        data: {
          predicted_sleep_quality: data.predicted_sleep_quality,
          improvement_potential: data.improvement_potential,
          factor_analysis: data.factor_analysis,
          recommendations: data.recommendations,
          confidence: data.confidence
        }
      };
    } catch (error) {
      console.error('Error analyzing sleep impact:', error);
      return {
        success: false,
        error: error.message,
        data: this._getDefaultSleepImpact()
      };
    }
  }

  /**
   * Process "What-If" scenarios for health predictions
   */
  async processWhatIfScenarios(baseData, proposedChanges) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/ai/what-if-scenarios`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          base_data: baseData,
          proposed_changes: proposedChanges
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        success: true,
        data: {
          scenario_id: data.scenario_id,
          changes_applied: data.changes_applied,
          current_state: data.current_state,
          predicted_state: data.predicted_state,
          impact_analysis: data.impact_analysis,
          recommendations: data.recommendations,
          confidence: data.confidence
        }
      };
    } catch (error) {
      console.error('Error processing what-if scenarios:', error);
      return {
        success: false,
        error: error.message,
        data: this._getDefaultWhatIfScenario()
      };
    }
  }

  /**
   * Get weekly health patterns analysis
   */
  async getWeeklyHealthPatterns(userId, weeksBack = 4) {
    const cacheKey = `weekly-patterns-${userId}-${weeksBack}`;
    
    // Check cache first
    if (this._getCachedData(cacheKey)) {
      return this._getCachedData(cacheKey);
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/ai/weekly-health-patterns/${userId}?weeks_back=${weeksBack}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const result = {
        success: true,
        data: {
          patterns: data.patterns,
          insights: data.insights,
          anomalies: data.anomalies,
          recommendations: data.recommendations,
          trend_direction: data.trend_direction,
          confidence: data.confidence || 0.8
        }
      };

      this._setCachedData(cacheKey, result);
      return result;
    } catch (error) {
      console.error('Error fetching weekly health patterns:', error);
      return {
        success: false,
        error: error.message,
        data: this._getDefaultWeeklyPatterns()
      };
    }
  }

  /**
   * Generate sample "what-if" scenario data for testing
   */
  generateSampleScenarios() {
    return [
      {
        id: 'protein-increase',
        name: 'Increase Protein by 20g',
        description: 'Add 20g more protein to your daily intake',
        changes: { protein_g: 20 },
        expectedImpacts: ['15% energy improvement', '8% muscle recovery boost']
      },
      {
        id: 'sugar-reduction',
        name: 'Reduce Sugar by 15g',
        description: 'Cut daily sugar intake by 15g',
        changes: { sugar_g: -15 },
        expectedImpacts: ['18% mood stability improvement', '12% energy consistency boost']
      },
      {
        id: 'exercise-increase',
        name: 'Add 30min Exercise',
        description: 'Increase daily exercise by 30 minutes',
        changes: { exercise_minutes: 30 },
        expectedImpacts: ['25% energy boost', '20% sleep quality improvement']
      },
      {
        id: 'sleep-optimization',
        name: 'Optimize Sleep Schedule',
        description: 'Get 8 hours of quality sleep consistently',
        changes: { sleep_hours: 8, sleep_consistency: 0.9 },
        expectedImpacts: ['30% energy improvement', '22% mood stability boost']
      }
    ];
  }

  // Cache management
  _getCachedData(key) {
    const cached = this.cache.get(key);
    if (cached && Date.now() - cached.timestamp < this.cacheExpiry) {
      return cached.data;
    }
    return null;
  }

  _setCachedData(key, data) {
    this.cache.set(key, {
      data,
      timestamp: Date.now()
    });
  }

  // Default fallback data
  _getDefaultEnergyPrediction() {
    return {
      predicted_energy: 6.5,
      confidence: 0.7,
      factors: {
        sleep_hours: { value: 7.5, importance: 0.8, impact: 'positive' },
        protein_g: { value: 100, importance: 0.6, impact: 'positive' },
        stress_level: { value: 5, importance: 0.7, impact: 'neutral' }
      },
      recommendations: ['Maintain balanced nutrition', 'Ensure adequate sleep'],
      model_accuracy: 0.75
    };
  }

  _getDefaultMoodCorrelation() {
    return {
      correlations: {
        sugar_mood: { correlation: -0.65, strength: 'moderate' },
        protein_mood: { correlation: 0.58, strength: 'moderate' }
      },
      trigger_foods: {
        processed_foods: { impact: -0.8, frequency: 0.3 }
      },
      mood_predictors: {
        meal_regularity: { importance: 0.74 }
      },
      recommendations: ['Reduce processed foods', 'Maintain regular meal timing'],
      confidence: 0.75
    };
  }

  _getDefaultSleepImpact() {
    return {
      predicted_sleep_quality: 7.2,
      improvement_potential: 1.5,
      factor_analysis: {
        caffeine_timing: { impact: -0.6, weight: 0.25 },
        meal_timing: { impact: -0.4, weight: 0.20 }
      },
      recommendations: ['Avoid late caffeine', 'Earlier dinner timing'],
      confidence: 0.7
    };
  }

  _getDefaultWhatIfScenario() {
    return {
      scenario_id: 'default',
      changes_applied: {},
      current_state: { energy: 6.0, sleep: 7.0, mood: 7.0 },
      predicted_state: { energy: 6.5, sleep: 7.5, mood: 7.5 },
      impact_analysis: {
        energy_change: 8.3,
        sleep_change: 7.1,
        mood_change: 7.1
      },
      recommendations: ['Try the suggested changes gradually'],
      confidence: 0.7
    };
  }

  _getDefaultWeeklyPatterns() {
    return {
      patterns: {
        nutrition_consistency: 8.5,
        energy_patterns: 6.8,
        sleep_trends: 7.2,
        activity_levels: 7.0,
        mood_stability: 7.5
      },
      insights: [
        'Nutrition consistency is excellent this week',
        'Energy levels dip on weekends',
        'Sleep quality shows improvement trend'
      ],
      anomalies: [
        {
          type: 'energy_dip',
          date: '2024-01-15',
          severity: 'moderate',
          description: 'Unusual energy drop detected'
        }
      ],
      recommendations: [
        'Maintain weekend nutrition consistency',
        'Consider earlier bedtime on Sunday'
      ],
      trend_direction: 'improving',
      confidence: 0.8
    };
  }
}

// Export singleton instance
export default new PredictiveAnalyticsService();