/**
 * Clinical Dashboard React Hooks
 * 
 * Custom React hooks for integrating Clinical Dashboard components with the service layer
 * Provides real-time data, loading states, error handling, and automatic updates
 * 
 * @author Clinical Dashboard Hooks
 * @version 1.0.0
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import clinicalDashboardService from '../services/clinicalDashboardService';

/**
 * Custom hook for Patient Queue Management
 */
export const usePatientQueue = (providerId, options = {}) => {
  const {
    realTime = false,
    refreshInterval = 30000,
    autoStart = true
  } = options;

  const [state, setState] = useState({
    loading: false,
    error: null,
    data: null,
    lastUpdated: null
  });

  const mounted = useRef(true);

  const fetchData = useCallback(async (useCache = true) => {
    if (!providerId) return;

    setState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      const response = await clinicalDashboardService.getPatientQueue(providerId, useCache);
      
      if (mounted.current) {
        setState({
          loading: false,
          error: null,
          data: response.data,
          lastUpdated: response.timestamp
        });
      }
    } catch (error) {
      if (mounted.current) {
        setState(prev => ({
          ...prev,
          loading: false,
          error: error.message
        }));
      }
    }
  }, [providerId]);

  const refresh = useCallback(() => fetchData(false), [fetchData]);

  useEffect(() => {
    if (autoStart && providerId) {
      fetchData();

      // Set up real-time monitoring if enabled
      if (realTime) {
        clinicalDashboardService.startPatientQueueMonitoring(providerId, refreshInterval);
        
        const callback = (data) => {
          if (mounted.current) {
            setState(prev => ({
              ...prev,
              data,
              lastUpdated: new Date().toISOString()
            }));
          }
        };
        
        clinicalDashboardService.subscribe('patientQueue', callback);

        return () => {
          clinicalDashboardService.stopPatientQueueMonitoring();
          clinicalDashboardService.unsubscribe('patientQueue', callback);
        };
      }
    }

    return () => {
      mounted.current = false;
    };
  }, [providerId, realTime, refreshInterval, autoStart, fetchData]);

  return {
    ...state,
    refresh,
    isStale: state.lastUpdated && Date.now() - new Date(state.lastUpdated).getTime() > refreshInterval
  };
};

/**
 * Custom hook for Clinical Decision Support
 */
export const useClinicalDecisionSupport = () => {
  const [state, setState] = useState({
    loading: false,
    error: null,
    data: null,
    lastRequest: null
  });

  const getSupport = useCallback(async (requestData) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      const response = await clinicalDashboardService.getClinicalDecisionSupport(requestData);
      
      setState({
        loading: false,
        error: null,
        data: response.data,
        lastRequest: new Date().toISOString()
      });

      return response.data;
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error.message
      }));
      throw error;
    }
  }, []);

  const reset = useCallback(() => {
    setState({
      loading: false,
      error: null,
      data: null,
      lastRequest: null
    });
  }, []);

  return {
    ...state,
    getSupport,
    reset
  };
};

/**
 * Custom hook for Clinical Insights
 */
export const useClinicalInsights = (providerId, options = {}) => {
  const { autoStart = true } = options;

  const [state, setState] = useState({
    loading: false,
    error: null,
    data: null,
    lastUpdated: null
  });

  const fetchData = useCallback(async () => {
    if (!providerId) return;

    setState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      const response = await clinicalDashboardService.getClinicalInsights(providerId);
      
      setState({
        loading: false,
        error: null,
        data: response.data,
        lastUpdated: response.timestamp
      });
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error.message
      }));
    }
  }, [providerId]);

  useEffect(() => {
    if (autoStart && providerId) {
      fetchData();
    }
  }, [autoStart, providerId, fetchData]);

  return {
    ...state,
    refresh: fetchData
  };
};

/**
 * Custom hook for Treatment Outcomes
 */
