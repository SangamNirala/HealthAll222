import React, { useState, useEffect, useRef } from 'react';
import {
  LayoutDashboard,
  Users,
  TrendingUp,
  ChefHat,
  Activity,
  FileText,
  AlertTriangle,
  Video,
  MessageSquare,
  Calendar,
  Settings,
  Monitor,
  Bell,
  Search,
  Filter,
  RefreshCw,
  Maximize2,
  Minimize2,
  BarChart3,
  Target,
  Heart,
  Brain,
  Zap,
  Clock,
  CheckCircle,
  AlertCircle,
  Info,
  ArrowRight,
  Grid3X3,
  List,
  MoreHorizontal
} from 'lucide-react';
import SmartNavigation from '../shared/SmartNavigation';

// Import all patient management components
import SmartPatientAssignmentPanel from './SmartPatientAssignmentPanel';
import RealTimeProgressDashboard from './RealTimeProgressDashboard';
import IntelligentMealPlanGenerator from './IntelligentMealPlanGenerator';
import AdvancedAdherenceMonitor from './AdvancedAdherenceMonitor';
import AutomatedReportGenerator from './AutomatedReportGenerator';
import IntelligentAlertSystem from './IntelligentAlertSystem';
import VirtualConsultationCenter from './VirtualConsultationCenter';
import PatientEngagementHub from './PatientEngagementHub';

