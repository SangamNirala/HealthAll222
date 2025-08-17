import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import FamilyEmergencyHub from './FamilyEmergencyHub';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { 
  Users, Heart, Calendar, Shield, Home, 
  BookOpen, ChefHat, UserPlus, Bell, CheckCircle,
  Clock, Star, ChevronRight, Plus, Baby, User
} from 'lucide-react';

// Component: Family Overview
const FamilyOverview = () => (
  <Card className="col-span-full lg:col-span-2">
    <CardHeader>
      <CardTitle className="flex items-center">
        <Home className="w-5 h-5 mr-2 text-amber-500" />
        Family Health Overview
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="text-center p-4 bg-amber-50 rounded-lg">
          <div className="text-2xl font-bold text-amber-600">4</div>
          <div className="text-sm text-gray-600">Family Members</div>
          <div className="text-xs text-green-600">All active</div>
        </div>
        <div className="text-center p-4 bg-red-50 rounded-lg">
          <div className="text-2xl font-bold text-red-600">2</div>
          <div className="text-sm text-gray-600">Health Alerts</div>
          <div className="text-xs text-red-600">Needs attention</div>
        </div>
        <div className="text-center p-4 bg-blue-50 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">3</div>
          <div className="text-sm text-gray-600">Appointments</div>
          <div className="text-xs text-blue-600">This week</div>
        </div>
        <div className="text-center p-4 bg-green-50 rounded-lg">
          <div className="text-2xl font-bold text-green-600">100%</div>
          <div className="text-sm text-gray-600">Coverage</div>
          <div className="text-xs text-green-600">All insured</div>
        </div>
      </div>
      
      {/* Family Members Quick View */}
      <div className="space-y-3">
        <h4 className="font-semibold text-gray-900">Family Members</h4>
        <div className="grid grid-cols-2 gap-3">
          <div className="flex items-center space-x-3 p-3 bg-blue-50 rounded-lg">
            <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-blue-600" />
            </div>
            <div>
              <div className="font-medium">John (Dad)</div>
              <div className="text-xs text-green-600">Healthy</div>
            </div>
          </div>
          <div className="flex items-center space-x-3 p-3 bg-pink-50 rounded-lg">
            <div className="w-10 h-10 bg-pink-100 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-pink-600" />
            </div>
            <div>
              <div className="font-medium">Sarah (Mom)</div>
              <div className="text-xs text-green-600">Healthy</div>
            </div>
          </div>
          <div className="flex items-center space-x-3 p-3 bg-purple-50 rounded-lg">
            <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
              <Baby className="w-5 h-5 text-purple-600" />
            </div>
            <div>
              <div className="font-medium">Emma (12)</div>
              <div className="text-xs text-yellow-600">Checkup due</div>
            </div>
          </div>
          <div className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg">
            <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
              <Baby className="w-5 h-5 text-green-600" />
            </div>
            <div>
              <div className="font-medium">Alex (8)</div>
              <div className="text-xs text-green-600">Healthy</div>
            </div>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
);

// Component: Family Meal Planning
const FamilyMealPlanning = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <ChefHat className="w-5 h-5 mr-2 text-orange-500" />
        Family Meal Planning
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-4">
      <div className="p-3 bg-orange-50 rounded-lg">
        <div className="flex items-center justify-between mb-2">
          <span className="font-medium text-orange-900">This Week's Plan</span>
          <Badge className="bg-orange-100 text-orange-800">85% Complete</Badge>
        </div>
        <div className="text-sm text-orange-700">5 of 7 days planned</div>
      </div>
      
      <div className="space-y-2">
        <h4 className="font-semibold text-gray-900">Upcoming Meals</h4>
        <div className="space-y-2">
          <div className="flex items-center justify-between p-2 bg-gray-50 rounded">
            <span className="text-sm">Tonight - Grilled Chicken</span>
            <CheckCircle className="w-4 h-4 text-green-500" />
          </div>
          <div className="flex items-center justify-between p-2 bg-gray-50 rounded">
            <span className="text-sm">Tomorrow - Pasta Primavera</span>
            <Clock className="w-4 h-4 text-gray-400" />
          </div>
        </div>
      </div>
      
      <Button className="w-full bg-orange-500 hover:bg-orange-600">
        <ChefHat className="w-4 h-4 mr-2" />
        Plan Family Meals
      </Button>
    </CardContent>
  </Card>
);

