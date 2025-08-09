import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { 
  ArrowLeft, Users, FileText, BarChart3, Stethoscope, 
  AlertTriangle, Calendar, TrendingUp, BookOpen, Activity,
  Clock, Star, ChevronRight, Plus
} from 'lucide-react';

// Component: Provider Header
const ProviderHeader = () => {
  const navigate = useNavigate();
  
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Button 
              variant="ghost" 
              onClick={() => navigate('/')}
              className="hover:bg-emerald-50"
            >
              <ArrowLeft className="w-5 h-5 mr-2" />
              Back to Home
            </Button>
            <div className="h-6 w-px bg-gray-300" />
            <h1 className="text-2xl font-bold text-gray-900">Healthcare Provider Portal</h1>
          </div>
          <div className="flex items-center space-x-4">
            <Button size="sm" className="bg-emerald-500 hover:bg-emerald-600">
              <Plus className="w-4 h-4 mr-2" />
              New Patient
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};

// Component: Patient Overview
const PatientOverview = () => (
  <Card className="col-span-full lg:col-span-2">
    <CardHeader>
      <CardTitle className="flex items-center">
        <Users className="w-5 h-5 mr-2 text-emerald-500" />
        Patient Overview
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="text-center p-4 bg-emerald-50 rounded-lg">
          <div className="text-2xl font-bold text-emerald-600">247</div>
          <div className="text-sm text-gray-600">Active Patients</div>
          <div className="text-xs text-green-600">+12 this month</div>
        </div>
        <div className="text-center p-4 bg-blue-50 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">156</div>
          <div className="text-sm text-gray-600">Prescriptions</div>
          <div className="text-xs text-blue-600">This month</div>
        </div>
        <div className="text-center p-4 bg-purple-50 rounded-lg">
          <div className="text-2xl font-bold text-purple-600">94%</div>
          <div className="text-sm text-gray-600">Compliance Rate</div>
          <div className="text-xs text-green-600">+2% improvement</div>
        </div>
        <div className="text-center p-4 bg-orange-50 rounded-lg">
          <div className="text-2xl font-bold text-orange-600">12</div>
          <div className="text-sm text-gray-600">Today's Visits</div>
          <div className="text-xs text-gray-600">3 remaining</div>
        </div>
      </div>
    </CardContent>
  </Card>
);

// Component: Clinical Alerts
const ClinicalAlerts = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <AlertTriangle className="w-5 h-5 mr-2 text-red-500" />
        Clinical Alerts
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-3">
      <div className="flex items-center space-x-3 p-3 bg-red-50 rounded-lg border-l-4 border-red-500">
        <AlertTriangle className="w-5 h-5 text-red-500" />
        <div className="flex-1">
          <div className="font-medium text-red-900">Critical: John D.</div>
          <div className="text-sm text-red-700">Blood pressure spike detected</div>
        </div>
        <Badge variant="destructive" className="text-xs">High</Badge>
      </div>
      <div className="flex items-center space-x-3 p-3 bg-yellow-50 rounded-lg border-l-4 border-yellow-500">
        <AlertTriangle className="w-5 h-5 text-yellow-500" />
        <div className="flex-1">
          <div className="font-medium text-yellow-900">Warning: Sarah M.</div>
          <div className="text-sm text-yellow-700">Missed medication doses</div>
        </div>
        <Badge variant="secondary" className="text-xs">Medium</Badge>
      </div>
      <div className="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg border-l-4 border-blue-500">
        <Activity className="w-5 h-5 text-blue-500" />
        <div className="flex-1">
          <div className="font-medium text-blue-900">Info: Mike R.</div>
          <div className="text-sm text-blue-700">Excellent progress this week</div>
        </div>
        <Badge variant="secondary" className="text-xs">Low</Badge>
      </div>
    </CardContent>
  </Card>
);

// Component: Today's Appointments
const TodayAppointments = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <Calendar className="w-5 h-5 mr-2 text-blue-500" />
        Today's Appointments
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-3">
      <div className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg">
        <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
          <Clock className="w-6 h-6 text-green-600" />
        </div>
        <div className="flex-1">
          <div className="font-medium">9:00 AM - Emma Wilson</div>
          <div className="text-sm text-gray-600">Nutrition consultation</div>
          <div className="text-xs text-green-600">Completed</div>
        </div>
      </div>
      <div className="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg border-l-4 border-blue-500">
        <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
          <Clock className="w-6 h-6 text-blue-600" />
        </div>
        <div className="flex-1">
          <div className="font-medium">11:30 AM - David Chen</div>
          <div className="text-sm text-gray-600">Follow-up appointment</div>
          <div className="text-xs text-blue-600">In Progress</div>
        </div>
      </div>
      <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
        <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center">
          <Clock className="w-6 h-6 text-gray-600" />
        </div>
        <div className="flex-1">
          <div className="font-medium">2:00 PM - Lisa Garcia</div>
          <div className="text-sm text-gray-600">Initial assessment</div>
          <div className="text-xs text-gray-600">Upcoming</div>
        </div>
      </div>
    </CardContent>
  </Card>
);

