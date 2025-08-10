import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  Users, Heart, Calendar, Shield, AlertTriangle, Clock,
  Phone, MapPin, Pill, Activity, Target, BookOpen,
  CheckCircle, XCircle, Bell, Plus, Edit, Eye
} from 'lucide-react';

const FamilyCoordination = () => {
  const { switchRole } = useRole();
  const [coordinationData, setCoordinationData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    switchRole('family');
    fetchCoordinationData();
  }, [switchRole]);

  const fetchCoordinationData = async () => {
    try {
      const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/family/health-overview/demo-family-123`);
      const data = await response.json();
      setCoordinationData(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching coordination data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
        <SmartNavigation />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center">Loading family coordination data...</div>
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
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Family Health Coordination</h1>
          <p className="text-gray-600">Comprehensive family health management and coordination</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-2 border-amber-200 bg-amber-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Users className="w-8 h-8 text-amber-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-amber-600">
                    {coordinationData?.multi_member_tracking?.total_members || 4}
                  </div>
                  <p className="text-sm text-gray-600">Family Members</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-green-200 bg-green-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Heart className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-green-600">
                    {coordinationData?.multi_member_tracking?.health_status?.excellent + 
                     coordinationData?.multi_member_tracking?.health_status?.good || 3}
                  </div>
                  <p className="text-sm text-gray-600">Healthy Members</p>
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
                    {coordinationData?.multi_member_tracking?.upcoming_appointments?.length || 2}
                  </div>
                  <p className="text-sm text-gray-600">Upcoming Appointments</p>
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
                    {coordinationData?.multi_member_tracking?.health_status?.needs_attention || 1}
                  </div>
                  <p className="text-sm text-gray-600">Need Attention</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Tabs */}
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="appointments">Calendar</TabsTrigger>
            <TabsTrigger value="goals">Family Goals</TabsTrigger>
            <TabsTrigger value="meals">Meal Coordination</TabsTrigger>
            <TabsTrigger value="emergency">Emergency</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Family Health Status */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Heart className="w-5 h-5 mr-2 text-red-500" />
                    Family Health Status
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {coordinationData?.multi_member_tracking?.upcoming_appointments?.map((appointment, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                          <Users className="w-5 h-5 text-blue-600" />
                        </div>
                        <div>
                          <div className="font-medium">{appointment.member}</div>
                          <div className="text-sm text-gray-600">{appointment.type}</div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-medium">{appointment.date}</div>
                        <div className="text-xs text-gray-500">{appointment.provider}</div>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              {/* Medication Schedule */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Pill className="w-5 h-5 mr-2 text-purple-500" />
                    Medication Schedule
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {coordinationData?.care_coordination?.medication_schedule?.map((med, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
                      <div>
                        <div className="font-medium">{med.member}</div>
                        <div className="text-sm text-gray-600">{med.medication}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-medium">{med.time}</div>
                        <Badge variant="secondary" className="text-xs">{med.frequency}</Badge>
                      </div>
                    </div>
                  ))}
                  <Button className="w-full bg-purple-500 hover:bg-purple-600">
                    <Plus className="w-4 h-4 mr-2" />
                    Add Medication
                  </Button>
                </CardContent>
              </Card>
            </div>

            {/* Emergency Contacts */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Shield className="w-5 h-5 mr-2 text-green-500" />
                  Emergency Contacts
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {coordinationData?.care_coordination?.emergency_contacts?.map((contact, index) => (
                    <div key={index} className="p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
                      <div className="flex items-center justify-between mb-2">
                        <div className="font-medium text-green-900">{contact.name}</div>
                        <Button size="sm" variant="outline">
                          <Phone className="w-4 h-4" />
                        </Button>
                      </div>
                      <div className="text-sm text-green-700">
                        <div>{contact.relationship}</div>
                        <div className="font-mono">{contact.phone}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Appointments/Calendar Tab */}
          <TabsContent value="appointments" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Calendar className="w-5 h-5 mr-2 text-blue-500" />
                    Family Calendar & Appointments
                  </div>
                  <Button className="bg-blue-500 hover:bg-blue-600">
                    <Plus className="w-4 h-4 mr-2" />
                    Add Appointment
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {coordinationData?.multi_member_tracking?.upcoming_appointments?.map((appointment, index) => (
                    <div key={index} className="border rounded-lg p-4 hover:bg-gray-50">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4">
                          <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                            <Calendar className="w-6 h-6 text-blue-600" />
                          </div>
                          <div>
                            <div className="font-semibold">{appointment.member} - {appointment.type}</div>
                            <div className="text-sm text-gray-600">
                              {appointment.date} • {appointment.provider}
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Badge className="bg-blue-100 text-blue-800">Confirmed</Badge>
                          <Button variant="outline" size="sm">
                            <Edit className="w-4 h-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Family Goals Tab */}
          <TabsContent value="goals" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center">
                    <Target className="w-5 h-5 mr-2 text-purple-500" />
                    Active Family Goals
                  </div>
                  <Button className="bg-purple-500 hover:bg-purple-600">
                    <Plus className="w-4 h-4 mr-2" />
                    Create Goal
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {coordinationData?.shared_goals?.map((goal, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <div className="font-semibold">{goal.title}</div>
                        <div className="text-sm text-gray-600">{goal.target}</div>
                      </div>
                      <div className="text-right">
                        <div className="text-lg font-bold text-purple-600">{goal.current_progress}%</div>
                        <div className="text-xs text-gray-500">Progress</div>
                      </div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
                      <div 
                        className="bg-purple-500 h-2 rounded-full" 
                        style={{ width: `${goal.current_progress}%` }}
                      />
                    </div>
                    <div className="flex items-center justify-between">
                      <div className="text-sm text-gray-600">
                        {goal.participants.length} participants • Ends {goal.end_date}
                      </div>
                      <Badge className={goal.type === 'nutrition' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}>
                        {goal.type}
                      </Badge>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Meal Coordination Tab */}
          <TabsContent value="meals" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BookOpen className="w-5 h-5 mr-2 text-orange-500" />
                  Family Meal Coordination
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Dietary Restrictions */}
                  <div className="space-y-4">
                    <h4 className="font-semibold text-gray-900">Dietary Restrictions</h4>
                    {coordinationData?.meal_coordination?.dietary_restrictions && 
                     Object.entries(coordinationData.meal_coordination.dietary_restrictions).map(([member, restrictions]) => (
                      <div key={member} className="p-3 bg-orange-50 rounded-lg">
                        <div className="font-medium text-orange-900">{member}</div>
                        <div className="text-sm text-orange-700">
                          {Array.isArray(restrictions) ? restrictions.join(', ') : restrictions}
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Family-Friendly Meals */}
                  <div className="space-y-4">
                    <h4 className="font-semibold text-gray-900">Recommended Family Meals</h4>
                    {coordinationData?.meal_coordination?.family_friendly_meals?.map((meal, index) => (
                      <div key={index} className="p-3 bg-green-50 rounded-lg">
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="font-medium text-green-900">{meal.name}</div>
                            <div className="text-sm text-green-700">
                              Accommodates: {meal.accommodates?.join(', ')}
                            </div>
                          </div>
                          <Badge className="bg-green-100 text-green-800">
                            Score: {meal.nutrition_score}/10
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="font-medium text-blue-900">Weekly Meal Success Rate</div>
                      <div className="text-sm text-blue-700">
                        Family satisfaction with meal planning
                      </div>
                    </div>
                    <div className="text-2xl font-bold text-blue-600">
                      {coordinationData?.meal_coordination?.weekly_meal_success || 85}%
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Emergency Tab */}
          <TabsContent value="emergency" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <AlertTriangle className="w-5 h-5 mr-2 text-red-500" />
                  Emergency Management
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Emergency Contacts */}
                  <div className="space-y-4">
                    <h4 className="font-semibold text-gray-900">Emergency Contacts</h4>
                    {coordinationData?.care_coordination?.emergency_contacts?.map((contact, index) => (
                      <div key={index} className="p-4 border-l-4 border-red-500 bg-red-50 rounded-lg">
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="font-medium text-red-900">{contact.name}</div>
                            <div className="text-sm text-red-700">{contact.relationship}</div>
                            <div className="text-sm font-mono text-red-800">{contact.phone}</div>
                          </div>
                          <Button size="sm" className="bg-red-500 hover:bg-red-600">
                            <Phone className="w-4 h-4 mr-2" />
                            Call
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Healthcare Providers */}
                  <div className="space-y-4">
                    <h4 className="font-semibold text-gray-900">Healthcare Providers</h4>
                    {coordinationData?.care_coordination?.healthcare_providers && 
                     Object.entries(coordinationData.care_coordination.healthcare_providers).map(([type, provider]) => (
                      <div key={type} className="p-4 border-l-4 border-blue-500 bg-blue-50 rounded-lg">
                        <div className="flex items-center justify-between">
                          <div>
                            <div className="font-medium text-blue-900 capitalize">{type.replace('_', ' ')}</div>
                            <div className="text-sm text-blue-700">{provider.name}</div>
                            {provider.phone && (
                              <div className="text-sm font-mono text-blue-800">{provider.phone}</div>
                            )}
                          </div>
                          <Button size="sm" variant="outline">
                            <Phone className="w-4 h-4 mr-2" />
                            Contact
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default FamilyCoordination;