import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { 
  AlertTriangle, Phone, Users, Heart, MapPin, 
  Clock, Plus, Edit, Trash2, Shield, Info,
  PhoneCall, Mail, Home, Activity, AlertCircle
} from 'lucide-react';

// Emergency Quick Access Component - Smaller and lighter colors
const EmergencyQuickAccess = ({ onCallEmergency, onViewContacts, onAlertContacts }) => (
  <div className="grid grid-cols-2 gap-3 mb-4">
    <Button 
      onClick={onCallEmergency}
      className="h-12 bg-red-500 hover:bg-red-600 text-white font-semibold"
    >
      <PhoneCall className="w-4 h-4 mr-2" />
      Call 911
    </Button>
    <Button 
      onClick={onViewContacts}
      className="h-12 bg-orange-400 hover:bg-orange-500 text-white font-semibold"
    >
      <Users className="w-4 h-4 mr-2" />
      Contacts
    </Button>
    <Button 
      onClick={onAlertContacts}
      className="h-12 bg-yellow-500 hover:bg-yellow-600 text-white font-semibold"
    >
      <AlertTriangle className="w-4 h-4 mr-2" />
      Alert All
    </Button>
    <Button 
      className="h-12 bg-blue-500 hover:bg-blue-600 text-white font-semibold"
    >
      <MapPin className="w-4 h-4 mr-2" />
      Hospitals
    </Button>
  </div>
);

// Emergency Contact Item Component
const EmergencyContactItem = ({ contact, onEdit, onDelete, onCall }) => (
  <div className="p-4 bg-gray-50 rounded-lg border-l-4 border-red-500">
    <div className="flex justify-between items-start mb-2">
      <div className="flex-1">
        <div className="flex items-center space-x-2 mb-1">
          <span className="font-semibold text-gray-900">{contact.contact_name}</span>
          {contact.is_primary_contact && (
            <Badge className="bg-red-100 text-red-800 text-xs">Primary</Badge>
          )}
          {contact.medical_authorization && (
            <Badge className="bg-blue-100 text-blue-800 text-xs">Medical Auth</Badge>
          )}
        </div>
        <div className="text-sm text-gray-600 mb-1">{contact.relationship}</div>
        <div className="flex items-center text-sm text-gray-700">
          <Phone className="w-4 h-4 mr-1" />
          {contact.primary_phone}
        </div>
        {contact.email && (
          <div className="flex items-center text-sm text-gray-700 mt-1">
            <Mail className="w-4 h-4 mr-1" />
            {contact.email}
          </div>
        )}
      </div>
      <div className="flex space-x-2">
        <Button 
          size="sm" 
          onClick={() => onCall(contact.primary_phone)}
          className="bg-green-600 hover:bg-green-700"
        >
          <PhoneCall className="w-4 h-4" />
        </Button>
        <Button size="sm" variant="outline" onClick={() => onEdit(contact)}>
          <Edit className="w-4 h-4" />
        </Button>
        <Button size="sm" variant="outline" onClick={() => onDelete(contact.id)}>
          <Trash2 className="w-4 h-4" />
        </Button>
      </div>
    </div>
    {contact.availability_notes && (
      <div className="text-xs text-gray-500 mt-2">
        <Clock className="w-3 h-3 inline mr-1" />
        {contact.availability_notes}
      </div>
    )}
  </div>
);

