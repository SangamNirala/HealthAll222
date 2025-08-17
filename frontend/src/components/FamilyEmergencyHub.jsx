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

// Emergency Contact Item Component - Smaller with lighter colors
const EmergencyContactItem = ({ contact, onEdit, onDelete, onCall }) => (
  <div className="p-3 bg-gray-50 rounded-lg border-l-4 border-red-300">
    <div className="flex justify-between items-start mb-2">
      <div className="flex-1">
        <div className="flex items-center space-x-2 mb-1">
          <span className="font-medium text-gray-900">{contact.contact_name}</span>
          {contact.is_primary_contact && (
            <Badge className="bg-red-50 text-red-700 text-xs">Primary</Badge>
          )}
          {contact.medical_authorization && (
            <Badge className="bg-blue-50 text-blue-700 text-xs">Medical Auth</Badge>
          )}
        </div>
        <div className="text-sm text-gray-600 mb-1">{contact.relationship}</div>
        <div className="flex items-center text-sm text-gray-700">
          <Phone className="w-3 h-3 mr-1" />
          {contact.primary_phone}
        </div>
        {contact.email && (
          <div className="flex items-center text-sm text-gray-700 mt-1">
            <Mail className="w-3 h-3 mr-1" />
            {contact.email}
          </div>
        )}
      </div>
      <div className="flex space-x-1">
        <Button 
          size="sm" 
          onClick={() => onCall(contact.primary_phone)}
          className="h-8 px-2 bg-green-500 hover:bg-green-600"
        >
          <PhoneCall className="w-3 h-3" />
        </Button>
        <Button size="sm" variant="outline" onClick={() => onEdit(contact)} className="h-8 px-2">
          <Edit className="w-3 h-3" />
        </Button>
        <Button size="sm" variant="outline" onClick={() => onDelete(contact.id)} className="h-8 px-2">
          <Trash2 className="w-3 h-3" />
        </Button>
      </div>
    </div>
    {contact.availability_notes && (
      <div className="text-xs text-gray-500 mt-1">
        <Clock className="w-3 h-3 inline mr-1" />
        {contact.availability_notes}
      </div>
    )}
  </div>
);

