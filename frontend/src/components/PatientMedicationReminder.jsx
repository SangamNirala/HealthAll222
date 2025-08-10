import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { 
  Pill, 
  Clock, 
  CheckCircle, 
  Plus, 
  Bell, 
  Zap, 
  Calendar, 
  TrendingUp,
  AlertCircle,
  User,
  Edit3,
  Trash2
} from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

const getPatientUserId = () => {
  try {
    const saved = localStorage.getItem('patient_user_id');
    if (saved && typeof saved === 'string' && saved.trim().length > 0) return saved;
  } catch (e) {}
  return 'demo-patient-123';
};

const PatientMedicationReminder = () => {
  const { switchRole } = useRole();
  const [userId, setUserId] = useState(getPatientUserId());
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [medications, setMedications] = useState([]);
  const [reminders, setReminders] = useState([]);
  const [adherenceStats, setAdherenceStats] = useState({});
  const [aiInsights, setAiInsights] = useState([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [actionMessage, setActionMessage] = useState('');
  
  const [newMedication, setNewMedication] = useState({
    name: '',
    dosage: '',
    frequency: 'daily',
    times: ['08:00'],
    with_food: false,
    condition: '',
    prescriber: ''
  });

  useEffect(() => {
    switchRole('patient');
    setUserId(getPatientUserId());
  }, [switchRole]);

  useEffect(() => {
    fetchMedicationData();
  }, [userId]);

  const fetchMedicationData = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE_URL}/api/patient/medications/${userId}`);
      const data = await response.json();
      
      if (!response.ok) throw new Error(data?.detail || 'Failed to load medications');
      
      setMedications(data.medications || []);
      setReminders(data.reminders || []);
      setAdherenceStats(data.adherence_stats || {});
      setAiInsights(data.ai_insights || []);
    } catch (e) {
      console.error(e);
      setError('Failed to load medication data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const markMedicationTaken = async (medicationId, reminderId) => {
    try {
      setActionMessage('Marking as taken...');
      const response = await fetch(`${API_BASE_URL}/api/patient/medications/${userId}/take`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ medication_id: medicationId, reminder_id: reminderId })
      });
      
      const data = await response.json();
      if (!response.ok) throw new Error(data?.detail || 'Failed to mark medication');
      
      setActionMessage('✓ Marked as taken!');
      setTimeout(() => setActionMessage(''), 2000);
      
      // Refresh data to update UI
      await fetchMedicationData();
      
    } catch (e) {
      setActionMessage(`Error: ${e.message}`);
      setTimeout(() => setActionMessage(''), 3000);
    }
  };

  const addMedication = async () => {
    if (!newMedication.name || !newMedication.dosage) {
      setActionMessage('Please fill in medication name and dosage');
      setTimeout(() => setActionMessage(''), 3000);
      return;
    }

    try {
      setActionMessage('Adding medication...');
      const response = await fetch(`${API_BASE_URL}/api/patient/medications/${userId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...newMedication,
          start_date: new Date().toISOString().split('T')[0]
        })
      });
      
      const data = await response.json();
      if (!response.ok) throw new Error(data?.detail || 'Failed to add medication');
      
      setActionMessage('✓ Medication added!');
      setShowAddForm(false);
      setNewMedication({
        name: '',
        dosage: '',
        frequency: 'daily',
        times: ['08:00'],
        with_food: false,
        condition: '',
        prescriber: ''
      });
      setTimeout(() => setActionMessage(''), 2000);
      
      // Refresh data
      await fetchMedicationData();
      
    } catch (e) {
      setActionMessage(`Error: ${e.message}`);
      setTimeout(() => setActionMessage(''), 3000);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'overdue': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getAdherenceColor = (rate) => {
    if (rate >= 90) return 'text-green-600';
    if (rate >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Medication Reminders</h1>
          <p className="text-gray-600">Stay on track with your medication schedule and health goals</p>
          {actionMessage && (
            <div className="mt-2 p-3 bg-blue-50 border border-blue-200 text-blue-700 rounded-lg">
              {actionMessage}
            </div>
          )}
        </div>

        {loading && (
          <div className="p-6 bg-white rounded-lg border text-gray-600">Loading medication data...</div>
        )}
        
        {error && (
          <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg mb-6">{error}</div>
        )}

        {!loading && !error && (
          <div className="space-y-8">
            {/* Adherence Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <Card className="border-2 border-blue-200 bg-blue-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <TrendingUp className="w-8 h-8 text-blue-600 mr-3" />
                    <div>
                      <div className={`text-2xl font-bold ${getAdherenceColor(adherenceStats.overall_adherence || 0)}`}>
                        {adherenceStats.overall_adherence || 0}%
                      </div>
                      <p className="text-sm text-gray-600">Overall Adherence</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-green-200 bg-green-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Zap className="w-8 h-8 text-green-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-green-600">
                        {adherenceStats.streak_days || 0}
                      </div>
                      <p className="text-sm text-gray-600">Day Streak</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-purple-200 bg-purple-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <Calendar className="w-8 h-8 text-purple-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-purple-600">
                        {adherenceStats.weekly_adherence || 0}%
                      </div>
                      <p className="text-sm text-gray-600">This Week</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
              
              <Card className="border-2 border-orange-200 bg-orange-50">
                <CardContent className="pt-6">
                  <div className="flex items-center">
                    <AlertCircle className="w-8 h-8 text-orange-600 mr-3" />
                    <div>
                      <div className="text-2xl font-bold text-orange-600">
                        {adherenceStats.missed_doses_week || 0}
                      </div>
                      <p className="text-sm text-gray-600">Missed This Week</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Pending Reminders */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Bell className="w-5 h-5 mr-2 text-amber-600" />
                  Pending Reminders
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {reminders.filter(r => r.status === 'pending').map((reminder) => {
                    const medication = medications.find(m => m.id === reminder.medication_id);
                    return (
                      <div key={reminder.id} className="flex items-center justify-between p-4 bg-amber-50 border border-amber-200 rounded-lg">
                        <div className="flex items-center space-x-4">
                          <div className="w-12 h-12 bg-amber-100 rounded-full flex items-center justify-center">
                            <Pill className="w-6 h-6 text-amber-600" />
                          </div>
                          <div>
                            <div className="font-semibold text-gray-900">{medication?.name}</div>
                            <div className="text-sm text-gray-600">{medication?.dosage} • {reminder.time}</div>
                            {medication?.with_food && (
                              <div className="text-xs text-amber-700 mt-1">Take with food</div>
                            )}
                          </div>
                        </div>
                        <div className="flex items-center space-x-3">
                          <div className="text-sm text-gray-500">
                            Due in {reminder.due_in_minutes || 0} minutes
                          </div>
                          <Button 
                            onClick={() => markMedicationTaken(medication?.id, reminder.id)}
                            className="bg-green-600 hover:bg-green-700"
                            size="sm"
                          >
                            <CheckCircle className="w-4 h-4 mr-2" />
                            Mark Taken
                          </Button>
                        </div>
                      </div>
                    );
                  })}
                  {reminders.filter(r => r.status === 'pending').length === 0 && (
                    <div className="text-center py-6 text-gray-500">
                      <CheckCircle className="w-12 h-12 mx-auto mb-2 text-green-500" />
                      <div>All caught up! No pending medication reminders.</div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Active Medications */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <span className="flex items-center">
                      <Pill className="w-5 h-5 mr-2 text-blue-600" />
                      Active Medications
                    </span>
                    <Button onClick={() => setShowAddForm(true)} size="sm" className="bg-blue-600 hover:bg-blue-700">
                      <Plus className="w-4 h-4 mr-2" />
                      Add Medication
                    </Button>
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {medications.filter(m => m.status === 'active').map((medication) => (
                      <div key={medication.id} className="border rounded-lg p-4 hover:bg-gray-50">
                        <div className="flex items-start justify-between mb-3">
                          <div>
                            <div className="font-semibold text-gray-900 text-lg">{medication.name}</div>
                            <div className="text-sm text-gray-600">{medication.dosage} • {medication.frequency}</div>
                            <div className="text-xs text-gray-500 mt-1">
                              For {medication.condition} • Prescribed by {medication.prescriber}
                            </div>
                          </div>
                          <div className="flex space-x-1">
                            <Button variant="ghost" size="sm">
                              <Edit3 className="w-4 h-4" />
                            </Button>
                            <Button variant="ghost" size="sm" className="text-red-500 hover:text-red-700">
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-4 mb-3">
                          <div>
                            <div className="text-xs text-gray-500">Schedule</div>
                            <div className="flex flex-wrap gap-1">
                              {medication.times.map((time, idx) => (
                                <Badge key={idx} variant="secondary">{time}</Badge>
                              ))}
                            </div>
                          </div>
                          <div>
                            <div className="text-xs text-gray-500">Adherence Rate</div>
                            <div className={`font-semibold ${getAdherenceColor(medication.adherence_rate)}`}>
                              {medication.adherence_rate}%
                            </div>
                          </div>
                        </div>
                        
                        <div className="flex items-center justify-between">
                          <div className="text-xs text-gray-500">
                            Last taken: {medication.last_taken}
                          </div>
                          <div className="text-xs text-gray-500">
                            Next due: {medication.next_due}
                          </div>
                        </div>
                        
                        {medication.with_food && (
                          <div className="mt-2 p-2 bg-blue-50 rounded text-sm text-blue-700">
                            💡 Take with food for better absorption
                          </div>
                        )}
                      </div>
                    ))}
                    
                    {medications.filter(m => m.status === 'active').length === 0 && (
                      <div className="text-center py-6 text-gray-500">
                        <Pill className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                        <div>No active medications. Click "Add Medication" to get started.</div>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>

              {/* AI Insights */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Zap className="w-5 h-5 mr-2 text-purple-600" />
                    AI Insights & Tips
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {aiInsights.map((insight, idx) => (
                      <div key={idx} className="p-3 bg-purple-50 rounded-md border-l-4 border-purple-400">
                        <div className="text-sm text-purple-900">{insight}</div>
                      </div>
                    ))}
                    
                    <div className="mt-4 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg">
                      <h4 className="font-semibold text-gray-900 mb-2">💡 Smart Tips</h4>
                      <ul className="text-sm text-gray-700 space-y-1">
                        <li>• Set consistent daily times for better habit formation</li>
                        <li>• Use meal times as natural reminders for food-dependent medications</li>
                        <li>• Track side effects to discuss with your healthcare provider</li>
                      </ul>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}

        {/* Add Medication Modal */}
        {showAddForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <Card className="w-full max-w-md mx-4">
              <CardHeader>
                <CardTitle>Add New Medication</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Medication Name</label>
                  <Input
                    placeholder="e.g., Metformin, Vitamin D..."
                    value={newMedication.name}
                    onChange={(e) => setNewMedication({ ...newMedication, name: e.target.value })}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Dosage</label>
                  <Input
                    placeholder="e.g., 500mg, 1 tablet..."
                    value={newMedication.dosage}
                    onChange={(e) => setNewMedication({ ...newMedication, dosage: e.target.value })}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Frequency</label>
                  <select 
                    className="w-full border border-gray-300 rounded-md px-3 py-2"
                    value={newMedication.frequency}
                    onChange={(e) => setNewMedication({ ...newMedication, frequency: e.target.value })}
                  >
                    <option value="daily">Daily</option>
                    <option value="twice_daily">Twice Daily</option>
                    <option value="three_times_daily">Three Times Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="as_needed">As Needed</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Condition/Purpose</label>
                  <Input
                    placeholder="e.g., Diabetes, Heart Health..."
                    value={newMedication.condition}
                    onChange={(e) => setNewMedication({ ...newMedication, condition: e.target.value })}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Prescriber</label>
                  <Input
                    placeholder="e.g., Dr. Smith, Self-prescribed..."
                    value={newMedication.prescriber}
                    onChange={(e) => setNewMedication({ ...newMedication, prescriber: e.target.value })}
                  />
                </div>
                
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    id="with_food"
                    checked={newMedication.with_food}
                    onChange={(e) => setNewMedication({ ...newMedication, with_food: e.target.checked })}
                    className="rounded"
                  />
                  <label htmlFor="with_food" className="text-sm text-gray-700">Take with food</label>
                </div>
                
                <div className="flex space-x-3 pt-4">
                  <Button onClick={addMedication} className="bg-blue-600 hover:bg-blue-700">
                    Add Medication
                  </Button>
                  <Button variant="outline" onClick={() => setShowAddForm(false)}>
                    Cancel
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default PatientMedicationReminder;