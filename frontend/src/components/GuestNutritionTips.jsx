import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { BookOpen, Heart, Apple, Droplets, Clock, Star, ChevronRight, TrendingUp } from 'lucide-react';

const GuestNutritionTips = () => {
  const { switchRole } = useRole();
  const [activeCategory, setActiveCategory] = useState('all');
  const [favorited, setFavorited] = useState([]);

  // Switch to guest role when component mounts
  useEffect(() => {
    switchRole('guest');
  }, [switchRole]);

  const categories = [
    { id: 'all', name: 'All Tips', icon: BookOpen },
    { id: 'hydration', name: 'Hydration', icon: Droplets },
    { id: 'nutrition', name: 'Nutrition', icon: Apple },
    { id: 'habits', name: 'Healthy Habits', icon: Heart },
    { id: 'timing', name: 'Meal Timing', icon: Clock }
  ];

  const nutritionTips = [
    {
      id: 1,
      title: 'Stay Hydrated',
      category: 'hydration',
      description: 'Drinking water before meals can help with portion control and digestion. Aim for at least 8 glasses throughout the day.',
      priority: 'high',
      readTime: '2 min',
      tags: ['hydration', 'digestion', 'weight management']
    },
    {
      id: 2,
      title: 'Fill Half Your Plate with Vegetables',
      category: 'nutrition',
      description: 'Choose whole grains over refined grains. Include protein in every meal to help maintain stable blood sugar levels.',
      priority: 'high',
      readTime: '3 min',
      tags: ['vegetables', 'portion control', 'nutrients']
    },
    {
      id: 3,
      title: 'Choose Whole Grains',
      category: 'nutrition',
      description: 'Whole grains provide more fiber, vitamins, and minerals compared to refined grains. Look for "100% whole grain" labels.',
      priority: 'medium',
      readTime: '2 min',
      tags: ['whole grains', 'fiber', 'nutrients']
    },
    {
      id: 4,
      title: 'Include Protein in Every Meal',
      category: 'nutrition',
      description: 'Protein helps maintain stable blood sugar levels and keeps you feeling full longer. Good sources include lean meats, fish, beans, and nuts.',
      priority: 'high',
      readTime: '3 min',
      tags: ['protein', 'blood sugar', 'satiety']
    },
    {
      id: 5,
      title: 'Eat Mindfully',
      category: 'habits',
      description: 'Take time to eat without distractions. Chew slowly and pay attention to hunger and fullness cues.',
      priority: 'medium',
      readTime: '4 min',
      tags: ['mindfulness', 'digestion', 'portion control']
    },
    {
      id: 6,
      title: 'Time Your Meals',
      category: 'timing',
      description: 'Try to eat regular meals and snacks. Avoid skipping meals as this can lead to overeating later.',
      priority: 'medium',
      readTime: '2 min',
      tags: ['meal timing', 'metabolism', 'hunger']
    },
    {
      id: 7,
      title: 'Healthy Snacking',
      category: 'habits',
      description: 'Choose nutrient-dense snacks like fruits, vegetables with hummus, or a handful of nuts instead of processed foods.',
      priority: 'medium',
      readTime: '3 min',
      tags: ['snacking', 'nutrients', 'energy']
    },
    {
      id: 8,
      title: 'Color Variety',
      category: 'nutrition',
      description: 'Eat a rainbow of fruits and vegetables. Different colors provide different vitamins, minerals, and antioxidants.',
      priority: 'high',
      readTime: '2 min',
      tags: ['variety', 'antioxidants', 'vitamins']
    }
  ];

  const filteredTips = activeCategory === 'all' 
    ? nutritionTips 
    : nutritionTips.filter(tip => tip.category === activeCategory);

  const toggleFavorite = (tipId) => {
    if (favorited.includes(tipId)) {
      setFavorited(favorited.filter(id => id !== tipId));
    } else {
      setFavorited([...favorited, tipId]);
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityLabel = (priority) => {
    switch (priority) {
      case 'high': return 'Must Know';
      case 'medium': return 'Good to Know';
      case 'low': return 'Bonus Tip';
      default: return 'Tip';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-violet-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Nutrition Tips</h1>
          <p className="text-gray-600">Simple, practical advice to help you make healthier food choices</p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-2 border-purple-200 bg-purple-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <BookOpen className="w-8 h-8 text-purple-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-purple-600">{nutritionTips.length}</div>
                  <p className="text-sm text-gray-600">Total Tips</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <TrendingUp className="w-8 h-8 text-red-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-red-600">
                    {nutritionTips.filter(tip => tip.priority === 'high').length}
                  </div>
                  <p className="text-sm text-gray-600">Must Know</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-yellow-200 bg-yellow-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Star className="w-8 h-8 text-yellow-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-yellow-600">{favorited.length}</div>
                  <p className="text-sm text-gray-600">Favorited</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-green-200 bg-green-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Clock className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-green-600">
                    {nutritionTips.reduce((total, tip) => total + parseInt(tip.readTime), 0)}
                  </div>
                  <p className="text-sm text-gray-600">Total Minutes</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Category Filter */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Categories</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {categories.map((category) => {
                    const IconComponent = category.icon;
                    const isActive = activeCategory === category.id;
                    return (
                      <Button
                        key={category.id}
                        variant={isActive ? "default" : "ghost"}
                        onClick={() => setActiveCategory(category.id)}
                        className={`w-full justify-start ${
                          isActive 
                            ? 'bg-purple-600 hover:bg-purple-700 text-white' 
                            : 'hover:bg-purple-50'
                        }`}
                      >
                        <IconComponent className="w-4 h-4 mr-2" />
                        {category.name}
                      </Button>
                    );
                  })}
                </div>
              </CardContent>
            </Card>

            {/* Today's Focus */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle className="text-lg flex items-center">
                  <Star className="w-5 h-5 mr-2 text-yellow-500" />
                  Today's Focus
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="p-3 bg-gradient-to-r from-purple-100 to-violet-100 rounded-lg">
                  <h4 className="font-semibold text-purple-900 mb-1">Stay Hydrated</h4>
                  <p className="text-sm text-purple-700">
                    Try to drink a glass of water every hour. Set reminders if needed!
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Tips Grid */}
          <div className="lg:col-span-3">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {filteredTips.map((tip) => (
                <Card key={tip.id} className="hover:shadow-lg transition-shadow cursor-pointer">
                  <CardHeader className="pb-3">
                    <div className="flex items-start justify-between">
                      <CardTitle className="text-lg leading-tight">{tip.title}</CardTitle>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => toggleFavorite(tip.id)}
                        className="p-1 h-auto"
                      >
                        <Star 
                          className={`w-4 h-4 ${
                            favorited.includes(tip.id) 
                              ? 'text-yellow-500 fill-current' 
                              : 'text-gray-400'
                          }`} 
                        />
                      </Button>
                    </div>
                    <div className="flex items-center space-x-2 mt-2">
                      <Badge className={getPriorityColor(tip.priority)}>
                        {getPriorityLabel(tip.priority)}
                      </Badge>
                      <Badge variant="outline" className="text-xs">
                        <Clock className="w-3 h-3 mr-1" />
                        {tip.readTime}
                      </Badge>
                    </div>
                  </CardHeader>
                  
                  <CardContent>
                    <p className="text-gray-600 mb-4 text-sm leading-relaxed">
                      {tip.description}
                    </p>
                    
                    <div className="flex flex-wrap gap-1 mb-3">
                      {tip.tags.map((tag, index) => (
                        <Badge 
                          key={index}
                          variant="secondary"
                          className="text-xs bg-purple-100 text-purple-700"
                        >
                          {tag}
                        </Badge>
                      ))}
                    </div>
                    
                    <Button variant="outline" size="sm" className="w-full">
                      Learn More
                      <ChevronRight className="w-4 h-4 ml-2" />
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
            
            {filteredTips.length === 0 && (
              <div className="text-center py-12">
                <BookOpen className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <div className="text-gray-500 mb-2">No tips found in this category</div>
                <p className="text-sm text-gray-400">Try selecting a different category</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default GuestNutritionTips;