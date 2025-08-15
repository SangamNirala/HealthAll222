import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Input } from '../ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Progress } from '../ui/progress';
import { 
  AlertTriangle, 
  Bell, 
  BellRing, 
  Clock, 
  Mail,
  Phone,
  MessageSquare,
  Settings,
  Filter,
  Search,
  CheckCircle,
  XCircle,
  Pause,
  Play,
  Users,
  Brain,
  TrendingUp,
  Eye,
  EyeOff,
  Loader2,
  Shield,
  Zap,
  Activity,
  Heart,
  Calendar,
  BarChart3
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts';
import SmartNavigation from '../shared/SmartNavigation';

const IntelligentAlertSystem = () => {
  const [alerts, setAlerts] = useState([]);
  const [alertRules, setAlertRules] = useState([]);
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Filters and search
  const [searchTerm, setSearchTerm] = useState('');
  const [severityFilter, setSeverityFilter] = useState('ALL');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [showRead, setShowRead] = useState(true);
  
  // Alert rule creation
  const [newRuleConfig, setNewRuleConfig] = useState({
    name: '',
    condition_type: 'threshold',
    threshold_value: 0,
    comparison: 'less_than',
    severity: 'MEDIUM',
    notification_methods: ['in_app'],
    escalation_time: 60
  });

  const providerId = 'provider-123';
  const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;

  // Fetch provider alerts
  const fetchAlerts = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/provider/patient-management/alerts/${providerId}`);
      if (response.ok) {
        const data = await response.json();
        setAlerts(data.alerts || []);
      } else {
        throw new Error('Failed to fetch alerts');
      }
    } catch (err) {
      setError(`Error fetching alerts: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Create new alert rule
  const createAlertRule = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/provider/patient-management/alert-rules`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          provider_id: providerId,
          rule_config: newRuleConfig,
          active: true
        })
      });
      
      if (response.ok) {
        await fetchAlerts();
        setNewRuleConfig({
          name: '',
          condition_type: 'threshold',
          threshold_value: 0,
          comparison: 'less_than',
          severity: 'MEDIUM',
          notification_methods: ['in_app'],
          escalation_time: 60
        });
      } else {
        throw new Error('Failed to create alert rule');
      }
    } catch (err) {
      setError(`Error creating rule: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Acknowledge alert
  const acknowledgeAlert = async (alertId, notes = '') => {
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/provider/patient-management/alerts/${alertId}/acknowledge`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          provider_id: providerId,
          notes: notes,
          acknowledged_at: new Date().toISOString()
        })
      });
      
      if (response.ok) {
        await fetchAlerts();
      } else {
        throw new Error('Failed to acknowledge alert');
      }
    } catch (err) {
      setError(`Error acknowledging alert: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Send browser notification
  const sendBrowserNotification = (alert) => {
    if ('Notification' in window) {
      if (Notification.permission === 'granted') {
        new Notification(`Alert: ${alert.title}`, {
          body: alert.message,
          icon: '/favicon.ico'
        });
      } else if (Notification.permission !== 'denied') {
        Notification.requestPermission().then(permission => {
          if (permission === 'granted') {
            new Notification(`Alert: ${alert.title}`, {
              body: alert.message,
              icon: '/favicon.ico'
            });
          }
        });
      }
    }
  };

  useEffect(() => {
    fetchAlerts();
    
    // Request notification permission on load
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }, []);

  // Sample alert data for demo
  const sampleAlerts = [
    {
      id: 'alert_001',
      title: 'Critical Medication Non-Adherence',
      message: 'Patient John Doe has missed 3 consecutive medication doses',
      severity: 'CRITICAL',
      urgency_score: 0.9,
      confidence: 0.85,
      patient_id: 'patient-456',
      patient_name: 'John Doe',
      created_at: '2024-01-29T10:30:00Z',
      status: 'active',
      acknowledged: false,
      notification_methods: ['in_app', 'email'],
      escalation_level: 0,
      category: 'adherence'
    },
    {
      id: 'alert_002',
      title: 'Abnormal Vital Signs Detected',
      message: 'Blood pressure reading of 180/110 detected for Jane Smith',
      severity: 'HIGH',
      urgency_score: 0.75,
      confidence: 0.92,
      patient_id: 'patient-789',
      patient_name: 'Jane Smith',
      created_at: '2024-01-29T09:15:00Z',
      status: 'active',
      acknowledged: false,
      notification_methods: ['in_app', 'email', 'browser'],
      escalation_level: 1,
      category: 'vital_signs'
    },
    {
      id: 'alert_003',
      title: 'Appointment No-Show Risk',
      message: 'Bob Johnson has a high probability of missing upcoming appointment',
      severity: 'MEDIUM',
      urgency_score: 0.45,
      confidence: 0.68,
      patient_id: 'patient-012',
      patient_name: 'Bob Johnson',
      created_at: '2024-01-29T08:00:00Z',
      status: 'active',
      acknowledged: true,
      notification_methods: ['in_app'],
      escalation_level: 0,
      category: 'appointments'
    }
  ];

  const displayAlerts = alerts.length > 0 ? alerts : sampleAlerts;

  // Filter alerts
  const filteredAlerts = displayAlerts.filter(alert => {
    const matchesSearch = alert.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         alert.patient_name?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSeverity = severityFilter === 'ALL' || alert.severity === severityFilter;
    const matchesStatus = statusFilter === 'ALL' || alert.status === statusFilter;
    const matchesRead = showRead || !alert.acknowledged;
    
    return matchesSearch && matchesSeverity && matchesStatus && matchesRead;
  });

  // Sort alerts by urgency and date
  const sortedAlerts = filteredAlerts.sort((a, b) => {
    if (a.urgency_score !== b.urgency_score) {
      return b.urgency_score - a.urgency_score;
    }
    return new Date(b.created_at) - new Date(a.created_at);
  });

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'CRITICAL': return 'bg-red-100 text-red-800 border-red-200';
      case 'HIGH': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'MEDIUM': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'LOW': return 'bg-blue-100 text-blue-800 border-blue-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'CRITICAL': return <AlertTriangle className="h-4 w-4 text-red-600" />;
      case 'HIGH': return <AlertTriangle className="h-4 w-4 text-orange-600" />;
      case 'MEDIUM': return <Bell className="h-4 w-4 text-yellow-600" />;
      case 'LOW': return <Bell className="h-4 w-4 text-blue-600" />;
      default: return <Bell className="h-4 w-4 text-gray-600" />;
    }
  };

  // Alert analytics data
  const alertAnalytics = {
    total_alerts: displayAlerts.length,
    unacknowledged: displayAlerts.filter(a => !a.acknowledged).length,
    by_severity: {
      CRITICAL: displayAlerts.filter(a => a.severity === 'CRITICAL').length,
      HIGH: displayAlerts.filter(a => a.severity === 'HIGH').length,
      MEDIUM: displayAlerts.filter(a => a.severity === 'MEDIUM').length,
      LOW: displayAlerts.filter(a => a.severity === 'LOW').length
    },
    trend_data: [
      { date: '2024-01-25', alerts: 8, critical: 1, high: 3, medium: 4, low: 0 },
      { date: '2024-01-26', alerts: 12, critical: 2, high: 4, medium: 5, low: 1 },
      { date: '2024-01-27', alerts: 6, critical: 0, high: 2, medium: 3, low: 1 },
      { date: '2024-01-28', alerts: 15, critical: 3, high: 5, medium: 6, low: 1 },
      { date: '2024-01-29', alerts: 9, critical: 1, high: 3, medium: 4, low: 1 }
    ]
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
        <SmartNavigation />
        <div className="container mx-auto px-4 py-8">
          <Card className="max-w-md mx-auto">
            <CardContent className="p-6 text-center">
              <AlertTriangle className="mx-auto mb-4 h-12 w-12 text-red-500" />
              <p className="text-red-600">{error}</p>
              <Button onClick={() => window.location.reload()} className="mt-4">
                Try Again
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
      <SmartNavigation />
      
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-4">
            <BellRing className="h-8 w-8 text-emerald-600" />
            <h1 className="text-3xl font-bold text-gray-900">Intelligent Alert System</h1>
          </div>
          <p className="text-gray-600 text-lg">
            Advanced notification management with smart prioritization and multi-channel alerts
          </p>
        </div>

        <Tabs defaultValue="dashboard" className="space-y-6">
          <TabsList className="grid w-full grid-cols-5 bg-white">
            <TabsTrigger value="dashboard">Alert Dashboard</TabsTrigger>
            <TabsTrigger value="active">Active Alerts</TabsTrigger>
            <TabsTrigger value="rules">Alert Rules</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
          </TabsList>

          {/* Alert Dashboard */}
          <TabsContent value="dashboard" className="space-y-6">
            {/* Key Metrics */}
            <div className="grid gap-6 md:grid-cols-4">
              <Card>
                <CardHeader className="pb-4">
                  <CardTitle className="text-sm font-medium flex items-center gap-2">
                    <Bell className="h-4 w-4" />
                    Total Alerts
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-gray-900">
                    {alertAnalytics.total_alerts}
                  </div>
                  <p className="text-sm text-gray-600">Last 24 hours</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-4">
                  <CardTitle className="text-sm font-medium flex items-center gap-2">
                    <AlertTriangle className="h-4 w-4 text-red-600" />
                    Unacknowledged
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-red-600">
                    {alertAnalytics.unacknowledged}
                  </div>
                  <p className="text-sm text-gray-600">Needs attention</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-4">
                  <CardTitle className="text-sm font-medium flex items-center gap-2">
                    <Activity className="h-4 w-4 text-orange-600" />
                    Critical & High
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-orange-600">
                    {alertAnalytics.by_severity.CRITICAL + alertAnalytics.by_severity.HIGH}
                  </div>
                  <p className="text-sm text-gray-600">Priority alerts</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-4">
                  <CardTitle className="text-sm font-medium flex items-center gap-2">
                    <TrendingUp className="h-4 w-4 text-emerald-600" />
                    Response Time
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-emerald-600">
                    4.2m
                  </div>
                  <p className="text-sm text-gray-600">Avg response</p>
                </CardContent>
              </Card>
            </div>

            {/* Alert Severity Breakdown */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5" />
                  Alert Severity Distribution
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid gap-6 md:grid-cols-2">
                  <div className="space-y-4">
                    {Object.entries(alertAnalytics.by_severity).map(([severity, count]) => (
                      <div key={severity} className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          {getSeverityIcon(severity)}
                          <span className="font-medium">{severity}</span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="font-semibold">{count}</span>
                          <div className="w-20 bg-gray-200 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full ${
                                severity === 'CRITICAL' ? 'bg-red-500' :
                                severity === 'HIGH' ? 'bg-orange-500' :
                                severity === 'MEDIUM' ? 'bg-yellow-500' : 'bg-blue-500'
                              }`}
                              style={{ width: `${(count / alertAnalytics.total_alerts) * 100}%` }}
                            />
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  <div className="flex items-center justify-center">
                    <ResponsiveContainer width="100%" height={200}>
                      <PieChart>
                        <Pie
                          data={Object.entries(alertAnalytics.by_severity).map(([severity, count]) => ({
                            name: severity,
                            value: count,
                            color: severity === 'CRITICAL' ? '#EF4444' : 
                                  severity === 'HIGH' ? '#F97316' : 
                                  severity === 'MEDIUM' ? '#EAB308' : '#3B82F6'
                          }))}
                          cx="50%"
                          cy="50%"
                          outerRadius={80}
                          dataKey="value"
                          label={({name, value}) => value > 0 ? `${name}: ${value}` : ''}
                        >
                          {Object.entries(alertAnalytics.by_severity).map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={
                              entry[0] === 'CRITICAL' ? '#EF4444' : 
                              entry[0] === 'HIGH' ? '#F97316' : 
                              entry[0] === 'MEDIUM' ? '#EAB308' : '#3B82F6'
                            } />
                          ))}
                        </Pie>
                        <Tooltip />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Recent High Priority Alerts */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5" />
                  High Priority Alerts
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {sortedAlerts.filter(a => ['CRITICAL', 'HIGH'].includes(a.severity)).slice(0, 5).map((alert) => (
                    <div key={alert.id} className="flex items-start justify-between p-3 border border-gray-200 rounded-lg">
                      <div className="flex items-start gap-3">
                        {getSeverityIcon(alert.severity)}
                        <div className="flex-1">
                          <h4 className="font-semibold text-sm">{alert.title}</h4>
                          <p className="text-sm text-gray-600">{alert.message}</p>
                          <div className="flex items-center gap-2 mt-1">
                            <span className="text-xs text-gray-500">{alert.patient_name}</span>
                            <span className="text-xs text-gray-500">•</span>
                            <span className="text-xs text-gray-500">
                              {new Date(alert.created_at).toLocaleTimeString()}
                            </span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        <Badge className={getSeverityColor(alert.severity)}>
                          {alert.severity}
                        </Badge>
                        {!alert.acknowledged && (
                          <Button 
                            size="sm" 
                            onClick={() => acknowledgeAlert(alert.id)}
                            className="bg-emerald-600 hover:bg-emerald-700"
                          >
                            <CheckCircle className="h-3 w-3" />
                          </Button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Active Alerts Tab */}
          <TabsContent value="active" className="space-y-6">
            {/* Filters */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Filter className="h-5 w-5" />
                  Alert Filters
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                    <Input
                      placeholder="Search alerts..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                  
                  <Select value={severityFilter} onValueChange={setSeverityFilter}>
                    <SelectTrigger>
                      <SelectValue placeholder="Severity" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="ALL">All Severities</SelectItem>
                      <SelectItem value="CRITICAL">Critical</SelectItem>
                      <SelectItem value="HIGH">High</SelectItem>
                      <SelectItem value="MEDIUM">Medium</SelectItem>
                      <SelectItem value="LOW">Low</SelectItem>
                    </SelectContent>
                  </Select>
                  
                  <Select value={statusFilter} onValueChange={setStatusFilter}>
                    <SelectTrigger>
                      <SelectValue placeholder="Status" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="ALL">All Statuses</SelectItem>
                      <SelectItem value="active">Active</SelectItem>
                      <SelectItem value="snoozed">Snoozed</SelectItem>
                      <SelectItem value="resolved">Resolved</SelectItem>
                    </SelectContent>
                  </Select>
                  
                  <Button 
                    variant={showRead ? "default" : "outline"}
                    onClick={() => setShowRead(!showRead)}
                    className="flex items-center gap-2"
                  >
                    {showRead ? <Eye className="h-4 w-4" /> : <EyeOff className="h-4 w-4" />}
                    {showRead ? 'Show All' : 'Hide Read'}
                  </Button>
                  
                  <Button 
                    onClick={fetchAlerts} 
                    disabled={loading}
                    className="bg-emerald-600 hover:bg-emerald-700"
                  >
                    {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Refresh'}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Alert List */}
            <div className="space-y-3">
              {loading && sortedAlerts.length === 0 ? (
                <Card>
                  <CardContent className="p-6 text-center">
                    <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-emerald-600" />
                    <p className="text-gray-600">Loading alerts...</p>
                  </CardContent>
                </Card>
              ) : sortedAlerts.length === 0 ? (
                <Card>
                  <CardContent className="p-6 text-center">
                    <Bell className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                    <p className="text-gray-600">No alerts found</p>
                  </CardContent>
                </Card>
              ) : (
                sortedAlerts.map((alert) => (
                  <Card key={alert.id} className={`${alert.acknowledged ? 'bg-gray-50' : 'bg-white'} ${
                    alert.severity === 'CRITICAL' ? 'border-red-300' : 
                    alert.severity === 'HIGH' ? 'border-orange-300' : 'border-gray-200'
                  }`}>
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between">
                        <div className="flex items-start gap-3 flex-1">
                          {getSeverityIcon(alert.severity)}
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <h4 className="font-semibold">{alert.title}</h4>
                              {alert.acknowledged && <CheckCircle className="h-4 w-4 text-green-600" />}
                            </div>
                            <p className="text-gray-600 mb-2">{alert.message}</p>
                            
                            <div className="flex items-center gap-4 text-sm text-gray-500">
                              <span>Patient: {alert.patient_name}</span>
                              <span>•</span>
                              <span>{new Date(alert.created_at).toLocaleString()}</span>
                              <span>•</span>
                              <span>Confidence: {(alert.confidence * 100).toFixed(0)}%</span>
                            </div>
                            
                            <div className="flex items-center gap-2 mt-2">
                              {alert.notification_methods.map(method => (
                                <Badge key={method} variant="outline" className="text-xs">
                                  {method === 'in_app' ? <Bell className="h-3 w-3 mr-1" /> :
                                   method === 'email' ? <Mail className="h-3 w-3 mr-1" /> :
                                   method === 'browser' ? <MessageSquare className="h-3 w-3 mr-1" /> : null}
                                  {method.replace('_', ' ')}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        </div>
                        
                        <div className="flex items-start gap-2 ml-4">
                          <Badge className={getSeverityColor(alert.severity)}>
                            {alert.severity}
                          </Badge>
                          <div className="text-right">
                            <div className="text-sm font-semibold text-emerald-600 mb-1">
                              {(alert.urgency_score * 100).toFixed(0)}%
                            </div>
                            <Progress value={alert.urgency_score * 100} className="h-2 w-16" />
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex gap-2 mt-4">
                        {!alert.acknowledged && (
                          <Button 
                            size="sm" 
                            onClick={() => acknowledgeAlert(alert.id, 'Reviewed and acknowledged')}
                            className="bg-emerald-600 hover:bg-emerald-700"
                          >
                            <CheckCircle className="h-4 w-4 mr-1" />
                            Acknowledge
                          </Button>
                        )}
                        
                        <Button 
                          size="sm" 
                          variant="outline"
                          onClick={() => sendBrowserNotification(alert)}
                        >
                          <BellRing className="h-4 w-4 mr-1" />
                          Notify
                        </Button>
                        
                        <Button 
                          size="sm" 
                          variant="outline"
                        >
                          <Pause className="h-4 w-4 mr-1" />
                          Snooze
                        </Button>
                        
                        <Button 
                          size="sm" 
                          variant="outline"
                          onClick={() => setSelectedAlert(alert)}
                        >
                          <Eye className="h-4 w-4 mr-1" />
                          Details
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </div>
          </TabsContent>

          {/* Alert Rules Tab */}
          <TabsContent value="rules" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="h-5 w-5" />
                  Create New Alert Rule
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid gap-4 md:grid-cols-2">
                  <div>
                    <label className="text-sm font-medium">Rule Name</label>
                    <Input
                      value={newRuleConfig.name}
                      onChange={(e) => setNewRuleConfig(prev => ({ ...prev, name: e.target.value }))}
                      placeholder="Enter rule name"
                    />
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium">Condition Type</label>
                    <Select 
                      value={newRuleConfig.condition_type} 
                      onValueChange={(value) => setNewRuleConfig(prev => ({ ...prev, condition_type: value }))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="threshold">Threshold-based</SelectItem>
                        <SelectItem value="pattern">Pattern-based</SelectItem>
                        <SelectItem value="time">Time-based</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium">Threshold Value</label>
                    <Input
                      type="number"
                      value={newRuleConfig.threshold_value}
                      onChange={(e) => setNewRuleConfig(prev => ({ ...prev, threshold_value: parseFloat(e.target.value) }))}
                      placeholder="Enter threshold"
                    />
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium">Severity Level</label>
                    <Select 
                      value={newRuleConfig.severity} 
                      onValueChange={(value) => setNewRuleConfig(prev => ({ ...prev, severity: value }))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="LOW">Low</SelectItem>
                        <SelectItem value="MEDIUM">Medium</SelectItem>
                        <SelectItem value="HIGH">High</SelectItem>
                        <SelectItem value="CRITICAL">Critical</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                
                <div>
                  <label className="text-sm font-medium">Notification Methods</label>
                  <div className="flex gap-2 mt-2">
                    {['in_app', 'email', 'browser'].map(method => (
                      <label key={method} className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          checked={newRuleConfig.notification_methods.includes(method)}
                          onChange={(e) => {
                            if (e.target.checked) {
                              setNewRuleConfig(prev => ({
                                ...prev,
                                notification_methods: [...prev.notification_methods, method]
                              }));
                            } else {
                              setNewRuleConfig(prev => ({
                                ...prev,
                                notification_methods: prev.notification_methods.filter(m => m !== method)
                              }));
                            }
                          }}
                        />
                        <span className="text-sm capitalize">{method.replace('_', ' ')}</span>
                      </label>
                    ))}
                  </div>
                </div>
                
                <Button 
                  onClick={createAlertRule}
                  disabled={!newRuleConfig.name || loading}
                  className="bg-emerald-600 hover:bg-emerald-700"
                >
                  {loading ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin mr-2" />
                      Creating...
                    </>
                  ) : (
                    <>
                      <Zap className="h-4 w-4 mr-2" />
                      Create Rule
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Analytics Tab */}
          <TabsContent value="analytics" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Alert Trends & Analytics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={alertAnalytics.trend_data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="alerts" stroke="#10B981" strokeWidth={3} name="Total Alerts" />
                    <Line type="monotone" dataKey="critical" stroke="#EF4444" strokeWidth={2} name="Critical" />
                    <Line type="monotone" dataKey="high" stroke="#F97316" strokeWidth={2} name="High" />
                    <Line type="monotone" dataKey="medium" stroke="#EAB308" strokeWidth={2} name="Medium" />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Settings Tab */}
          <TabsContent value="settings" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="h-5 w-5" />
                  Notification Settings
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <h4 className="font-medium mb-4">Notification Preferences</h4>
                  <div className="space-y-2">
                    <label className="flex items-center space-x-2">
                      <input type="checkbox" defaultChecked />
                      <span className="text-sm">Enable browser notifications</span>
                    </label>
                    <label className="flex items-center space-x-2">
                      <input type="checkbox" defaultChecked />
                      <span className="text-sm">Enable email notifications</span>
                    </label>
                    <label className="flex items-center space-x-2">
                      <input type="checkbox" />
                      <span className="text-sm">Enable mobile push notifications</span>
                    </label>
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium mb-4">Alert Thresholds</h4>
                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <label className="text-sm font-medium">Critical Alert Threshold</label>
                      <Input type="number" defaultValue="0.8" min="0" max="1" step="0.1" />
                    </div>
                    <div>
                      <label className="text-sm font-medium">High Alert Threshold</label>
                      <Input type="number" defaultValue="0.6" min="0" max="1" step="0.1" />
                    </div>
                  </div>
                </div>
                
                <Button className="bg-emerald-600 hover:bg-emerald-700">
                  Save Settings
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default IntelligentAlertSystem;