// Component: Health Summaries
const HealthSummaries = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <Heart className="w-5 h-5 mr-2 text-red-500" />
        Health Summaries
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-3">
      <div className="p-3 bg-green-50 rounded-lg border-l-4 border-green-500">
        <div className="flex items-center justify-between">
          <div>
            <div className="font-medium text-green-900">Overall Family Health</div>
            <div className="text-sm text-green-700">Excellent status</div>
          </div>
          <Star className="w-5 h-5 text-green-600" />
        </div>
      </div>
      
      <div className="p-3 bg-yellow-50 rounded-lg border-l-4 border-yellow-500">
        <div className="flex items-center justify-between">
          <div>
            <div className="font-medium text-yellow-900">Emma's Checkup</div>
            <div className="text-sm text-yellow-700">Due in 2 weeks</div>
          </div>
          <Bell className="w-5 h-5 text-yellow-600" />
        </div>
      </div>
      
      <div className="p-3 bg-blue-50 rounded-lg border-l-4 border-blue-500">
        <div className="flex items-center justify-between">
          <div>
            <div className="font-medium text-blue-900">Vaccination Records</div>
            <div className="text-sm text-blue-700">All up to date</div>
          </div>
          <Shield className="w-5 h-5 text-blue-600" />
        </div>
      </div>
    </CardContent>
  </Card>
);

// Component: Shared Goals
const SharedGoals = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <Star className="w-5 h-5 mr-2 text-purple-500" />
        Family Goals
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-4">
      <div className="p-3 bg-purple-50 rounded-lg">
        <div className="flex items-center justify-between mb-2">
          <span className="font-medium text-purple-900">Healthy Eating Challenge</span>
          <Badge className="bg-purple-100 text-purple-800">Week 2</Badge>
        </div>
        <div className="text-sm text-purple-700">Family goal: 5 servings of vegetables daily</div>
        <div className="text-xs text-green-600 mt-1">3/4 members on track</div>
      </div>
      
      <div className="p-3 bg-blue-50 rounded-lg">
        <div className="flex items-center justify-between mb-2">
          <span className="font-medium text-blue-900">Weekend Fitness</span>
          <Badge className="bg-blue-100 text-blue-800">Active</Badge>
        </div>
        <div className="text-sm text-blue-700">Family bike rides every Saturday</div>
        <div className="text-xs text-green-600 mt-1">4 consecutive weeks!</div>
      </div>
      
      <Button className="w-full bg-purple-500 hover:bg-purple-600">
        <Plus className="w-4 h-4 mr-2" />
        Create Family Goal
      </Button>
    </CardContent>
  </Card>
);

// Component: Family Calendar
const FamilyCalendar = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <Calendar className="w-5 h-5 mr-2 text-blue-500" />
        Family Calendar
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-3">
      <div className="space-y-2">
        <h4 className="font-semibold text-gray-900">This Week</h4>
        <div className="space-y-2">
          <div className="flex items-center space-x-3 p-2 bg-red-50 rounded-lg">
            <div className="w-2 h-2 bg-red-500 rounded-full"></div>
            <div className="flex-1">
              <div className="text-sm font-medium">Emma - Dental Checkup</div>
              <div className="text-xs text-gray-600">Tomorrow, 3:00 PM</div>
            </div>
          </div>
          <div className="flex items-center space-x-3 p-2 bg-blue-50 rounded-lg">
            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            <div className="flex-1">
              <div className="text-sm font-medium">Alex - Soccer Practice</div>
              <div className="text-xs text-gray-600">Wednesday, 4:30 PM</div>
            </div>
          </div>
          <div className="flex items-center space-x-3 p-2 bg-green-50 rounded-lg">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <div className="flex-1">
              <div className="text-sm font-medium">Family Dinner Planning</div>
              <div className="text-xs text-gray-600">Friday, 6:00 PM</div>
            </div>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
);

// Component: Nutrition Education
const NutritionEducation = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <BookOpen className="w-5 h-5 mr-2 text-green-500" />
        Nutrition Education
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-3">
      <div className="p-3 bg-green-50 rounded-lg">
        <div className="font-medium text-green-900">Kids' Nutrition Guide</div>
        <div className="text-sm text-green-700 mt-1">
          Age-appropriate nutrition tips for Emma and Alex
        </div>
        <Button size="sm" variant="ghost" className="mt-2 text-green-600 hover:text-green-700">
          <BookOpen className="w-3 h-3 mr-1" />
          Read More
        </Button>
      </div>
      
      <div className="p-3 bg-blue-50 rounded-lg">
        <div className="font-medium text-blue-900">Healthy Snack Ideas</div>
        <div className="text-sm text-blue-700 mt-1">
          10 nutritious snacks kids actually love
        </div>
        <Button size="sm" variant="ghost" className="mt-2 text-blue-600 hover:text-blue-700">
          <ChefHat className="w-3 h-3 mr-1" />
          View Recipes
        </Button>
      </div>
    </CardContent>
  </Card>
);

