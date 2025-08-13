/**
 * Clinical Dashboard Service
 * 
 * Centralized API calls for all Enhanced Clinical Dashboard components
 * Provides real-time data fetching, state management, error handling, and loading states
 * 
 * @author Enhanced Clinical Dashboard Service
 * @version 1.0.0
 */

// Get backend URL from environment
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

/**
 * Base API utility class with error handling and retry logic
 */
class APIClient {
  constructor(baseURL) {
    this.baseURL = baseURL;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}/api${endpoint}`;
    const config = {
      headers: { ...this.defaultHeaders, ...options.headers },
      ...options
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      return {
        success: true,
        data,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error(`API Request failed for ${endpoint}:`, error);
      return {
        success: false,
        error: error.message,
        timestamp: new Date().toISOString()
      };
    }
  }

  get(endpoint, params = {}) {
    const queryParams = new URLSearchParams(params).toString();
    const fullEndpoint = queryParams ? `${endpoint}?${queryParams}` : endpoint;
    return this.request(fullEndpoint);
  }

  post(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    });
  }

  put(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  delete(endpoint) {
    return this.request(endpoint, {
      method: 'DELETE'
    });
  }
}

// Initialize API client
const apiClient = new APIClient(BACKEND_URL);

/**
 * Clinical Dashboard Service Class
 * Provides comprehensive API integration for all clinical dashboard components
 */
class ClinicalDashboardService {
  constructor() {
    this.api = apiClient;
    this.cache = new Map();
    this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    this.refreshIntervals = new Map();
    this.subscribers = new Map(); // For real-time updates
  }

  /**
   * Cache management utilities
   */
  getCacheKey(endpoint, params = {}) {
    return `${endpoint}_${JSON.stringify(params)}`;
  }

  getCachedData(cacheKey) {
    const cached = this.cache.get(cacheKey);
    if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
      return cached.data;
    }
    return null;
  }

  setCachedData(cacheKey, data) {
    this.cache.set(cacheKey, {
      data,
      timestamp: Date.now()
    });
  }

  clearCache() {
    this.cache.clear();
  }

  /**
   * Real-time subscription management
   */
  subscribe(component, callback) {
    if (!this.subscribers.has(component)) {
      this.subscribers.set(component, []);
    }
    this.subscribers.get(component).push(callback);
  }

  unsubscribe(component, callback) {
    if (this.subscribers.has(component)) {
      const callbacks = this.subscribers.get(component);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  notifySubscribers(component, data) {
    if (this.subscribers.has(component)) {
      this.subscribers.get(component).forEach(callback => callback(data));
    }
  }

  /**
   * PATIENT QUEUE MANAGEMENT
   */
  async getPatientQueue(providerId, useCache = true) {
    const cacheKey = this.getCacheKey('patient-queue', { providerId });
    
    if (useCache) {
      const cached = this.getCachedData(cacheKey);
      if (cached) return cached;
    }

    const response = await this.api.get(`/provider/patient-queue/${providerId}`);
    
    if (response.success) {
      this.setCachedData(cacheKey, response);
      this.notifySubscribers('patientQueue', response.data);
      return response;
    }
    
    throw new Error(response.error || 'Failed to fetch patient queue');
  }

  // Real-time patient queue updates
  startPatientQueueMonitoring(providerId, interval = 30000) {
    const intervalId = setInterval(async () => {
      try {
        await this.getPatientQueue(providerId, false);
      } catch (error) {
        console.error('Patient queue monitoring error:', error);
      }
    }, interval);

    this.refreshIntervals.set('patientQueue', intervalId);
  }

  stopPatientQueueMonitoring() {
    const intervalId = this.refreshIntervals.get('patientQueue');
    if (intervalId) {
      clearInterval(intervalId);
      this.refreshIntervals.delete('patientQueue');
    }
  }

  /**
   * CLINICAL DECISION SUPPORT
   */
  async getClinicalDecisionSupport(requestData) {
    const response = await this.api.post('/provider/clinical-decision-support', requestData);
    
    if (response.success) {
      this.notifySubscribers('clinicalDecision', response.data);
      return response;
    }
    
    throw new Error(response.error || 'Failed to get clinical decision support');
  }

  async getClinicalInsights(providerId) {
    const cacheKey = this.getCacheKey('clinical-insights', { providerId });
    const cached = this.getCachedData(cacheKey);
    if (cached) return cached;

    const response = await this.api.get(`/provider/clinical-insights/${providerId}`);
    
    if (response.success) {
      this.setCachedData(cacheKey, response);
      this.notifySubscribers('clinicalInsights', response.data);
      return response;
    }
    
    throw new Error(response.error || 'Failed to fetch clinical insights');
  }

  /**
   * TREATMENT OUTCOME TRACKING
   */
  async getTreatmentOutcomes(providerId, timeframe = '30d', useCache = true) {
    const cacheKey = this.getCacheKey('treatment-outcomes', { providerId, timeframe });
    
    if (useCache) {
      const cached = this.getCachedData(cacheKey);
      if (cached) return cached;
    }

    const response = await this.api.get(`/provider/treatment-outcomes/${providerId}`, { timeframe });
    
    if (response.success) {
      this.setCachedData(cacheKey, response);
      this.notifySubscribers('treatmentOutcomes', response.data);
      return response;
    }
    
    throw new Error(response.error || 'Failed to fetch treatment outcomes');
  }

  /**
   * POPULATION HEALTH ANALYTICS
   */
  async getPopulationHealth(providerId, useCache = true) {
    const cacheKey = this.getCacheKey('population-health', { providerId });
    
    if (useCache) {
      const cached = this.getCachedData(cacheKey);
      if (cached) return cached;
    }

    const response = await this.api.get(`/provider/population-health/${providerId}`);
    
    if (response.success) {
      this.setCachedData(cacheKey, response);
      this.notifySubscribers('populationHealth', response.data);
      return response;
    }
    
    throw new Error(response.error || 'Failed to fetch population health data');
  }

  /**
   * EVIDENCE-BASED RECOMMENDATIONS
   */
  async getEvidenceRecommendations(requestData) {
    const response = await this.api.post('/provider/evidence-recommendations', requestData);
    
    if (response.success) {
      this.notifySubscribers('evidenceRecommendations', response.data);
      return response;
    }
    
    throw new Error(response.error || 'Failed to get evidence-based recommendations');
  }

  /**
   * PROFESSIONAL CONTINUING EDUCATION
   */
  async getContinuingEducation(providerId, useCache = true) {
    const cacheKey = this.getCacheKey('continuing-education', { providerId });
    
    if (useCache) {
      const cached = this.getCachedData(cacheKey);
      if (cached) return cached;
    }

    const response = await this.api.get(`/provider/continuing-education/${providerId}`);
    
    if (response.success) {
      this.setCachedData(cacheKey, response);
      this.notifySubscribers('continuingEducation', response.data);
      return response;
    }
    
    throw new Error(response.error || 'Failed to fetch continuing education data');
  }

  async enrollInCourse(courseId, providerId) {
    const response = await this.api.post(`/provider/courses/${courseId}/enroll`, { provider_id: providerId });
    
    if (response.success) {
      // Clear cache to refresh continuing education data
      const cacheKey = this.getCacheKey('continuing-education', { providerId });
      this.cache.delete(cacheKey);
      
      this.notifySubscribers('courseEnrollment', response.data);
      return response;
    }
    
    throw new Error(response.error || 'Failed to enroll in course');
  }

  /**
   * COMPREHENSIVE DASHBOARD DATA
   */
  async getDashboardOverview(providerId) {
    try {
      const [
        patientQueue,
        clinicalInsights,
        treatmentOutcomes,
        populationHealth,
        continuingEducation
      ] = await Promise.allSettled([
        this.getPatientQueue(providerId),
        this.getClinicalInsights(providerId),
        this.getTreatmentOutcomes(providerId),
        this.getPopulationHealth(providerId),
        this.getContinuingEducation(providerId)
      ]);

      const dashboard = {
        patientQueue: patientQueue.status === 'fulfilled' ? patientQueue.value.data : null,
        clinicalInsights: clinicalInsights.status === 'fulfilled' ? clinicalInsights.value.data : null,
        treatmentOutcomes: treatmentOutcomes.status === 'fulfilled' ? treatmentOutcomes.value.data : null,
        populationHealth: populationHealth.status === 'fulfilled' ? populationHealth.value.data : null,
        continuingEducation: continuingEducation.status === 'fulfilled' ? continuingEducation.value.data : null,
        errors: []
      };

      // Collect any errors
      if (patientQueue.status === 'rejected') dashboard.errors.push('patientQueue');
      if (clinicalInsights.status === 'rejected') dashboard.errors.push('clinicalInsights');
      if (treatmentOutcomes.status === 'rejected') dashboard.errors.push('treatmentOutcomes');
      if (populationHealth.status === 'rejected') dashboard.errors.push('populationHealth');
      if (continuingEducation.status === 'rejected') dashboard.errors.push('continuingEducation');

      this.notifySubscribers('dashboardOverview', dashboard);
      return dashboard;
    } catch (error) {
      console.error('Dashboard overview fetch error:', error);
      throw error;
    }
  }

  /**
   * REAL-TIME MONITORING
   */
  startRealTimeMonitoring(providerId, options = {}) {
    const {
      patientQueueInterval = 30000, // 30 seconds
      treatmentOutcomesInterval = 300000, // 5 minutes
      populationHealthInterval = 600000 // 10 minutes
    } = options;

    // Start patient queue monitoring (most frequent updates)
    this.startPatientQueueMonitoring(providerId, patientQueueInterval);

    // Start treatment outcomes monitoring
    const treatmentInterval = setInterval(async () => {
      try {
        await this.getTreatmentOutcomes(providerId, '30d', false);
      } catch (error) {
        console.error('Treatment outcomes monitoring error:', error);
      }
    }, treatmentOutcomesInterval);

    // Start population health monitoring
    const populationInterval = setInterval(async () => {
      try {
        await this.getPopulationHealth(providerId, false);
      } catch (error) {
        console.error('Population health monitoring error:', error);
      }
    }, populationHealthInterval);

    this.refreshIntervals.set('treatmentOutcomes', treatmentInterval);
    this.refreshIntervals.set('populationHealth', populationInterval);
  }

  stopRealTimeMonitoring() {
    this.refreshIntervals.forEach((intervalId, key) => {
      clearInterval(intervalId);
    });
    this.refreshIntervals.clear();
  }

  /**
   * ERROR HANDLING & RETRY LOGIC
   */
  async retryRequest(requestFn, maxRetries = 3, delay = 1000) {
    let lastError;
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
      try {
        return await requestFn();
      } catch (error) {
        lastError = error;
        if (attempt < maxRetries) {
          await new Promise(resolve => setTimeout(resolve, delay * attempt));
        }
      }
    }
    
    throw lastError;
  }

  /**
   * BATCH OPERATIONS
   */
  async batchRequest(requests) {
    const results = await Promise.allSettled(requests);
    return results.map((result, index) => ({
      index,
      success: result.status === 'fulfilled',
      data: result.status === 'fulfilled' ? result.value : null,
      error: result.status === 'rejected' ? result.reason : null
    }));
  }

  /**
   * HEALTH CHECK
   */
  async healthCheck() {
    try {
      const response = await this.api.get('/');
      return {
        healthy: response.success,
        timestamp: new Date().toISOString(),
        backend: BACKEND_URL
      };
    } catch (error) {
      return {
        healthy: false,
        error: error.message,
        timestamp: new Date().toISOString(),
        backend: BACKEND_URL
      };
    }
  }

  /**
   * CLEANUP
   */
  cleanup() {
    this.stopRealTimeMonitoring();
    this.clearCache();
    this.subscribers.clear();
  }
}

// Export singleton instance
const clinicalDashboardService = new ClinicalDashboardService();

export default clinicalDashboardService;

// Export individual service methods for convenience
export {
  ClinicalDashboardService,
  clinicalDashboardService
};

// Export utility hooks for React components
export const useClinicalDashboardService = () => {
  return clinicalDashboardService;
};

/**
 * React Hook for loading states and error handling
 */
export const useApiState = (initialState = {}) => {
  const [state, setState] = React.useState({
    loading: false,
    error: null,
    data: null,
    lastUpdated: null,
    ...initialState
  });

  const setLoading = (loading) => setState(prev => ({ ...prev, loading }));
  const setError = (error) => setState(prev => ({ ...prev, error, loading: false }));
  const setData = (data) => setState(prev => ({ 
    ...prev, 
    data, 
    loading: false, 
    error: null, 
    lastUpdated: new Date().toISOString() 
  }));
  const reset = () => setState({ loading: false, error: null, data: null, lastUpdated: null });

  return {
    ...state,
    setLoading,
    setError,
    setData,
    reset
  };
};