// Component: Patient Progress
const PatientProgress = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <TrendingUp className="w-5 h-5 mr-2 text-purple-500" />
        Patient Progress
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-4">
      <div className="p-3 bg-green-50 rounded-lg">
        <div className="flex items-center justify-between mb-2">
          <span className="font-medium text-green-900">Weight Loss Goals</span>
          <Star className="w-4 h-4 text-green-600" />
        </div>
        <div className="text-sm text-green-700">87% of patients on track</div>
      </div>
      <div className="p-3 bg-blue-50 rounded-lg">
        <div className="flex items-center justify-between mb-2">
          <span className="font-medium text-blue-900">Medication Adherence</span>
          <TrendingUp className="w-4 h-4 text-blue-600" />
        </div>
        <div className="text-sm text-blue-700">94% compliance rate</div>
      </div>
      <div className="p-3 bg-purple-50 rounded-lg">
        <div className="flex items-center justify-between mb-2">
          <span className="font-medium text-purple-900">Lifestyle Changes</span>
          <Activity className="w-4 h-4 text-purple-600" />
        </div>
        <div className="text-sm text-purple-700">76% showing improvement</div>
      </div>
    </CardContent>
  </Card>
);

// Component: Clinical Tools
const ClinicalTools = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <Stethoscope className="w-5 h-5 mr-2 text-emerald-500" />
        Clinical Tools
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-3">
      <Button className="w-full justify-start bg-emerald-500 hover:bg-emerald-600">
        <Users className="w-4 h-4 mr-3" />
        Patient Management
      </Button>
      <Button className="w-full justify-start bg-blue-500 hover:bg-blue-600">
        <FileText className="w-4 h-4 mr-3" />
        Diet Prescription Tools
      </Button>
      <Button className="w-full justify-start bg-purple-500 hover:bg-purple-600">
        <BarChart3 className="w-4 h-4 mr-3" />
        Clinical Analytics
      </Button>
      <Button className="w-full justify-start bg-orange-500 hover:bg-orange-600">
        <BookOpen className="w-4 h-4 mr-3" />
        Evidence Database
      </Button>
    </CardContent>
  </Card>
);

// Component: Research Insights
const ResearchInsights = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <BookOpen className="w-5 h-5 mr-2 text-blue-500" />
        Research Insights
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-3">
      <div className="p-3 bg-blue-50 rounded-lg">
        <div className="font-medium text-blue-900">Latest Study</div>
        <div className="text-sm text-blue-700 mt-1">
          Mediterranean diet shows 23% improvement in cardiovascular outcomes
        </div>
        <div className="text-xs text-gray-600 mt-2">Published: 2 days ago</div>
      </div>
      <div className="p-3 bg-green-50 rounded-lg">
        <div className="font-medium text-green-900">Clinical Guideline</div>
        <div className="text-sm text-green-700 mt-1">
          Updated diabetes management protocols for 2024
        </div>
        <div className="text-xs text-gray-600 mt-2">Updated: 1 week ago</div>
      </div>
    </CardContent>
  </Card>
);

// Component: Professional Resources
const ProfessionalResources = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <FileText className="w-5 h-5 mr-2 text-orange-500" />
        Professional Resources
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-3">
      <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer">
        <FileText className="w-5 h-5 text-orange-500" />
        <div className="flex-1">
          <div className="font-medium">Clinical Guidelines</div>
          <div className="text-sm text-gray-600">Evidence-based protocols</div>
        </div>
        <ChevronRight className="w-4 h-4 text-gray-400" />
      </div>
      <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer">
        <BookOpen className="w-5 h-5 text-blue-500" />
        <div className="flex-1">
          <div className="font-medium">Research Database</div>
          <div className="text-sm text-gray-600">Latest medical research</div>
        </div>
        <ChevronRight className="w-4 h-4 text-gray-400" />
      </div>
      <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer">
        <BarChart3 className="w-5 h-5 text-purple-500" />
        <div className="flex-1">
          <div className="font-medium">Population Health</div>
          <div className="text-sm text-gray-600">Community health data</div>
        </div>
        <ChevronRight className="w-4 h-4 text-gray-400" />
      </div>
    </CardContent>
  </Card>
);

// Component: Population Health
const PopulationHealth = () => (
  <Card className="col-span-full lg:col-span-2">
    <CardHeader>
      <CardTitle className="flex items-center">
        <BarChart3 className="w-5 h-5 mr-2 text-purple-500" />
        Population Health Analytics
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div className="h-64 bg-gradient-to-r from-emerald-50 to-blue-50 rounded-lg flex items-center justify-center">
        <div className="text-center">
          <BarChart3 className="w-12 h-12 text-purple-500 mx-auto mb-4" />
          <div className="text-lg font-medium text-gray-900">Community Health Trends</div>
          <div className="text-sm text-gray-600">Advanced analytics visualization coming soon</div>
        </div>
      </div>
    </CardContent>
  </Card>
);

// Main Provider Dashboard Component
const ProviderDashboard = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
      <ProviderHeader />
      <div className="max-w-7xl mx-auto p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <PatientOverview />
          <ClinicalAlerts />
          <TodayAppointments />
          <PatientProgress />
          <ClinicalTools />
          <ResearchInsights />
          <ProfessionalResources />
          <PopulationHealth />
        </div>
      </div>
    </div>
  );
};

export default ProviderDashboard;