import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { BookOpen, Heart, Apple, Droplets, Clock, Star, ChevronRight, TrendingUp, X, Brain, Activity, Utensils, Leaf, Zap } from 'lucide-react';

const GuestNutritionTips = () => {
  const { switchRole } = useRole();
  const [activeCategory, setActiveCategory] = useState('all');
  const [favorited, setFavorited] = useState([]);
  const [selectedTip, setSelectedTip] = useState(null);
  const [showModal, setShowModal] = useState(false);

  // Switch to guest role when component mounts
  useEffect(() => {
    switchRole('guest');
  }, [switchRole]);

  const categories = [
    { id: 'all', name: 'All Tips', icon: BookOpen },
    { id: 'hydration', name: 'Hydration', icon: Droplets },
    { id: 'nutrition', name: 'Basic Nutrition', icon: Apple },
    { id: 'habits', name: 'Healthy Habits', icon: Heart },
    { id: 'timing', name: 'Meal Timing', icon: Clock },
    { id: 'gut-health', name: 'Gut Health', icon: Leaf },
    { id: 'brain-foods', name: 'Brain Foods', icon: Brain },
    { id: 'heart-health', name: 'Heart Health', icon: Activity },
    { id: 'meal-prep', name: 'Meal Prep', icon: Utensils },
    { id: 'metabolism', name: 'Metabolism', icon: Zap }
  ];

  const nutritionTips = [
    {
      id: 1,
      title: 'Stay Hydrated',
      category: 'hydration',
      description: 'Drinking water before meals can help with portion control and digestion. Aim for at least 8 glasses throughout the day.',
      priority: 'high',
      readTime: '2 min',
      tags: ['hydration', 'digestion', 'weight management'],
      detailedContent: {
        scientificBasis: 'Studies show that drinking 16 oz of water before meals can lead to 13% reduction in calorie intake and improved weight loss outcomes.',
        benefits: ['Improved digestion', 'Better portion control', 'Enhanced metabolism', 'Clearer skin', 'Reduced fatigue'],
        implementationSteps: [
          'Start your day with a glass of water upon waking',
          'Drink water 30 minutes before each meal',
          'Keep a water bottle with you throughout the day',
          'Set hourly reminders to drink water',
          'Add lemon or cucumber for flavor if needed'
        ],
        mealIdeas: ['Infused water with mint and lime', 'Herbal teas count towards daily intake', 'Water-rich foods like watermelon and cucumber'],
        tracking: 'Use a water tracking app or mark glasses on your phone to monitor daily intake'
      }
    },
    {
      id: 2,
      title: 'Fill Half Your Plate with Vegetables',
      category: 'nutrition',
      description: 'Choose colorful vegetables to maximize nutrient intake. Include protein in every meal to help maintain stable blood sugar levels.',
      priority: 'high',
      readTime: '3 min',
      tags: ['vegetables', 'portion control', 'nutrients'],
      detailedContent: {
        scientificBasis: 'Research indicates that filling half your plate with vegetables increases fiber intake by 40% and reduces calorie density of meals.',
        benefits: ['Higher nutrient density', 'Improved digestion', 'Better weight management', 'Reduced disease risk'],
        implementationSteps: [
          'Start each meal by adding vegetables first',
          'Choose 2-3 different colored vegetables per meal',
          'Prep vegetables in advance for easy access',
          'Try roasted, steamed, or fresh preparations',
          'Gradually increase portion sizes if new to this habit'
        ],
        mealIdeas: ['Rainbow salads with mixed greens', 'Roasted vegetable medleys', 'Vegetable stir-fries with protein'],
        tracking: 'Take photos of your plates to visually track vegetable portions over time'
      }
    },
    {
      id: 3,
      title: 'Choose Whole Grains Over Refined',
      category: 'nutrition',
      description: 'Whole grains provide more fiber, vitamins, and minerals compared to refined grains. Look for "100% whole grain" labels.',
      priority: 'medium',
      readTime: '2 min',
      tags: ['whole grains', 'fiber', 'nutrients'],
      detailedContent: {
        scientificBasis: 'Whole grains contain 25% more protein and up to 17 times more fiber than refined grains, supporting better blood sugar control.',
        benefits: ['Stable blood sugar', 'Improved heart health', 'Better digestive health', 'Sustained energy'],
        implementationSteps: [
          'Replace white rice with brown rice or quinoa',
          'Choose whole grain bread over white bread',
          'Try oatmeal instead of sugary cereals',
          'Experiment with ancient grains like farro and bulgur',
          'Read labels to ensure "whole grain" is the first ingredient'
        ],
        mealIdeas: ['Quinoa Buddha bowls', 'Overnight oats with berries', 'Brown rice stir-fries'],
        tracking: 'Aim for 3-5 servings of whole grains daily and track in a food diary'
      }
    },
    {
      id: 4,
      title: 'Include Protein in Every Meal',
      category: 'nutrition',
      description: 'Protein helps maintain stable blood sugar levels and keeps you feeling full longer. Good sources include lean meats, fish, beans, and nuts.',
      priority: 'high',
      readTime: '3 min',
      tags: ['protein', 'blood sugar', 'satiety'],
      detailedContent: {
        scientificBasis: 'Protein increases satiety hormones by up to 50% and can boost metabolism by 20-35% through the thermic effect of food.',
        benefits: ['Increased satiety', 'Better muscle maintenance', 'Stable blood sugar', 'Higher metabolism'],
        implementationSteps: [
          'Aim for 20-30g of protein per meal',
          'Include both animal and plant-based proteins',
          'Add protein powder to smoothies if needed',
          'Choose lean cuts of meat and fish',
          'Combine incomplete proteins (rice + beans) for complete amino acids'
        ],
        mealIdeas: ['Greek yogurt with nuts', 'Grilled salmon with quinoa', 'Lentil curry with vegetables'],
        tracking: 'Track daily protein intake and aim for 0.8-1g per kg of body weight'
      }
    },
    {
      id: 5,
      title: 'Eat Mindfully',
      category: 'habits',
      description: 'Take time to eat without distractions. Chew slowly and pay attention to hunger and fullness cues.',
      priority: 'medium',
      readTime: '4 min',
      tags: ['mindfulness', 'digestion', 'portion control'],
      detailedContent: {
        scientificBasis: 'Mindful eating can reduce calorie intake by up to 25% and improve digestion by activating the parasympathetic nervous system.',
        benefits: ['Better portion control', 'Improved digestion', 'Enhanced food enjoyment', 'Reduced stress eating'],
        implementationSteps: [
          'Put away phones and TV during meals',
          'Chew each bite 15-20 times',
          'Take breaks between bites',
          'Focus on taste, texture, and aroma',
          'Check hunger levels halfway through meals'
        ],
        mealIdeas: ['Small, colorful plates to encourage slower eating', 'Sit-down meals at a dedicated table', 'Practice gratitude before eating'],
        tracking: 'Rate hunger (1-10) before and after meals to develop awareness'
      }
    },
    {
      id: 6,
      title: 'Time Your Meals Strategically',
      category: 'timing',
      description: 'Try to eat regular meals and snacks. Avoid skipping meals as this can lead to overeating later.',
      priority: 'medium',
      readTime: '2 min',
      tags: ['meal timing', 'metabolism', 'hunger'],
      detailedContent: {
        scientificBasis: 'Eating at consistent times helps regulate circadian rhythms and can improve metabolism by up to 10%.',
        benefits: ['Stable blood sugar', 'Better sleep quality', 'Improved metabolism', 'Reduced cravings'],
        implementationSteps: [
          'Eat within 1 hour of waking up',
          'Space meals 3-4 hours apart',
          'Have your last meal 3 hours before bed',
          'Include healthy snacks if meals are >4 hours apart',
          'Stay consistent with timing even on weekends'
        ],
        mealIdeas: ['Balanced breakfast within 1 hour of waking', 'Light dinner 3 hours before bedtime', 'Protein-rich snacks between meals'],
        tracking: 'Log meal times for a week to identify and optimize your eating patterns'
      }
    },
    {
      id: 7,
      title: 'Choose Nutrient-Dense Snacks',
      category: 'habits',
      description: 'Choose nutrient-dense snacks like fruits, vegetables with hummus, or a handful of nuts instead of processed foods.',
      priority: 'medium',
      readTime: '3 min',
      tags: ['snacking', 'nutrients', 'energy'],
      detailedContent: {
        scientificBasis: 'Nutrient-dense snacks provide 50% more vitamins and minerals per calorie compared to processed snacks.',
        benefits: ['Sustained energy', 'Better nutrient intake', 'Reduced sugar cravings', 'Improved mood stability'],
        implementationSteps: [
          'Prep snacks in advance and portion them out',
          'Combine protein with fiber for satiety',
          'Choose whole foods over packaged options',
          'Keep healthy snacks visible and accessible',
          'Remove tempting processed snacks from easy reach'
        ],
        mealIdeas: ['Apple slices with almond butter', 'Greek yogurt with berries', 'Hummus with carrot sticks', 'Mixed nuts and seeds'],
        tracking: 'Plan and log your snacks to ensure they align with your nutrition goals'
      }
    },
    {
      id: 8,
      title: 'Eat a Rainbow of Colors',
      category: 'nutrition',
      description: 'Eat a rainbow of fruits and vegetables. Different colors provide different vitamins, minerals, and antioxidants.',
      priority: 'high',
      readTime: '2 min',
      tags: ['variety', 'antioxidants', 'vitamins'],
      detailedContent: {
        scientificBasis: 'Different colored produce contains unique phytonutrients - aiming for 5-7 colors daily can increase antioxidant intake by 200%.',
        benefits: ['Higher antioxidant intake', 'Better immune function', 'Reduced inflammation', 'Improved skin health'],
        implementationSteps: [
          'Aim for 5-7 different colors of produce daily',
          'Start with one new colorful food per week',
          'Make smoothies with mixed colorful fruits',
          'Try exotic fruits and vegetables for variety',
          'Focus on deeply colored options for maximum nutrients'
        ],
        mealIdeas: ['Rainbow smoothie bowls', 'Colorful vegetable stir-fries', 'Mixed berry salads'],
        tracking: 'Take daily photos of your meals and count the colors you consume'
      }
    },
    // NEW TIPS START HERE
    {
      id: 9,
      title: 'Support Your Gut Health',
      category: 'gut-health',
      description: 'Include fermented foods and prebiotics in your diet to support a healthy gut microbiome for better digestion and immunity.',
      priority: 'high',
      readTime: '4 min',
      tags: ['gut health', 'probiotics', 'immunity', 'digestion'],
      detailedContent: {
        scientificBasis: 'A healthy gut microbiome contains over 1000 different bacterial species and influences 70% of immune function and neurotransmitter production.',
        benefits: ['Better digestion', 'Stronger immunity', 'Improved mood', 'Better nutrient absorption', 'Reduced inflammation'],
        implementationSteps: [
          'Include 1-2 servings of fermented foods daily (yogurt, kefir, sauerkraut)',
          'Eat prebiotic foods like garlic, onions, and bananas',
          'Limit processed foods that harm gut bacteria',
          'Consider a daily probiotic supplement',
          'Eat a diverse variety of plant foods (aim for 30 different plants per week)'
        ],
        mealIdeas: ['Kefir smoothies with berries', 'Kimchi fried rice', 'Yogurt parfaits with fiber-rich fruits', 'Miso soup with vegetables'],
        tracking: 'Log digestive symptoms and energy levels to see how gut-supporting foods affect you'
      }
    },
    {
      id: 10,
      title: 'Boost Brain Function with Smart Foods',
      category: 'brain-foods',
      description: 'Incorporate omega-3 rich foods, antioxidant-rich berries, and brain-supporting nutrients to enhance cognitive function.',
      priority: 'high',
      readTime: '4 min',
      tags: ['brain health', 'omega-3', 'antioxidants', 'cognitive function'],
      detailedContent: {
        scientificBasis: 'Omega-3 fatty acids make up 30% of brain tissue, and studies show regular consumption can improve memory by up to 23%.',
        benefits: ['Enhanced memory', 'Better focus', 'Improved mood', 'Reduced brain fog', 'Protection against cognitive decline'],
        implementationSteps: [
          'Eat fatty fish (salmon, sardines, mackerel) 2-3 times per week',
          'Include blueberries or other dark berries daily',
          'Add walnuts and flaxseeds to meals',
          'Consume dark leafy greens rich in folate',
          'Include turmeric and dark chocolate for brain protection'
        ],
        mealIdeas: ['Salmon and avocado bowls', 'Blueberry walnut oatmeal', 'Dark chocolate and berry smoothies', 'Spinach and walnut salads'],
        tracking: 'Monitor your focus and mental clarity throughout the day after incorporating brain foods'
      }
    },
    {
      id: 11,
      title: 'Protect Your Heart with Smart Nutrition',
      category: 'heart-health',
      description: 'Focus on heart-healthy fats, fiber-rich foods, and potassium-rich vegetables to support cardiovascular health.',
      priority: 'high',
      readTime: '4 min',
      tags: ['heart health', 'healthy fats', 'fiber', 'cardiovascular'],
      detailedContent: {
        scientificBasis: 'A heart-healthy diet can reduce cardiovascular disease risk by up to 80% and lower bad cholesterol by 15-25%.',
        benefits: ['Lower cholesterol', 'Reduced blood pressure', 'Better circulation', 'Reduced inflammation', 'Lower heart disease risk'],
        implementationSteps: [
          'Replace saturated fats with unsaturated fats (olive oil, avocado)',
          'Eat 25-35g of fiber daily from whole foods',
          'Include potassium-rich foods like bananas and spinach',
          'Limit sodium to under 2300mg per day',
          'Choose lean proteins and reduce red meat consumption'
        ],
        mealIdeas: ['Mediterranean-style salads with olive oil', 'Oatmeal with berries and nuts', 'Grilled fish with roasted vegetables', 'Bean and vegetable soups'],
        tracking: 'Monitor blood pressure and cholesterol levels, track fiber and sodium intake'
      }
    },
    {
      id: 12,
      title: 'Master Meal Prep for Success',
      category: 'meal-prep',
      description: 'Plan and prepare meals in advance to ensure consistent healthy eating and save time during busy weekdays.',
      priority: 'medium',
      readTime: '5 min',
      tags: ['meal prep', 'planning', 'convenience', 'consistency'],
      detailedContent: {
        scientificBasis: 'People who meal prep consume 2.5 more servings of fruits and vegetables and have better diet quality overall.',
        benefits: ['Consistent healthy eating', 'Time savings', 'Cost effectiveness', 'Reduced food waste', 'Less stress around meals'],
        implementationSteps: [
          'Dedicate 2-3 hours on weekends for meal prep',
          'Prepare base ingredients (grains, proteins, chopped vegetables)',
          'Use versatile ingredients that work in multiple meals',
          'Invest in quality food storage containers',
          'Start small with prepping just lunches or snacks'
        ],
        mealIdeas: ['Mason jar salads', 'Freezer smoothie packs', 'Batch-cooked grains and proteins', 'Pre-portioned snack containers'],
        tracking: 'Plan weekly menus and track which prep strategies work best for your schedule'
      }
    },
    {
      id: 13,
      title: 'Optimize Your Metabolism',
      category: 'metabolism',
      description: 'Support your metabolic health through strategic eating patterns, thermogenic foods, and proper hydration.',
      priority: 'medium',
      readTime: '4 min',
      tags: ['metabolism', 'thermogenesis', 'energy', 'weight management'],
      detailedContent: {
        scientificBasis: 'Protein has a thermic effect of 20-35%, meaning you burn more calories digesting it compared to carbs (5-10%) or fats (0-5%).',
        benefits: ['Increased calorie burn', 'Better energy levels', 'Improved weight management', 'Enhanced athletic performance'],
        implementationSteps: [
          'Eat protein at every meal to boost thermic effect',
          'Include metabolism-boosting foods like green tea and chili peppers',
          'Stay hydrated as dehydration can slow metabolism by 3%',
          'Don\'t skip meals as this can slow metabolic rate',
          'Include strength training to build metabolically active muscle'
        ],
        mealIdeas: ['Green tea with meals', 'Spicy protein stir-fries', 'Cold water with lemon', 'High-protein breakfast options'],
        tracking: 'Monitor energy levels and body composition changes rather than just weight'
      }
    },
    {
      id: 14,
      title: 'Embrace Anti-Inflammatory Foods',
      category: 'gut-health',
      description: 'Choose foods rich in omega-3s, antioxidants, and polyphenols to reduce chronic inflammation in your body.',
      priority: 'high',
      readTime: '4 min',
      tags: ['anti-inflammatory', 'omega-3', 'polyphenols', 'chronic disease prevention'],
      detailedContent: {
        scientificBasis: 'Chronic inflammation is linked to heart disease, diabetes, and cancer. Anti-inflammatory diets can reduce inflammatory markers by 25-40%.',
        benefits: ['Reduced chronic disease risk', 'Better joint health', 'Improved skin health', 'Enhanced recovery', 'Better mood stability'],
        implementationSteps: [
          'Include fatty fish, walnuts, and flaxseeds for omega-3s',
          'Eat colorful berries rich in anthocyanins',
          'Use turmeric and ginger in cooking',
          'Choose green tea over sugary beverages',
          'Limit processed foods, sugar, and trans fats'
        ],
        mealIdeas: ['Turmeric golden milk lattes', 'Berry and walnut salads', 'Ginger-infused vegetable soups', 'Green tea smoothies'],
        tracking: 'Note improvements in joint pain, skin quality, and overall well-being'
      }
    },
    {
      id: 15,
      title: 'Balance Blood Sugar Naturally',
      category: 'metabolism',
      description: 'Maintain stable blood sugar levels through strategic food combinations and timing to improve energy and health.',
      priority: 'high',
      readTime: '4 min',
      tags: ['blood sugar', 'glycemic control', 'energy stability', 'diabetes prevention'],
      detailedContent: {
        scientificBasis: 'Blood sugar spikes and crashes affect energy, mood, and long-term health. Stable blood sugar can improve energy consistency by 60%.',
        benefits: ['Stable energy levels', 'Better mood', 'Reduced cravings', 'Improved focus', 'Lower diabetes risk'],
        implementationSteps: [
          'Pair carbohydrates with protein and healthy fats',
          'Choose low glycemic index foods',
          'Eat smaller, more frequent meals',
          'Include fiber-rich foods to slow sugar absorption',
          'Avoid eating carbs alone, especially refined sugars'
        ],
        mealIdeas: ['Apple with almond butter', 'Quinoa bowls with protein and vegetables', 'Greek yogurt with berries and nuts'],
        tracking: 'Monitor energy levels 1-2 hours after meals and adjust food combinations accordingly'
      }
    },
    {
      id: 16,
      title: 'Seasonal Eating for Optimal Nutrition',
      category: 'habits',
      description: 'Align your diet with seasonal produce to maximize nutrient density, flavor, and environmental sustainability.',
      priority: 'medium',
      readTime: '3 min',
      tags: ['seasonal eating', 'sustainability', 'nutrient density', 'local produce'],
      detailedContent: {
        scientificBasis: 'Seasonal produce can contain up to 50% more nutrients when consumed at peak ripeness compared to out-of-season alternatives.',
        benefits: ['Higher nutrient content', 'Better flavor', 'Cost savings', 'Environmental benefits', 'Connection to natural cycles'],
        implementationSteps: [
          'Visit local farmers markets to see what\'s in season',
          'Learn the seasonal calendar for your region',
          'Try one new seasonal fruit or vegetable each month',
          'Preserve seasonal foods through freezing or fermentation',
          'Plan meals around seasonal availability'
        ],
        mealIdeas: ['Spring: asparagus and pea salads', 'Summer: tomato and basil dishes', 'Fall: squash and apple recipes', 'Winter: root vegetable stews'],
        tracking: 'Keep a seasonal eating journal noting new foods tried and seasonal recipes discovered'
      }
    },
    {
      id: 17,
      title: 'Optimize Nutrient Timing',
      category: 'timing',
      description: 'Time your nutrient intake around activity and sleep patterns to maximize absorption and energy utilization.',
      priority: 'medium',
      readTime: '4 min',
      tags: ['nutrient timing', 'performance', 'recovery', 'circadian rhythm'],
      detailedContent: {
        scientificBasis: 'Nutrient timing can improve athletic performance by 15-25% and enhance recovery when aligned with circadian rhythms.',
        benefits: ['Better athletic performance', 'Enhanced recovery', 'Improved sleep quality', 'Optimized nutrient absorption'],
        implementationSteps: [
          'Eat complex carbs earlier in the day for sustained energy',
          'Include protein within 2 hours post-workout for recovery',
          'Have your largest meal when most active (usually midday)',
          'Limit caffeine 6 hours before bedtime',
          'Include tryptophan-rich foods in evening meals for better sleep'
        ],
        mealIdeas: ['Pre-workout: banana with nut butter', 'Post-workout: protein smoothie', 'Evening: turkey with sweet potato'],
        tracking: 'Log workout performance and recovery quality when experimenting with nutrient timing'
      }
    },
    {
      id: 18,
      title: 'Hydrate Beyond Water',
      category: 'hydration',
      description: 'Maximize hydration through water-rich foods, electrolyte balance, and strategic timing for optimal cellular function.',
      priority: 'medium',
      readTime: '3 min',
      tags: ['hydration', 'electrolytes', 'cellular function', 'performance'],
      detailedContent: {
        scientificBasis: 'Cellular hydration depends on electrolyte balance - proper hydration can improve cognitive function by 23% and physical performance by 15%.',
        benefits: ['Better cognitive function', 'Improved physical performance', 'Enhanced skin health', 'Better temperature regulation'],
        implementationSteps: [
          'Include water-rich foods like cucumber, watermelon, and soup',
          'Add a pinch of natural salt to water for electrolyte balance',
          'Drink water consistently throughout the day, not just when thirsty',
          'Increase intake during hot weather or exercise',
          'Monitor urine color as a hydration indicator'
        ],
        mealIdeas: ['Cucumber and mint infused water', 'Coconut water after workouts', 'Watermelon and feta salads', 'Bone broth for electrolytes'],
        tracking: 'Monitor urine color, energy levels, and skin elasticity as hydration indicators'
      }
    },
    {
      id: 19,
      title: 'Build Healthy Food Relationships',
      category: 'habits',
      description: 'Develop a positive relationship with food by practicing intuitive eating and removing guilt around food choices.',
      priority: 'high',
      readTime: '5 min',
      tags: ['food relationship', 'intuitive eating', 'mental health', 'sustainability'],
      detailedContent: {
        scientificBasis: 'Restrictive dieting can increase stress hormones by 50% and often leads to rebound weight gain in 95% of cases.',
        benefits: ['Reduced food anxiety', 'Better long-term adherence', 'Improved mental health', 'Sustainable habits', 'Enhanced food enjoyment'],
        implementationSteps: [
          'Practice eating without judgment or guilt',
          'Listen to hunger and fullness cues',
          'Allow yourself all foods in moderation',
          'Focus on how foods make you feel rather than arbitrary rules',
          'Seek support if you struggle with disordered eating patterns'
        ],
        mealIdeas: ['Mindful tasting sessions', 'Intuitive meal planning based on cravings and needs', 'Social eating experiences without restrictions'],
        tracking: 'Journal about your relationship with food and notice patterns in emotional eating'
      }
    },
    {
      id: 20,
      title: 'Maximize Nutrient Absorption',
      category: 'nutrition',
      description: 'Enhance your body\'s ability to absorb nutrients through proper food combinations and preparation methods.',
      priority: 'medium',
      readTime: '4 min',
      tags: ['nutrient absorption', 'bioavailability', 'food combining', 'preparation'],
      detailedContent: {
        scientificBasis: 'Proper food combining can increase nutrient absorption by up to 300% - for example, vitamin C increases iron absorption by 5-fold.',
        benefits: ['Better nutrient utilization', 'Improved energy', 'Enhanced immunity', 'Better value from healthy foods'],
        implementationSteps: [
          'Combine vitamin C foods with iron-rich foods (bell peppers with spinach)',
          'Eat healthy fats with fat-soluble vitamins A, D, E, K',
          'Soak nuts and seeds to improve mineral absorption',
          'Ferment or sprout grains and legumes to reduce antinutrients',
          'Cook tomatoes to increase lycopene availability'
        ],
        mealIdeas: ['Spinach salad with strawberries and iron-rich ingredients', 'Avocado with sweet potato for beta-carotene absorption'],
        tracking: 'Notice improvements in energy and health markers when optimizing nutrient combinations'
      }
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

  const handleLearnMore = (tip) => {
    setSelectedTip(tip);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedTip(null);
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