export const useTreatmentOutcomes = (providerId, timeframe = '30d', options = {}) => {
  const { realTime = false, refreshInterval = 300000, autoStart = true } = options;

  const [state, setState] = useState({
    loading: false,
    error: null,
    data: null,
    lastUpdated: null
  });

  const mounted = useRef(true);

  const fetchData = useCallback(async (useCache = true) => {
    if (!providerId) return;

    setState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      const response = await clinicalDashboardService.getTreatmentOutcomes(providerId, timeframe, useCache);
      
      if (mounted.current) {
        setState({
          loading: false,
          error: null,
          data: response.data,
          lastUpdated: response.timestamp
        });
      }
    } catch (error) {
      if (mounted.current) {
        setState(prev => ({
          ...prev,
          loading: false,
          error: error.message
        }));
      }
    }
  }, [providerId, timeframe]);

  const refresh = useCallback(() => fetchData(false), [fetchData]);

  useEffect(() => {
    if (autoStart && providerId) {
      fetchData();

      if (realTime) {
        const interval = setInterval(() => fetchData(false), refreshInterval);
        
        const callback = (data) => {
          if (mounted.current) {
            setState(prev => ({
              ...prev,
              data,
              lastUpdated: new Date().toISOString()
            }));
          }
        };
        
        clinicalDashboardService.subscribe('treatmentOutcomes', callback);

        return () => {
          clearInterval(interval);
          clinicalDashboardService.unsubscribe('treatmentOutcomes', callback);
        };
      }
    }

    return () => {
      mounted.current = false;
    };
  }, [providerId, timeframe, realTime, refreshInterval, autoStart, fetchData]);

  return {
    ...state,
    refresh,
    isStale: state.lastUpdated && Date.now() - new Date(state.lastUpdated).getTime() > refreshInterval
  };
};

/**
 * Custom hook for Population Health Analytics
 */
export const usePopulationHealth = (providerId, options = {}) => {
  const { realTime = false, refreshInterval = 600000, autoStart = true } = options;

  const [state, setState] = useState({
    loading: false,
    error: null,
    data: null,
    lastUpdated: null
  });

  const mounted = useRef(true);

  const fetchData = useCallback(async (useCache = true) => {
    if (!providerId) return;

    setState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      const response = await clinicalDashboardService.getPopulationHealth(providerId, useCache);
      
      if (mounted.current) {
        setState({
          loading: false,
          error: null,
          data: response.data,
          lastUpdated: response.timestamp
        });
      }
    } catch (error) {
      if (mounted.current) {
        setState(prev => ({
          ...prev,
          loading: false,
          error: error.message
        }));
      }
    }
  }, [providerId]);

  const refresh = useCallback(() => fetchData(false), [fetchData]);

  useEffect(() => {
    if (autoStart && providerId) {
      fetchData();

      if (realTime) {
        const interval = setInterval(() => fetchData(false), refreshInterval);
        
        const callback = (data) => {
          if (mounted.current) {
            setState(prev => ({
              ...prev,
              data,
              lastUpdated: new Date().toISOString()
            }));
          }
        };
        
        clinicalDashboardService.subscribe('populationHealth', callback);

        return () => {
          clearInterval(interval);
          clinicalDashboardService.unsubscribe('populationHealth', callback);
        };
      }
    }

    return () => {
      mounted.current = false;
    };
  }, [providerId, realTime, refreshInterval, autoStart, fetchData]);

  return {
    ...state,
    refresh,
    isStale: state.lastUpdated && Date.now() - new Date(state.lastUpdated).getTime() > refreshInterval
  };
};

/**
 * Custom hook for Evidence-Based Recommendations
 */
export const useEvidenceRecommendations = () => {
  const [state, setState] = useState({
    loading: false,
    error: null,
    data: null,
    lastRequest: null
  });

  const getRecommendations = useCallback(async (requestData) => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      const response = await clinicalDashboardService.getEvidenceRecommendations(requestData);
      
      setState({
        loading: false,
        error: null,
        data: response.data,
        lastRequest: new Date().toISOString()
      });

      return response.data;
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error.message
      }));
      throw error;
    }
  }, []);

  const reset = useCallback(() => {
    setState({
      loading: false,
      error: null,
      data: null,
      lastRequest: null
    });
  }, []);

  return {
    ...state,
    getRecommendations,
    reset
  };
};

/**
 * Custom hook for Continuing Education
 */