const EnhancedPatientManagementSystem = () => {
  // Main State Management
  const [activeComponent, setActiveComponent] = useState('dashboard');
  const [viewMode, setViewMode] = useState('grid'); // grid, list, expanded
  const [isFullScreen, setIsFullScreen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterCategory, setFilterCategory] = useState('all');
  
  // Real-time Updates
  const [realTimeData, setRealTimeData] = useState({});
  const [connectionStatus, setConnectionStatus] = useState('connected');
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [notifications, setNotifications] = useState([]);
  
  // Component States
  const [componentStates, setComponentStates] = useState({
    smartAssignment: { active: true, hasUpdates: false, alertCount: 0 },
    progressDashboard: { active: true, hasUpdates: true, alertCount: 3 },
    mealPlanning: { active: true, hasUpdates: false, alertCount: 0 },
    adherenceMonitor: { active: true, hasUpdates: true, alertCount: 2 },
    reportGenerator: { active: false, hasUpdates: false, alertCount: 0 },
    alertSystem: { active: true, hasUpdates: true, alertCount: 7 },
    virtualConsultation: { active: false, hasUpdates: false, alertCount: 1 },
    patientEngagement: { active: true, hasUpdates: true, alertCount: 4 }
  });
  
  // WebSocket for Real-time Updates
  const wsRef = useRef(null);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const refreshIntervalRef = useRef(null);

  // Component Configuration
  const components = [
    {
      id: 'smartAssignment',
      title: 'Smart Patient Assignment',
      description: 'AI-powered patient matching and load balancing',
      component: SmartPatientAssignmentPanel,
      icon: Users,
      color: 'bg-blue-500',
      category: 'management',
      path: '/smart-patient-assignments'
    },
    {
      id: 'progressDashboard',
      title: 'Real-Time Progress Dashboard',
      description: 'Live progress monitoring with predictive analytics',
      component: RealTimeProgressDashboard,
      icon: TrendingUp,
      color: 'bg-emerald-500',
      category: 'analytics',
      path: '/progress-dashboard'
    },
    {
      id: 'mealPlanning',
      title: 'Intelligent Meal Planning',
      description: 'AI recipe generation with nutritional optimization',
      component: IntelligentMealPlanGenerator,
      icon: ChefHat,
      color: 'bg-orange-500',
      category: 'nutrition',
      path: '/intelligent-meal-planning'
    },
    {
      id: 'adherenceMonitor',
      title: 'Advanced Adherence Monitor',
      description: 'Smart compliance tracking with predictive insights',
      component: AdvancedAdherenceMonitor,
      icon: Activity,
      color: 'bg-purple-500',
      category: 'monitoring',
      path: '/adherence-monitor'
    },
    {
      id: 'reportGenerator',
      title: 'Automated Report Generator',
      description: 'AI-powered report creation with PDF export',
      component: AutomatedReportGenerator,
      icon: FileText,
      color: 'bg-indigo-500',
      category: 'reporting',
      path: '/report-generator'
    },
    {
      id: 'alertSystem',
      title: 'Intelligent Alert System',
      description: 'Smart notifications with escalation workflows',
      component: IntelligentAlertSystem,
      icon: AlertTriangle,
      color: 'bg-red-500',
      category: 'monitoring',
      path: '/alert-system'
    },
    {
      id: 'virtualConsultation',
      title: 'Virtual Consultation Center',
      description: 'WebRTC video calls with screen sharing',
      component: VirtualConsultationCenter,
      icon: Video,
      color: 'bg-cyan-500',
      category: 'communication',
      path: '/virtual-consultation'
    },
    {
      id: 'patientEngagement',
      title: 'Patient Engagement Hub',
      description: 'Interactive patient portal with educational content',
      component: PatientEngagementHub,
      icon: MessageSquare,
      color: 'bg-pink-500',
      category: 'engagement',
      path: '/patient-engagement'
    }
  ];

  const categories = [
    { id: 'all', label: 'All Components', count: components.length },
    { id: 'management', label: 'Patient Management', count: components.filter(c => c.category === 'management').length },
    { id: 'analytics', label: 'Analytics & Reporting', count: components.filter(c => c.category === 'analytics' || c.category === 'reporting').length },
    { id: 'monitoring', label: 'Monitoring & Alerts', count: components.filter(c => c.category === 'monitoring').length },
    { id: 'communication', label: 'Communication', count: components.filter(c => c.category === 'communication' || c.category === 'engagement').length },
    { id: 'nutrition', label: 'Nutrition & Wellness', count: components.filter(c => c.category === 'nutrition').length }
  ];

  // ===== REAL-TIME UPDATES =====

  const initializeRealTimeUpdates = () => {
    // Initialize WebSocket connection for real-time updates
    try {
      const ws = new WebSocket(`ws://localhost:8001/ws/patient-management/system`);
      
      ws.onopen = () => {
        setConnectionStatus('connected');
        addNotification('Real-time updates connected', 'success');
      };
      
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          handleRealTimeUpdate(data);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };
      
      ws.onclose = () => {
        setConnectionStatus('disconnected');
        addNotification('Real-time updates disconnected', 'error');
      };
      
      ws.onerror = () => {
        setConnectionStatus('error');
      };
      
      wsRef.current = ws;
    } catch (error) {
      console.error('Error initializing WebSocket:', error);
      setConnectionStatus('error');
    }
  };

  const handleRealTimeUpdate = (data) => {
    const { type, componentId, payload, timestamp } = data;
    
    setRealTimeData(prev => ({
      ...prev,
      [componentId]: {
        ...prev[componentId],
        [type]: payload,
        lastUpdate: timestamp
      }
    }));
    
    // Update component states based on real-time data
    if (componentId && components.find(c => c.id === componentId)) {
      setComponentStates(prev => ({
        ...prev,
        [componentId]: {
          ...prev[componentId],
          hasUpdates: true,
          alertCount: payload.alertCount || prev[componentId].alertCount
        }
      }));
    }
    
    setLastUpdate(new Date(timestamp));
    addNotification(`${componentId}: ${type} updated`, 'info');
  };

  // ===== AUTO-REFRESH =====

  const startAutoRefresh = () => {
    if (refreshIntervalRef.current) {
      clearInterval(refreshIntervalRef.current);
    }
    
    refreshIntervalRef.current = setInterval(() => {
      refreshAllComponents();
    }, 30000); // Refresh every 30 seconds
  };

  const stopAutoRefresh = () => {
    if (refreshIntervalRef.current) {
      clearInterval(refreshIntervalRef.current);
      refreshIntervalRef.current = null;
    }
  };

  const refreshAllComponents = async () => {
    try {
      setLastUpdate(new Date());
      
      // Simulate component refresh
      const updatedStates = { ...componentStates };
      Object.keys(updatedStates).forEach(key => {
        updatedStates[key].hasUpdates = Math.random() > 0.7; // 30% chance of updates
        updatedStates[key].alertCount = Math.floor(Math.random() * 5);
      });
      
      setComponentStates(updatedStates);
      addNotification('All components refreshed', 'success');
    } catch (error) {
      console.error('Error refreshing components:', error);
      addNotification('Refresh failed', 'error');
    }
  };

  // ===== COMPONENT NAVIGATION =====

  const navigateToComponent = (component) => {
    setActiveComponent(component.id);
    window.history.pushState({}, '', component.path);
    
    // Mark component as viewed
    setComponentStates(prev => ({
      ...prev,
      [component.id]: {
        ...prev[component.id],
        hasUpdates: false
      }
    }));
  };

  const renderActiveComponent = () => {
    const component = components.find(c => c.id === activeComponent);
    if (!component) return null;
    
    const ComponentToRender = component.component;
    return (
      <div className={`${isFullScreen ? 'fixed inset-0 z-50 bg-white' : ''}`}>
        <ComponentToRender />
      </div>
    );
  };

  // ===== DASHBOARD OVERVIEW =====

  const renderDashboardOverview = () => (
    <div className="space-y-6">
      {/* System Status */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-gray-900">System Overview</h2>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${
                connectionStatus === 'connected' ? 'bg-emerald-500' : 
                connectionStatus === 'error' ? 'bg-red-500' : 'bg-yellow-500'
              }`} />
              <span className="text-sm text-gray-600 capitalize">{connectionStatus}</span>
            </div>
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-gray-500" />
              <span className="text-sm text-gray-600">
                Last update: {lastUpdate.toLocaleTimeString()}
              </span>
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          {[
            { 
              label: 'Active Components', 
              value: Object.values(componentStates).filter(s => s.active).length,
              total: components.length,
              color: 'text-emerald-600',
              icon: Grid3X3
            },
            { 
              label: 'Total Alerts', 
              value: Object.values(componentStates).reduce((acc, s) => acc + s.alertCount, 0),
              color: 'text-red-600',
              icon: AlertTriangle
            },
            { 
              label: 'Updates Available', 
              value: Object.values(componentStates).filter(s => s.hasUpdates).length,
              color: 'text-blue-600',
              icon: RefreshCw
            },
            { 
              label: 'System Health', 
              value: connectionStatus === 'connected' ? '100%' : '75%',
              color: 'text-purple-600',
              icon: Heart
            }
          ].map((stat, index) => {
            const Icon = stat.icon;
            return (
              <div key={index} className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center">
                  <div className="p-2 bg-white rounded-lg">
                    <Icon className="w-5 h-5 text-gray-600" />
                  </div>
                  <div className="ml-3">
                    <p className="text-sm text-gray-600">{stat.label}</p>
                    <p className={`text-xl font-bold ${stat.color}`}>
                      {stat.value}{stat.total ? `/${stat.total}` : ''}
                    </p>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Component Grid */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-gray-900">Component Management</h2>
          <div className="flex items-center space-x-3">
            {/* Search */}
            <div className="relative">
              <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
              <input
                type="text"
                placeholder="Search components..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-emerald-500 focus:border-emerald-500"
              />
            </div>
            
            {/* View Mode Toggle */}
            <div className="flex border border-gray-300 rounded-lg">
              <button
                onClick={() => setViewMode('grid')}
                className={`p-2 ${viewMode === 'grid' ? 'bg-emerald-100 text-emerald-700' : 'text-gray-600'}`}
              >
                <Grid3X3 className="w-4 h-4" />
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`p-2 ${viewMode === 'list' ? 'bg-emerald-100 text-emerald-700' : 'text-gray-600'}`}
              >
                <List className="w-4 h-4" />
              </button>
            </div>
            
            {/* Auto-refresh Toggle */}
            <button
              onClick={() => {
                setAutoRefresh(!autoRefresh);
                if (!autoRefresh) {
                  startAutoRefresh();
                } else {
                  stopAutoRefresh();
                }
              }}
              className={`p-2 rounded-lg ${autoRefresh ? 'bg-emerald-100 text-emerald-700' : 'text-gray-600'}`}
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap gap-2 mb-6">
          {categories.map((category) => (
            <button
              key={category.id}
              onClick={() => setFilterCategory(category.id)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filterCategory === category.id
                  ? 'bg-emerald-100 text-emerald-700 border border-emerald-200'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100 border border-gray-200'
              }`}
            >
              {category.label} ({category.count})
            </button>
          ))}
        </div>

        {/* Components Display */}
        {renderComponentsDisplay()}
      </div>
    </div>
  );

  const renderComponentsDisplay = () => {
    const filteredComponents = components.filter(component => {
      const matchesSearch = !searchTerm || 
        component.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        component.description.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesFilter = filterCategory === 'all' || component.category === filterCategory;
      return matchesSearch && matchesFilter;
    });

    if (viewMode === 'grid') {
      return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredComponents.map((component) => {
            const Icon = component.icon;
            const state = componentStates[component.id];
            
            return (
              <div
                key={component.id}
                onClick={() => navigateToComponent(component)}
                className="relative bg-gray-50 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer border-2 border-transparent hover:border-emerald-200"
              >
                {/* Status Indicators */}
                <div className="absolute top-2 right-2 flex space-x-1">
                  {state.hasUpdates && (
                    <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  )}
                  {state.alertCount > 0 && (
                    <div className="bg-red-500 text-white text-xs rounded-full px-1 min-w-[16px] h-4 flex items-center justify-center">
                      {state.alertCount}
                    </div>
                  )}
                  <div className={`w-2 h-2 rounded-full ${state.active ? 'bg-emerald-500' : 'bg-gray-400'}`}></div>
                </div>
                
                <div className="flex items-center mb-3">
                  <div className={`p-3 ${component.color} rounded-lg`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                </div>
                
                <h3 className="font-semibold text-gray-900 mb-2">{component.title}</h3>
                <p className="text-sm text-gray-600 mb-3">{component.description}</p>
                
                <div className="flex items-center justify-between">
                  <span className={`text-xs px-2 py-1 rounded ${state.active ? 'bg-emerald-100 text-emerald-800' : 'bg-gray-100 text-gray-800'}`}>
                    {state.active ? 'Active' : 'Inactive'}
                  </span>
                  <ArrowRight className="w-4 h-4 text-gray-400" />
                </div>
              </div>
            );
          })}
        </div>
      );
    } else {
      return (
        <div className="space-y-3">
          {filteredComponents.map((component) => {
            const Icon = component.icon;
            const state = componentStates[component.id];
            
            return (
              <div
                key={component.id}
                onClick={() => navigateToComponent(component)}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer transition-colors"
              >
                <div className="flex items-center">
                  <div className={`p-2 ${component.color} rounded-lg mr-4`}>
                    <Icon className="w-5 h-5 text-white" />
                  </div>
                  <div>
                    <h3 className="font-medium text-gray-900">{component.title}</h3>
                    <p className="text-sm text-gray-600">{component.description}</p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-3">
                  {state.hasUpdates && (
                    <div className="flex items-center text-blue-600 text-sm">
                      <RefreshCw className="w-3 h-3 mr-1" />
                      Updates
                    </div>
                  )}
                  {state.alertCount > 0 && (
                    <div className="flex items-center text-red-600 text-sm">
                      <AlertTriangle className="w-3 h-3 mr-1" />
                      {state.alertCount}
                    </div>
                  )}
                  <div className={`w-2 h-2 rounded-full ${state.active ? 'bg-emerald-500' : 'bg-gray-400'}`}></div>
                  <ArrowRight className="w-4 h-4 text-gray-400" />
                </div>
              </div>
            );
          })}
        </div>
      );
    }
  };

  // ===== UTILITY FUNCTIONS =====

  const addNotification = (message, type) => {
    const notification = {
      id: Date.now(),
      message,
      type,
      timestamp: new Date()
    };
    setNotifications(prev => [...prev, notification]);
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== notification.id));
    }, 5000);
  };

  const toggleFullScreen = () => {
    setIsFullScreen(!isFullScreen);
  };

  // ===== EFFECTS =====

  useEffect(() => {
    if (autoRefresh) {
      startAutoRefresh();
    } else {
      stopAutoRefresh();
    }
    
    return () => {
      stopAutoRefresh();
    };
  }, [autoRefresh]);

  useEffect(() => {
    // Initialize real-time updates (commented out as WebSocket endpoint doesn't exist yet)
    // initializeRealTimeUpdates();
    
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <SmartNavigation />
      
      <div className="container mx-auto px-4 py-6">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Enhanced Patient Management System</h1>
              <p className="text-gray-600 mt-2">Unified dashboard for comprehensive patient care management</p>
            </div>
            
            {/* Header Controls */}
            <div className="flex items-center space-x-4">
              {activeComponent !== 'dashboard' && (
                <button
                  onClick={() => setActiveComponent('dashboard')}
                  className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 flex items-center space-x-2"
                >
                  <LayoutDashboard className="w-4 h-4" />
                  <span>Dashboard</span>
                </button>
              )}
              
              {activeComponent !== 'dashboard' && (
                <button
                  onClick={toggleFullScreen}
                  className="bg-gray-100 text-gray-700 p-2 rounded-lg hover:bg-gray-200"
                >
                  {isFullScreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
                </button>
              )}
              
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full ${
                  connectionStatus === 'connected' ? 'bg-emerald-500' : 
                  connectionStatus === 'error' ? 'bg-red-500' : 'bg-yellow-500'
                }`} />
                <span className="text-sm text-gray-600">
                  {Object.values(componentStates).filter(s => s.active).length}/{components.length} Active
                </span>
              </div>
            </div>
          </div>
          
          {/* Breadcrumb Navigation */}
          {activeComponent !== 'dashboard' && (
            <div className="flex items-center space-x-2 mt-4 text-sm text-gray-600">
              <button 
                onClick={() => setActiveComponent('dashboard')}
                className="hover:text-emerald-600"
              >
                Dashboard
              </button>
              <ArrowRight className="w-3 h-3" />
              <span className="text-gray-900">
                {components.find(c => c.id === activeComponent)?.title || 'Component'}
              </span>
            </div>
          )}
        </div>

        {/* Notifications */}
        {notifications.length > 0 && (
          <div className="fixed top-4 right-4 z-50 space-y-2">
            {notifications.map((notification) => (
              <div
                key={notification.id}
                className={`p-4 rounded-lg shadow-lg border max-w-sm ${
                  notification.type === 'success' ? 'bg-emerald-50 border-emerald-200 text-emerald-800' :
                  notification.type === 'error' ? 'bg-red-50 border-red-200 text-red-800' :
                  'bg-blue-50 border-blue-200 text-blue-800'
                }`}
              >
                <div className="flex items-center">
                  {notification.type === 'success' && <CheckCircle className="w-5 h-5 mr-3" />}
                  {notification.type === 'error' && <AlertCircle className="w-5 h-5 mr-3" />}
                  {notification.type === 'info' && <Info className="w-5 h-5 mr-3" />}
                  <p className="text-sm font-medium">{notification.message}</p>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Main Content Area */}
        {activeComponent === 'dashboard' ? renderDashboardOverview() : renderActiveComponent()}
      </div>
    </div>
  );
};

export default EnhancedPatientManagementSystem;