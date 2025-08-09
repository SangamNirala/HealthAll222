import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { ArrowLeft, Zap, Clock, Eye, UserX } from 'lucide-react';

const GuestDashboard = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-violet-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button 
                variant="ghost" 
                onClick={() => navigate('/')}
                className="hover:bg-purple-50"
              >
                <ArrowLeft className="w-5 h-5 mr-2" />
                Back to Home
              </Button>
              <div className="h-6 w-px bg-gray-300" />
              <h1 className="text-2xl font-bold text-gray-900">Quick Health Tracking</h1>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Welcome, Guest User!</h2>
          <p className="text-gray-600">Quick nutrition tracking and health monitoring without account creation. Perfect for trying out our platform.</p>
        </div>

        {/* Guest Mode Notice */}
        <div className="bg-purple-100 border border-purple-200 rounded-lg p-6 mb-8">
          <div className="flex items-center space-x-3">
            <UserX className="w-6 h-6 text-purple-600" />
            <div>
              <h3 className="text-lg font-semibold text-purple-900">Guest Mode Active</h3>
              <p className="text-purple-700">Your data is temporarily stored and will not be saved permanently. Create an account to save your progress.</p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="bg-gradient-to-br from-purple-500 to-purple-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-purple-100">Quick Logs</p>
                  <p className="text-2xl font-bold">5</p>
                </div>
                <Zap className="w-8 h-8 text-purple-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-indigo-500 to-indigo-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-indigo-100">Session Time</p>
                  <p className="text-2xl font-bold">15m</p>
                </div>
                <Clock className="w-8 h-8 text-indigo-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-violet-500 to-violet-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-violet-100">Features Used</p>
                  <p className="text-2xl font-bold">3</p>
                </div>
                <Eye className="w-8 h-8 text-violet-200" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-pink-500 to-pink-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-pink-100">Experience</p>
                  <p className="text-2xl font-bold">Good</p>
                </div>
                <UserX className="w-8 h-8 text-pink-200" />
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <Card>
            <CardHeader>
              <CardTitle>Quick Access Tools</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Button className="w-full justify-start bg-purple-500 hover:bg-purple-600">
                <Zap className="w-5 h-5 mr-3" />
                Simple Food Logging
              </Button>
              <Button className="w-full justify-start bg-indigo-500 hover:bg-indigo-600">
                <Eye className="w-5 h-5 mr-3" />
                Basic Nutrition Info
              </Button>
              <Button className="w-full justify-start bg-violet-500 hover:bg-violet-600">
                <Clock className="w-5 h-5 mr-3" />
                Temporary Tracking
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Upgrade to Full Experience</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center py-8">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Enjoying the platform?</h3>
                <p className="text-gray-600 mb-6">Create an account to save your data, access advanced features, and get personalized recommendations.</p>
                <div className="space-y-3">
                  <Button className="w-full bg-gradient-to-r from-purple-500 to-violet-600 hover:from-purple-600 hover:to-violet-700">
                    Create Patient Account
                  </Button>
                  <Button variant="outline" className="w-full">
                    Learn More About Features
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default GuestDashboard;