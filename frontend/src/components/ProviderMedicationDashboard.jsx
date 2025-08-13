import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  AlertTriangle, 
  Activity, 
  TrendingUp, 
  Users, 
  MessageSquare, 
  Shield,
  Clock,
  AlertCircle,
  CheckCircle,
  XCircle,
  Mail,
  Phone,
  Search,
  Filter,
  Download,
  Eye,
  Send
} from 'lucide-react';

const ProviderMedicationDashboard = ({ providerId = "provider_001" }) => {
  const [dashboardData, setDashboardData] = useState(null);
  const [adherenceReport, setAdherenceReport] = useState(null);
  const [sideEffectsReport, setSideEffectsReport] = useState(null);
  const [providerInbox, setProviderInbox] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [drugSearchQuery, setDrugSearchQuery] = useState('');
  const [drugSafetyInfo, setDrugSafetyInfo] = useState(null);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  useEffect(() => {
    loadDashboardData();
  }, [providerId]);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      const [dashboardRes, adherenceRes, sideEffectsRes, inboxRes] = await Promise.all([
        fetch(`${backendUrl}/api/provider/dashboard/overview/${providerId}`),
        fetch(`${backendUrl}/api/provider/medications/adherence-report/${providerId}`),
        fetch(`${backendUrl}/api/provider/medications/side-effects/${providerId}`),
        fetch(`${backendUrl}/api/provider/communications/inbox/${providerId}`)
      ]);

      const [dashboard, adherence, sideEffects, inbox] = await Promise.all([
        dashboardRes.json(),
        adherenceRes.json(),
        sideEffectsRes.json(),
        inboxRes.json()
      ]);

      setDashboardData(dashboard);
      setAdherenceReport(adherence);
      setSideEffectsReport(sideEffects);
      setProviderInbox(inbox);

    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const searchDrugSafety = async () => {
    if (!drugSearchQuery.trim()) return;
    
    try {
      const response = await fetch(`${backendUrl}/api/provider/medications/drug-safety/${encodeURIComponent(drugSearchQuery)}`);
      const data = await response.json();
      setDrugSafetyInfo(data);
    } catch (error) {
      console.error('Error searching drug safety:', error);
    }
  };

  const sendMessage = async (patientId, patientEmail, subject, message, messageType = 'general') => {
    try {
      const response = await fetch(`${backendUrl}/api/provider/communications/send-message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          provider_id: providerId,
          patient_id: patientId,
          patient_email: patientEmail,
          subject: subject,
          message: message,
          message_type: messageType
        })
      });

      const result = await response.json();
      if (result.success) {
        alert('Message sent successfully!');
        loadDashboardData(); // Refresh data
      } else {
        alert('Failed to send message: ' + result.error);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Error sending message');
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'severe': return 'bg-red-100 text-red-800 border-red-200';
      case 'moderate': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'mild': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getAdherenceColor = (percentage) => {
    if (percentage >= 90) return 'text-green-600';
    if (percentage >= 80) return 'text-yellow-600';
    if (percentage >= 70) return 'text-orange-600';
    return 'text-red-600';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Provider Medication Dashboard</h1>
          <p className="text-gray-600">Comprehensive medication management and patient monitoring</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={loadDashboardData}>
            <Activity className="w-4 h-4 mr-2" />
            Refresh
          </Button>
          <Button variant="outline">
            <Download className="w-4 h-4 mr-2" />
            Export Report
          </Button>
        </div>
      </div>

      {/* Summary Cards */}
      {dashboardData && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <Users className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Patients</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {dashboardData.summary_stats?.total_patients || 0}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <TrendingUp className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Avg Adherence</p>
                  <p className={`text-2xl font-bold ${getAdherenceColor(dashboardData.summary_stats?.average_adherence || 0)}`}>
                    {dashboardData.summary_stats?.average_adherence?.toFixed(1) || 0}%
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <AlertTriangle className="h-8 w-8 text-red-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Low Adherence</p>
                  <p className="text-2xl font-bold text-red-600">
                    {dashboardData.summary_stats?.patients_low_adherence || 0}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <AlertCircle className="h-8 w-8 text-orange-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Pending Reviews</p>
                  <p className="text-2xl font-bold text-orange-600">
                    {dashboardData.summary_stats?.pending_side_effect_reviews || 0}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Main Content Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="adherence">Adherence</TabsTrigger>
          <TabsTrigger value="side-effects">Side Effects</TabsTrigger>
          <TabsTrigger value="drug-safety">Drug Safety</TabsTrigger>
          <TabsTrigger value="communications">Messages</TabsTrigger>
          <TabsTrigger value="emergency">Emergency</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Critical Alerts */}
          {dashboardData?.alerts && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <AlertTriangle className="w-5 h-5 mr-2 text-red-600" />
                  Critical Alerts
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {dashboardData.alerts.critical_adherence?.map((alert, index) => (
                  <Alert key={index} className="border-red-200 bg-red-50">
                    <AlertTriangle className="h-4 w-4" />
                    <AlertDescription>
                      <strong>{alert.patient}:</strong> {alert.message}
                      <div className="mt-2">
                        <Badge variant="destructive">{alert.type}</Badge>
                        <span className="ml-2 text-sm text-gray-600">{alert.action}</span>
                      </div>
                    </AlertDescription>
                  </Alert>
                ))}

                {dashboardData.alerts.side_effect_alerts?.map((alert, index) => (
                  <Alert key={index} className="border-orange-200 bg-orange-50">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>
                      <strong>Side Effect:</strong> {alert.patient_name} - {alert.medication_name}
                      <div className="mt-2">
                        <Badge className={getSeverityColor(alert.severity)}>{alert.severity}</Badge>
                        <span className="ml-2 text-sm text-gray-600">{alert.side_effect}</span>
                      </div>
                    </AlertDescription>
                  </Alert>
                ))}

                {(!dashboardData.alerts.critical_adherence?.length && !dashboardData.alerts.side_effect_alerts?.length) && (
                  <div className="text-center text-gray-500 py-8">
                    <CheckCircle className="w-12 h-12 mx-auto mb-4 text-green-500" />
                    <p>No critical alerts at this time</p>
                  </div>
                )}
              </CardContent>
            </Card>
          )}

          {/* Recent Activities */}
          <Card>
            <CardHeader>
              <CardTitle>Recent Activities</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {dashboardData?.recent_activities?.map((activity, index) => (
                  <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex items-center">
                      <Activity className="w-5 h-5 mr-3 text-blue-600" />
                      <div>
                        <p className="font-medium">{activity.patient}</p>
                        <p className="text-sm text-gray-600">
                          {activity.type === 'side_effect_report' && `Reported ${activity.severity} side effect with ${activity.medication}`}
                          {activity.type === 'adherence_improvement' && `Adherence improved: ${activity.improvement}`}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <Badge variant={activity.status === 'positive' ? 'default' : 'secondary'}>
                        {activity.status}
                      </Badge>
                      <p className="text-xs text-gray-500 mt-1">
                        {new Date(activity.timestamp).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Adherence Tab */}
        <TabsContent value="adherence">
          {adherenceReport && (
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Medication Adherence Report</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {adherenceReport.patient_details?.map((patient, index) => (
                      <div key={index} className="border rounded-lg p-4">
                        <div className="flex justify-between items-start mb-3">
                          <div>
                            <h3 className="font-semibold">{patient.patient_name}</h3>
                            <p className="text-sm text-gray-600">{patient.medication_count} medications</p>
                          </div>
                          <div className="text-right">
                            <p className={`text-lg font-bold ${getAdherenceColor(patient.adherence_percentage)}`}>
                              {patient.adherence_percentage?.toFixed(1)}%
                            </p>
                            <p className="text-sm text-gray-600">
                              {patient.missed_doses_week} missed this week
                            </p>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          {patient.medications?.map((med, medIndex) => (
                            <div key={medIndex} className="bg-gray-50 p-3 rounded">
                              <div className="flex justify-between items-center">
                                <span className="font-medium">{med.name}</span>
                                <span className={`font-semibold ${getAdherenceColor(med.adherence)}`}>
                                  {med.adherence?.toFixed(1)}%
                                </span>
                              </div>
                              <p className="text-sm text-gray-600">
                                Last taken: {new Date(med.last_taken).toLocaleString()}
                              </p>
                              {med.doses_missed_week > 0 && (
                                <p className="text-sm text-red-600">
                                  {med.doses_missed_week} doses missed this week
                                </p>
                              )}
                            </div>
                          ))}
                        </div>
                        
                        <div className="mt-3 flex gap-2">
                          <Button size="sm" variant="outline" onClick={() => setSelectedPatient(patient)}>
                            <Eye className="w-4 h-4 mr-1" />
                            View Details
                          </Button>
                          <Button size="sm" variant="outline">
                            <MessageSquare className="w-4 h-4 mr-1" />
                            Contact Patient
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Recommendations */}
              <Card>
                <CardHeader>
                  <CardTitle>Adherence Recommendations</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {adherenceReport.recommendations?.map((rec, index) => (
                      <li key={index} className="flex items-start">
                        <CheckCircle className="w-5 h-5 mr-2 text-green-600 mt-0.5" />
                        <span>{rec}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </div>
          )}
        </TabsContent>

        {/* Side Effects Tab */}
        <TabsContent value="side-effects">
          {sideEffectsReport && (
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Side Effects Monitoring</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div className="text-center p-4 bg-red-50 rounded-lg">
                      <p className="text-2xl font-bold text-red-600">
                        {sideEffectsReport.severity_breakdown?.severe || 0}
                      </p>
                      <p className="text-sm text-gray-600">Severe Reactions</p>
                    </div>
                    <div className="text-center p-4 bg-yellow-50 rounded-lg">
                      <p className="text-2xl font-bold text-yellow-600">
                        {sideEffectsReport.severity_breakdown?.moderate || 0}
                      </p>
                      <p className="text-sm text-gray-600">Moderate Reactions</p>
                    </div>
                    <div className="text-center p-4 bg-green-50 rounded-lg">
                      <p className="text-2xl font-bold text-green-600">
                        {sideEffectsReport.severity_breakdown?.mild || 0}
                      </p>
                      <p className="text-sm text-gray-600">Mild Reactions</p>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <h3 className="font-semibold text-lg">Recent Reports</h3>
                    {sideEffectsReport.recent_reports?.map((report, index) => (
                      <div key={index} className="border rounded-lg p-4">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                              <h4 className="font-medium">{report.patient_name}</h4>
                              <Badge className={getSeverityColor(report.severity)}>
                                {report.severity}
                              </Badge>
                              {!report.provider_reviewed && (
                                <Badge variant="outline" className="text-orange-600 border-orange-600">
                                  Needs Review
                                </Badge>
                              )}
                            </div>
                            <p className="text-sm text-gray-600 mb-1">
                              <strong>Medication:</strong> {report.medication_name}
                            </p>
                            <p className="text-sm text-gray-700 mb-2">
                              <strong>Side Effect:</strong> {report.side_effect}
                            </p>
                            {report.provider_response && (
                              <div className="bg-blue-50 p-2 rounded text-sm">
                                <strong>Your Response:</strong> {report.provider_response}
                              </div>
                            )}
                          </div>
                          <div className="text-right text-sm text-gray-500">
                            {new Date(report.reported_date).toLocaleDateString()}
                          </div>
                        </div>
                        
                        {!report.provider_reviewed && (
                          <div className="mt-3 flex gap-2">
                            <Button size="sm" variant="outline">
                              Review & Respond
                            </Button>
                            <Button size="sm" variant="outline">
                              Contact Patient
                            </Button>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </TabsContent>

        {/* Drug Safety Tab */}
        <TabsContent value="drug-safety">
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Shield className="w-5 h-5 mr-2" />
                  Drug Safety Information (OpenFDA)
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex gap-2 mb-4">
                  <Input
                    placeholder="Enter drug name (e.g., Metformin, Lisinopril)"
                    value={drugSearchQuery}
                    onChange={(e) => setDrugSearchQuery(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && searchDrugSafety()}
                  />
                  <Button onClick={searchDrugSafety}>
                    <Search className="w-4 h-4 mr-2" />
                    Search
                  </Button>
                </div>

                {drugSafetyInfo && (
                  <div className="space-y-4">
                    <div className="border rounded-lg p-4">
                      <div className="flex justify-between items-center mb-4">
                        <h3 className="font-semibold text-lg">{drugSafetyInfo.drug_name}</h3>
                        <div className="text-right">
                          <p className="text-sm text-gray-600">Safety Score</p>
                          <p className={`text-xl font-bold ${
                            drugSafetyInfo.safety_score >= 80 ? 'text-green-600' : 
                            drugSafetyInfo.safety_score >= 60 ? 'text-yellow-600' : 'text-red-600'
                          }`}>
                            {drugSafetyInfo.safety_score?.toFixed(1)}/100
                          </p>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Drug Interactions */}
                        <div>
                          <h4 className="font-medium mb-2">Drug Interactions</h4>
                          <div className="space-y-2">
                            {drugSafetyInfo.interactions?.interactions?.map((interaction, index) => (
                              <div key={index} className="p-2 bg-yellow-50 rounded text-sm">
                                <Badge className={getSeverityColor(interaction.severity)} size="sm">
                                  {interaction.severity}
                                </Badge>
                                <p className="mt-1">{interaction.description}</p>
                              </div>
                            ))}
                          </div>
                        </div>

                        {/* Food Interactions */}
                        <div>
                          <h4 className="font-medium mb-2">Food Interactions</h4>
                          <div className="space-y-2">
                            {drugSafetyInfo.food_interactions?.food_interactions?.map((interaction, index) => (
                              <div key={index} className="p-2 bg-blue-50 rounded text-sm">
                                <p className="font-medium">{interaction.type}</p>
                                <p>{interaction.description}</p>
                                <p className="text-gray-600 mt-1">{interaction.recommendation}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>

                      {/* Adverse Events */}
                      {drugSafetyInfo.adverse_events?.adverse_events?.length > 0 && (
                        <div className="mt-4">
                          <h4 className="font-medium mb-2">Common Adverse Events</h4>
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                            {drugSafetyInfo.adverse_events.adverse_events.slice(0, 6).map((event, index) => (
                              <div key={index} className="p-2 bg-gray-50 rounded text-sm">
                                <p className="font-medium">{event.reaction}</p>
                                <p className="text-gray-600">{event.count} reports</p>
                                <Badge className={getSeverityColor(event.severity)} size="sm">
                                  {event.severity}
                                </Badge>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        {/* Communications Tab */}
        <TabsContent value="communications">
          {providerInbox && (
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <div className="flex items-center">
                      <MessageSquare className="w-5 h-5 mr-2" />
                      Provider Inbox
                    </div>
                    <div className="flex gap-2 text-sm">
                      <Badge variant="secondary">
                        {providerInbox.unread_count} unread
                      </Badge>
                      <Badge variant="destructive">
                        {providerInbox.high_priority_count} high priority
                      </Badge>
                    </div>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {providerInbox.messages?.map((message, index) => (
                      <div key={index} className={`border rounded-lg p-4 ${
                        message.status === 'unread' ? 'bg-blue-50 border-blue-200' : ''
                      }`}>
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                              <h4 className="font-medium">{message.patient_name}</h4>
                              <Badge variant={message.priority === 'high' ? 'destructive' : 'secondary'}>
                                {message.priority}
                              </Badge>
                              <Badge variant="outline">{message.category}</Badge>
                              {message.status === 'unread' && (
                                <Badge className="bg-blue-600 text-white">New</Badge>
                              )}
                            </div>
                            <h5 className="font-medium text-gray-900 mb-1">{message.subject}</h5>
                            <p className="text-sm text-gray-600 mb-2">{message.preview}</p>
                          </div>
                          <div className="text-right">
                            <p className="text-sm text-gray-500">
                              {new Date(message.received_date).toLocaleDateString()}
                            </p>
                            <div className="mt-2 flex gap-1">
                              <Button size="sm" variant="outline">
                                <Eye className="w-4 h-4" />
                              </Button>
                              <Button size="sm" variant="outline">
                                <Send className="w-4 h-4" />
                              </Button>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </TabsContent>

        {/* Emergency Tab */}
        <TabsContent value="emergency">
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center text-red-600">
                  <AlertTriangle className="w-5 h-5 mr-2" />
                  Emergency Contact System
                </CardTitle>
              </CardHeader>
              <CardContent>
                <Alert className="border-red-200 bg-red-50 mb-4">
                  <AlertTriangle className="h-4 w-4" />
                  <AlertDescription>
                    This section provides emergency contact information and protocols for critical medication situations.
                  </AlertDescription>
                </Alert>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h3 className="font-semibold mb-4">Emergency Protocols</h3>
                    <div className="space-y-3">
                      <div className="p-3 border border-red-200 rounded-lg">
                        <h4 className="font-medium text-red-600">Severe Adverse Reaction</h4>
                        <p className="text-sm text-gray-600">
                          1. Discontinue medication immediately<br/>
                          2. Contact patient within 15 minutes<br/>
                          3. Send to emergency department if needed<br/>
                          4. Document incident thoroughly
                        </p>
                      </div>
                      <div className="p-3 border border-orange-200 rounded-lg">
                        <h4 className="font-medium text-orange-600">Critical Missed Doses</h4>
                        <p className="text-sm text-gray-600">
                          1. Contact patient within 2 hours<br/>
                          2. Assess reason for missed doses<br/>
                          3. Provide guidance on next steps<br/>
                          4. Consider medication adjustment
                        </p>
                      </div>
                      <div className="p-3 border border-yellow-200 rounded-lg">
                        <h4 className="font-medium text-yellow-600">Drug Interaction Alert</h4>
                        <p className="text-sm text-gray-600">
                          1. Review interaction severity<br/>
                          2. Contact patient same day<br/>
                          3. Consider alternative medications<br/>
                          4. Monitor closely for side effects
                        </p>
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="font-semibold mb-4">Contact Information</h3>
                    <div className="space-y-3">
                      <div className="p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center mb-2">
                          <Phone className="w-4 h-4 mr-2 text-green-600" />
                          <span className="font-medium">24/7 Provider Hotline</span>
                        </div>
                        <p className="text-lg font-bold text-green-600">+1-800-PROVIDER</p>
                        <p className="text-sm text-gray-600">For urgent medication concerns</p>
                      </div>
                      
                      <div className="p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center mb-2">
                          <Mail className="w-4 h-4 mr-2 text-blue-600" />
                          <span className="font-medium">Secure Messaging</span>
                        </div>
                        <p className="text-sm text-gray-600">
                          Use the Communications tab for non-urgent messages
                        </p>
                      </div>

                      <div className="p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center mb-2">
                          <AlertTriangle className="w-4 h-4 mr-2 text-red-600" />
                          <span className="font-medium">Emergency Services</span>
                        </div>
                        <p className="text-lg font-bold text-red-600">911</p>
                        <p className="text-sm text-gray-600">For life-threatening situations</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-6">
                  <Button className="bg-red-600 hover:bg-red-700 text-white">
                    <AlertTriangle className="w-4 h-4 mr-2" />
                    Send Emergency Alert
                  </Button>
                  <p className="text-sm text-gray-600 mt-2">
                    Use only for immediate patient safety concerns
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ProviderMedicationDashboard;