// Medical Profile Item Component
const MedicalProfileItem = ({ profile }) => (
  <div className="p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
    <div className="flex justify-between items-start mb-2">
      <span className="font-semibold text-blue-900">{profile.member_name}</span>
      <Badge className="bg-blue-100 text-blue-800 text-xs">
        {profile.medical_info?.blood_type || 'Unknown'}
      </Badge>
    </div>
    
    {profile.medical_info?.allergies?.length > 0 && (
      <div className="mb-2">
        <div className="text-xs font-medium text-gray-700 mb-1">Allergies:</div>
        <div className="flex flex-wrap gap-1">
          {profile.medical_info.allergies.map((allergy, idx) => (
            <Badge key={idx} className="bg-red-100 text-red-800 text-xs">
              {allergy}
            </Badge>
          ))}
        </div>
      </div>
    )}
    
    {profile.medical_info?.chronic_conditions?.length > 0 && (
      <div className="mb-2">
        <div className="text-xs font-medium text-gray-700 mb-1">Conditions:</div>
        <div className="flex flex-wrap gap-1">
          {profile.medical_info.chronic_conditions.map((condition, idx) => (
            <Badge key={idx} className="bg-orange-100 text-orange-800 text-xs">
              {condition}
            </Badge>
          ))}
        </div>
      </div>
    )}
    
    {profile.medical_info?.current_medications?.length > 0 && (
      <div>
        <div className="text-xs font-medium text-gray-700 mb-1">Medications:</div>
        <div className="text-xs text-gray-600">
          {profile.medical_info.current_medications.map((med, idx) => 
            `${med.name}${idx < profile.medical_info.current_medications.length - 1 ? ', ' : ''}`
          )}
        </div>
      </div>
    )}
  </div>
);

// Emergency Services List Component
const EmergencyServices = ({ services }) => (
  <div className="space-y-3">
    {services?.national_emergency && (
      <div>
        <h4 className="font-semibold text-gray-900 mb-2">Emergency Services</h4>
        {services.national_emergency.map((service, idx) => (
          <div key={idx} className="p-3 bg-red-50 rounded-lg mb-2">
            <div className="flex justify-between items-center">
              <div>
                <div className="font-medium text-red-900">{service.name}</div>
                <div className="text-sm text-red-700">{service.description}</div>
              </div>
              <Button 
                size="sm"
                className="bg-red-600 hover:bg-red-700"
                onClick={() => window.location.href = `tel:${service.phone}`}
              >
                {service.phone}
              </Button>
            </div>
          </div>
        ))}
      </div>
    )}
    
    {services?.mental_health && (
      <div>
        <h4 className="font-semibold text-gray-900 mb-2">Mental Health</h4>
        {services.mental_health.map((service, idx) => (
          <div key={idx} className="p-3 bg-blue-50 rounded-lg mb-2">
            <div className="flex justify-between items-center">
              <div>
                <div className="font-medium text-blue-900">{service.name}</div>
                <div className="text-sm text-blue-700">{service.description}</div>
              </div>
              <Button 
                size="sm"
                className="bg-blue-600 hover:bg-blue-700"
                onClick={() => window.location.href = `tel:${service.phone}`}
              >
                {service.phone}
              </Button>
            </div>
          </div>
        ))}
      </div>
    )}
  </div>
);