// Medical Profile Item Component - Smaller with lighter colors
const MedicalProfileItem = ({ profile }) => (
  <div className="p-3 bg-blue-50 rounded-lg border-l-4 border-blue-300">
    <div className="flex justify-between items-start mb-2">
      <span className="font-medium text-blue-900">{profile.member_name}</span>
      <Badge className="bg-blue-100 text-blue-700 text-xs">
        {profile.medical_info?.blood_type || 'Unknown'}
      </Badge>
    </div>
    
    {profile.medical_info?.allergies?.length > 0 && (
      <div className="mb-2">
        <div className="text-xs font-medium text-gray-700 mb-1">Allergies:</div>
        <div className="flex flex-wrap gap-1">
          {profile.medical_info.allergies.map((allergy, idx) => (
            <Badge key={idx} className="bg-red-50 text-red-700 text-xs">
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
            <Badge key={idx} className="bg-orange-50 text-orange-700 text-xs">
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

// Emergency Services List Component - With Add button and lighter colors
const EmergencyServices = ({ services, onAddService }) => (
  <div className="space-y-3">
    <div className="flex justify-between items-center mb-3">
      <h4 className="font-medium text-gray-900">Emergency Services Directory</h4>
      <Button 
        onClick={onAddService}
        size="sm"
        className="bg-gray-500 hover:bg-gray-600 text-white"
      >
        <Plus className="w-3 h-3 mr-1" />
        Add Service
      </Button>
    </div>
    
    {services?.national_emergency && (
      <div>
        <h5 className="font-medium text-gray-800 mb-2 text-sm">Emergency Services</h5>
        {services.national_emergency.map((service, idx) => (
          <div key={idx} className="p-2 bg-red-50 rounded-lg mb-2 border border-red-100">
            <div className="flex justify-between items-center">
              <div>
                <div className="font-medium text-red-800 text-sm">{service.name}</div>
                <div className="text-xs text-red-600">{service.description}</div>
              </div>
              <Button 
                size="sm"
                className="h-8 px-3 bg-red-500 hover:bg-red-600 text-xs"
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
        <h5 className="font-medium text-gray-800 mb-2 text-sm">Mental Health Support</h5>
        {services.mental_health.map((service, idx) => (
          <div key={idx} className="p-2 bg-blue-50 rounded-lg mb-2 border border-blue-100">
            <div className="flex justify-between items-center">
              <div>
                <div className="font-medium text-blue-800 text-sm">{service.name}</div>
                <div className="text-xs text-blue-600">{service.description}</div>
              </div>
              <Button 
                size="sm"
                className="h-8 px-3 bg-blue-500 hover:bg-blue-600 text-xs"
                onClick={() => window.location.href = `tel:${service.phone}`}
              >
                {service.phone}
              </Button>
            </div>
          </div>
        ))}
      </div>
    )}
    
    {services?.child_services && (
      <div>
        <h5 className="font-medium text-gray-800 mb-2 text-sm">Child Services</h5>
        {services.child_services.map((service, idx) => (
          <div key={idx} className="p-2 bg-purple-50 rounded-lg mb-2 border border-purple-100">
            <div className="flex justify-between items-center">
              <div>
                <div className="font-medium text-purple-800 text-sm">{service.name}</div>
                <div className="text-xs text-purple-600">{service.description}</div>
              </div>
              <Button 
                size="sm"
                className="h-8 px-3 bg-purple-500 hover:bg-purple-600 text-xs"
                onClick={() => window.location.href = `tel:${service.phone}`}
              >
                {service.phone}
              </Button>
            </div>
          </div>
        ))}
      </div>
    )}

    {services?.specialized && (
      <div>
        <h5 className="font-medium text-gray-800 mb-2 text-sm">Specialized Services</h5>
        {services.specialized.map((service, idx) => (
          <div key={idx} className="p-2 bg-green-50 rounded-lg mb-2 border border-green-100">
            <div className="flex justify-between items-center">
              <div>
                <div className="font-medium text-green-800 text-sm">{service.name}</div>
                <div className="text-xs text-green-600">{service.description}</div>
              </div>
              <Button 
                size="sm"
                className="h-8 px-3 bg-green-500 hover:bg-green-600 text-xs"
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

  const handleAddService = () => {
    alert('Add Custom Emergency Service functionality will be implemented in Phase 2');
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
    <Card className="border-red-200 shadow-md bg-gradient-to-br from-red-25 to-orange-25">
      <CardHeader className="bg-red-500 text-white">
        <CardTitle className="flex items-center text-lg">
          <AlertTriangle className="w-5 h-5 mr-2" />
          🚨 FAMILY EMERGENCY HUB
          <Badge className="ml-auto bg-white text-red-500 text-xs">PRIORITY</Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="p-4">
        {/* Emergency Quick Access */}
        <EmergencyQuickAccess 
          onCallEmergency={handleCallEmergency}
          onViewContacts={handleViewContacts}
          onAlertContacts={handleAlertContacts}
        />

        {/* Tab Navigation */}
        <div className="flex space-x-4 mb-4 border-b">
          {['overview', 'contacts', 'medical', 'services'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`pb-2 px-2 text-sm font-medium ${
                activeTab === tab 
                  ? 'border-b-2 border-red-400 text-red-600' 
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
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="text-center p-3 bg-red-50 rounded-lg">
                <div className="text-xl font-bold text-red-600">
                  {hubData?.emergency_contacts?.length || 0}
                </div>
                <div className="text-xs text-gray-600">Emergency Contacts</div>
              </div>
              <div className="text-center p-3 bg-blue-50 rounded-lg">
                <div className="text-xl font-bold text-blue-600">
                  {hubData?.medical_profiles?.length || 0}
                </div>
                <div className="text-xs text-gray-600">Medical Profiles</div>
              </div>
              <div className="text-center p-3 bg-green-50 rounded-lg">
                <div className="text-xl font-bold text-green-600">
                  {hubData?.family_members?.length || 0}
                </div>
                <div className="text-xs text-gray-600">Family Members</div>
              </div>
              <div className="text-center p-3 bg-yellow-50 rounded-lg">
                <div className="text-xl font-bold text-yellow-600">
                  {hubData?.recent_incidents?.length || 0}
                </div>
                <div className="text-xs text-gray-600">Recent Incidents</div>
              </div>
            </div>
            
            <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
              <div className="flex items-start space-x-2">
                <Info className="w-4 h-4 text-yellow-600 mt-0.5" />
                <div>
                  <div className="font-medium text-yellow-800 text-sm">Emergency Preparedness</div>
                  <div className="text-xs text-yellow-700 mt-1">
                    Keep this information updated. In emergencies, every second counts.
                    Ensure all family members know how to access this hub.
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'contacts' && (
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <h3 className="text-base font-medium text-gray-900">Emergency Contacts</h3>
              <Button 
                onClick={() => setShowAddContact(true)}
                size="sm"
                className="bg-red-500 hover:bg-red-600"
              >
                <Plus className="w-3 h-3 mr-1" />
                Add Contact
              </Button>
            </div>
            
            <div className="space-y-2">
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
                <div className="text-center py-6 text-gray-500">
                  <AlertCircle className="w-10 h-10 mx-auto mb-2 text-gray-400" />
                  <div className="text-sm">No emergency contacts added yet</div>
                  <div className="text-xs">Add contacts to ensure help is always available</div>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'medical' && (
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <h3 className="text-base font-medium text-gray-900">Medical Profiles</h3>
              <Button 
                size="sm" 
                className="bg-blue-500 hover:bg-blue-600"
              >
                <Plus className="w-3 h-3 mr-1" />
                Add Profile
              </Button>
            </div>
            
            <div className="space-y-2">
              {hubData?.medical_profiles?.map((profile) => (
                <MedicalProfileItem key={profile.id} profile={profile} />
              ))}
              
              {(!hubData?.medical_profiles || hubData.medical_profiles.length === 0) && (
                <div className="text-center py-6 text-gray-500">
                  <Heart className="w-10 h-10 mx-auto mb-2 text-gray-400" />
                  <div className="text-sm">No medical profiles created yet</div>
                  <div className="text-xs">Add profiles to provide critical medical information during emergencies</div>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'services' && (
          <div className="space-y-3">
            <EmergencyServices 
              services={hubData?.emergency_services}
              onAddService={handleAddService}
            />
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default FamilyEmergencyHub;