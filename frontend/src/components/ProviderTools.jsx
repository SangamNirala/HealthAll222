import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Stethoscope, Calculator, FileText, Clipboard, Heart, Activity, Scale, Thermometer } from 'lucide-react';

const ProviderTools = () => {
  const { switchRole } = useRole();
  const [activeCategory, setActiveCategory] = useState('all');

  useEffect(() => {
    switchRole('provider');
  }, [switchRole]);

  const toolCategories = [
    { id: 'all', name: 'All Tools', icon: Stethoscope },
    { id: 'assessment', name: 'Assessment', icon: Clipboard },
    { id: 'calculators', name: 'Calculators', icon: Calculator },
    { id: 'monitoring', name: 'Monitoring', icon: Activity },
    { id: 'documentation', name: 'Documentation', icon: FileText }
  ];

  const clinicalTools = [
    {
      id: 1,
      title: 'BMI Calculator',
      category: 'calculators',
      description: 'Calculate Body Mass Index and assess weight status',
      icon: Scale,
      color: 'blue',
      status: 'available'
    },
    {
      id: 2,
      title: 'Blood Pressure Assessment',
      category: 'assessment', 
      description: 'Evaluate BP readings and risk stratification',
      icon: Heart,
      color: 'red',
      status: 'available'
    },
    {
      id: 3,
      title: 'Diabetes Risk Calculator',
      category: 'calculators',
      description: 'Assess diabetes risk using validated scoring systems',
      icon: Activity,
      color: 'purple',
      status: 'available'
    },
    {
      id: 4,
      title: 'Vital Signs Monitor',
      category: 'monitoring',
      description: 'Track and analyze patient vital signs trends',
      icon: Thermometer,
      color: 'green',
      status: 'available'
    },
    {
      id: 5,
      title: 'Clinical Notes Template',
      category: 'documentation',
      description: 'Structured templates for clinical documentation',
      icon: FileText,
      color: 'orange',
      status: 'available'
    },
    {
      id: 6,
      title: 'Medication Review',
      category: 'assessment',
      description: 'Comprehensive medication assessment tool',
      icon: Clipboard,
      color: 'indigo',
      status: 'coming_soon'
    }
  ];

  const filteredTools = activeCategory === 'all' 
    ? clinicalTools 
    : clinicalTools.filter(tool => tool.category === activeCategory);

  const getColorClasses = (color) => {
    const colors = {
      blue: 'border-blue-200 bg-blue-50 text-blue-600',
      red: 'border-red-200 bg-red-50 text-red-600',
      purple: 'border-purple-200 bg-purple-50 text-purple-600',
      green: 'border-green-200 bg-green-50 text-green-600',
      orange: 'border-orange-200 bg-orange-50 text-orange-600',
      indigo: 'border-indigo-200 bg-indigo-50 text-indigo-600'
    };
    return colors[color] || colors.blue;
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'available': return 'bg-green-100 text-green-800';
      case 'coming_soon': return 'bg-yellow-100 text-yellow-800';
      case 'maintenance': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Clinical Tools</h1>
          <p className="text-gray-600">Access professional healthcare assessment and calculation tools</p>
        </div>

        {/* Tool Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="border-2 border-emerald-200 bg-emerald-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Stethoscope className="w-8 h-8 text-emerald-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-emerald-600">{clinicalTools.length}</div>
                  <p className="text-sm text-gray-600">Available Tools</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-blue-200 bg-blue-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Calculator className="w-8 h-8 text-blue-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-blue-600">
                    {clinicalTools.filter(t => t.category === 'calculators').length}
                  </div>
                  <p className="text-sm text-gray-600">Calculators</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-purple-200 bg-purple-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Clipboard className="w-8 h-8 text-purple-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-purple-600">
                    {clinicalTools.filter(t => t.category === 'assessment').length}
                  </div>
                  <p className="text-sm text-gray-600">Assessments</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card className="border-2 border-green-200 bg-green-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Activity className="w-8 h-8 text-green-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-green-600">
                    {clinicalTools.filter(t => t.category === 'monitoring').length}
                  </div>
                  <p className="text-sm text-gray-600">Monitoring</p>
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
                <CardTitle className="text-lg">Tool Categories</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {toolCategories.map((category) => {
                    const IconComponent = category.icon;
                    const isActive = activeCategory === category.id;
                    return (
                      <Button
                        key={category.id}
                        variant={isActive ? "default" : "ghost"}
                        onClick={() => setActiveCategory(category.id)}
                        className={`w-full justify-start ${
                          isActive 
                            ? 'bg-emerald-600 hover:bg-emerald-700 text-white' 
                            : 'hover:bg-emerald-50'
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

            {/* Quick Access */}
            <Card className="mt-6">
              <CardHeader>
                <CardTitle className="text-lg">Quick Access</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Button variant="outline" className="w-full justify-start" size="sm">
                    <Calculator className="w-4 h-4 mr-2" />
                    BMI Calculator
                  </Button>
                  <Button variant="outline" className="w-full justify-start" size="sm">
                    <Heart className="w-4 h-4 mr-2" />
                    BP Assessment
                  </Button>
                  <Button variant="outline" className="w-full justify-start" size="sm">
                    <FileText className="w-4 h-4 mr-2" />
                    Clinical Notes
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Tools Grid */}
          <div className="lg:col-span-3">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {filteredTools.map((tool) => {
                const IconComponent = tool.icon;
                return (
                  <Card 
                    key={tool.id} 
                    className={`border-2 hover:shadow-lg transition-all duration-200 cursor-pointer ${getColorClasses(tool.color)}`}
                  >
                    <CardHeader className="pb-3">
                      <div className="flex items-start justify-between">
                        <div className="flex items-center space-x-3">
                          <div className={`p-2 rounded-lg ${getColorClasses(tool.color)}`}>
                            <IconComponent className="w-6 h-6" />
                          </div>
                          <div>
                            <CardTitle className="text-lg leading-tight text-gray-900">
                              {tool.title}
                            </CardTitle>
                            <Badge className={`${getStatusColor(tool.status)} mt-1`}>
                              {tool.status === 'coming_soon' ? 'Coming Soon' : 'Available'}
                            </Badge>
                          </div>
                        </div>
                      </div>
                    </CardHeader>
                    
                    <CardContent>
                      <p className="text-gray-600 mb-4 text-sm leading-relaxed">
                        {tool.description}
                      </p>
                      
                      <Button 
                        className={`w-full ${tool.status === 'available' 
                          ? 'bg-emerald-600 hover:bg-emerald-700' 
                          : 'bg-gray-400 cursor-not-allowed'
                        }`}
                        disabled={tool.status !== 'available'}
                      >
                        {tool.status === 'available' ? 'Launch Tool' : 'Coming Soon'}
                      </Button>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
            
            {filteredTools.length === 0 && (
              <div className="text-center py-12">
                <Stethoscope className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <div className="text-gray-500 mb-2">No tools found in this category</div>
                <p className="text-sm text-gray-400">Try selecting a different category</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProviderTools;