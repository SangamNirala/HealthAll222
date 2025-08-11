import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';

// Import existing components
import PatientMedicationReminder from './PatientMedicationReminder';
import SmartReminders from './medications/SmartReminders';

import { 
  Pill, 
  Brain,
  Clock, 
  Bell,
  Settings,
  TrendingUp,
  User,
  Utensils
} from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

const getPatientUserId = () => {
  try {
    const saved = localStorage.getItem('patient_user_id');
    if (saved && typeof saved === 'string' && saved.trim().length > 0) return saved;
  } catch (e) {}
  return 'demo-patient-123';
};

/**
 * Enhanced Medication Management with Smart Reminders Integration
 * This demonstrates how SmartReminders can be plugged into existing functionality
 */
const EnhancedMedicationManager = () => {
  const { switchRole } = useRole();
  const [userId, setUserId] = useState(getPatientUserId());
  const [activeTab, setActiveTab] = useState('traditional');
  const [loading, setLoading] = useState(false);
  
  // Medication data state
  const [medications, setMedications] = useState([]);
  const [adherenceData, setAdherenceData] = useState([]);
  const [smartRemindersEnabled, setSmartRemindersEnabled] = useState(false);
  
  // User preferences for smart reminders
  const [userPreferences, setUserPreferences] = useState({
    mealTimes: {
      BREAKFAST: { start: '06:00', end: '10:00', optimal: '08:00' },
      LUNCH: { start: '11:00', end: '15:00', optimal: '12:30' },
      DINNER: { start: '17:00', end: '21:00', optimal: '18:30' },
      BEDTIME: { start: '21:00', end: '23:59', optimal: '22:00' }
    },
    sleepSchedule: { 
      bedtime: '22:00', 
      wakeup: '07:00' 
    },
    snoozePreference: 'PROGRESSIVE',
    emergencyContacts: [
      { name: 'Dr. Smith', phone: '+1-555-0123', relationship: 'Primary Care' },
      { name: 'Emergency Contact', phone: '+1-555-0911', relationship: 'Family' }
    ]
  });

  useEffect(() => {
    switchRole('patient');
    setUserId(getPatientUserId());
  }, [switchRole]);

  useEffect(() => {
    fetchMedicationData();
    generateMockAdherenceData();
  }, [userId]);

  const fetchMedicationData = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/patient/medications/${userId}`);
      const data = await response.json();
      
      if (response.ok) {
        setMedications(data.medications || []);
      }
    } catch (e) {
      console.error('Failed to fetch medications:', e);
    } finally {
      setLoading(false);
    }
  };

  // Generate mock adherence data for demonstration
  const generateMockAdherenceData = () => {
    const mockData = [];
    const now = new Date();
    
    // Generate 30 days of mock adherence data
    for (let i = 0; i < 30; i++) {
      const date = new Date(now);
      date.setDate(date.getDate() - i);
      
      // Mock data for different medications
      const medicationIds = ['med_001', 'med_002'];
      
      medicationIds.forEach(medId => {
        // Morning dose
        mockData.push({
          medication_id: medId,
          scheduled_time: new Date(date.setHours(8, 0, 0, 0)).toISOString(),
          actual_time: Math.random() > 0.15 
            ? new Date(date.setHours(8, Math.floor(Math.random() * 30), 0, 0)).toISOString()
            : null,
          taken: Math.random() > 0.15,
          delay_minutes: Math.random() > 0.5 ? Math.floor(Math.random() * 45) : 0,
          reason_missed: Math.random() > 0.85 ? 'Forgot' : null
        });
        
        // Evening dose for twice daily medications
        if (medId === 'med_001') {
          mockData.push({
            medication_id: medId,
            scheduled_time: new Date(date.setHours(20, 0, 0, 0)).toISOString(),
            actual_time: Math.random() > 0.1 
              ? new Date(date.setHours(20, Math.floor(Math.random() * 30), 0, 0)).toISOString()
              : null,
            taken: Math.random() > 0.1,
            delay_minutes: Math.random() > 0.5 ? Math.floor(Math.random() * 60) : 0,
            reason_missed: Math.random() > 0.9 ? 'Side effects' : null
          });
        }
      });
    }
    
    setAdherenceData(mockData);
  };

  // Handle smart reminder updates
  const handleSmartReminderUpdate = (updateData) => {
    console.log('Smart Reminder Update:', updateData);
    
    // In a real app, you would sync this with your backend
    switch (updateData.type) {
      case 'SNOOZE':
        console.log('Smart snooze applied:', updateData.snoozeData);
        break;
      case 'ESCALATION':
        console.log('Emergency escalation triggered:', updateData.escalationData);
        break;
      default:
        console.log('Other reminder update:', updateData);
    }
  };

  // Handle schedule changes from smart reminders
  const handleScheduleChange = (schedules) => {
    console.log('Smart schedules updated:', schedules);
    // In a real app, you would update the backend with new optimal times
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Enhanced Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Enhanced Medication Management
              </h1>
              <p className="text-gray-600">
                Traditional reminders enhanced with AI-powered smart scheduling
              </p>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="text-right text-sm">
                <div className="font-medium text-gray-900">Smart Features</div>
                <div className={`text-xs ${smartRemindersEnabled ? 'text-green-600' : 'text-gray-500'}`}>
                  {smartRemindersEnabled ? 'Active' : 'Available'}
                </div>
              </div>
              <Button
                onClick={() => setSmartRemindersEnabled(!smartRemindersEnabled)}
                variant={smartRemindersEnabled ? "default" : "outline"}
                className={smartRemindersEnabled ? "bg-green-600 hover:bg-green-700" : ""}
              >
                <Brain className="w-4 h-4 mr-2" />
                {smartRemindersEnabled ? 'Smart Mode On' : 'Enable Smart Mode'}
              </Button>
            </div>
          </div>

          {/* Feature Comparison */}
          <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card className="border-2 border-blue-200">
              <CardContent className="pt-4">
                <div className="flex items-center mb-2">
                  <Bell className="w-5 h-5 mr-2 text-blue-600" />
                  <span className="font-medium">Traditional Reminders</span>
                </div>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Fixed reminder times</li>
                  <li>• Manual scheduling</li>
                  <li>• Basic snooze functionality</li>
                  <li>• Standard notifications</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="border-2 border-purple-200">
              <CardContent className="pt-4">
                <div className="flex items-center mb-2">
                  <Brain className="w-5 h-5 mr-2 text-purple-600" />
                  <span className="font-medium">Smart Reminders</span>
                  {smartRemindersEnabled && <Badge className="ml-2 bg-green-100 text-green-800">Active</Badge>}
                </div>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>• Meal-timing optimization</li>
                  <li>• Adaptive learning from patterns</li>
                  <li>• Intelligent snooze algorithms</li>
                  <li>• Emergency escalation protocols</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Tabbed Interface */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-2 lg:w-auto">
            <TabsTrigger value="traditional" className="flex items-center">
              <Clock className="w-4 h-4 mr-2" />
              Traditional View
            </TabsTrigger>
            <TabsTrigger value="smart" className="flex items-center">
              <Brain className="w-4 h-4 mr-2" />
              Smart Reminders
            </TabsTrigger>
          </TabsList>

          {/* Traditional Medication Reminder View */}
          <TabsContent value="traditional">
            <div className="bg-white rounded-lg border p-1">
              <PatientMedicationReminder />
            </div>
          </TabsContent>

          {/* Smart Reminders View */}
          <TabsContent value="smart">
            {smartRemindersEnabled ? (
              <SmartReminders
                medications={medications}
                adherenceData={adherenceData}
                userPreferences={userPreferences}
                onReminderUpdate={handleSmartReminderUpdate}
                onScheduleChange={handleScheduleChange}
              />
            ) : (
              <Card className="border-2 border-gray-200">
                <CardContent className="p-12 text-center">
                  <Brain className="w-16 h-16 mx-auto mb-4 text-gray-400" />
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    Smart Reminders Available
                  </h3>
                  <p className="text-gray-600 mb-6 max-w-md mx-auto">
                    Enable smart reminders to get AI-powered medication scheduling that learns 
                    from your patterns and optimizes timing around your meals and lifestyle.
                  </p>
                  <Button 
                    onClick={() => setSmartRemindersEnabled(true)}
                    className="bg-purple-600 hover:bg-purple-700"
                  >
                    <Brain className="w-4 h-4 mr-2" />
                    Enable Smart Reminders
                  </Button>
                  
                  <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-2xl mx-auto">
                    <div className="text-left p-4 bg-blue-50 rounded-lg">
                      <Utensils className="w-6 h-6 text-blue-600 mb-2" />
                      <div className="font-medium text-blue-900">Meal Optimization</div>
                      <div className="text-sm text-blue-700">
                        Automatically schedules medications around your meal times
                      </div>
                    </div>
                    <div className="text-left p-4 bg-green-50 rounded-lg">
                      <TrendingUp className="w-6 h-6 text-green-600 mb-2" />
                      <div className="font-medium text-green-900">Adaptive Learning</div>
                      <div className="text-sm text-green-700">
                        Learns from your adherence patterns to optimize timing
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        </Tabs>

        {/* Integration Demo Info */}
        {smartRemindersEnabled && (
          <Card className="mt-6 border-2 border-green-200 bg-green-50">
            <CardContent className="p-4">
              <div className="flex items-center mb-2">
                <Settings className="w-5 h-5 mr-2 text-green-600" />
                <span className="font-medium text-green-900">Integration Demo</span>
              </div>
              <div className="text-sm text-green-800">
                This demonstrates how SmartReminders seamlessly integrates with existing medication management. 
                The component is designed to be pluggable and doesn't interfere with current functionality.
              </div>
              <div className="mt-3 flex flex-wrap gap-2">
                <Badge variant="secondary">Reusable Component</Badge>
                <Badge variant="secondary">Non-Breaking Integration</Badge>
                <Badge variant="secondary">Configurable Preferences</Badge>
                <Badge variant="secondary">Mock Data for Demo</Badge>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default EnhancedMedicationManager;