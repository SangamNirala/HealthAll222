import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Users, Search, UserPlus, Eye, MessageCircle, Calendar, AlertTriangle, Clock, Activity } from 'lucide-react';

const ProviderPatients = () => {
  const { switchRole } = useRole();
  const [searchQuery, setSearchQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [activeTab, setActiveTab] = useState('queue');
  const [queueData, setQueueData] = useState(null);
  
  const [patients] = useState([
    {
      id: 1,
      name: 'Sarah Johnson',
      age: 34,
      condition: 'Type 2 Diabetes',
      status: 'stable',
      lastVisit: '2024-01-10',
      nextAppointment: '2024-02-15',
      riskLevel: 'low',
      phone: '(555) 123-4567'
    },
    {
      id: 2,
      name: 'Michael Chen',
      age: 28,
      condition: 'Hypertension',
      status: 'improving',
      lastVisit: '2024-01-08',
      nextAppointment: '2024-01-22',
      riskLevel: 'medium',
      phone: '(555) 234-5678'
    },
    {
      id: 3,
      name: 'Emma Davis',
      age: 45,
      condition: 'Obesity',
      status: 'needs_attention',
      lastVisit: '2023-12-20',
      nextAppointment: 'Not scheduled',
      riskLevel: 'high',
      phone: '(555) 345-6789'
    },
    {
      id: 4,
      name: 'Robert Wilson',
      age: 52,
      condition: 'Heart Disease',
      status: 'stable',
      lastVisit: '2024-01-12',
      nextAppointment: '2024-02-20',
      riskLevel: 'medium',
      phone: '(555) 456-7890'
    }
  ]);

  useEffect(() => {
    switchRole('provider');
    
    // Fetch patient queue data
    const fetchQueueData = async () => {
      try {
        const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;
        const response = await fetch(`${backendUrl}/api/provider/patient-queue/provider-123`);
        const data = await response.json();
        setQueueData(data);
      } catch (error) {
        console.error('Error fetching queue data:', error);
      }
    };
    
    fetchQueueData();
  }, [switchRole]);

  const filteredPatients = patients.filter(patient => {
    const matchesSearch = patient.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         patient.condition.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = filterStatus === 'all' || patient.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const getStatusColor = (status) => {
    switch (status) {
      case 'stable': return 'bg-green-100 text-green-800';
      case 'improving': return 'bg-blue-100 text-blue-800';
      case 'needs_attention': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getRiskColor = (risk) => {
    switch (risk) {
      case 'low': return 'text-green-600';
      case 'medium': return 'text-yellow-600';
      case 'high': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getRiskBadgeColor = (risk) => {
    switch (risk) {
      case 'low': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'high': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'urgent': return 'bg-red-500 text-white';
      case 'routine': return 'bg-blue-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Patient Management</h1>
          <p className="text-gray-600">Monitor and manage your patient caseload</p>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('queue')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'queue'
                    ? 'border-emerald-500 text-emerald-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Patient Queue
              </button>
              <button
                onClick={() => setActiveTab('patients')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'patients'
                    ? 'border-emerald-500 text-emerald-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                All Patients
              </button>
            </nav>
          </div>
        </div>

        {activeTab === 'queue' && queueData && (
          <>
            {/* Queue Stats */}
            <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
              <Card className="border-2 border-emerald-200 bg-emerald-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Users className="w-8 h-8 text-emerald-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-emerald-600">{queueData.queue_stats.total_in_queue}</div>
                      <p className="text-sm text-gray-600">In Queue</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-red-200 bg-red-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <AlertTriangle className="w-8 h-8 text-red-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-red-600">{queueData.queue_stats.urgent}</div>
                      <p className="text-sm text-gray-600">Urgent</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-blue-200 bg-blue-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Calendar className="w-8 h-8 text-blue-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-blue-600">{queueData.queue_stats.scheduled}</div>
                      <p className="text-sm text-gray-600">Scheduled</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-green-200 bg-green-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Activity className="w-8 h-8 text-green-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-green-600">{queueData.completed_today}</div>
                      <p className="text-sm text-gray-600">Completed</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-orange-200 bg-orange-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Clock className="w-8 h-8 text-orange-600 mr-3" />
                    <div>
                      <div className="text-lg font-bold text-orange-600">{queueData.queue_stats.avg_wait_time}</div>
                      <p className="text-sm text-gray-600">Avg Wait</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Priority Queue */}
            <Card className="mb-6">
              <CardHeader>
                <CardTitle className="flex items-center text-red-600">
                  <AlertTriangle className="w-5 h-5 mr-2" />
                  Priority Queue - Urgent Cases
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {queueData.priority_queue.map((patient) => (
                    <div key={patient.id} className="border-l-4 border-red-500 bg-red-50 p-4 rounded-lg">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <h4 className="font-semibold text-gray-900">{patient.patient_name}</h4>
                            <Badge className={getPriorityColor(patient.priority)}>
                              {patient.priority.toUpperCase()}
                            </Badge>
                            <Badge variant="secondary">{patient.room}</Badge>
                          </div>
                          <p className="text-sm text-gray-700 mb-2">{patient.condition}</p>
                          <div className="grid grid-cols-3 gap-4 text-xs text-gray-600">
                            {Object.entries(patient.vitals).map(([key, value]) => (
                              <span key={key}>{key.toUpperCase()}: {value}</span>
                            ))}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="text-sm font-medium text-red-600">{patient.wait_time}</div>
                          <Badge className="mt-1" variant="outline">{patient.status.replace('_', ' ')}</Badge>
                        </div>
                      </div>
                      <div className="mt-3 flex space-x-2">
                        <Button size="sm" className="bg-red-600 hover:bg-red-700">
                          <Eye className="w-4 h-4 mr-1" />
                          See Now
                        </Button>
                        <Button size="sm" variant="outline">
                          <MessageCircle className="w-4 h-4 mr-1" />
                          Message
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Scheduled Queue */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center text-blue-600">
                  <Calendar className="w-5 h-5 mr-2" />
                  Scheduled Appointments
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {queueData.scheduled_queue.map((patient) => (
                    <div key={patient.id} className="border-l-4 border-blue-500 bg-blue-50 p-4 rounded-lg">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <h4 className="font-semibold text-gray-900">{patient.patient_name}</h4>
                            <Badge className={getPriorityColor(patient.priority)}>
                              {patient.appointment_time}
                            </Badge>
                            <Badge variant="secondary">{patient.room}</Badge>
                          </div>
                          <p className="text-sm text-gray-700">{patient.condition}</p>
                        </div>
                        <div className="text-right">
                          <div className="text-sm font-medium text-blue-600">{patient.wait_time}</div>
                          <Badge className="mt-1" variant="outline">{patient.status}</Badge>
                        </div>
                      </div>
                      <div className="mt-3 flex space-x-2">
                        <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                          <Eye className="w-4 h-4 mr-1" />
                          Start Visit
                        </Button>
                        <Button size="sm" variant="outline">
                          <Calendar className="w-4 h-4 mr-1" />
                          Reschedule
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </>
        )}

        {activeTab === 'patients' && (
          <>
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <Card className="border-2 border-emerald-200 bg-emerald-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Users className="w-8 h-8 text-emerald-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-emerald-600">{patients.length}</div>
                      <p className="text-sm text-gray-600">Total Patients</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-green-200 bg-green-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-green-500 rounded-full mr-3 flex items-center justify-center">
                      <span className="text-white font-bold text-sm">✓</span>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-green-600">
                        {patients.filter(p => p.status === 'stable').length}
                      </div>
                      <p className="text-sm text-gray-600">Stable</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-red-200 bg-red-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <AlertTriangle className="w-8 h-8 text-red-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-red-600">
                        {patients.filter(p => p.status === 'needs_attention').length}
                      </div>
                      <p className="text-sm text-gray-600">Need Attention</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-blue-200 bg-blue-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Calendar className="w-8 h-8 text-blue-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-blue-600">
                        {patients.filter(p => p.nextAppointment !== 'Not scheduled').length}
                      </div>
                      <p className="text-sm text-gray-600">Scheduled</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Controls */}
            <div className="flex flex-col md:flex-row gap-4 mb-6">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    placeholder="Search patients..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
              </div>
              
              <select 
                className="border border-gray-300 rounded-md px-3 py-2 bg-white"
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
              >
                <option value="all">All Statuses</option>
                <option value="stable">Stable</option>
                <option value="improving">Improving</option>
                <option value="needs_attention">Needs Attention</option>
              </select>
              
              <Button className="bg-emerald-600 hover:bg-emerald-700">
                <UserPlus className="w-4 h-4 mr-2" />
                Add Patient
              </Button>
            </div>

            {/* Patients Table */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Users className="w-5 h-5 mr-2 text-emerald-600" />
                  Patients ({filteredPatients.length})
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-gray-200">
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Patient</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Condition</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Status</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Risk Level</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Last Visit</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Next Appointment</th>
                        <th className="text-left py-3 px-4 font-semibold text-gray-700">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredPatients.map((patient) => (
                        <tr key={patient.id} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                          <td className="py-4 px-4">
                            <div>
                              <div className="font-semibold text-gray-900">{patient.name}</div>
                              <div className="text-sm text-gray-500">Age {patient.age} • {patient.phone}</div>
                            </div>
                          </td>
                          <td className="py-4 px-4">
                            <span className="text-gray-900">{patient.condition}</span>
                          </td>
                          <td className="py-4 px-4">
                            <Badge className={getStatusColor(patient.status)}>
                              {patient.status.replace('_', ' ')}
                            </Badge>
                          </td>
                          <td className="py-4 px-4">
                            <Badge className={getRiskBadgeColor(patient.riskLevel)}>
                              {patient.riskLevel} risk
                            </Badge>
                          </td>
                          <td className="py-4 px-4 text-gray-600">
                            {patient.lastVisit}
                          </td>
                          <td className="py-4 px-4">
                            <span className={patient.nextAppointment === 'Not scheduled' ? 'text-red-600' : 'text-gray-900'}>
                              {patient.nextAppointment}
                            </span>
                          </td>
                          <td className="py-4 px-4">
                            <div className="flex space-x-2">
                              <Button variant="ghost" size="sm">
                                <Eye className="w-4 h-4" />
                              </Button>
                              <Button variant="ghost" size="sm">
                                <MessageCircle className="w-4 h-4" />
                              </Button>
                              <Button variant="ghost" size="sm">
                                <Calendar className="w-4 h-4" />
                              </Button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  
                  {filteredPatients.length === 0 && (
                    <div className="text-center py-8">
                      <Users className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                      <div className="text-gray-500 mb-2">No patients found</div>
                      <p className="text-sm text-gray-400">Try adjusting your search or filters</p>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </>
        )}
      </div>
    </div>
  );
};

export default ProviderPatients;