export const useContinuingEducation = (providerId, options = {}) => {
  const { autoStart = true } = options;

  const [state, setState] = useState({
    loading: false,
    error: null,
    data: null,
    lastUpdated: null,
    enrolling: false,
    enrollmentError: null
  });

  const fetchData = useCallback(async () => {
    if (!providerId) return;

    setState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      const response = await clinicalDashboardService.getContinuingEducation(providerId);
      
      setState(prev => ({
        ...prev,
        loading: false,
        error: null,
        data: response.data,
        lastUpdated: response.timestamp
      }));
    } catch (error) {
      setState(prev => ({
        ...prev,
        loading: false,
        error: error.message
      }));
    }
  }, [providerId]);

  const enrollInCourse = useCallback(async (courseId) => {
    setState(prev => ({ ...prev, enrolling: true, enrollmentError: null }));
    
    try {
      const response = await clinicalDashboardService.enrollInCourse(courseId, providerId);
      
      setState(prev => ({
        ...prev,
        enrolling: false,
        enrollmentError: null
      }));

      // Refresh education data after successful enrollment
      await fetchData();

      return response.data;
    } catch (error) {
      setState(prev => ({
        ...prev,
        enrolling: false,
        enrollmentError: error.message
      }));
      throw error;
    }
  }, [providerId, fetchData]);

  useEffect(() => {
    if (autoStart && providerId) {
      fetchData();
    }
  }, [autoStart, providerId, fetchData]);

  return {
    ...state,
    refresh: fetchData,
    enrollInCourse
  };
};

/**
 * Comprehensive Dashboard Hook
 * Fetches all dashboard data in a single call
 */
export const useDashboardOverview = (providerId, options = {}) => {
  const { autoStart = true, realTime = false } = options;

  const [state, setState] = useState({
    loading: false,
    error: null,
    data: null,
    lastUpdated: null
  });

  const mounted = useRef(true);

  const fetchData = useCallback(async () => {
    if (!providerId) return;

    setState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      const dashboard = await clinicalDashboardService.getDashboardOverview(providerId);
      
      if (mounted.current) {
        setState({
          loading: false,
          error: dashboard.errors.length > 0 ? `Failed to load: ${dashboard.errors.join(', ')}` : null,
          data: dashboard,
          lastUpdated: new Date().toISOString()
        });
      }
    } catch (error) {
      if (mounted.current) {
        setState(prev => ({
          ...prev,
          loading: false,
          error: error.message
        }));
      }
    }
  }, [providerId]);

  useEffect(() => {
    if (autoStart && providerId) {
      fetchData();

      if (realTime) {
        clinicalDashboardService.startRealTimeMonitoring(providerId);
        
        const callback = (data) => {
          if (mounted.current) {
            setState(prev => ({
              ...prev,
              data: prev.data ? { ...prev.data, ...data } : data,
              lastUpdated: new Date().toISOString()
            }));
          }
        };
        
        clinicalDashboardService.subscribe('dashboardOverview', callback);

        return () => {
          clinicalDashboardService.stopRealTimeMonitoring();
          clinicalDashboardService.unsubscribe('dashboardOverview', callback);
        };
      }
    }

    return () => {
      mounted.current = false;
    };
  }, [providerId, autoStart, realTime, fetchData]);

  return {
    ...state,
    refresh: fetchData
  };
};

/**
 * Service Health Check Hook
 */
export const useServiceHealth = () => {
  const [health, setHealth] = useState({
    healthy: null,
    checking: false,
    lastCheck: null,
    error: null
  });

  const checkHealth = useCallback(async () => {
    setHealth(prev => ({ ...prev, checking: true, error: null }));
    
    try {
      const result = await clinicalDashboardService.healthCheck();
      setHealth({
        healthy: result.healthy,
        checking: false,
        lastCheck: result.timestamp,
        error: result.error || null
      });
    } catch (error) {
      setHealth({
        healthy: false,
        checking: false,
        lastCheck: new Date().toISOString(),
        error: error.message
      });
    }
  }, []);

  useEffect(() => {
    checkHealth();
  }, [checkHealth]);

  return {
    ...health,
    checkHealth
  };
};

// Export utility function for manual cleanup
export const cleanupClinicalDashboard = () => {
  clinicalDashboardService.cleanup();
};