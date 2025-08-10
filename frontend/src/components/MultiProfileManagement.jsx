import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Progress } from './ui/progress';
import { 
  Users, User, Heart, Activity, Calendar, Shield, Phone,
  CheckCircle, Clock, RefreshCw, Edit, Eye, Settings,
  FileText, MessageSquare, School, Stethoscope, AlertTriangle
} from 'lucide-react';

const MultiProfileManagement = () => {
  const { switchRole } = useRole();
  const [profileData, setProfileData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    switchRole('family');
    fetchProfileData();
  }, [switchRole]);

  const fetchProfileData = async () => {
    try {
      const backendUrl = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/family/multi-profile-management/demo-family-123`);
      const data = await response.json();
      setProfileData(data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching profile data:', error);
      setLoading(false);
    }
  };

  const getCompletionColor = (completion) => {
    if (completion >= 90) return 'text-green-600';
    if (completion >= 75) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getActivityLevelColor = (level) => {
    switch (level) {
      case 'very_active': return 'bg-green-100 text-green-800';
      case 'moderately_active': return 'bg-blue-100 text-blue-800';
      case 'lightly_active': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getRoleIcon = (role) => {
    if (role.includes('Primary')) return <Shield className="w-5 h-5 text-blue-600" />;
    if (role.includes('Secondary')) return <Users className="w-5 h-5 text-green-600" />;
    return <User className="w-5 h-5 text-gray-600" />;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
        <SmartNavigation />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <div className="text-center">Loading profile management...</div>
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
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Multi-Profile Management</h1>
          <p className="text-gray-600">Comprehensive family profile coordination and management</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-2 border-blue-200 bg-blue-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Users className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-blue-600">
                    {profileData?.profile_overview?.total_profiles || 0}
                  </div>
                  <p className="text-sm text-gray-600">Total Profiles</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-green-200 bg-green-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <CheckCircle className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-green-600">
                    {profileData?.profile_overview?.completion_status ? 
                      Object.values(profileData.profile_overview.completion_status).filter(p => p.status === 'complete').length : 0}
                  </div>
                  <p className="text-sm text-gray-600">Complete Profiles</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-purple-200 bg-purple-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <RefreshCw className="w-8 h-8 text-purple-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-purple-600">
                    {profileData?.profile_overview?.data_synchronization?.conflicts_resolved || 0}
                  </div>
                  <p className="text-sm text-gray-600">Conflicts Resolved</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-orange-200 bg-orange-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Clock className="w-8 h-8 text-orange-600 mr-3" />
                <div>
                  <div className="text-sm font-bold text-orange-600">
                    {profileData?.profile_overview?.data_synchronization?.last_sync || 'N/A'}
                  </div>
                  <p className="text-sm text-gray-600">Last Sync</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="profiles" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="profiles">Family Profiles</TabsTrigger>
            <TabsTrigger value="coordination">Coordination</TabsTrigger>
            <TabsTrigger value="communication">Communication</TabsTrigger>
            <TabsTrigger value="sync">Data Sync</TabsTrigger>
          </TabsList>

          {/* Family Profiles Tab */}
          <TabsContent value="profiles" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {profileData?.member_profiles?.map((member, index) => (
                <Card key={index} className="overflow-hidden">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex items-start space-x-4">
                        <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                          {getRoleIcon(member.role)}
                        </div>
                        <div>
                          <CardTitle className="text-lg">{member.member}</CardTitle>
                          <div className="text-sm text-gray-600">{member.role} • Age {member.age}</div>
                          <Badge className={getActivityLevelColor(member.activity_level)} variant="secondary">
                            {member.activity_level?.replace('_', ' ')}
                          </Badge>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className={`text-2xl font-bold ${getCompletionColor(
                          profileData?.profile_overview?.completion_status?.[member.member]?.completion || 0
                        )}`}>
                          {profileData?.profile_overview?.completion_status?.[member.member]?.completion || 0}%
                        </div>
                        <div className="text-xs text-gray-500">Complete</div>
                      </div>
                    </div>
                  </CardHeader>
                  
                  <CardContent>
                    {/* Progress Bar */}
                    <div className="mb-4">
                      <Progress 
                        value={profileData?.profile_overview?.completion_status?.[member.member]?.completion || 0} 
                        className="w-full h-2" 
                      />
                    </div>

                    {/* Health Summary */}
                    <div className="mb-4">
                      <h4 className="font-semibold text-gray-900 mb-3">Health Summary</h4>
                      <div className="space-y-2">
                        {member.health_summary?.current_conditions?.length > 0 && (
                          <div className="p-2 bg-red-50 rounded border-l-4 border-red-400">
                            <div className="text-sm font-medium text-red-900">Current Conditions:</div>
                            <div className="text-sm text-red-700">
                              {member.health_summary.current_conditions.join(', ')}
                            </div>
                          </div>
                        )}
                        
                        {member.health_summary?.allergies?.length > 0 && member.health_summary.allergies?.[0] !== 'none' && (
                          <div className="p-2 bg-yellow-50 rounded border-l-4 border-yellow-400">
                            <div className="text-sm font-medium text-yellow-900">Allergies:</div>
                            <div className="text-sm text-yellow-700">
                              {member.health_summary.allergies.join(', ')}
                            </div>
                          </div>
                        )}
                        
                        {member.health_summary?.medications?.length > 0 && (
                          <div className="p-2 bg-purple-50 rounded border-l-4 border-purple-400">
                            <div className="text-sm font-medium text-purple-900">Medications:</div>
                            <div className="text-sm text-purple-700">
                              {member.health_summary.medications.join(', ')}
                            </div>
                          </div>
                        )}

                        {member.health_summary?.recent_vitals && (
                          <div className="p-2 bg-blue-50 rounded border-l-4 border-blue-400">
                            <div className="text-sm font-medium text-blue-900">Recent Vitals:</div>
                            <div className="text-sm text-blue-700">
                              {Object.entries(member.health_summary.recent_vitals).map(([key, value]) => (
                                <span key={key} className="mr-3">
                                  {key.replace('_', ' ')}: {value}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Dietary Information */}
                    {member.dietary_preferences && (
                      <div className="mb-4">
                        <h4 className="font-semibold text-gray-900 mb-3">Dietary Information</h4>
                        <div className="space-y-2">
                          {member.dietary_preferences.restrictions?.length > 0 && 
                           member.dietary_preferences.restrictions?.[0] !== 'none' && (
                            <div className="flex flex-wrap gap-1">
                              <span className="text-sm text-gray-600">Restrictions:</span>
                              {member.dietary_preferences.restrictions.map((restriction, rIndex) => (
                                <Badge key={rIndex} variant="outline" className="text-xs">
                                  {restriction.replace('_', ' ')}
                                </Badge>
                              ))}
                            </div>
                          )}
                          
                          {member.dietary_preferences.preferences && (
                            <div className="flex flex-wrap gap-1">
                              <span className="text-sm text-gray-600">Preferences:</span>
                              {member.dietary_preferences.preferences.map((pref, pIndex) => (
                                <Badge key={pIndex} variant="secondary" className="text-xs">
                                  {pref.replace('_', ' ')}
                                </Badge>
                              ))}
                            </div>
                          )}

                          {member.dietary_preferences.challenges && (
                            <div className="p-2 bg-orange-50 rounded">
                              <div className="text-sm font-medium text-orange-900">Challenges:</div>
                              <div className="text-sm text-orange-700">
                                {member.dietary_preferences.challenges.join(', ').replace('_', ' ')}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Responsibilities (for adults) */}
                    {member.responsibilities && (
                      <div className="mb-4">
                        <h4 className="font-semibold text-gray-900 mb-2">Responsibilities</h4>
                        <div className="flex flex-wrap gap-1">
                          {member.responsibilities.map((resp, rIndex) => (
                            <Badge key={rIndex} className="bg-green-100 text-green-800 text-xs">
                              {resp.replace('_', ' ')}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* School Coordination (for kids) */}
                    {member.school_coordination && (
                      <div className="mb-4">
                        <h4 className="font-semibold text-gray-900 mb-2">School Coordination</h4>
                        <div className="space-y-2 text-sm">
                          <div className="flex items-center justify-between">
                            <span className="text-gray-600">Nurse Informed:</span>
                            <Badge className={member.school_coordination.school_nurse_informed ? 
                              'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                              {member.school_coordination.school_nurse_informed ? 'Yes' : 'No'}
                            </Badge>
                          </div>
                          {member.school_coordination.emergency_action_plan && (
                            <div className="flex items-center justify-between">
                              <span className="text-gray-600">Emergency Plan:</span>
                              <Badge className="bg-blue-100 text-blue-800">
                                {member.school_coordination.emergency_action_plan}
                              </Badge>
                            </div>
                          )}
                          {member.school_coordination.lunch_modifications && (
                            <div className="p-2 bg-yellow-50 rounded">
                              <div className="text-yellow-900 font-medium">Lunch Modifications:</div>
                              <div className="text-yellow-700">
                                {member.school_coordination.lunch_modifications}
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Actions */}
                    <div className="flex space-x-2 pt-4 border-t">
                      <Button variant="outline" size="sm">
                        <Eye className="w-4 h-4 mr-2" />
                        View Full Profile
                      </Button>
                      <Button variant="outline" size="sm">
                        <Edit className="w-4 h-4 mr-2" />
                        Edit Profile
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Coordination Tab */}
          <TabsContent value="coordination" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Shared Calendar */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Calendar className="w-5 h-5 mr-2 text-blue-500" />
                    Shared Calendar Overview
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {profileData?.coordination_tools?.shared_calendar && 
                   Object.entries(profileData.coordination_tools.shared_calendar).map(([type, count]) => (
                    <div key={type} className="flex items-center justify-between p-3 bg-blue-50 rounded-lg mb-2">
                      <div className="flex items-center space-x-3">
                        <Calendar className="w-5 h-5 text-blue-600" />
                        <span className="font-medium text-blue-900 capitalize">
                          {type.replace('_', ' ')}
                        </span>
                      </div>
                      <Badge className="bg-blue-100 text-blue-800">{count}</Badge>
                    </div>
                  ))}
                </CardContent>
              </Card>

              {/* Communication System */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <MessageSquare className="w-5 h-5 mr-2 text-green-500" />
                    Communication Systems
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {profileData?.coordination_tools?.communication_system && 
                   Object.entries(profileData.coordination_tools.communication_system).map(([system, active]) => (
                    <div key={system} className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <MessageSquare className="w-5 h-5 text-green-600" />
                        <span className="font-medium text-green-900 capitalize">
                          {system.replace('_', ' ')}
                        </span>
                      </div>
                      <Badge className={active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}>
                        {active ? 'Active' : 'Inactive'}
                      </Badge>
                    </div>
                  ))}
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Communication Tab */}
          <TabsContent value="communication" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Phone className="w-5 h-5 mr-2 text-purple-500" />
                  Data Sharing Settings
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {profileData?.coordination_tools?.data_sharing && 
                   Object.entries(profileData.coordination_tools.data_sharing).map(([entity, settings]) => (
                    <div key={entity} className="border rounded-lg p-4">
                      <div className="font-semibold text-gray-900 mb-3 capitalize">
                        {entity.replace('_', ' ')}
                      </div>
                      <div className="space-y-2">
                        {Array.isArray(settings) ? settings.map((setting, index) => (
                          <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                            <span className="text-sm text-gray-700">{setting.replace('_', ' ')}</span>
                            <Badge className="bg-blue-100 text-blue-800">Enabled</Badge>
                          </div>
                        )) : (
                          <div className="flex items-center justify-between p-2 bg-gray-50 rounded">
                            <span className="text-sm text-gray-700">{settings}</span>
                            <Badge className="bg-blue-100 text-blue-800">Active</Badge>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Sync Tab */}
          <TabsContent value="sync" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center">
                    <RefreshCw className="w-5 h-5 mr-2 text-orange-500" />
                    Data Synchronization Status
                  </div>
                  <Button className="bg-orange-500 hover:bg-orange-600">
                    <RefreshCw className="w-4 h-4 mr-2" />
                    Sync Now
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Sync Status */}
                  <div className="space-y-4">
                    <h4 className="font-semibold text-gray-900">Synchronization Overview</h4>
                    <div className="p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
                      <div className="font-medium text-green-900">Status: Up to Date</div>
                      <div className="text-sm text-green-700">
                        Last sync: {profileData?.profile_overview?.data_synchronization?.last_sync}
                      </div>
                      <div className="text-sm text-green-700">
                        Conflicts resolved: {profileData?.profile_overview?.data_synchronization?.conflicts_resolved}
                      </div>
                    </div>
                  </div>

                  {/* Profile Completion Status */}
                  <div className="space-y-4">
                    <h4 className="font-semibold text-gray-900">Profile Completion</h4>
                    <div className="space-y-2">
                      {profileData?.profile_overview?.completion_status && 
                       Object.entries(profileData.profile_overview.completion_status).map(([member, status]) => (
                        <div key={member} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                          <div>
                            <div className="font-medium">{member}</div>
                            <div className="text-sm text-gray-600">
                              Updated: {status.last_updated}
                            </div>
                          </div>
                          <div className="text-right">
                            <div className={`text-lg font-bold ${getCompletionColor(status.completion)}`}>
                              {status.completion}%
                            </div>
                            <Badge className={status.status === 'complete' ? 
                              'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}>
                              {status.status}
                            </Badge>
                          </div>
                        </div>
                      ))}
                    </div>
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

export default MultiProfileManagement;