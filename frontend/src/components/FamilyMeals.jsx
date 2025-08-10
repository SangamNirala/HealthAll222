import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { ChefHat, Plus, Calendar, Clock, Users, Utensils, ShoppingCart, Star } from 'lucide-react';

const FamilyMeals = () => {
  const { switchRole } = useRole();
  const [activeTab, setActiveTab] = useState('plan');
  
  const [mealPlans] = useState([
    {
      id: 1,
      name: 'Weekly Family Plan',
      date: 'Jan 15-21, 2024',
      meals: 21,
      status: 'active',
      familyMembers: 4
    },
    {
      id: 2,
      name: 'Healthy Kids Menu',
      date: 'Jan 8-14, 2024',
      meals: 14,
      status: 'completed',
      familyMembers: 2
    }
  ]);

  const [weeklyMeals] = useState([
    { day: 'Monday', breakfast: 'Oatmeal with berries', lunch: 'Turkey sandwiches', dinner: 'Grilled chicken & vegetables' },
    { day: 'Tuesday', breakfast: 'Scrambled eggs & toast', lunch: 'Soup & salad', dinner: 'Pasta with marinara' },
    { day: 'Wednesday', breakfast: 'Greek yogurt parfait', lunch: 'Leftover pasta', dinner: 'Fish tacos' },
    { day: 'Thursday', breakfast: 'Smoothie bowls', lunch: 'Chicken wraps', dinner: 'Beef stir-fry' },
    { day: 'Friday', breakfast: 'Pancakes (weekend treat)', lunch: 'Pizza (homemade)', dinner: 'Family BBQ' },
    { day: 'Saturday', breakfast: 'Weekend brunch', lunch: 'Light snacks', dinner: 'Slow cooker stew' },
    { day: 'Sunday', breakfast: 'French toast', lunch: 'Leftover stew', dinner: 'Sunday roast' }
  ]);

  const [shoppingList] = useState([
    { category: 'Proteins', items: ['Chicken breast (2 lbs)', 'Ground beef (1 lb)', 'Salmon fillets (4)', 'Eggs (dozen)'] },
    { category: 'Vegetables', items: ['Broccoli (2 heads)', 'Carrots (bag)', 'Bell peppers (4)', 'Spinach (bag)'] },
    { category: 'Pantry', items: ['Rice (bag)', 'Pasta (2 boxes)', 'Olive oil', 'Spices'] },
    { category: 'Dairy', items: ['Milk (gallon)', 'Greek yogurt (large)', 'Cheese (blocks)'] }
  ]);

  const [favorites] = useState([
    { name: 'Family Taco Night', rating: 5, prepTime: '30 min', serves: 4 },
    { name: 'Chicken Stir Fry', rating: 4, prepTime: '25 min', serves: 4 },
    { name: 'Homemade Pizza', rating: 5, prepTime: '45 min', serves: 4 },
    { name: 'Slow Cooker Chili', rating: 4, prepTime: '15 min', serves: 6 }
  ]);

  useEffect(() => {
    switchRole('family');
  }, [switchRole]);

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800';
      case 'completed': return 'bg-blue-100 text-blue-800';
      case 'draft': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getMealTime = (meal) => {
    switch (meal) {
      case 'breakfast': return 'bg-yellow-100 text-yellow-800';
      case 'lunch': return 'bg-green-100 text-green-800'; 
      case 'dinner': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star 
        key={i} 
        className={`w-4 h-4 ${i < rating ? 'text-yellow-400 fill-current' : 'text-gray-300'}`} 
      />
    ));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Family Meal Planning</h1>
          <p className="text-gray-600">Plan, organize, and track family meals and nutrition</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-2 border-amber-200 bg-amber-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <ChefHat className="w-8 h-8 text-amber-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-amber-600">{mealPlans.length}</div>
                  <p className="text-sm text-gray-600">Meal Plans</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-green-200 bg-green-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Calendar className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-green-600">21</div>
                  <p className="text-sm text-gray-600">This Week's Meals</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-purple-200 bg-purple-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Users className="w-8 h-8 text-purple-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-purple-600">4</div>
                  <p className="text-sm text-gray-600">Family Members</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-blue-200 bg-blue-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <ShoppingCart className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-blue-600">16</div>
                  <p className="text-sm text-gray-600">Shopping Items</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Tab Navigation */}
        <div className="flex space-x-2 mb-8">
          {[
            { id: 'plan', label: 'Weekly Plan', icon: Calendar },
            { id: 'shopping', label: 'Shopping List', icon: ShoppingCart },
            { id: 'favorites', label: 'Family Favorites', icon: Star },
            { id: 'history', label: 'Meal History', icon: Clock }
          ].map((tab) => {
            const IconComponent = tab.icon;
            return (
              <Button
                key={tab.id}
                variant={activeTab === tab.id ? 'default' : 'outline'}
                onClick={() => setActiveTab(tab.id)}
                className={activeTab === tab.id ? 'bg-amber-600 hover:bg-amber-700' : ''}
              >
                <IconComponent className="w-4 h-4 mr-2" />
                {tab.label}
              </Button>
            );
          })}
        </div>

        {/* Tab Content */}
        {activeTab === 'plan' && (
          <div className="space-y-6">
            {/* Current Meal Plan */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center">
                    <Calendar className="w-5 h-5 mr-2 text-amber-600" />
                    This Week's Meal Plan
                  </CardTitle>
                  <Button className="bg-amber-600 hover:bg-amber-700">
                    <Plus className="w-4 h-4 mr-2" />
                    Edit Plan
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 gap-4">
                  {weeklyMeals.map((day) => (
                    <div key={day.day} className="border rounded-lg p-4">
                      <h3 className="font-semibold text-gray-900 mb-3">{day.day}</h3>
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                          <Badge className={getMealTime('breakfast')} variant="secondary">Breakfast</Badge>
                          <p className="text-sm text-gray-600 mt-1">{day.breakfast}</p>
                        </div>
                        <div>
                          <Badge className={getMealTime('lunch')} variant="secondary">Lunch</Badge>
                          <p className="text-sm text-gray-600 mt-1">{day.lunch}</p>
                        </div>
                        <div>
                          <Badge className={getMealTime('dinner')} variant="secondary">Dinner</Badge>
                          <p className="text-sm text-gray-600 mt-1">{day.dinner}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {activeTab === 'shopping' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {shoppingList.map((category) => (
              <Card key={category.category}>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <ShoppingCart className="w-5 h-5 mr-2 text-amber-600" />
                    {category.category}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {category.items.map((item, index) => (
                      <div key={index} className="flex items-center space-x-3 p-2 hover:bg-gray-50 rounded">
                        <input type="checkbox" className="rounded" />
                        <span className="text-gray-700">{item}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {activeTab === 'favorites' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {favorites.map((recipe, index) => (
              <Card key={index} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <CardTitle className="text-lg">{recipe.name}</CardTitle>
                    <div className="flex">
                      {renderStars(recipe.rating)}
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Prep Time:</span>
                      <span className="font-medium">{recipe.prepTime}</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-600">Serves:</span>
                      <span className="font-medium">{recipe.serves} people</span>
                    </div>
                    <div className="pt-2">
                      <Button variant="outline" className="w-full">
                        <Utensils className="w-4 h-4 mr-2" />
                        View Recipe
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {activeTab === 'history' && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Clock className="w-5 h-5 mr-2 text-amber-600" />
                Previous Meal Plans
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {mealPlans.map((plan) => (
                  <div key={plan.id} className="border rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="font-semibold text-gray-900">{plan.name}</h3>
                        <p className="text-sm text-gray-500">{plan.date}</p>
                      </div>
                      <div className="flex items-center space-x-3">
                        <Badge className={getStatusColor(plan.status)}>
                          {plan.status}
                        </Badge>
                        <div className="text-sm text-gray-600">
                          {plan.meals} meals • {plan.familyMembers} members
                        </div>
                        <Button variant="outline" size="sm">
                          View Plan
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default FamilyMeals;