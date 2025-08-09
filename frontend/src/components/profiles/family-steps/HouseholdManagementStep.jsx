import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import FormField from '../../shared/FormField';
import { Home, DollarSign, ShoppingCart, ChefHat } from 'lucide-react';

const HouseholdManagementStep = ({ data, onChange, icon: Icon }) => {
  const handleChange = (field, value) => {
    const updatedData = {
      ...data,
      [field]: value
    };
    onChange(updatedData);
  };

  const handleArrayChange = (field, value) => {
    const items = value.split(',').map(item => item.trim()).filter(item => item);
    handleChange(field, items);
  };

  const budgetPriorityOptions = [
    { value: 'cost_effective', label: 'Cost-effective options' },
    { value: 'balanced', label: 'Balance cost and quality' },
    { value: 'premium', label: 'Premium/organic preferred' },
    { value: 'no_concern', label: 'Budget is not a concern' }
  ];

  const cookingSkillOptions = [
    { value: 'beginner', label: 'Beginner (simple recipes)' },
    { value: 'intermediate', label: 'Intermediate (most recipes)' },
    { value: 'advanced', label: 'Advanced (complex cooking)' },
    { value: 'professional', label: 'Professional level' }
  ];

  return (
    <div className="space-y-8">
      {/* Step Header */}
      <div className="text-center">
        <div className="mx-auto w-16 h-16 bg-amber-100 rounded-full flex items-center justify-center mb-4">
          <Icon className="w-8 h-8 text-amber-600" />
        </div>
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Household Management</h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Set up meal planning, budget considerations, and family responsibilities
        </p>
      </div>

      {/* Dietary Management */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Home className="w-5 h-5 mr-2 text-amber-600" />
            Family Dietary Management
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <FormField
            type="input"
            label="Common Dietary Restrictions"
            value={data?.common_dietary_restrictions?.join(', ') || ''}
            onChange={(value) => handleArrayChange('common_dietary_restrictions', value)}
            placeholder="e.g., Vegetarian, Gluten-free, Dairy-free"
            helpText="List any dietary restrictions that apply to the whole family"
          />

          <FormField
            type="input"
            label="Family Meal Preferences"
            value={data?.family_meal_preferences?.join(', ') || ''}
            onChange={(value) => handleArrayChange('family_meal_preferences', value)}
            placeholder="e.g., Mediterranean, Asian cuisine, Comfort foods"
            helpText="What types of meals does your family enjoy?"
          />
        </CardContent>
      </Card>

      {/* Budget Considerations */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <DollarSign className="w-5 h-5 mr-2 text-amber-600" />
            Budget & Shopping
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <FormField
            type="select"
            label="Budget Priority"
            value={data?.budget_considerations?.priority || ''}
            onChange={(value) => handleChange('budget_considerations', { 
              ...data?.budget_considerations, 
              priority: value 
            })}
            options={budgetPriorityOptions}
            placeholder="Select budget approach"
            helpText="How do you approach grocery budgeting for your family?"
          />

          <FormField
            type="number"
            label="Weekly Grocery Budget (Optional)"
            value={data?.budget_considerations?.weekly_budget || ''}
            onChange={(value) => handleChange('budget_considerations', { 
              ...data?.budget_considerations, 
              weekly_budget: parseFloat(value) || 0
            })}
            placeholder="Enter weekly budget"
            helpText="This helps us suggest cost-appropriate meal plans"
          />

          <FormField
            type="input"
            label="Shopping Responsibilities"
            value={data?.shopping_responsibilities?.join(', ') || ''}
            onChange={(value) => handleArrayChange('shopping_responsibilities', value)}
            placeholder="e.g., Mom does main shopping, Dad handles weekend runs"
            helpText="Who handles grocery shopping in your family?"
          />
        </CardContent>
      </Card>

      {/* Cooking Management */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <ChefHat className="w-5 h-5 mr-2 text-amber-600" />
            Cooking & Meal Preparation
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <FormField
            type="input"
            label="Cooking Responsibilities"
            value={data?.cooking_responsibilities?.join(', ') || ''}
            onChange={(value) => handleArrayChange('cooking_responsibilities', value)}
            placeholder="e.g., Mom cooks dinner, Kids help with breakfast"
            helpText="How are cooking duties shared in your family?"
          />

          <FormField
            type="select"
            label="Family Cooking Skill Level"
            value={data?.cooking_skill_level || ''}
            onChange={(value) => handleChange('cooking_skill_level', value)}
            options={cookingSkillOptions}
            placeholder="Select overall skill level"
            helpText="This helps us suggest appropriate recipes"
          />

          <FormField
            type="number"
            label="Available Cooking Time per Day"
            value={data?.cooking_time_available || ''}
            onChange={(value) => handleChange('cooking_time_available', parseInt(value) || 0)}
            placeholder="Enter minutes"
            min="0"
            max="300"
            helpText="How much time can you typically spend cooking each day?"
          />
        </CardContent>
      </Card>

      {/* Additional Notes */}
      <Card>
        <CardContent className="pt-6">
          <div className="bg-amber-50 p-4 rounded-lg">
            <h4 className="font-semibold text-amber-800 mb-2">Household Management Benefits:</h4>
            <ul className="text-sm text-amber-700 space-y-1">
              <li>• Generate family-friendly meal plans within your budget</li>
              <li>• Create shared shopping lists and assign responsibilities</li>
              <li>• Coordinate cooking schedules and skill-appropriate recipes</li>
              <li>• Track family dietary needs and preferences</li>
              <li>• Streamline household food management</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default HouseholdManagementStep;