import React, { useState, useEffect, useMemo } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { 
  Stethoscope, Users, Brain, BarChart3, 
  BookOpen, GraduationCap, RefreshCw, Settings,
  Activity, TrendingUp, AlertTriangle, Loader2,
  Wifi, WifiOff
} from 'lucide-react';

// Import service layer and hooks
import {
  useDashboardOverview,
  useServiceHealth,
  cleanupClinicalDashboard
} from '../hooks/useClinicalDashboard';

// Import sub-components
import PatientQueue from './clinical/PatientQueue';
import ClinicalDecisionSupport from './clinical/ClinicalDecisionSupport';
import TreatmentOutcomeTracking from './clinical/TreatmentOutcomeTracking';
import PopulationHealthAnalytics from './clinical/PopulationHealthAnalytics';
import EvidenceBasedRecommendations from './clinical/EvidenceBasedRecommendations';
import ProfessionalContinuingEducation from './clinical/ProfessionalContinuingEducation';

const ClinicalDashboard = () => {
  const { switchRole } = useRole();
  const [activeView, setActiveView] = useState('overview');
  const [realTimeEnabled, setRealTimeEnabled] = useState(true);
  
  // Provider ID (in real implementation, this would come from auth/context)
  const providerId = 'demo-provider-123';
  
  // Use comprehensive dashboard hook with real-time monitoring
  const {
    loading: dashboardLoading,
    error: dashboardError,
    data: dashboardData,
    lastUpdated,
    refresh: refreshDashboard
  } = useDashboardOverview(providerId, {
    autoStart: true,
    realTime: realTimeEnabled
  });

  // Service health monitoring
  const {
    healthy: serviceHealthy,
    checking: healthChecking,
    lastCheck: lastHealthCheck,
    checkHealth
  } = useServiceHealth();

  // Set role to provider when component mounts
  useEffect(() => {
    switchRole('provider');
  }, [switchRole]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      cleanupClinicalDashboard();
    };
  }, []);

  // Dashboard metrics derived from API data
  const dashboardMetrics = useMemo(() => {
    if (!dashboardData) return null;
    
    const { patientQueue, treatmentOutcomes, populationHealth } = dashboardData;
    
    return {
      queueCount: patientQueue?.queue_stats?.total_in_queue || 0,
      urgentCases: patientQueue?.queue_stats?.urgent_cases || 0,
      scheduledToday: patientQueue?.queue_stats?.scheduled_today || 0,
      successRate: Math.round((treatmentOutcomes?.outcome_summary?.success_rate || 0) * 100),
      activePatients: populationHealth?.population_overview?.active_patients || 0,
      satisfactionScore: treatmentOutcomes?.patient_satisfaction?.average_rating || 0
    };
  }, [dashboardData]);

  const handleRefresh = async () => {
    await refreshDashboard();
    await checkHealth();
  };

  const toggleRealTime = () => {
    setRealTimeEnabled(!realTimeEnabled);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Dashboard Header */}
        <div className="mb-8">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Enhanced Clinical Dashboard
              </h1>
              <p className="text-gray-600">
                Comprehensive clinical interface for patient management and decision support
              </p>
            </div>
            <div className="flex items-center space-x-3">
              {/* Service Health Indicator */}
              <div className="flex items-center space-x-2">
                {serviceHealthy === null ? (
                  <Loader2 className="w-4 h-4 animate-spin text-gray-400" />
                ) : serviceHealthy ? (
                  <Wifi className="w-4 h-4 text-green-500" />
                ) : (
                  <WifiOff className="w-4 h-4 text-red-500" />
                )}
                <span className="text-xs text-gray-500">
                  {serviceHealthy === null ? 'Checking...' : 
                   serviceHealthy ? 'Connected' : 'Disconnected'}
                </span>
              </div>

              {/* Last Updated */}
              <div className="text-sm text-gray-500">
                {lastUpdated ? (
                  `Last updated: ${new Date(lastUpdated).toLocaleTimeString()}`
                ) : 'Loading...'}
              </div>

              {/* Real-time Toggle */}
              <Button
                variant="outline"
                size="sm"
                onClick={toggleRealTime}
                className={realTimeEnabled ? 'bg-green-50 border-green-200' : ''}
              >
                {realTimeEnabled ? 'Real-time ON' : 'Real-time OFF'}
              </Button>

              {/* Refresh Button */}
              <Button 
                variant="outline" 
                size="sm" 
                onClick={handleRefresh}
                disabled={dashboardLoading || healthChecking}
              >
                {(dashboardLoading || healthChecking) ? (
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                ) : (
                  <RefreshCw className="w-4 h-4 mr-2" />
                )}
                Refresh
              </Button>

              <Button variant="outline" size="sm">
                <Settings className="w-4 h-4 mr-2" />
                Settings
              </Button>
            </div>
          </div>

          {/* Error Alert */}
          {dashboardError && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <div className="flex items-center">
                <AlertTriangle className="w-5 h-5 text-red-500 mr-2" />
                <span className="text-red-700">
                  Dashboard Error: {dashboardError}
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Clinical Overview Metrics */}
        {dashboardMetrics && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-6 mb-8">
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold text-blue-600">
                  {dashboardMetrics.queueCount}
                </div>
                <p className="text-sm text-gray-600">Queue</p>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold text-red-600">
                  {dashboardMetrics.urgentCases}
                </div>
                <p className="text-sm text-gray-600">Urgent</p>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold text-blue-600">
                  {dashboardMetrics.scheduledToday}
                </div>
                <p className="text-sm text-gray-600">Scheduled</p>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold text-purple-600">
                  {dashboardMetrics.successRate}%
                </div>
                <p className="text-sm text-gray-600">Success Rate</p>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold text-orange-600">
                  {dashboardMetrics.activePatients}
                </div>
                <p className="text-sm text-gray-600">Active Patients</p>
              </CardContent>
            </Card>
            
            <Card>
              <CardContent className="p-4">
                <div className="text-2xl font-bold text-green-600">
                  {dashboardMetrics.satisfactionScore.toFixed(1)}
                </div>
                <p className="text-sm text-gray-600">Satisfaction</p>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Navigation Tabs */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8 overflow-x-auto">
              {dashboardViews.map((view) => {
                const Icon = view.icon;
                return (
                  <button
                    key={view.id}
                    onClick={() => setActiveView(view.id)}
                    className={`py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap ${
                      activeView === view.id
                        ? 'border-emerald-500 text-emerald-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <Icon className="w-4 h-4 inline mr-2" />
                    {view.label}
                  </button>
                );
              })}
            </nav>
          </div>
        </div>

        {/* Dashboard Content */}
        <div className="clinical-interface">
          {activeView === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
              {/* Quick Stats Overview */}
              <Card className="xl:col-span-3">
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Activity className="w-5 h-5 mr-2 text-emerald-600" />
                    Clinical Overview
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                    <div className="text-center p-4 bg-emerald-50 rounded-lg">
                      <div className="text-2xl font-bold text-emerald-600">12</div>
                      <div className="text-sm text-gray-600">Queue</div>
                    </div>
                    <div className="text-center p-4 bg-red-50 rounded-lg">
                      <div className="text-2xl font-bold text-red-600">3</div>
                      <div className="text-sm text-gray-600">Urgent</div>
                    </div>
                    <div className="text-center p-4 bg-blue-50 rounded-lg">
                      <div className="text-2xl font-bold text-blue-600">8</div>
                      <div className="text-sm text-gray-600">Scheduled</div>
                    </div>
                    <div className="text-center p-4 bg-purple-50 rounded-lg">
                      <div className="text-2xl font-bold text-purple-600">85%</div>
                      <div className="text-sm text-gray-600">Success Rate</div>
                    </div>
                    <div className="text-center p-4 bg-orange-50 rounded-lg">
                      <div className="text-2xl font-bold text-orange-600">247</div>
                      <div className="text-sm text-gray-600">Active Patients</div>
                    </div>
                    <div className="text-center p-4 bg-green-50 rounded-lg">
                      <div className="text-2xl font-bold text-green-600">4.7</div>
                      <div className="text-sm text-gray-600">Satisfaction</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Mini Component Previews */}
              <Card className="cursor-pointer hover:shadow-md transition-shadow" onClick={() => setActiveView('queue')}>
                <CardHeader>
                  <CardTitle className="flex items-center text-sm">
                    <Users className="w-4 h-4 mr-2 text-emerald-600" />
                    Patient Queue Preview
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-lg font-semibold">3 Urgent Cases</div>
                  <div className="text-sm text-gray-600">18 min avg wait time</div>
                </CardContent>
              </Card>

              <Card className="cursor-pointer hover:shadow-md transition-shadow" onClick={() => setActiveView('decision-support')}>
                <CardHeader>
                  <CardTitle className="flex items-center text-sm">
                    <Brain className="w-4 h-4 mr-2 text-purple-600" />
                    AI Decision Support
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-lg font-semibold">Ready for Analysis</div>
                  <div className="text-sm text-gray-600">Enter patient data</div>
                </CardContent>
              </Card>

              <Card className="cursor-pointer hover:shadow-md transition-shadow" onClick={() => setActiveView('outcomes')}>
                <CardHeader>
                  <CardTitle className="flex items-center text-sm">
                    <BarChart3 className="w-4 h-4 mr-2 text-blue-600" />
                    Treatment Outcomes
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-lg font-semibold">85% Success Rate</div>
                  <div className="text-sm text-gray-600">156 patients this month</div>
                </CardContent>
              </Card>

              <Card className="cursor-pointer hover:shadow-md transition-shadow" onClick={() => setActiveView('population')}>
                <CardHeader>
                  <CardTitle className="flex items-center text-sm">
                    <TrendingUp className="w-4 h-4 mr-2 text-green-600" />
                    Population Health
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-lg font-semibold">2,847 Patients</div>
                  <div className="text-sm text-gray-600">284 high-risk</div>
                </CardContent>
              </Card>

              <Card className="cursor-pointer hover:shadow-md transition-shadow" onClick={() => setActiveView('evidence')}>
                <CardHeader>
                  <CardTitle className="flex items-center text-sm">
                    <BookOpen className="w-4 h-4 mr-2 text-orange-600" />
                    Latest Evidence
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-lg font-semibold">New Guidelines</div>
                  <div className="text-sm text-gray-600">2024 Updates available</div>
                </CardContent>
              </Card>

              <Card className="cursor-pointer hover:shadow-md transition-shadow" onClick={() => setActiveView('education')}>
                <CardHeader>
                  <CardTitle className="flex items-center text-sm">
                    <GraduationCap className="w-4 h-4 mr-2 text-indigo-600" />
                    CME Progress
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-lg font-semibold">32.5 / 50 Credits</div>
                  <div className="text-sm text-gray-600">65% complete</div>
                </CardContent>
              </Card>
            </div>
          )}

          {activeView === 'queue' && <PatientQueue lastUpdated={lastUpdated} />}
          {activeView === 'decision-support' && <ClinicalDecisionSupport />}
          {activeView === 'outcomes' && <TreatmentOutcomeTracking />}
          {activeView === 'population' && <PopulationHealthAnalytics />}
          {activeView === 'evidence' && <EvidenceBasedRecommendations />}
          {activeView === 'education' && <ProfessionalContinuingEducation />}
        </div>
      </div>
    </div>
  );
};

export default ClinicalDashboard;