// Main Family Emergency Hub Component
const FamilyEmergencyHub = ({ familyId }) => {
  const [hubData, setHubData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [showAddContact, setShowAddContact] = useState(false);
  const [editingContact, setEditingContact] = useState(null);

  useEffect(() => {
    fetchEmergencyHub();
  }, [familyId]);

  const fetchEmergencyHub = async () => {
    try {
      setLoading(true);
      const backendUrl = process.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/family/${familyId}/emergency-hub`);
      
      if (response.ok) {
        const data = await response.json();
        setHubData(data);
      } else {
        console.error('Failed to fetch emergency hub data');
      }
    } catch (error) {
      console.error('Error fetching emergency hub:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCallEmergency = () => {
    window.location.href = 'tel:911';
  };

  const handleViewContacts = () => {
    setActiveTab('contacts');
  };

  const handleAlertContacts = async () => {
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/family/${familyId}/emergency-alert`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          incident_type: 'manual_alert',
          description: 'Manual emergency alert triggered from dashboard',
          timestamp: new Date().toISOString()
        }),
      });

      if (response.ok) {
        const result = await response.json();
        alert(`Emergency alert logged. ${result.contacts_to_notify} contacts would be notified in production.`);
      }
    } catch (error) {
      console.error('Error sending emergency alert:', error);
    }
  };

  const handleCallContact = (phoneNumber) => {
    window.location.href = `tel:${phoneNumber}`;
  };

  if (loading) {
    return (
      <Card className="border-red-200 shadow-lg">
        <CardContent className="p-6">
          <div className="flex items-center space-x-2">
            <Activity className="w-5 h-5 animate-spin text-red-500" />
            <span>Loading Emergency Hub...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border-red-200 shadow-lg bg-gradient-to-br from-red-50 to-orange-50">
      <CardHeader className="bg-red-600 text-white">
        <CardTitle className="flex items-center text-xl">
          <AlertTriangle className="w-6 h-6 mr-3" />
          🚨 FAMILY EMERGENCY HUB
          <Badge className="ml-auto bg-white text-red-600">PRIORITY</Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="p-6">
        {/* Emergency Quick Access */}
        <EmergencyQuickAccess 
          onCallEmergency={handleCallEmergency}
          onViewContacts={handleViewContacts}
          onAlertContacts={handleAlertContacts}
        />

        {/* Tab Navigation */}
        <div className="flex space-x-4 mb-6 border-b">
          {['overview', 'contacts', 'medical', 'services'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`pb-2 px-3 text-sm font-medium ${
                activeTab === tab 
                  ? 'border-b-2 border-red-500 text-red-600' 
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && (
          <div className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-3 bg-red-50 rounded-lg">
                <div className="text-2xl font-bold text-red-600">
                  {hubData?.emergency_contacts?.length || 0}
                </div>
                <div className="text-sm text-gray-600">Emergency Contacts</div>
              </div>
              <div className="text-center p-3 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">
                  {hubData?.medical_profiles?.length || 0}
                </div>
                <div className="text-sm text-gray-600">Medical Profiles</div>
              </div>
              <div className="text-center p-3 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">
                  {hubData?.family_members?.length || 0}
                </div>
                <div className="text-sm text-gray-600">Family Members</div>
              </div>
              <div className="text-center p-3 bg-yellow-50 rounded-lg">
                <div className="text-2xl font-bold text-yellow-600">
                  {hubData?.recent_incidents?.length || 0}
                </div>
                <div className="text-sm text-gray-600">Recent Incidents</div>
              </div>
            </div>
            
            <div className="p-4 bg-yellow-50 rounded-lg border border-yellow-200">
              <div className="flex items-start space-x-2">
                <Info className="w-5 h-5 text-yellow-600 mt-0.5" />
                <div>
                  <div className="font-semibold text-yellow-800">Emergency Preparedness</div>
                  <div className="text-sm text-yellow-700 mt-1">
                    Keep this information updated. In emergencies, every second counts.
                    Ensure all family members know how to access this hub.
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'contacts' && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-semibold text-gray-900">Emergency Contacts</h3>
              <Button 
                onClick={() => setShowAddContact(true)}
                className="bg-red-600 hover:bg-red-700"
              >
                <Plus className="w-4 h-4 mr-2" />
                Add Contact
              </Button>
            </div>
            
            <div className="space-y-3">
              {hubData?.emergency_contacts?.map((contact) => (
                <EmergencyContactItem 
                  key={contact.id}
                  contact={contact}
                  onEdit={setEditingContact}
                  onDelete={(id) => {/* Handle delete */}}
                  onCall={handleCallContact}
                />
              ))}
              
              {(!hubData?.emergency_contacts || hubData.emergency_contacts.length === 0) && (
                <div className="text-center py-8 text-gray-500">
                  <AlertCircle className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                  <div>No emergency contacts added yet</div>
                  <div className="text-sm">Add contacts to ensure help is always available</div>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'medical' && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-lg font-semibold text-gray-900">Medical Profiles</h3>
              <Button className="bg-blue-600 hover:bg-blue-700">
                <Plus className="w-4 h-4 mr-2" />
                Add Profile
              </Button>
            </div>
            
            <div className="space-y-3">
              {hubData?.medical_profiles?.map((profile) => (
                <MedicalProfileItem key={profile.id} profile={profile} />
              ))}
              
              {(!hubData?.medical_profiles || hubData.medical_profiles.length === 0) && (
                <div className="text-center py-8 text-gray-500">
                  <Heart className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                  <div>No medical profiles created yet</div>
                  <div className="text-sm">Add profiles to provide critical medical information during emergencies</div>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'services' && (
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-gray-900">Emergency Services</h3>
            <EmergencyServices services={hubData?.emergency_services} />
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default FamilyEmergencyHub;