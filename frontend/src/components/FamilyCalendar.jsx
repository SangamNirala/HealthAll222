import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Calendar, Clock, User, MapPin, Bell, Plus, Edit, Trash2,
  Stethoscope, Pill, Activity, Heart, AlertCircle, CheckCircle
} from 'lucide-react';

const FamilyCalendar = () => {
  const { switchRole } = useRole();
  const [calendarData, setCalendarData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    switchRole('family');
    fetchCalendarData();
  }, [switchRole]);

  const fetchCalendarData = async () => {
    try {
      const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/family/calendar-integration/demo-family-123`);
      const data = await response.json();
      setCalendarData(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching calendar data:', error);
      setLoading(false);
    }
  };

  const getEventIcon = (type) => {
    switch (type) {
      case 'medical_appointment': return <Stethoscope className="w-5 h-5 text-blue-600" />;
      case 'meal_prep': return <Heart className="w-5 h-5 text-green-600" />;
      case 'physical_activity': return <Activity className="w-5 h-5 text-orange-600" />;
      default: return <Calendar className="w-5 h-5 text-gray-600" />;
    }
  };

  const getEventColor = (type) => {
    switch (type) {
      case 'medical_appointment': return 'border-l-blue-500 bg-blue-50';
      case 'meal_prep': return 'border-l-green-500 bg-green-50';
      case 'physical_activity': return 'border-l-orange-500 bg-orange-50';
      default: return 'border-l-gray-500 bg-gray-50';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
        <SmartNavigation />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center">Loading family calendar...</div>
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
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Family Calendar</h1>
          <p className="text-gray-600">Coordinate family health events, appointments, and activities</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-2 border-blue-200 bg-blue-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Calendar className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-blue-600">
                    {calendarData?.calendar_overview?.this_week_events?.length || 0}
                  </div>
                  <p className="text-sm text-gray-600">This Week</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-green-200 bg-green-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Stethoscope className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-green-600">
                    {calendarData?.calendar_overview?.upcoming_medical?.length || 0}
                  </div>
                  <p className="text-sm text-gray-600">Medical Appointments</p>
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
                    {calendarData?.calendar_overview?.medication_schedule?.daily_reminders?.length || 0}
                  </div>
                  <p className="text-sm text-gray-600">Daily Medications</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-amber-200 bg-amber-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Bell className="w-8 h-8 text-amber-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-amber-600">
                    {calendarData?.synchronization ? 
                      Object.values(calendarData.synchronization).filter(sync => sync.connected).length : 0}
                  </div>
                  <p className="text-sm text-gray-600">Synced Calendars</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="week" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="week">This Week</TabsTrigger>
            <TabsTrigger value="medical">Medical</TabsTrigger>
            <TabsTrigger value="medications">Medications</TabsTrigger>
            <TabsTrigger value="coordination">Coordination</TabsTrigger>
          </TabsList>

          {/* This Week Tab */}
          <TabsContent value="week" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Calendar className="w-5 h-5 mr-2 text-blue-500" />
                    This Week's Events
                  </div>
                  <Button className="bg-blue-500 hover:bg-blue-600">
                    <Plus className="w-4 h-4 mr-2" />
                    Add Event
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {calendarData?.calendar_overview?.this_week_events?.map((event, index) => (
                  <div key={index} className={`border-l-4 rounded-lg p-4 ${getEventColor(event.type)}`}>
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-3">
                        {getEventIcon(event.type)}
                        <div className="flex-1">
                          <div className="font-semibold text-gray-900">{event.title}</div>
                          <div className="text-sm text-gray-600 mt-1">
                            <span className="inline-flex items-center mr-4">
                              <Clock className="w-4 h-4 mr-1" />
                              {event.date} at {event.time}
                            </span>
                            {event.location && (
                              <span className="inline-flex items-center mr-4">
                                <MapPin className="w-4 h-4 mr-1" />
                                {event.location}
                              </span>
                            )}
                            {event.member && (
                              <span className="inline-flex items-center">
                                <User className="w-4 h-4 mr-1" />
                                {event.member}
                              </span>
                            )}
                          </div>
                          
                          {/* Event-specific information */}
                          {event.type === 'medical_appointment' && event.preparation_needed && (
                            <div className="mt-2 p-2 bg-yellow-50 rounded border-l-2 border-yellow-400">
                              <div className="text-sm font-medium text-yellow-800">Preparation needed:</div>
                              <ul className="text-xs text-yellow-700 mt-1 list-disc list-inside">
                                {event.preparation_needed.map((item, idx) => (
                                  <li key={idx}>{item}</li>
                                ))}
                              </ul>
                            </div>
                          )}
                          
                          {event.type === 'meal_prep' && event.planned_meals && (
                            <div className="mt-2 p-2 bg-green-50 rounded border-l-2 border-green-400">
                              <div className="text-sm font-medium text-green-800">Planned meals:</div>
                              <div className="text-xs text-green-700 mt-1">
                                {event.planned_meals.join(', ')}
                              </div>
                            </div>
                          )}
                          
                          {event.type === 'physical_activity' && event.health_benefits && (
                            <div className="mt-2 p-2 bg-orange-50 rounded border-l-2 border-orange-400">
                              <div className="text-sm font-medium text-orange-800">Health benefits:</div>
                              <div className="text-xs text-orange-700 mt-1">
                                {event.health_benefits.join(', ')}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        {event.reminders_set && (
                          <Badge className="bg-green-100 text-green-800">
                            <Bell className="w-3 h-3 mr-1" />
                            Reminder Set
                          </Badge>
                        )}
                        <Button variant="outline" size="sm">
                          <Edit className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Medical Appointments Tab */}
          <TabsContent value="medical" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Stethoscope className="w-5 h-5 mr-2 text-blue-500" />
                    Upcoming Medical Appointments
                  </div>
                  <Button className="bg-blue-500 hover:bg-blue-600">
                    <Plus className="w-4 h-4 mr-2" />
                    Schedule Appointment
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {calendarData?.calendar_overview?.upcoming_medical?.map((appointment, index) => (
                  <div key={index} className="border rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                          <Stethoscope className="w-6 h-6 text-blue-600" />
                        </div>
                        <div>
                          <div className="font-semibold">{appointment.member} - {appointment.appointment}</div>
                          <div className="text-sm text-gray-600">
                            {appointment.date}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge className={
                          appointment.status === 'confirmed' ? 'bg-green-100 text-green-800' : 
                          appointment.status === 'tentative' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-gray-100 text-gray-800'
                        }>
                          {appointment.status}
                        </Badge>
                        <Button variant="outline" size="sm">
                          <Edit className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Medications Tab */}
          <TabsContent value="medications" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Daily Medications */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Pill className="w-5 h-5 mr-2 text-purple-500" />
                    Daily Medication Schedule
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {calendarData?.calendar_overview?.medication_schedule?.daily_reminders?.map((med, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                          <Pill className="w-5 h-5 text-purple-600" />
                        </div>
                        <div>
                          <div className="font-medium">{med.member}</div>
                          <div className="text-sm text-gray-600">{med.medication}</div>
                          {med.condition && (
                            <div className="text-xs text-gray-500">For: {med.condition}</div>
                          )}
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-medium">{med.time}</div>
                        <Badge className={
                          med.status === 'active' ? 'bg-green-100 text-green-800' :
                          med.status === 'as_needed' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-gray-100 text-gray-800'
                        }>
                          {med.status}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              {/* Upcoming Refills */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <AlertCircle className="w-5 h-5 mr-2 text-orange-500" />
                    Upcoming Refills
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {calendarData?.calendar_overview?.medication_schedule?.upcoming_refills?.map((refill, index) => (
                    <div key={index} className="p-3 bg-orange-50 rounded-lg border-l-4 border-orange-500">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-medium text-orange-900">{refill.member}</div>
                          <div className="text-sm text-orange-700">{refill.medication}</div>
                          <div className="text-xs text-orange-600">{refill.pharmacy}</div>
                        </div>
                        <div className="text-right">
                          <div className="text-sm font-medium text-orange-900">
                            Due: {refill.refill_due}
                          </div>
                          <Button size="sm" className="bg-orange-500 hover:bg-orange-600 mt-1">
                            Order Refill
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Coordination Tab */}
          <TabsContent value="coordination" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Shared Responsibilities */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <User className="w-5 h-5 mr-2 text-green-500" />
                    Shared Responsibilities
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {calendarData?.family_coordination?.shared_responsibilities?.map((responsibility, index) => (
                    <div key={index} className="p-3 bg-green-50 rounded-lg">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-medium text-green-900">{responsibility.task}</div>
                          <div className="text-sm text-green-700">
                            Assigned to: {responsibility.assigned_to} • Backup: {responsibility.backup}
                          </div>
                          <div className="text-xs text-green-600">{responsibility.date}</div>
                        </div>
                        <CheckCircle className="w-5 h-5 text-green-600" />
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              {/* Calendar Synchronization */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Calendar className="w-5 h-5 mr-2 text-blue-500" />
                    Calendar Synchronization
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {calendarData?.synchronization && Object.entries(calendarData.synchronization).map(([platform, sync]) => (
                    <div key={platform} className="p-3 bg-blue-50 rounded-lg">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="font-medium text-blue-900 capitalize">
                            {platform.replace('_', ' ')}
                          </div>
                          {sync.connected ? (
                            <div className="text-sm text-blue-700">
                              Last sync: {sync.last_sync}
                            </div>
                          ) : (
                            <div className="text-sm text-gray-600">Not connected</div>
                          )}
                        </div>
                        <Button 
                          size="sm" 
                          variant={sync.connected ? "outline" : "default"}
                          className={sync.connected ? "" : "bg-blue-500 hover:bg-blue-600"}
                        >
                          {sync.connected ? 'Disconnect' : 'Connect'}
                        </Button>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default FamilyCalendar;