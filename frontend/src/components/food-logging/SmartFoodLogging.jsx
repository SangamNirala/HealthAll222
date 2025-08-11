import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Badge } from '../ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { 
  Camera, 
  Mic, 
  Scan, 
  Search, 
  Plus,
  Clock,
  Utensils,
  Sparkles,
  CheckCircle
} from 'lucide-react';

import AIPhotoRecognition from './AIPhotoRecognition';
import VoiceLogging from './VoiceLogging';
import NutritionBarScanner from './NutritionBarScanner';
import MealPredictions from './MealPredictions';
import QuickAddButtons from './QuickAddButtons';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

const SmartFoodLogging = ({ userId, onFoodLogged }) => {
  const [activeTab, setActiveTab] = useState('search');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isSearching, setIsSearching] = useState(false);
  const [recentLogs, setRecentLogs] = useState([]);
  const [dailySummary, setDailySummary] = useState({
    calories: 0,
    protein: 0,
    carbs: 0,
    fat: 0,
    meals: 0
  });

  useEffect(() => {
    fetchDailySummary();
    fetchRecentLogs();
  }, [userId]);

  const fetchDailySummary = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/patient/food-log/${userId}/daily-summary`);
      if (response.ok) {
        const data = await response.json();
        setDailySummary(data.summary || dailySummary);
      }
    } catch (error) {
      console.error('Failed to fetch daily summary:', error);
    }
  };

  const fetchRecentLogs = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/patient/food-log/${userId}/recent`);
      if (response.ok) {
        const data = await response.json();
        setRecentLogs(data.logs || []);
      }
    } catch (error) {
      console.error('Failed to fetch recent logs:', error);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    setIsSearching(true);
    try {
      // Use Open Food Facts service for search
      const { default: openFoodFactsService } = await import('../../services/openFoodFactsService');
      const result = await openFoodFactsService.searchProducts(searchQuery, 20);
      
      if (result.success) {
        setSearchResults(result.products);
      } else {
        console.error('Search failed:', result.error);
        setSearchResults([]);
      }
    } catch (error) {
      console.error('Search error:', error);
      setSearchResults([]);
    } finally {
      setIsSearching(false);
    }
  };

  const handleFoodAdd = async (foodData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/patient/food-log`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId,
          food_name: foodData.name,
          brand: foodData.brand || '',
          calories: foodData.nutrition?.calories || 0,
          protein: foodData.nutrition?.protein || 0,
          carbs: foodData.nutrition?.carbs || 0,
          fat: foodData.nutrition?.fat || 0,
          fiber: foodData.nutrition?.fiber || 0,
          sodium: foodData.nutrition?.sodium || 0,
          serving_size: foodData.nutrition?.servingSize || '100g',
          meal_type: getCurrentMealType(),
          source: foodData.source || 'manual'
        })
      });

      if (response.ok) {
        const result = await response.json();
        
        // Refresh data
        await fetchDailySummary();
        await fetchRecentLogs();
        
        // Notify parent component
        if (onFoodLogged) {
          onFoodLogged(result);
        }
        
        // Show success feedback
        setActiveTab('success');
        setTimeout(() => setActiveTab('search'), 2000);
      }
    } catch (error) {
      console.error('Failed to log food:', error);
    }
  };

  const getCurrentMealType = () => {
    const hour = new Date().getHours();
    if (hour >= 5 && hour <= 10) return 'breakfast';
    if (hour >= 11 && hour <= 15) return 'lunch';
    if (hour >= 17 && hour <= 22) return 'dinner';
    return 'snack';
  };

  const DailySummaryCard = () => (
    <Card className="bg-gradient-to-r from-blue-50 to-indigo-50 border-blue-200">
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-semibold text-blue-900">Today's Progress</h3>
          <Badge variant="secondary" className="bg-blue-100 text-blue-800">
            {dailySummary.meals} meals logged
          </Badge>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div className="text-center">
            <div className="text-lg font-bold text-blue-600">{dailySummary.calories}</div>
            <div className="text-xs text-blue-700">Calories</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-green-600">{dailySummary.protein}g</div>
            <div className="text-xs text-green-700">Protein</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-yellow-600">{dailySummary.carbs}g</div>
            <div className="text-xs text-yellow-700">Carbs</div>
          </div>
          <div className="text-center">
            <div className="text-lg font-bold text-red-600">{dailySummary.fat}g</div>
            <div className="text-xs text-red-700">Fat</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );

  const SearchResultCard = ({ product, onAdd }) => (
    <Card className="hover:shadow-md transition-shadow cursor-pointer" onClick={() => onAdd(product)}>
      <CardContent className="p-4">
        <div className="flex items-start gap-3">
          {product.image && (
            <img 
              src={product.image} 
              alt={product.name}
              className="w-12 h-12 object-cover rounded-lg"
            />
          )}
          <div className="flex-1">
            <h4 className="font-medium text-gray-900 line-clamp-2">{product.name}</h4>
            {product.brand && (
              <p className="text-sm text-gray-600">{product.brand}</p>
            )}
            <div className="flex gap-4 mt-2 text-xs text-gray-700">
              <span>{product.nutrition?.calories || 0} cal</span>
              <span>{product.nutrition?.protein || 0}g protein</span>
              <span>{product.nutrition?.carbs || 0}g carbs</span>
            </div>
            {product.nutritionGrade && (
              <Badge variant="outline" className="mt-2">
                Grade: {product.nutritionGrade.toUpperCase()}
              </Badge>
            )}
          </div>
          <Button size="sm" variant="outline">
            <Plus className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="space-y-6">
      {/* Daily Summary */}
      <DailySummaryCard />

      {/* Quick Add Suggestions */}
      <QuickAddButtons userId={userId} onFoodAdd={handleFoodAdd} />

      {/* Main Logging Interface */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Utensils className="h-5 w-5" />
            Smart Food Logging
          </CardTitle>
          <p className="text-sm text-gray-600">
            Log your food using AI-powered recognition, voice commands, or barcode scanning
          </p>
        </CardHeader>
        <CardContent>
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-5">
              <TabsTrigger value="search" className="flex items-center gap-1">
                <Search className="h-4 w-4" />
                Search
              </TabsTrigger>
              <TabsTrigger value="photo" className="flex items-center gap-1">
                <Camera className="h-4 w-4" />
                Photo
              </TabsTrigger>
              <TabsTrigger value="voice" className="flex items-center gap-1">
                <Mic className="h-4 w-4" />
                Voice
              </TabsTrigger>
              <TabsTrigger value="scan" className="flex items-center gap-1">
                <Scan className="h-4 w-4" />
                Scan
              </TabsTrigger>
              <TabsTrigger value="predict" className="flex items-center gap-1">
                <Sparkles className="h-4 w-4" />
                Predict
              </TabsTrigger>
            </TabsList>

            <TabsContent value="search" className="space-y-4 mt-4">
              <div className="flex gap-2">
                <Input
                  placeholder="Search for food (e.g., 'grilled chicken', 'apple')"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                />
                <Button onClick={handleSearch} disabled={isSearching}>
                  {isSearching ? 'Searching...' : 'Search'}
                </Button>
              </div>

              {searchResults.length > 0 && (
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  <h4 className="font-medium text-gray-900">
                    Found {searchResults.length} results
                  </h4>
                  {searchResults.map((product, index) => (
                    <SearchResultCard 
                      key={index} 
                      product={product}
                      onAdd={handleFoodAdd}
                    />
                  ))}
                </div>
              )}

              {searchQuery && searchResults.length === 0 && !isSearching && (
                <div className="text-center py-8 text-gray-500">
                  <Search className="h-12 w-12 mx-auto mb-2 opacity-50" />
                  <p>No results found. Try a different search term or use photo recognition.</p>
                </div>
              )}
            </TabsContent>

            <TabsContent value="photo" className="mt-4">
              <AIPhotoRecognition userId={userId} onFoodRecognized={handleFoodAdd} />
            </TabsContent>

            <TabsContent value="voice" className="mt-4">
              <VoiceLogging userId={userId} onFoodLogged={handleFoodAdd} />
            </TabsContent>

            <TabsContent value="scan" className="mt-4">
              <NutritionBarScanner userId={userId} onProductScanned={handleFoodAdd} />
            </TabsContent>

            <TabsContent value="predict" className="mt-4">
              <MealPredictions userId={userId} onMealSelected={handleFoodAdd} />
            </TabsContent>

            <TabsContent value="success" className="mt-4">
              <div className="text-center py-8">
                <CheckCircle className="h-16 w-16 mx-auto mb-4 text-green-500" />
                <h3 className="text-lg font-semibold text-green-700 mb-2">
                  Food Logged Successfully!
                </h3>
                <p className="text-gray-600">
                  Your nutrition data has been updated.
                </p>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      {/* Recent Logs */}
      {recentLogs.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Recent Logs
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {recentLogs.slice(0, 5).map((log, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="font-medium">{log.food_name}</p>
                    {log.brand && <p className="text-sm text-gray-600">{log.brand}</p>}
                    <p className="text-xs text-gray-500">{log.meal_type} • {log.timestamp}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium">{log.calories} cal</p>
                    <p className="text-xs text-gray-600">
                      {log.protein}P • {log.carbs}C • {log.fat}F
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default SmartFoodLogging;