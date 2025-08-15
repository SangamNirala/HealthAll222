import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Input } from '../ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { 
  Users, 
  UserCheck, 
  Brain, 
  AlertCircle, 
  Clock, 
  Search, 
  Filter,
  Star,
  TrendingUp,
  Activity,
  Heart,
  CheckCircle,
  XCircle,
  Loader2
} from 'lucide-react';
import SmartNavigation from '../shared/SmartNavigation';

const SmartPatientAssignmentPanel = () => {
  const [assignments, setAssignments] = useState([]);
  const [availablePatients, setAvailablePatients] = useState([]);
  const [matchingResults, setMatchingResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Filters and search
  const [searchTerm, setSearchTerm] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('ALL');
  const [statusFilter, setStatusFilter] = useState('ALL');
  
  // Assignment creation
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [assignmentPriority, setAssignmentPriority] = useState('MEDIUM');
  const [matchingCriteria, setMatchingCriteria] = useState({
    conditions: [],
    expertise: [],
    workload_preference: 'BALANCED'
  });

  const providerId = 'provider-123';
  const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;

  // Fetch existing assignments
  const fetchAssignments = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/provider/patient-management/assignments/${providerId}`);
      if (response.ok) {
        const data = await response.json();
        setAssignments(data.assignments || []);
      } else {
        throw new Error('Failed to fetch assignments');
      }
    } catch (err) {
      setError(`Error fetching assignments: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // AI-powered patient matching
  const performAIMatching = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/provider/patient-management/ai-matching`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          provider_id: providerId,
          criteria: matchingCriteria,
          max_patients: 10
        })
      });
      
      if (response.ok) {
        const data = await response.json();
        setMatchingResults(data.matched_patients || []);
      } else {
        throw new Error('AI matching failed');
      }
    } catch (err) {
      setError(`Error in AI matching: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Create new assignment
  const createAssignment = async (patientId, priority = 'MEDIUM') => {
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/provider/patient-management/assignments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          provider_id: providerId,
          patient_id: patientId,
          priority: priority,
          assignment_type: 'AI_MATCHED',
          notes: 'AI-generated assignment based on matching criteria'
        })
      });
      
      if (response.ok) {
        await fetchAssignments(); // Refresh assignments
        setSelectedPatient(null);
      } else {
        throw new Error('Failed to create assignment');
      }
    } catch (err) {
      setError(`Error creating assignment: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Update assignment status
  const updateAssignmentStatus = async (assignmentId, newStatus) => {
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/provider/patient-management/assignments/${assignmentId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          status: newStatus,
          updated_by: providerId,
          notes: `Status updated to ${newStatus}`
        })
      });
      
      if (response.ok) {
        await fetchAssignments(); // Refresh assignments
      } else {
        throw new Error('Failed to update assignment');
      }
    } catch (err) {
      setError(`Error updating assignment: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAssignments();
  }, []);

  // Filter assignments
  const filteredAssignments = assignments.filter(assignment => {
    const matchesSearch = assignment.patient_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         assignment.patient_id?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesPriority = priorityFilter === 'ALL' || assignment.priority === priorityFilter;
    const matchesStatus = statusFilter === 'ALL' || assignment.status === statusFilter;
    
    return matchesSearch && matchesPriority && matchesStatus;
  });

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'CRITICAL': return 'bg-red-100 text-red-800 border-red-200';
      case 'URGENT': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'HIGH': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'MEDIUM': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'LOW': return 'bg-gray-100 text-gray-800 border-gray-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'PENDING': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'ACTIVE': return 'bg-emerald-100 text-emerald-800 border-emerald-200';
      case 'COMPLETED': return 'bg-green-100 text-green-800 border-green-200';
      case 'CANCELLED': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
        <SmartNavigation />
        <div className="container mx-auto px-4 py-8">
          <Card className="max-w-md mx-auto">
            <CardContent className="p-6 text-center">
              <AlertCircle className="mx-auto mb-4 h-12 w-12 text-red-500" />
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
            <UserCheck className="h-8 w-8 text-emerald-600" />
            <h1 className="text-3xl font-bold text-gray-900">Smart Patient Assignment Panel</h1>
          </div>
          <p className="text-gray-600 text-lg">
            AI-powered patient matching and assignment management system
          </p>
        </div>

        <Tabs defaultValue="assignments" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3 bg-white">
            <TabsTrigger value="assignments">Current Assignments</TabsTrigger>
            <TabsTrigger value="matching">AI Matching</TabsTrigger>
            <TabsTrigger value="create">Create Assignment</TabsTrigger>
          </TabsList>

          {/* Current Assignments Tab */}
          <TabsContent value="assignments" className="space-y-6">
            {/* Filters */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Filter className="h-5 w-5" />
                  Filters & Search
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                    <Input
                      placeholder="Search patients..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                  
                  <Select value={priorityFilter} onValueChange={setPriorityFilter}>
                    <SelectTrigger>
                      <SelectValue placeholder="Priority" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="ALL">All Priorities</SelectItem>
                      <SelectItem value="CRITICAL">Critical</SelectItem>
                      <SelectItem value="URGENT">Urgent</SelectItem>
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
                      <SelectItem value="PENDING">Pending</SelectItem>
                      <SelectItem value="ACTIVE">Active</SelectItem>
                      <SelectItem value="COMPLETED">Completed</SelectItem>
                      <SelectItem value="CANCELLED">Cancelled</SelectItem>
                    </SelectContent>
                  </Select>
                  
                  <Button 
                    onClick={fetchAssignments} 
                    disabled={loading}
                    className="bg-emerald-600 hover:bg-emerald-700"
                  >
                    {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : 'Refresh'}
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Assignments Grid */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {loading && filteredAssignments.length === 0 ? (
                <div className="col-span-full flex justify-center items-center py-12">
                  <Loader2 className="h-8 w-8 animate-spin text-emerald-600" />
                  <span className="ml-2 text-gray-600">Loading assignments...</span>
                </div>
              ) : filteredAssignments.length === 0 ? (
                <div className="col-span-full text-center py-12">
                  <Users className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                  <p className="text-gray-600">No assignments found</p>
                  <Button 
                    onClick={performAIMatching}
                    className="mt-4 bg-emerald-600 hover:bg-emerald-700"
                  >
                    Find AI Matches
                  </Button>
                </div>
              ) : (
                filteredAssignments.map((assignment) => (
                  <Card key={assignment.assignment_id} className="hover:shadow-lg transition-shadow">
                    <CardHeader className="pb-4">
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="font-semibold text-lg">{assignment.patient_name || 'Unknown Patient'}</h3>
                          <p className="text-sm text-gray-600">ID: {assignment.patient_id}</p>
                        </div>
                        <Badge className={getPriorityColor(assignment.priority)}>
                          {assignment.priority}
                        </Badge>
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600">Status:</span>
                          <Badge className={getStatusColor(assignment.status)}>
                            {assignment.status}
                          </Badge>
                        </div>
                        
                        {assignment.ai_match_score && (
                          <div className="flex items-center justify-between">
                            <span className="text-sm text-gray-600">AI Match:</span>
                            <div className="flex items-center gap-2">
                              <div className="w-16 bg-gray-200 rounded-full h-2">
                                <div 
                                  className="bg-emerald-600 h-2 rounded-full"
                                  style={{ width: `${assignment.ai_match_score * 100}%` }}
                                />
                              </div>
                              <span className="text-sm font-semibold">
                                {(assignment.ai_match_score * 100).toFixed(1)}%
                              </span>
                            </div>
                          </div>
                        )}
                        
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600">Created:</span>
                          <span className="text-sm">
                            {assignment.created_at ? new Date(assignment.created_at).toLocaleDateString() : 'Recently'}
                          </span>
                        </div>
                        
                        <div className="flex gap-2 pt-2">
                          {assignment.status === 'PENDING' && (
                            <Button 
                              size="sm" 
                              onClick={() => updateAssignmentStatus(assignment.assignment_id, 'ACTIVE')}
                              className="flex-1 bg-emerald-600 hover:bg-emerald-700"
                            >
                              <CheckCircle className="h-4 w-4 mr-1" />
                              Activate
                            </Button>
                          )}
                          {assignment.status === 'ACTIVE' && (
                            <Button 
                              size="sm" 
                              onClick={() => updateAssignmentStatus(assignment.assignment_id, 'COMPLETED')}
                              className="flex-1 bg-green-600 hover:bg-green-700"
                            >
                              <CheckCircle className="h-4 w-4 mr-1" />
                              Complete
                            </Button>
                          )}
                          {(assignment.status === 'PENDING' || assignment.status === 'ACTIVE') && (
                            <Button 
                              size="sm" 
                              variant="outline"
                              onClick={() => updateAssignmentStatus(assignment.assignment_id, 'CANCELLED')}
                              className="text-red-600 border-red-300 hover:bg-red-50"
                            >
                              <XCircle className="h-4 w-4" />
                            </Button>
                          )}
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </div>
          </TabsContent>

          {/* AI Matching Tab */}
          <TabsContent value="matching" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Brain className="h-5 w-5" />
                  AI-Powered Patient Matching
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="text-sm font-medium">Workload Preference</label>
                    <Select 
                      value={matchingCriteria.workload_preference} 
                      onValueChange={(value) => setMatchingCriteria(prev => ({...prev, workload_preference: value}))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="LIGHT">Light Workload</SelectItem>
                        <SelectItem value="BALANCED">Balanced</SelectItem>
                        <SelectItem value="HEAVY">Heavy Workload</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div className="md:col-span-2">
                    <Button 
                      onClick={performAIMatching}
                      disabled={loading}
                      className="w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700"
                    >
                      {loading ? (
                        <>
                          <Loader2 className="h-4 w-4 animate-spin mr-2" />
                          Analyzing Matches...
                        </>
                      ) : (
                        <>
                          <Brain className="h-4 w-4 mr-2" />
                          Run AI Matching
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Matching Results */}
            {matchingResults.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>AI Matching Results</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid gap-4 md:grid-cols-2">
                    {matchingResults.map((match, index) => (
                      <Card key={index} className="border-emerald-200">
                        <CardContent className="p-4">
                          <div className="flex justify-between items-start mb-3">
                            <div>
                              <h4 className="font-semibold">{match.patient_name || `Patient ${match.patient_id}`}</h4>
                              <p className="text-sm text-gray-600">ID: {match.patient_id}</p>
                            </div>
                            <div className="text-right">
                              <div className="flex items-center gap-2 mb-1">
                                <Star className="h-4 w-4 text-yellow-500" />
                                <span className="font-bold text-emerald-600">
                                  {(match.match_score * 100).toFixed(1)}%
                                </span>
                              </div>
                              <Badge className="bg-emerald-100 text-emerald-800">
                                {match.confidence_level || 'High'}
                              </Badge>
                            </div>
                          </div>
                          
                          <div className="space-y-2 text-sm">
                            <div><strong>Conditions:</strong> {match.conditions?.join(', ') || 'None specified'}</div>
                            <div><strong>Match Factors:</strong> {match.match_factors?.join(', ') || 'AI optimized'}</div>
                          </div>
                          
                          <Button 
                            onClick={() => createAssignment(match.patient_id, 'HIGH')}
                            className="w-full mt-3 bg-emerald-600 hover:bg-emerald-700"
                            size="sm"
                          >
                            Create Assignment
                          </Button>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* Create Assignment Tab */}
          <TabsContent value="create" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  Manual Assignment Creation
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium">Patient ID</label>
                    <Input
                      placeholder="Enter patient ID"
                      value={selectedPatient || ''}
                      onChange={(e) => setSelectedPatient(e.target.value)}
                    />
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium">Priority Level</label>
                    <Select value={assignmentPriority} onValueChange={setAssignmentPriority}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="LOW">Low</SelectItem>
                        <SelectItem value="MEDIUM">Medium</SelectItem>
                        <SelectItem value="HIGH">High</SelectItem>
                        <SelectItem value="URGENT">Urgent</SelectItem>
                        <SelectItem value="CRITICAL">Critical</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                
                <Button 
                  onClick={() => selectedPatient && createAssignment(selectedPatient, assignmentPriority)}
                  disabled={!selectedPatient || loading}
                  className="w-full bg-emerald-600 hover:bg-emerald-700"
                >
                  {loading ? (
                    <>
                      <Loader2 className="h-4 w-4 animate-spin mr-2" />
                      Creating Assignment...
                    </>
                  ) : (
                    <>
                      <UserCheck className="h-4 w-4 mr-2" />
                      Create Assignment
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default SmartPatientAssignmentPanel;