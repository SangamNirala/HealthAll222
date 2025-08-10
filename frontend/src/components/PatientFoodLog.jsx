import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Search, Plus, Clock, Trash2, Edit3 } from 'lucide-react';

const PatientFoodLog = () => {
  const { switchRole } = useRole();
  const [searchQuery, setSearchQuery] = useState('');
  const [loggedFoods, setLoggedFoods] = useState([
    {
      id: 1,
      name: 'Greek Yogurt with Berries',
      time: '8:00 AM',
      calories: 180,
      meal: 'Breakfast',
      protein: 15,
      carbs: 20,
      fat: 8
    },
    {
      id: 2,
      name: 'Grilled Chicken Salad',
      time: '1:00 PM', 
      calories: 320,
      meal: 'Lunch',
      protein: 35,
      carbs: 15,
      fat: 12
    }
  ]);

  const [newFood, setNewFood] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);

  // Switch to patient role when component mounts
  useEffect(() => {
    switchRole('patient');
  }, [switchRole]);

  const handleAddFood = () => {
    if (newFood.trim()) {
      const newEntry = {
        id: loggedFoods.length + 1,
        name: newFood,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        calories: Math.floor(Math.random() * 300) + 100, // Random for demo
        meal: getMealTime(),
        protein: Math.floor(Math.random() * 20) + 5,
        carbs: Math.floor(Math.random() * 30) + 10,
        fat: Math.floor(Math.random() * 15) + 5
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
      case 'Dinner': return 'bg-blue-100 text-blue-800';
      default: return 'bg-purple-100 text-purple-800';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Food Log</h1>
          <p className="text-gray-600">Track your daily nutrition and maintain healthy eating habits</p>
        </div>

        {/* Daily Summary */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Total Calories</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">{getTotalCalories()}</div>
              <p className="text-xs text-gray-500">of 2000 goal</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Meals Logged</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{loggedFoods.length}</div>
              <p className="text-xs text-gray-500">entries today</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Protein</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-purple-600">
                {loggedFoods.reduce((total, food) => total + food.protein, 0)}g
              </div>
              <p className="text-xs text-gray-500">of 150g goal</p>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Water</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-cyan-600">6</div>
              <p className="text-xs text-gray-500">glasses today</p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Food Search and Add */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Plus className="w-5 h-5 mr-2 text-blue-600" />
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
                      placeholder="Enter food name..."
                      value={newFood}
                      onChange={(e) => setNewFood(e.target.value)}
                    />
                    <div className="flex space-x-2">
                      <Button onClick={handleAddFood} className="bg-blue-600 hover:bg-blue-700">
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
                    className="w-full bg-blue-600 hover:bg-blue-700"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Quick Add
                  </Button>
                )}

                <div className="border-t pt-4">
                  <h3 className="font-semibold text-gray-900 mb-2">Quick Options</h3>
                  <div className="grid grid-cols-2 gap-2">
                    {['Apple', 'Banana', 'Water', 'Coffee', 'Almonds', 'Yogurt'].map((food) => (
                      <Button
                        key={food}
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setNewFood(food);
                          setShowAddForm(true);
                        }}
                        className="text-xs"
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
                    <Clock className="w-5 h-5 mr-2 text-blue-600" />
                    Today's Food Log
                  </span>
                  <Badge variant="secondary">{loggedFoods.length} entries</Badge>
                </CardTitle>
              </CardHeader>
              <CardContent>
                {loggedFoods.length === 0 ? (
                  <div className="text-center py-8">
                    <div className="text-gray-400 mb-2">No food logged yet</div>
                    <p className="text-sm text-gray-500">Start logging your meals to track your nutrition</p>
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
                          <div className="flex space-x-1">
                            <Button variant="ghost" size="sm">
                              <Edit3 className="w-4 h-4" />
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="sm"
                              onClick={() => removeFood(food.id)}
                              className="text-red-500 hover:text-red-700"
                            >
                              <Trash2 className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>
                        
                        <div className="mb-3">
                          <h3 className="font-semibold text-gray-900">{food.name}</h3>
                        </div>
                        
                        <div className="grid grid-cols-4 gap-4 text-sm">
                          <div>
                            <div className="text-gray-500">Calories</div>
                            <div className="font-semibold text-orange-600">{food.calories}</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Protein</div>
                            <div className="font-semibold text-purple-600">{food.protein}g</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Carbs</div>
                            <div className="font-semibold text-blue-600">{food.carbs}g</div>
                          </div>
                          <div>
                            <div className="text-gray-500">Fat</div>
                            <div className="font-semibold text-green-600">{food.fat}g</div>
                          </div>
                        </div>
                      </div>
                    ))}
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

export default PatientFoodLog;