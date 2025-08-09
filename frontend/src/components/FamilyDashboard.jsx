import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { ArrowLeft, Users, Heart, Calendar, Shield } from 'lucide-react';

const FamilyDashboard = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button 
                variant="ghost" 
                onClick={() => navigate('/')}
                className="hover:bg-amber-50"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Back to Home
              </Button>
              <div className="h-6 w-px bg-gray-300" />
              <h1 className="text-2xl font-bold text-gray-900">Family Health Management</h1>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Welcome, Family Caregiver!</h2>
          <p className="text-gray-600">Manage your family's health, coordinate care, and track multiple health profiles.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-br from-amber-500 to-amber-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-amber-100">Family Members</p>
                  <p className="text-2xl font-bold">4</p>
                </div>
                <Users className="w-8 h-8 text-amber-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-rose-500 to-rose-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-rose-100">Health Alerts</p>
                  <p className="text-2xl font-bold">2</p>
                </div>
                <Heart className="w-8 h-8 text-rose-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-blue-500 to-blue-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-blue-100">Appointments</p>
                  <p className="text-2xl font-bold">3</p>
                </div>
                <Calendar className="w-8 h-8 text-blue-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-green-500 to-green-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-100">Coverage</p>
                  <p className="text-2xl font-bold">100%</p>
                </div>
                <Shield className="w-8 h-8 text-green-200" />
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <Card>
            <CardHeader>
              <CardTitle>Family Management</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button className="w-full justify-start bg-amber-500 hover:bg-amber-600">
                <Users className="w-5 h-5 mr-3" />
                Multiple Profile Management
              </Button>
              <Button className="w-full justify-start bg-rose-500 hover:bg-rose-600">
                <Heart className="w-5 h-5 mr-3" />
                Family Meal Planning
              </Button>
              <Button className="w-full justify-start bg-blue-500 hover:bg-blue-600">
                <Calendar className="w-5 h-5 mr-3" />
                Health Coordination
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Family Health Updates</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                  <div className="w-2 h-2 bg-amber-500 rounded-full"></div>
                  <span className="text-sm">Emma completed her daily nutrition goals</span>
                </div>
                <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                  <div className="w-2 h-2 bg-rose-500 rounded-full"></div>
                  <span className="text-sm">Reminder: Alex's doctor appointment tomorrow</span>
                </div>
                <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <span className="text-sm">Weekly family health report available</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default FamilyDashboard;