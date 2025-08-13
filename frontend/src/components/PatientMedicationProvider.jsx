import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { 
  AlertTriangle, 
  Shield, 
  Clock, 
  MessageSquare,
  Phone,
  Send,
  CheckCircle,
  XCircle,
  Info
} from 'lucide-react';

const PatientMedicationProvider = ({ patientId = "demo-patient-123" }) => {
  const [medications, setMedications] = useState([]);
  const [emergencyContacts, setEmergencyContacts] = useState([]);
  const [sideEffectForm, setSideEffectForm] = useState({
    medication_id: '',
    medication_name: '',
    side_effect: '',
    severity: 'mild',
    notes: ''
  });
  const [loading, setLoading] = useState(true);
  const [submitStatus, setSubmitStatus] = useState(null);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  useEffect(() => {
    loadMedicationData();
    loadEmergencyContacts();
  }, [patientId]);

  const loadMedicationData = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/patient/medications/${patientId}`);
      const data = await response.json();
      setMedications(data.medications || []);
    } catch (error) {
      console.error('Error loading medications:', error);
    }
  };

  const loadEmergencyContacts = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/provider/medications/emergency-contacts/${patientId}`);
      const data = await response.json();
      setEmergencyContacts(data.emergency_contacts || []);
    } catch (error) {
      console.error('Error loading emergency contacts:', error);
    } finally {
      setLoading(false);
    }
  };

  const reportSideEffect = async () => {
    if (!sideEffectForm.medication_id || !sideEffectForm.side_effect) {
      alert('Please select a medication and describe the side effect');
      return;
    }

    try {
      setSubmitStatus('submitting');
      
      const response = await fetch(`${backendUrl}/api/provider/medications/side-effect-report`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          patient_id: patientId,
          patient_name: "Patient User", // In production, get from user context
          medication_id: sideEffectForm.medication_id,
          medication_name: sideEffectForm.medication_name,
          side_effect: sideEffectForm.side_effect,
          severity: sideEffectForm.severity,
          provider_email: "provider@example.com", // In production, get from patient's provider
          notes: sideEffectForm.notes
        })
      });

      const result = await response.json();
      
      if (result.success) {
        setSubmitStatus('success');
        setSideEffectForm({
          medication_id: '',
          medication_name: '',
          side_effect: '',
          severity: 'mild',
          notes: ''
        });
        
        // Show success message
        setTimeout(() => setSubmitStatus(null), 5000);
      } else {
        setSubmitStatus('error');
        console.error('Failed to report side effect:', result.error);
      }
    } catch (error) {
      setSubmitStatus('error');
      console.error('Error reporting side effect:', error);
    }
  };

  const sendEmergencyAlert = async (alertType) => {
    try {
      const response = await fetch(`${backendUrl}/api/provider/medications/emergency-alert`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          patient_id: patientId,
          alert_type: alertType,
          medication_name: sideEffectForm.medication_name || "Unknown",
          severity: "high",
          notes: `Emergency alert triggered by patient: ${alertType}`
        })
      });

      const result = await response.json();
      
      if (result.success) {
        alert(`Emergency alert sent successfully! ${result.contacts_notified} contacts were notified.`);
      } else {
        alert('Failed to send emergency alert: ' + result.error);
      }
    } catch (error) {
      console.error('Error sending emergency alert:', error);
      alert('Error sending emergency alert');
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

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">Healthcare Provider Connection</h1>
        <p className="text-gray-600 mt-2">Report medication concerns and access emergency support</p>
      </div>

      {/* Side Effect Reporting */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <AlertTriangle className="w-5 h-5 mr-2 text-orange-600" />
            Report Side Effects
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {submitStatus === 'success' && (
            <Alert className="border-green-200 bg-green-50">
              <CheckCircle className="h-4 w-4" />
              <AlertDescription>
                Side effect reported successfully! Your healthcare provider has been notified and will follow up as needed.
              </AlertDescription>
            </Alert>
          )}

          {submitStatus === 'error' && (
            <Alert className="border-red-200 bg-red-50">
              <XCircle className="h-4 w-4" />
              <AlertDescription>
                Failed to submit side effect report. Please try again or contact your provider directly.
              </AlertDescription>
            </Alert>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select Medication
              </label>
              <Select 
                value={sideEffectForm.medication_id}
                onValueChange={(value) => {
                  const med = medications.find(m => m.id === value);
                  setSideEffectForm({
                    ...sideEffectForm,
                    medication_id: value,
                    medication_name: med?.name || ''
                  });
                }}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Choose medication..." />
                </SelectTrigger>
                <SelectContent>
                  {medications.map((med) => (
                    <SelectItem key={med.id} value={med.id}>
                      {med.name} ({med.dosage})
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Severity Level
              </label>
              <Select 
                value={sideEffectForm.severity}
                onValueChange={(value) => setSideEffectForm({...sideEffectForm, severity: value})}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="mild">Mild - Minor discomfort</SelectItem>
                  <SelectItem value="moderate">Moderate - Noticeable effects</SelectItem>
                  <SelectItem value="severe">Severe - Serious concern</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Describe the Side Effect
            </label>
            <Textarea
              placeholder="Please describe what you experienced (e.g., nausea, dizziness, rash)..."
              value={sideEffectForm.side_effect}
              onChange={(e) => setSideEffectForm({...sideEffectForm, side_effect: e.target.value})}
              rows={3}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Additional Notes (Optional)
            </label>
            <Textarea
              placeholder="Any additional details about timing, duration, or circumstances..."
              value={sideEffectForm.notes}
              onChange={(e) => setSideEffectForm({...sideEffectForm, notes: e.target.value})}
              rows={2}
            />
          </div>

          <div className="flex gap-2">
            <Button 
              onClick={reportSideEffect}
              disabled={submitStatus === 'submitting'}
              className="bg-orange-600 hover:bg-orange-700"
            >
              {submitStatus === 'submitting' ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Submitting...
                </>
              ) : (
                <>
                  <Send className="w-4 h-4 mr-2" />
                  Report Side Effect
                </>
              )}
            </Button>
            
            {sideEffectForm.severity === 'severe' && (
              <Button 
                onClick={() => sendEmergencyAlert('severe_reaction')}
                variant="destructive"
              >
                <AlertTriangle className="w-4 h-4 mr-2" />
                Send Emergency Alert
              </Button>
            )}
          </div>

          {sideEffectForm.severity === 'severe' && (
            <Alert className="border-red-200 bg-red-50">
              <AlertTriangle className="h-4 w-4" />
              <AlertDescription>
                <strong>Severe side effects require immediate attention.</strong> 
                Your provider will be notified immediately. If this is life-threatening, call 911 or go to the nearest emergency room.
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>

      {/* Emergency Contacts */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Phone className="w-5 h-5 mr-2 text-red-600" />
            Emergency Contacts
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {emergencyContacts.map((contact, index) => (
              <div key={index} className="border rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h3 className="font-semibold text-gray-900">{contact.name}</h3>
                    <p className="text-sm text-gray-600">{contact.role}</p>
                  </div>
                  <Badge variant={contact.priority === 1 ? 'destructive' : 'secondary'}>
                    Priority {contact.priority}
                  </Badge>
                </div>
                
                <div className="space-y-1 text-sm">
                  <div className="flex items-center">
                    <Phone className="w-4 h-4 mr-2 text-gray-500" />
                    <span>{contact.phone}</span>
                  </div>
                  {contact.email && (
                    <div className="flex items-center">
                      <MessageSquare className="w-4 h-4 mr-2 text-gray-500" />
                      <span>{contact.email}</span>
                    </div>
                  )}
                  <div className="flex items-center">
                    <Clock className="w-4 h-4 mr-2 text-gray-500" />
                    <span>{contact.available_hours}</span>
                  </div>
                  {contact.after_hours_phone && (
                    <div className="flex items-center">
                      <Phone className="w-4 h-4 mr-2 text-gray-500" />
                      <span>After hours: {contact.after_hours_phone}</span>
                    </div>
                  )}
                </div>

                <div className="mt-3 flex gap-2">
                  <Button size="sm" variant="outline" onClick={() => window.open(`tel:${contact.phone}`)}>
                    <Phone className="w-4 h-4 mr-1" />
                    Call
                  </Button>
                  {contact.email && (
                    <Button size="sm" variant="outline" onClick={() => window.open(`mailto:${contact.email}`)}>
                      <MessageSquare className="w-4 h-4 mr-1" />
                      Email
                    </Button>
                  )}
                </div>
              </div>
            ))}
          </div>

          <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-start">
              <AlertTriangle className="w-5 h-5 mr-2 text-red-600 mt-0.5" />
              <div className="flex-1">
                <h3 className="font-medium text-red-800 mb-2">Emergency Situations</h3>
                <div className="space-y-2 text-sm text-red-700">
                  <p><strong>Call 911 immediately if you experience:</strong></p>
                  <ul className="list-disc list-inside space-y-1 ml-4">
                    <li>Difficulty breathing or swallowing</li>
                    <li>Severe allergic reaction (swelling, hives)</li>
                    <li>Chest pain or heart palpitations</li>
                    <li>Loss of consciousness or severe dizziness</li>
                    <li>Severe bleeding or inability to stop bleeding</li>
                  </ul>
                </div>
                
                <div className="mt-4 flex gap-2">
                  <Button 
                    size="sm" 
                    variant="destructive"
                    onClick={() => sendEmergencyAlert('severe_reaction')}
                  >
                    <AlertTriangle className="w-4 h-4 mr-1" />
                    Alert All Contacts
                  </Button>
                  <Button 
                    size="sm" 
                    variant="outline"
                    onClick={() => window.open('tel:911')}
                  >
                    <Phone className="w-4 h-4 mr-1" />
                    Call 911
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Medication Adherence Support */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Shield className="w-5 h-5 mr-2 text-blue-600" />
            Medication Adherence Support
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-medium mb-3">Quick Actions</h3>
              <div className="space-y-2">
                <Button 
                  variant="outline" 
                  className="w-full justify-start"
                  onClick={() => alert('Medication reminder feature would be implemented here')}
                >
                  <Clock className="w-4 h-4 mr-2" />
                  Set Medication Reminders
                </Button>
                <Button 
                  variant="outline" 
                  className="w-full justify-start"
                  onClick={() => sendEmergencyAlert('missed_critical_dose')}
                >
                  <AlertTriangle className="w-4 h-4 mr-2" />
                  Report Missed Critical Doses
                </Button>
                <Button 
                  variant="outline" 
                  className="w-full justify-start"
                  onClick={() => alert('Provider messaging feature would be implemented here')}
                >
                  <MessageSquare className="w-4 h-4 mr-2" />
                  Ask Provider Question
                </Button>
              </div>
            </div>
            
            <div>
              <h3 className="font-medium mb-3">Adherence Tips</h3>
              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex items-start">
                  <Info className="w-4 h-4 mr-2 text-blue-500 mt-0.5" />
                  <span>Take medications at the same time each day</span>
                </div>
                <div className="flex items-start">
                  <Info className="w-4 h-4 mr-2 text-blue-500 mt-0.5" />
                  <span>Use a pill organizer for multiple medications</span>
                </div>
                <div className="flex items-start">
                  <Info className="w-4 h-4 mr-2 text-blue-500 mt-0.5" />
                  <span>Set phone alarms or use medication apps</span>
                </div>
                <div className="flex items-start">
                  <Info className="w-4 h-4 mr-2 text-blue-500 mt-0.5" />
                  <span>Keep a medication log or diary</span>
                </div>
                <div className="flex items-start">
                  <Info className="w-4 h-4 mr-2 text-blue-500 mt-0.5" />
                  <span>Don't stop medications without consulting your provider</span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default PatientMedicationProvider;