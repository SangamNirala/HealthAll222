import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Search, Plus, Clock, Trash2, Target, Apple } from 'lucide-react';

const GuestFoodLog = () => {
  const { switchRole } = useRole();
  const [searchQuery, setSearchQuery] = useState('');
  const [loggedFoods, setLoggedFoods] = useState([
    {
      id: 1,
      name: 'Toast with avocado',
      time: '8:30 AM',
      calories: 320,
      meal: 'Breakfast'
    }
  ]);

  const [newFood, setNewFood] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);

  // Switch to guest role when component mounts
  useEffect(() => {
    switchRole('guest');
  }, [switchRole]);

  const handleAddFood = () => {
    if (newFood.trim()) {
      const newEntry = {
        id: loggedFoods.length + 1,
        name: newFood,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        calories: Math.floor(Math.random() * 300) + 100, // Random for demo
        meal: getMealTime()
      };
      setLoggedFoods([...loggedFoods, newEntry]);
      setNewFood('');
      setShowAddForm(false);
    }
  };

  const getMealTime = () => {
    const hour = new Date().getHours();
    if (hour < 11) return 'Breakfast';
    if (hour < 16) return 'Lunch';
    if (hour < 20) return 'Dinner';
    return 'Snack';
  };

  const removeFood = (id) => {
    setLoggedFoods(loggedFoods.filter(food => food.id !== id));
  };

  const getTotalCalories = () => {
    return loggedFoods.reduce((total, food) => total + food.calories, 0);
  };

  const getMealColor = (meal) => {
    switch (meal) {
      case 'Breakfast': return 'bg-yellow-100 text-yellow-800';
      case 'Lunch': return 'bg-green-100 text-green-800';
      case 'Dinner': return 'bg-purple-100 text-purple-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-violet-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Quick Food Log</h1>
          <p className="text-gray-600">Simple food tracking to get started with healthy habits</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card className="border-2 border-purple-200 bg-purple-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                <Apple className="w-4 h-4 mr-2 text-purple-600" />
                Total Calories
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-purple-600">{getTotalCalories()}</div>
              <p className="text-xs text-gray-500">logged today</p>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-green-200 bg-green-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                <Clock className="w-4 h-4 mr-2 text-green-600" />
                Meals Logged
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{loggedFoods.length}</div>
              <p className="text-xs text-gray-500">entries today</p>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-orange-200 bg-orange-50">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 flex items-center">
                <Target className="w-4 h-4 mr-2 text-orange-600" />
                Daily Goal
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-orange-600">2000</div>
              <p className="text-xs text-gray-500">calories target</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Quick Add Food */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Plus className="w-5 h-5 mr-2 text-purple-600" />
                  Add Food
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="relative">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    placeholder="Search for food..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
                
                {showAddForm ? (
                  <div className="space-y-3">
                    <Input
                      placeholder="What did you eat?"
                      value={newFood}
                      onChange={(e) => setNewFood(e.target.value)}
                    />
                    <div className="flex space-x-2">
                      <Button onClick={handleAddFood} className="bg-purple-600 hover:bg-purple-700">
                        Add Food
                      </Button>
                      <Button variant="outline" onClick={() => setShowAddForm(false)}>
                        Cancel
                      </Button>
                    </div>
                  </div>
                ) : (
                  <Button 
                    onClick={() => setShowAddForm(true)}
                    className="w-full bg-purple-600 hover:bg-purple-700"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Quick Add
                  </Button>
                )}

                <div className="border-t pt-4">
                  <h3 className="font-semibold text-gray-900 mb-2">Popular Foods</h3>
                  <div className="grid grid-cols-1 gap-2">
                    {[
                      'Scrambled eggs', 'Greek yogurt', 'Banana', 'Chicken breast', 
                      'Brown rice', 'Salmon', 'Mixed salad', 'Oatmeal'
                    ].map((food) => (
                      <Button
                        key={food}
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setNewFood(food);
                          setShowAddForm(true);
                        }}
                        className="text-xs justify-start"
                      >
                        {food}
                      </Button>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Food Log Entries */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <Clock className="w-5 h-5 mr-2 text-purple-600" />
                    Today's Food Log
                  </span>
                  <Badge variant="secondary" className="bg-purple-100 text-purple-800">
                    {loggedFoods.length} entries
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {loggedFoods.length === 0 ? (
                  <div className="text-center py-12">
                    <Apple className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                    <div className="text-gray-400 mb-2">No food logged yet</div>
                    <p className="text-sm text-gray-500">Start by adding your first meal!</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {loggedFoods.map((food) => (
                      <div key={food.id} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                        <div className="flex items-center justify-between mb-2">
                          <div className="flex items-center space-x-3">
                            <Badge className={getMealColor(food.meal)}>{food.meal}</Badge>
                            <span className="text-sm text-gray-500">{food.time}</span>
                          </div>
                          <Button 
                            variant="ghost" 
                            size="sm"
                            onClick={() => removeFood(food.id)}
                            className="text-red-500 hover:text-red-700"
                          >
                            <Trash2 className="w-4 h-4" />
                          </Button>
                        </div>
                        
                        <div className="flex items-center justify-between">
                          <h3 className="font-semibold text-gray-900">{food.name}</h3>
                          <div className="text-lg font-bold text-purple-600">
                            {food.calories} <span className="text-sm text-gray-500">cal</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                
                {loggedFoods.length > 0 && (
                  <div className="mt-6 p-4 bg-purple-50 rounded-lg">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-gray-900">Daily Total</span>
                      <span className="text-xl font-bold text-purple-600">
                        {getTotalCalories()} calories
                      </span>
                    </div>
                    <div className="mt-2 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-purple-600 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${Math.min((getTotalCalories() / 2000) * 100, 100)}%` }}
                      ></div>
                    </div>
                    <p className="text-xs text-gray-500 mt-1">
                      {Math.round((getTotalCalories() / 2000) * 100)}% of daily goal
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GuestFoodLog;