import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import FormField from '../../shared/FormField';
import { Utensils, Clock, ChefHat, Globe } from 'lucide-react';

const DietaryProfileStep = ({ data = {}, onChange, icon: Icon }) => {
  const updateField = (field, value) => {
    const updatedData = { ...data, [field]: value };
    onChange(updatedData);
  };

  const updateListField = (field, item, checked) => {
    const currentItems = data[field] || [];
    let updatedItems;
    
    if (checked) {
      updatedItems = [...currentItems, item];
    } else {
      updatedItems = currentItems.filter(i => i !== item);
    }
    
    updateField(field, updatedItems);
  };

  const dietTypes = [
    {
      value: 'OMNIVORE',
      label: 'Omnivore',
      description: 'Eat all types of food including meat, fish, and dairy'
    },
    {
      value: 'VEGETARIAN',
      label: 'Vegetarian',
      description: 'No meat or fish, but includes dairy and eggs'
    },
    {
      value: 'VEGAN',
      label: 'Vegan',
      description: 'No animal products at all'
    },
    {
      value: 'PESCATARIAN',
      label: 'Pescatarian',
      description: 'No meat, but includes fish, dairy, and eggs'
    },
    {
      value: 'FLEXITARIAN',
      label: 'Flexitarian',
      description: 'Mostly vegetarian with occasional meat'
    }
  ];

  const mealTimingPreferences = [
    {
      value: 'TRADITIONAL_3_MEALS',
      label: 'Traditional 3 Meals',
      description: 'Breakfast, lunch, and dinner'
    },
    {
      value: 'SMALL_FREQUENT',
      label: 'Small Frequent Meals',
      description: '5-6 smaller meals throughout the day'
    },
    {
      value: 'INTERMITTENT_FASTING',
      label: 'Intermittent Fasting',
      description: 'Eating within specific time windows'
    }
  ];

  const culturalRestrictions = [
    'Halal',
    'Kosher',
    'Hindu (no beef)',
    'Jain (no root vegetables)',
    'Buddhist (no meat)',
    'Seventh-day Adventist',
    'None'
  ];

  const specificDiets = [
    'Ketogenic (Keto)',
    'Paleo',
    'Mediterranean',
    'DASH',
    'Low-Carb',
    'Low-Fat',
    'Gluten-Free',
    'Whole30',
    'Anti-Inflammatory',
    'Plant-Based',
    'Low-FODMAP',
    'None/Standard'
  ];

  const commonFoodDislikes = [
    'Seafood',
    'Mushrooms',
    'Cilantro',
    'Coconut',
    'Brussels Sprouts',
    'Liver/Organ Meats',
    'Spicy Food',
    'Very Sweet Foods',
    'Bitter Foods',
    'Sour Foods',
    'Strong Cheeses',
    'Raw Fish/Sushi'
  ];

  const cookingSkillLabels = [
    'Beginner - Can make basic meals',
    'Novice - Comfortable with simple recipes',
    'Intermediate - Can follow most recipes',
    'Advanced - Comfortable with complex dishes',
    'Expert - Can create recipes and modify dishes'
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-3 mb-6">
        {Icon && <Icon className="w-8 h-8 text-blue-500" />}
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Dietary Profile</h2>
          <p className="text-gray-600">Your food preferences and dietary requirements</p>
        </div>
      </div>

      {/* Diet Type */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Utensils className="w-5 h-5 mr-2" />
            Diet Type
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <FormField
            type="radio"
            label="Primary Diet Type"
            value={data.diet_type}
            onChange={(value) => updateField('diet_type', value)}
            options={dietTypes.map(diet => ({
              value: diet.value,
              label: (
                <div>
                  <div className="font-medium">{diet.label}</div>
                  <div className="text-sm text-gray-500">{diet.description}</div>
                </div>
              )
            }))}
            required
          />
        </CardContent>
      </Card>

      {/* Cultural & Religious Restrictions */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Globe className="w-5 h-5 mr-2" />
            Cultural & Religious Considerations
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Cultural or Religious Dietary Restrictions (select all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {culturalRestrictions.map((restriction) => (
                <FormField
                  key={restriction}
                  type="checkbox"
                  label={restriction}
                  value={data.cultural_restrictions?.includes(restriction)}
                  onChange={(checked) => updateListField('cultural_restrictions', restriction, checked)}
                />
              ))}
            </div>
          </div>

          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Specific Diet Plans or Protocols (select all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {specificDiets.map((diet) => (
                <FormField
                  key={diet}
                  type="checkbox"
                  label={diet}
                  value={data.specific_diets?.includes(diet)}
                  onChange={(checked) => updateListField('specific_diets', diet, checked)}
                />
              ))}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Food Preferences */}
      <Card>
        <CardHeader>
          <CardTitle>Food Preferences & Dislikes</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <FormField
            type="textarea"
            label="Food Allergies"
            value={data.food_allergies?.join(', ')}
            onChange={(value) => updateField('food_allergies', value.split(', ').filter(item => item.trim()))}
            placeholder="List any food allergies (separate with commas)"
            helpText="Critical for meal planning - be specific about allergens"
          />

          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Foods You Dislike or Avoid (select all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {commonFoodDislikes.map((food) => (
                <FormField
                  key={food}
                  type="checkbox"
                  label={food}
                  value={data.food_dislikes?.includes(food)}
                  onChange={(checked) => updateListField('food_dislikes', food, checked)}
                />
              ))}
            </div>
          </div>

          <FormField
            type="textarea"
            label="Additional Food Preferences or Dislikes"
            value={data.additional_preferences}
            onChange={(value) => updateField('additional_preferences', value)}
            placeholder="Describe any other food preferences, textures you dislike, or specific foods you love"
            rows={3}
          />
        </CardContent>
      </Card>

      {/* Meal Timing & Cooking */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Clock className="w-5 h-5 mr-2" />
            Meal Timing & Preparation
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <FormField
            type="radio"
            label="Meal Timing Preference"
            value={data.meal_timing_preference}
            onChange={(value) => updateField('meal_timing_preference', value)}
            options={mealTimingPreferences.map(timing => ({
              value: timing.value,
              label: (
                <div>
                  <div className="font-medium">{timing.label}</div>
                  <div className="text-sm text-gray-500">{timing.description}</div>
                </div>
              )
            }))}
            required
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <FormField
              type="radio"
              label="Cooking Skill Level"
              value={data.cooking_skill_level}
              onChange={(value) => updateField('cooking_skill_level', parseInt(value))}
              options={cookingSkillLabels.map((label, index) => ({
                value: (index + 1).toString(),
                label: `${index + 1} - ${label.split(' - ')[1]}`
              }))}
              required
            />

            <FormField
              type="number"
              label="Available Cooking Time (minutes per day)"
              value={data.available_cooking_time}
              onChange={(value) => updateField('available_cooking_time', parseInt(value) || 0)}
              placeholder="30"
              min="0"
              max="480"
              helpText="How much time you can dedicate to cooking daily"
              required
            />
          </div>
        </CardContent>
      </Card>

      {/* Kitchen & Equipment */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <ChefHat className="w-5 h-5 mr-2" />
            Kitchen Setup (Optional)
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium text-gray-700 mb-3 block">
              Available Kitchen Equipment (select all you have)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {[
                'Stovetop', 'Oven', 'Microwave', 'Air Fryer', 'Slow Cooker', 
                'Instant Pot', 'Blender', 'Food Processor', 'Grill', 'Steamer',
                'Rice Cooker', 'Toaster Oven'
              ].map((equipment) => (
                <FormField
                  key={equipment}
                  type="checkbox"
                  label={equipment}
                  value={data.kitchen_equipment?.includes(equipment)}
                  onChange={(checked) => updateListField('kitchen_equipment', equipment, checked)}
                />
              ))}
            </div>
          </div>

          <FormField
            type="select"
            label="Typical Grocery Budget (per week)"
            value={data.grocery_budget}
            onChange={(value) => updateField('grocery_budget', value)}
            placeholder="Select budget range"
            options={[
              { value: 'low', label: 'Low ($50-100/week)' },
              { value: 'moderate', label: 'Moderate ($100-200/week)' },
              { value: 'high', label: 'High ($200+/week)' },
              { value: 'no_limit', label: 'No specific limit' }
            ]}
            helpText="Helps us suggest cost-appropriate meal plans"
          />
        </CardContent>
      </Card>

      {/* Dietary Tips */}
      <div className="bg-green-50 p-4 rounded-lg">
        <h4 className="font-medium text-green-900 mb-2">🥗 Personalized Nutrition</h4>
        <ul className="text-sm text-green-800 space-y-1">
          <li>• Your dietary preferences help us create meal plans you'll actually enjoy</li>
          <li>• We'll respect all allergies, restrictions, and cultural preferences</li>
          <li>• Recipes will match your cooking skill level and available time</li>
          <li>• All meal suggestions consider your health goals and dietary needs</li>
        </ul>
      </div>
    </div>
  );
};

export default DietaryProfileStep;