// Component: Family Recipes
const FamilyRecipes = () => (
  <Card>
    <CardHeader>
      <CardTitle className="flex items-center">
        <ChefHat className="w-5 h-5 mr-2 text-orange-500" />
        Family Recipes
      </CardTitle>
    </CardHeader>
    <CardContent className="space-y-3">
      <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer">
        <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
          <ChefHat className="w-6 h-6 text-orange-500" />
        </div>
        <div className="flex-1">
          <div className="font-medium">Mom's Healthy Lasagna</div>
          <div className="text-sm text-gray-600">Kid-approved, veggie-packed</div>
          <div className="text-xs text-green-600">★★★★★ Family favorite</div>
        </div>
        <ChevronRight className="w-4 h-4 text-gray-400" />
      </div>
      
      <div className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 cursor-pointer">
        <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
          <ChefHat className="w-6 h-6 text-green-500" />
        </div>
        <div className="flex-1">
          <div className="font-medium">Rainbow Smoothie Bowls</div>
          <div className="text-sm text-gray-600">Fun breakfast for kids</div>
          <div className="text-xs text-blue-600">★★★★☆ Emma's choice</div>
        </div>
        <ChevronRight className="w-4 h-4 text-gray-400" />
      </div>
      
      <Button className="w-full bg-orange-500 hover:bg-orange-600">
        <Plus className="w-4 h-4 mr-2" />
        Add New Recipe
      </Button>
    </CardContent>
  </Card>
);

// Component: Care Coordination
const CareCoordination = () => (
  <Card className="col-span-full lg:col-span-2">
    <CardHeader>
      <CardTitle className="flex items-center">
        <Users className="w-5 h-5 mr-2 text-amber-500" />
        Care Coordination
      </CardTitle>
    </CardHeader>
    <CardContent>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-3">
          <h4 className="font-semibold text-gray-900">Healthcare Providers</h4>
          <div className="space-y-2">
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div>
                <div className="font-medium">Dr. Johnson - Family Physician</div>
                <div className="text-sm text-gray-600">Last visit: 2 weeks ago</div>
              </div>
              <Button size="sm" variant="outline">Contact</Button>
            </div>
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div>
                <div className="font-medium">Dr. Smith - Pediatrician</div>
                <div className="text-sm text-gray-600">Next visit: Next week</div>
              </div>
              <Button size="sm" variant="outline">Contact</Button>
            </div>
          </div>
        </div>
        
        <div className="space-y-3">
          <h4 className="font-semibold text-gray-900">Shared Documents</h4>
          <div className="space-y-2">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <div className="font-medium">Family Medical History</div>
                <div className="text-sm text-gray-600">Updated 1 month ago</div>
              </div>
              <Button size="sm" variant="outline">View</Button>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <div className="font-medium">Insurance Information</div>
                <div className="text-sm text-gray-600">Valid until Dec 2024</div>
              </div>
              <Button size="sm" variant="outline">View</Button>
            </div>
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
);

// Main Family Dashboard Component
const FamilyDashboard = () => {
  const { switchRole } = useRole();

  // Set role to family when component mounts
  useEffect(() => {
    switchRole('family');
  }, [switchRole]);

  // Get family ID (in production, this would come from auth/context)
  const familyId = localStorage.getItem('family_user_id') || 'demo-family-123';

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
      <SmartNavigation />
      <div className="max-w-7xl mx-auto p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {/* 🚨 TOP-LEFT PRIMARY CARD: FAMILY EMERGENCY HUB */}
          <div className="col-span-full lg:col-span-2 order-first">
            <FamilyEmergencyHub familyId={familyId} />
          </div>
          
          {/* Rest of the dashboard components */}
          <FamilyMealPlanning />
          <HealthSummaries />
          <SharedGoals />
          <FamilyCalendar />
          <NutritionEducation />
          <FamilyRecipes />
          <CareCoordination />
        </div>
      </div>
    </div>
  );
};

export default FamilyDashboard;