import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { 
  Users, AlertTriangle, Calendar, Clock, Activity,
  Eye, MessageCircle, Phone, UserPlus, Filter,
  RefreshCw, Settings, Loader2
} from 'lucide-react';
import { usePatientQueue } from '../../hooks/useClinicalDashboard';

const PatientQueue = ({ providerId }) => {
  const [selectedQueue, setSelectedQueue] = useState('all');
  const [showFilters, setShowFilters] = useState(false);

  // Use the custom hook for patient queue data with real-time updates
  const {
    loading,
    error,
    data: queueData,
    lastUpdated,
    refresh,
    isStale
  } = usePatientQueue(providerId, {
    realTime: true,
    refreshInterval: 30000,
    autoStart: true
  });

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'urgent': return 'bg-red-500 text-white';
      case 'routine': return 'bg-blue-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'ready_for_provider': return 'bg-green-100 text-green-800';
      case 'vitals_taken': return 'bg-blue-100 text-blue-800';
      case 'checked_in': return 'bg-yellow-100 text-yellow-800';
      case 'waiting': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <Card>
          <CardContent className="pt-6">
            <div className="animate-pulse space-y-4">
              <div className="h-4 bg-gray-200 rounded w-1/4"></div>
              <div className="space-y-3">
                <div className="h-4 bg-gray-200 rounded"></div>
                <div className="h-4 bg-gray-200 rounded w-5/6"></div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Queue Statistics */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <Card className="border-2 border-emerald-200 bg-emerald-50">
          <CardContent className="pt-6">
            <div className="flex items-center">
              <Users className="w-8 h-8 text-emerald-600 mr-3" />
              <div>
                <div className="text-2xl font-bold text-emerald-600">
                  {queueData?.queue_stats?.total_in_queue || 0}
                </div>
                <p className="text-sm text-gray-600">Total in Queue</p>
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
                  {queueData?.queue_stats?.urgent || 0}
                </div>
                <p className="text-sm text-gray-600">Urgent Cases</p>
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
                  {queueData?.queue_stats?.scheduled || 0}
                </div>
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
                <div className="text-2xl font-bold text-green-600">
                  {queueData?.completed_today || 0}
                </div>
                <p className="text-sm text-gray-600">Completed Today</p>
              </div>
            </div>
          </CardContent>
        </Card>
        
        <Card className="border-2 border-orange-200 bg-orange-50">
          <CardContent className="pt-6">
            <div className="flex items-center">
              <Clock className="w-8 h-8 text-orange-600 mr-3" />
              <div>
                <div className="text-lg font-bold text-orange-600">
                  {queueData?.queue_stats?.avg_wait_time || 'N/A'}
                </div>
                <p className="text-sm text-gray-600">Avg Wait Time</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Queue Controls */}
      <div className="flex justify-between items-center">
        <div className="flex space-x-2">
          <Button
            variant={selectedQueue === 'all' ? 'default' : 'outline'}
            onClick={() => setSelectedQueue('all')}
            size="sm"
          >
            All Patients
          </Button>
          <Button
            variant={selectedQueue === 'urgent' ? 'default' : 'outline'}
            onClick={() => setSelectedQueue('urgent')}
            size="sm"
          >
            Urgent Only
          </Button>
          <Button
            variant={selectedQueue === 'scheduled' ? 'default' : 'outline'}
            onClick={() => setSelectedQueue('scheduled')}
            size="sm"
          >
            Scheduled
          </Button>
        </div>
        
        <div className="flex space-x-2">
          <Button variant="outline" size="sm" onClick={() => setShowFilters(!showFilters)}>
            <Filter className="w-4 h-4 mr-2" />
            Filters
          </Button>
          <Button variant="outline" size="sm">
            <UserPlus className="w-4 h-4 mr-2" />
            Add Patient
          </Button>
          <Button variant="outline" size="sm" onClick={fetchQueueData}>
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Priority Queue - Urgent Cases */}
      {(selectedQueue === 'all' || selectedQueue === 'urgent') && queueData?.priority_queue?.length > 0 && (
        <Card className="border-l-4 border-red-500">
          <CardHeader>
            <CardTitle className="flex items-center text-red-600">
              <AlertTriangle className="w-5 h-5 mr-2" />
              Priority Queue - Urgent Cases
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {queueData.priority_queue.map((patient) => (
                <div key={patient.id} className="border rounded-lg p-4 bg-red-50">
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
                      <div className="grid grid-cols-3 gap-4 text-xs text-gray-600 mb-3">
                        {Object.entries(patient.vitals || {}).map(([key, value]) => (
                          <span key={key}>{key.toUpperCase()}: {value}</span>
                        ))}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-red-600">{patient.wait_time}</div>
                      <Badge className={`mt-1 ${getStatusColor(patient.status)}`}>
                        {patient.status?.replace('_', ' ')}
                      </Badge>
                    </div>
                  </div>
                  <div className="flex space-x-2">
                    <Button size="sm" className="bg-red-600 hover:bg-red-700">
                      <Eye className="w-4 h-4 mr-1" />
                      See Now
                    </Button>
                    <Button size="sm" variant="outline">
                      <MessageCircle className="w-4 h-4 mr-1" />
                      Message
                    </Button>
                    <Button size="sm" variant="outline">
                      <Phone className="w-4 h-4 mr-1" />
                      Call
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Scheduled Queue */}
      {(selectedQueue === 'all' || selectedQueue === 'scheduled') && queueData?.scheduled_queue?.length > 0 && (
        <Card className="border-l-4 border-blue-500">
          <CardHeader>
            <CardTitle className="flex items-center text-blue-600">
              <Calendar className="w-5 h-5 mr-2" />
              Scheduled Appointments
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {queueData.scheduled_queue.map((patient) => (
                <div key={patient.id} className="border rounded-lg p-4 bg-blue-50">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h4 className="font-semibold text-gray-900">{patient.patient_name}</h4>
                        <Badge className="bg-blue-500 text-white">
                          {patient.appointment_time}
                        </Badge>
                        <Badge variant="secondary">{patient.room}</Badge>
                      </div>
                      <p className="text-sm text-gray-700">{patient.condition}</p>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-blue-600">{patient.wait_time}</div>
                      <Badge className={`mt-1 ${getStatusColor(patient.status)}`}>
                        {patient.status}
                      </Badge>
                    </div>
                  </div>
                  <div className="flex space-x-2 mt-3">
                    <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
                      <Eye className="w-4 h-4 mr-1" />
                      Start Visit
                    </Button>
                    <Button size="sm" variant="outline">
                      <Calendar className="w-4 h-4 mr-1" />
                      Reschedule
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
      )}

      {/* No Patients Message */}
      {(!queueData?.priority_queue?.length && !queueData?.scheduled_queue?.length) && (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-8">
              <Users className="w-12 h-12 text-gray-300 mx-auto mb-4" />
              <div className="text-gray-500 mb-2">No patients in queue</div>
              <p className="text-sm text-gray-400">All appointments completed or no scheduled patients</p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default PatientQueue;