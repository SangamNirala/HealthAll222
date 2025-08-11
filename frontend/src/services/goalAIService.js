// Goal AI Service - Integrates with backend AI APIs for goal suggestions and analysis
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

class GoalAIService {
  constructor() {
    this.apiClient = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
    });

    // Add auth token to requests
    this.apiClient.interceptors.request.use((config) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  /**
   * Generate AI-powered goal suggestions based on user's current goals and progress
   * @param {Array} goals - User's current goals
   * @param {Array} achievements - User's achievements history
   * @param {Object} preferences - User preferences for suggestions
   * @returns {Promise<Array>} Array of AI-generated suggestions
   */
  async generateGoalSuggestions(goals, achievements, preferences = {}) {
    try {
      const requestData = {
        current_goals: goals.map(goal => ({
          id: goal.id,
          title: goal.title,
          category: goal.category,
          progress: goal.progress,
          target_value: goal.target_value,
          current_value: goal.current_value,
          deadline: goal.deadline,
          created_date: goal.created_date
        })),
        achievements: achievements.map(achievement => ({
          id: achievement.id,
          goal_id: achievement.goal_id,
          category: achievement.category,
          date_achieved: achievement.date_achieved,
          badge_type: achievement.badge_type
        })),
        user_preferences: preferences,
        analysis_type: 'goal_optimization'
      };

      const response = await this.apiClient.post('/api/ai/goal-suggestions', requestData);
      
      if (response.data && response.data.suggestions) {
        return this.processSuggestions(response.data.suggestions);
      }

      // Fallback to mock data if API unavailable
      return this.generateMockSuggestions(goals, achievements);
      
    } catch (error) {
      console.error('Error generating goal suggestions:', error);
      // Return mock suggestions as fallback
      return this.generateMockSuggestions(goals, achievements);
    }
  }

  /**
   * Analyze goal correlations and patterns
   * @param {Array} goals - User's goals
   * @param {Array} dailyData - Daily progress data
   * @returns {Promise<Object>} Correlation analysis results
   */
  async analyzeGoalCorrelations(goals, dailyData) {
    try {
      const requestData = {
        goals: goals,
        daily_progress_data: dailyData,
        analysis_period: '30days',
        correlation_types: ['goal_interdependence', 'timing_patterns', 'success_factors']
      };

      const response = await this.apiClient.post('/api/ai/correlation-analysis', requestData);
      
      if (response.data && response.data.correlations) {
        return this.processCorrelationData(response.data.correlations);
      }

      return this.generateMockCorrelationData(goals);
      
    } catch (error) {
      console.error('Error analyzing goal correlations:', error);
      return this.generateMockCorrelationData(goals);
    }
  }

  /**
   * Get AI insights about goal achievement probability
   * @param {Object} goal - Individual goal to analyze
   * @param {Array} historicalData - Historical progress data
   * @returns {Promise<Object>} AI insights about goal
   */
  async getGoalInsights(goal, historicalData) {
    try {
      const requestData = {
        goal: {
          id: goal.id,
          title: goal.title,
          category: goal.category,
          progress: goal.progress,
          target_value: goal.target_value,
          current_value: goal.current_value,
          deadline: goal.deadline
        },
        historical_data: historicalData,
        insight_types: ['success_probability', 'optimization_recommendations', 'risk_factors']
      };

      const response = await this.apiClient.post('/api/ai/goal-insights', requestData);
      
      if (response.data && response.data.insights) {
        return response.data.insights;
      }

      return this.generateMockGoalInsights(goal);
      
    } catch (error) {
      console.error('Error getting goal insights:', error);
      return this.generateMockGoalInsights(goal);
    }
  }

  /**
   * Process AI suggestions response and add metadata
   */
  processSuggestions(suggestions) {
    return suggestions.map(suggestion => ({
      ...suggestion,
      id: suggestion.id || `suggestion_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      generated_at: new Date().toISOString(),
      confidence: Math.round(suggestion.confidence * 100) / 100,
      estimated_success_rate: Math.round(suggestion.estimated_success_rate * 100) / 100
    }));
  }

  /**
   * Process correlation analysis data
   */
  processCorrelationData(correlations) {
    return {
      ...correlations,
      processed_at: new Date().toISOString(),
      correlations: correlations.correlations.map(corr => ({
        ...corr,
        correlation: Math.round(corr.correlation * 100) / 100,
        significance: corr.significance || this.calculateSignificance(corr.correlation)
      }))
    };
  }

  /**
   * Calculate statistical significance of correlation
   */
  calculateSignificance(correlation) {
    const absCorr = Math.abs(correlation);
    if (absCorr >= 0.7) return 'high';
    if (absCorr >= 0.5) return 'moderate';
    if (absCorr >= 0.3) return 'low';
    return 'negligible';
  }

  /**
   * Generate mock suggestions for fallback
   */
  generateMockSuggestions(goals, achievements) {
    const mockSuggestions = [
      {
        id: 'mock_suggestion_1',
        type: 'adjustment',
        title: 'Optimize Goal Timeline',
        description: 'Based on your progress patterns, consider adjusting your timeline for better success rates.',
        confidence: 0.78,
        priority: 'medium',
        category: goals.length > 0 ? goals[0].category : 'FITNESS',
        goal_id: goals.length > 0 ? goals[0].id : null,
        recommendation: {
          suggested_adjustment: 'Extend timeline by 1 week',
          reasoning: 'Your current pace suggests a slightly longer timeframe would improve success probability.'
        },
        estimated_success_rate: 0.85,
        timeline: '1 week adjustment'
      }
    ];

    return this.processSuggestions(mockSuggestions);
  }

  /**
   * Generate mock correlation data for fallback
   */
  generateMockCorrelationData(goals) {
    return {
      correlations: [
        {
          goal1: goals[0]?.category || 'FITNESS',
          goal2: goals[1]?.category || 'NUTRITION',
          correlation: 0.73,
          significance: 'high',
          relationship_type: 'positive'
        }
      ],
      insights: [
        'Strong positive correlation detected between fitness and nutrition goals',
        'Progress in one area typically leads to progress in the other'
      ],
      processed_at: new Date().toISOString()
    };
  }

  /**
   * Generate mock goal insights for fallback
   */
  generateMockGoalInsights(goal) {
    return {
      goal_id: goal.id,
      success_probability: Math.random() * 0.4 + 0.6, // 60-100%
      confidence: Math.random() * 0.3 + 0.7, // 70-100%
      key_factors: [
        'Current progress trajectory',
        'Historical performance patterns',
        'Goal difficulty assessment',
        'Time remaining analysis'
      ],
      recommendations: [
        'Maintain current pace for optimal results',
        'Consider breaking down into smaller milestones'
      ],
      risk_factors: goal.progress < 50 ? ['Behind target pace'] : [],
      generated_at: new Date().toISOString()
    };
  }

  /**
   * Submit goal adjustment based on AI suggestion
   * @param {String} goalId - Goal to adjust
   * @param {Object} adjustments - Adjustments to make
   * @returns {Promise<Object>} Updated goal data
   */
  async applyGoalAdjustment(goalId, adjustments) {
    try {
      const response = await this.apiClient.put(`/api/goals/${goalId}`, adjustments);
      return response.data;
    } catch (error) {
      console.error('Error applying goal adjustment:', error);
      throw error;
    }
  }

  /**
   * Create new goal from AI suggestion
   * @param {Object} goalData - New goal data from suggestion
   * @returns {Promise<Object>} Created goal
   */
  async createGoalFromSuggestion(goalData) {
    try {
      const response = await this.apiClient.post('/api/goals', {
        ...goalData,
        source: 'ai_suggestion',
        created_at: new Date().toISOString()
      });
      return response.data;
    } catch (error) {
      console.error('Error creating goal from suggestion:', error);
      throw error;
    }
  }
}

// Export singleton instance
export default new GoalAIService();