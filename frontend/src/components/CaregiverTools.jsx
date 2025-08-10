import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Progress } from './ui/progress';
import { 
  Shield, Phone, AlertTriangle, Heart, Clock, MapPin,
  Pill, FileText, Users, Eye, Edit, Plus, Copy,
  Stethoscope, Activity, TrendingUp, Calendar, Bell
} from 'lucide-react';

const CaregiverTools = () => {
  const { switchRole } = useRole();
  const [caregiverData, setCaregiverData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    switchRole('family');
    fetchCaregiverData();
  }, [switchRole]);

  const fetchCaregiverData = async () => {
    try {
      const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/family/caregiver-tools/demo-family-123`);
      const data = await response.json();
      setCaregiverData(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching caregiver data:', error);
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'as_needed': return 'bg-yellow-100 text-yellow-800';
      case 'scheduled': return 'bg-blue-100 text-blue-800';
      case 'reminder_set': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
        <SmartNavigation />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center">Loading caregiver tools...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Advanced Caregiver Tools</h1>
          <p className="text-gray-600">Comprehensive tools for family care coordination and emergency management</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-2 border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Shield className="w-8 h-8 text-red-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-red-600">
                    {caregiverData?.emergency_management?.emergency_contacts?.length || 0}
                  </div>
                  <p className="text-sm text-gray-600">Emergency Contacts</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-purple-200 bg-purple-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Pill className="w-8 h-8 text-purple-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-purple-600">
                    {caregiverData?.medication_management?.current_medications?.length || 0}
                  </div>
                  <p className="text-sm text-gray-600">Active Medications</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-blue-200 bg-blue-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Stethoscope className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-blue-600">
                    {caregiverData?.health_monitoring?.wellness_checks?.length || 0}
                  </div>
                  <p className="text-sm text-gray-600">Health Monitors</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-green-200 bg-green-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Users className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-green-600">
                    {caregiverData?.care_coordination?.shared_tasks?.length || 0}
                  </div>
                  <p className="text-sm text-gray-600">Care Tasks</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="emergency" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="emergency">Emergency</TabsTrigger>
            <TabsTrigger value="medications">Medications</TabsTrigger>
            <TabsTrigger value="health">Health Monitoring</TabsTrigger>
            <TabsTrigger value="coordination">Coordination</TabsTrigger>
          </TabsList>

          {/* Emergency Management Tab */}
          <TabsContent value="emergency" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Emergency Contacts */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <div className="flex items-center">
                      <Phone className="w-5 h-5 mr-2 text-red-500" />
                      Emergency Contacts
                    </div>
                    <Button size="sm" className="bg-red-500 hover:bg-red-600">
                      <Plus className="w-4 h-4 mr-2" />
                      Add Contact
                    </Button>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {caregiverData?.emergency_management?.emergency_contacts?.map((contact, index) => (
                    <div key={index} className="border-l-4 border-red-500 bg-red-50 rounded-lg p-4">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="font-semibold text-red-900">{contact.name}</div>
                          <div className="text-sm text-red-700">{contact.relationship}</div>
                          <div className="text-sm font-mono text-red-800 mt-1">{contact.phone}</div>
                          <div className="text-xs text-red-600 mt-2">{contact.availability}</div>
                          
                          {/* Special capabilities */}
                          <div className="flex flex-wrap gap-1 mt-2">
                            {contact.medical_authority && (
                              <Badge className="bg-red-200 text-red-800 text-xs">Medical Authority</Badge>
                            )}
                            {contact.key_holder && (
                              <Badge className="bg-blue-200 text-blue-800 text-xs">Key Holder</Badge>
                            )}
                          </div>
                          
                          {contact.special_instructions && (
                            <div className="text-xs text-red-700 mt-2 p-2 bg-red-100 rounded">
                              {contact.special_instructions}
                            </div>
                          )}
                        </div>
                        
                        <div className="flex flex-col space-y-2">
                          <Button size="sm" className="bg-red-500 hover:bg-red-600">
                            <Phone className="w-4 h-4 mr-1" />
                            Call
                          </Button>
                          <Button size="sm" variant="outline">
                            <Edit className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              {/* Healthcare Providers */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Stethoscope className="w-5 h-5 mr-2 text-blue-500" />
                    Healthcare Providers
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {caregiverData?.emergency_management?.healthcare_providers && 
                   Object.entries(caregiverData.emergency_management.healthcare_providers).map(([type, provider]) => (
                    <div key={type} className="border-l-4 border-blue-500 bg-blue-50 rounded-lg p-4">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-semibold text-blue-900 capitalize">
                            {type.replace('_', ' ')}
                          </div>
                          <div className="text-sm text-blue-700">{provider.name}</div>
                          {provider.phone && (
                            <div className="text-sm font-mono text-blue-800">{provider.phone}</div>
                          )}
                          {provider.available && (
                            <div className="text-xs text-blue-600 mt-1">{provider.available}</div>
                          )}
                          {provider.address && (
                            <div className="text-xs text-blue-600">{provider.address}</div>
                          )}
                        </div>
                        <Button size="sm" className="bg-blue-500 hover:bg-blue-600">
                          <Phone className="w-4 h-4 mr-1" />
                          Contact
                        </Button>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>

            {/* Medical Information */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <FileText className="w-5 h-5 mr-2 text-green-500" />
                  Family Medical Information
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {caregiverData?.emergency_management?.medical_information && 
                   Object.entries(caregiverData.emergency_management.medical_information).map(([member, info]) => (
                    <div key={member} className="border rounded-lg p-4">
                      <div className="font-semibold text-gray-900 mb-3">{member}</div>
                      
                      {/* Allergies */}
                      <div className="mb-3">
                        <div className="text-sm font-medium text-gray-700">Allergies:</div>
                        <div className="text-sm text-gray-600">
                          {info.allergies?.join(', ') || 'None'}
                        </div>
                      </div>
                      
                      {/* Medications */}
                      <div className="mb-3">
                        <div className="text-sm font-medium text-gray-700">Medications:</div>
                        <div className="text-sm text-gray-600">
                          {info.medications?.join(', ') || 'None'}
                        </div>
                      </div>
                      
                      {/* Emergency Protocols */}
                      {info.emergency_protocols && (
                        <div className="mb-3">
                          <div className="text-sm font-medium text-red-700">Emergency Protocols:</div>
                          <ul className="text-sm text-red-600 list-disc list-inside">
                            {info.emergency_protocols.map((protocol, idx) => (
                              <li key={idx}>{protocol}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {/* Insurance */}
                      {info.insurance && (
                        <div className="p-2 bg-blue-50 rounded text-sm">
                          <div className="font-medium text-blue-900">{info.insurance.provider}</div>
                          <div className="text-blue-700">Policy: {info.insurance.policy}</div>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Medication Management Tab */}
          <TabsContent value="medications" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Current Medications */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    <div className="flex items-center">
                      <Pill className="w-5 h-5 mr-2 text-purple-500" />
                      Current Medications
                    </div>
                    <Button size="sm" className="bg-purple-500 hover:bg-purple-600">
                      <Plus className="w-4 h-4 mr-2" />
                      Add Medication
                    </Button>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {caregiverData?.medication_management?.current_medications?.map((med, index) => (
                    <div key={index} className="border rounded-lg p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <div className="font-semibold text-gray-900">{med.member}</div>
                          <div className="text-lg text-purple-600">{med.medication}</div>
                          <div className="text-sm text-gray-600">{med.dosage}</div>
                          {med.condition && (
                            <div className="text-sm text-gray-500">For: {med.condition}</div>
                          )}
                        </div>
                        <Badge className={getStatusColor(med.reminder_enabled ? 'active' : 'inactive')}>
                          {med.reminder_enabled ? 'Reminder On' : 'No Reminder'}
                        </Badge>
                      </div>

                      {/* Schedule */}
                      <div className="grid grid-cols-2 gap-4 mb-3">
                        <div>
                          <div className="text-sm font-medium text-gray-700">Schedule:</div>
                          <div className="text-sm text-gray-600">{med.time}</div>
                        </div>
                        <div>
                          <div className="text-sm font-medium text-gray-700">Refill Date:</div>
                          <div className="text-sm text-gray-600">{med.refill_date}</div>
                        </div>
                      </div>

                      {/* Special Instructions */}
                      {med.side_effects_to_watch && (
                        <div className="p-2 bg-yellow-50 rounded border-l-2 border-yellow-400 mb-3">
                          <div className="text-sm font-medium text-yellow-800">Watch for side effects:</div>
                          <div className="text-sm text-yellow-700">
                            {med.side_effects_to_watch.join(', ')}
                          </div>
                        </div>
                      )}

                      {med.training_needed && (
                        <div className="p-2 bg-red-50 rounded border-l-2 border-red-400 mb-3">
                          <div className="text-sm font-medium text-red-800">Training needed:</div>
                          <div className="text-sm text-red-700">
                            {med.training_needed.join(', ')}
                          </div>
                        </div>
                      )}

                      {/* Actions */}
                      <div className="flex space-x-2 pt-2 border-t">
                        <Button size="sm" variant="outline">
                          <Edit className="w-4 h-4 mr-1" />
                          Edit
                        </Button>
                        <Button size="sm" className="bg-purple-500 hover:bg-purple-600">
                          <Bell className="w-4 h-4 mr-1" />
                          Set Reminder
                        </Button>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              {/* Medication Adherence */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <TrendingUp className="w-5 h-5 mr-2 text-green-500" />
                    Medication Adherence
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {caregiverData?.medication_management?.medication_adherence && 
                   Object.entries(caregiverData.medication_management.medication_adherence).map(([member, adherence]) => (
                    <div key={member} className="border rounded-lg p-4">
                      <div className="font-semibold text-gray-900 mb-3">{member}</div>
                      
                      <div className="space-y-3">
                        <div className="flex items-center justify-between">
                          <span className="text-sm text-gray-600">Compliance Rate</span>
                          <span className="font-semibold text-green-600">{adherence.compliance_rate}%</span>
                        </div>
                        <Progress value={adherence.compliance_rate} className="w-full h-2" />
                        
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <span className="text-gray-600">Missed Doses:</span>
                            <span className="font-medium ml-2">{adherence.missed_doses}</span>
                          </div>
                          <div>
                            <span className="text-gray-600">Current Streak:</span>
                            <span className="font-medium ml-2">{adherence.streak} days</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>

            {/* Refill Management */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Clock className="w-5 h-5 mr-2 text-orange-500" />
                  Refill Management
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {caregiverData?.medication_management?.refill_management?.map((refill, index) => (
                    <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                      <div>
                        <div className="font-medium text-gray-900">{refill.medication}</div>
                        <div className="text-sm text-gray-600">Due: {refill.due_date}</div>
                      </div>
                      <div className="flex items-center space-x-3">
                        <Badge className={getStatusColor(refill.status)}>
                          {refill.status.replace('_', ' ')}
                        </Badge>
                        <Button size="sm" className="bg-orange-500 hover:bg-orange-600">
                          {refill.auto_refill ? 'Auto-Refill On' : 'Order Refill'}
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Health Monitoring Tab */}
          <TabsContent value="health" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Wellness Checks */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Heart className="w-5 h-5 mr-2 text-red-500" />
                    Wellness Monitoring
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {caregiverData?.health_monitoring?.wellness_checks?.map((check, index) => (
                    <div key={index} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <div className="font-medium text-gray-900">{check.member}</div>
                        <Badge className="bg-blue-100 text-blue-800">{check.frequency}</Badge>
                      </div>
                      <div className="text-sm text-gray-600 mb-2">{check.type.replace('_', ' ')}</div>
                      <div className="text-xs text-gray-500">Last entry: {check.last_entry}</div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              {/* Symptom Tracking */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Activity className="w-5 h-5 mr-2 text-orange-500" />
                    Symptom Tracking
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {caregiverData?.health_monitoring?.symptom_tracking && 
                   Object.entries(caregiverData.health_monitoring.symptom_tracking).map(([member, tracking]) => (
                    <div key={member} className="border rounded-lg p-4">
                      <div className="font-medium text-gray-900 mb-2">{member}</div>
                      <div className="space-y-2 text-sm">
                        <div>
                          <span className="text-gray-600">Symptoms:</span>
                          <span className="ml-2">{tracking.tracked_symptoms?.join(', ')}</span>
                        </div>
                        <div>
                          <span className="text-gray-600">Triggers:</span>
                          <span className="ml-2">{tracking.triggers?.join(', ')}</span>
                        </div>
                        <div className="p-2 bg-blue-50 rounded">
                          <div className="text-blue-800 font-medium">Patterns:</div>
                          <div className="text-blue-700">{tracking.patterns}</div>
                        </div>
                        <div className="p-2 bg-green-50 rounded">
                          <div className="text-green-800 font-medium">Improvements:</div>
                          <div className="text-green-700">{tracking.improvements}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>

            {/* Growth Tracking */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2 text-green-500" />
                  Growth Tracking
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {caregiverData?.health_monitoring?.growth_tracking && 
                   Object.entries(caregiverData.health_monitoring.growth_tracking).map(([member, growth]) => (
                    <div key={member} className="border rounded-lg p-4">
                      <div className="font-semibold text-gray-900 mb-3">{member}</div>
                      
                      <div className="space-y-3">
                        <div className="grid grid-cols-2 gap-4">
                          <div className="p-3 bg-blue-50 rounded">
                            <div className="text-sm font-medium text-blue-900">Height</div>
                            <div className="text-lg font-bold text-blue-600">{growth.height?.current}</div>
                            <div className="text-xs text-blue-700">
                              {growth.height?.percentile} percentile
                            </div>
                          </div>
                          <div className="p-3 bg-green-50 rounded">
                            <div className="text-sm font-medium text-green-900">Weight</div>
                            <div className="text-lg font-bold text-green-600">{growth.weight?.current}</div>
                            <div className="text-xs text-green-700">
                              {growth.weight?.percentile} percentile
                            </div>
                          </div>
                        </div>
                        
                        <div className="text-sm text-gray-600">
                          Next measurement: {growth.next_measurement}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Care Coordination Tab */}
          <TabsContent value="coordination" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Shared Tasks */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Users className="w-5 h-5 mr-2 text-green-500" />
                    Shared Care Tasks
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {caregiverData?.care_coordination?.shared_tasks?.map((task, index) => (
                    <div key={index} className="border rounded-lg p-3">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-medium text-gray-900">{task.task}</div>
                          <div className="text-sm text-gray-600">
                            Assigned: {task.assigned_to} • Backup: {task.backup}
                          </div>
                          <div className="text-xs text-gray-500">{task.frequency}</div>
                        </div>
                        <Button size="sm" variant="outline">
                          <Edit className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              {/* Communication Hub */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Phone className="w-5 h-5 mr-2 text-blue-500" />
                    Communication Hub
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {caregiverData?.care_coordination?.communication_hub && (
                    <>
                      <div className="p-3 bg-blue-50 rounded-lg">
                        <div className="font-medium text-blue-900">Family Chat</div>
                        <div className="text-sm text-blue-700">
                          Status: {caregiverData.care_coordination.communication_hub.family_chat?.enabled ? 'Active' : 'Inactive'}
                        </div>
                      </div>
                      
                      <div className="p-3 bg-green-50 rounded-lg">
                        <div className="font-medium text-green-900">Provider Communication</div>
                        <div className="text-sm text-green-700">
                          Secure portal: {caregiverData.care_coordination.communication_hub.provider_communication ? 'Connected' : 'Not connected'}
                        </div>
                        {caregiverData.care_coordination.communication_hub.recent_messages && (
                          <div className="text-xs text-green-600">
                            {caregiverData.care_coordination.communication_hub.recent_messages} recent messages
                          </div>
                        )}
                      </div>
                      
                      {caregiverData.care_coordination.communication_hub.school_nurse_contact && (
                        <div className="p-3 bg-purple-50 rounded-lg">
                          <div className="font-medium text-purple-900">School Nurse</div>
                          <div className="text-sm text-purple-700">
                            {caregiverData.care_coordination.communication_hub.school_nurse_contact.name}
                          </div>
                          <div className="text-xs text-purple-600">
                            {caregiverData.care_coordination.communication_hub.school_nurse_contact.phone}
                          </div>
                        </div>
                      )}
                    </>
                  )}
                </CardContent>
              </Card>
            </div>

            {/* Document Management */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <FileText className="w-5 h-5 mr-2 text-orange-500" />
                  Document Management
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {caregiverData?.care_coordination?.document_management && 
                   Object.entries(caregiverData.care_coordination.document_management).map(([docType, info]) => (
                    <div key={docType} className="border rounded-lg p-4">
                      <div className="font-medium text-gray-900 mb-2 capitalize">
                        {docType.replace('_', ' ')}
                      </div>
                      <div className="space-y-2 text-sm">
                        <div>
                          <span className="text-gray-600">Location:</span>
                          <span className="ml-2 text-gray-800">{info.location}</span>
                        </div>
                        <div>
                          <span className="text-gray-600">Last Updated:</span>
                          <span className="ml-2 text-gray-800">{info.last_updated}</span>
                        </div>
                        {info.expiration && (
                          <div>
                            <span className="text-gray-600">Expires:</span>
                            <span className="ml-2 text-gray-800">{info.expiration}</span>
                          </div>
                        )}
                        {info.review_due && (
                          <div>
                            <span className="text-gray-600">Review Due:</span>
                            <span className="ml-2 text-orange-600">{info.review_due}</span>
                          </div>
                        )}
                      </div>
                      <Button size="sm" variant="outline" className="w-full mt-3">
                        <Eye className="w-4 h-4 mr-2" />
                        View Document
                      </Button>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default CaregiverTools;