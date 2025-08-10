import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { Stethoscope, Calculator, FileText, Clipboard, Heart, Activity, Scale, Thermometer, Brain, Search, Lightbulb } from 'lucide-react';

const ProviderTools = () => {
  const { switchRole } = useRole();
  const [activeCategory, setActiveCategory] = useState('all');
  const [showDecisionSupport, setShowDecisionSupport] = useState(false);
  const [decisionSupportData, setDecisionSupportData] = useState(null);
  const [patientSymptoms, setPatientSymptoms] = useState('');
  const [patientHistory, setPatientHistory] = useState('');

  useEffect(() => {
    switchRole('provider');
  }, [switchRole]);

  const toolCategories = [
    { id: 'all', name: 'All Tools', icon: Stethoscope },
    { id: 'ai_support', name: 'AI Support', icon: Brain },
    { id: 'assessment', name: 'Assessment', icon: Clipboard },
    { id: 'calculators', name: 'Calculators', icon: Calculator },
    { id: 'monitoring', name: 'Monitoring', icon: Activity },
    { id: 'documentation', name: 'Documentation', icon: FileText }
  ];

  const clinicalTools = [
    // AI-Powered Tools
    {
      id: 1,
      title: 'Clinical Decision Support',
      category: 'ai_support',
      description: 'AI-powered diagnostic assistance and treatment recommendations',
      icon: Brain,
      color: 'purple',
      status: 'available',
      isAI: true
    },
    {
      id: 2,
      title: 'Evidence-Based Recommendations',
      category: 'ai_support',
      description: 'Get AI-powered, evidence-based treatment recommendations',
      icon: Lightbulb,
      color: 'indigo',
      status: 'available',
      isAI: true
    },
    // Existing Tools
    {
      id: 3,
      title: 'BMI Calculator',
      category: 'calculators',
      description: 'Calculate Body Mass Index and assess weight status',
      icon: Scale,
      color: 'blue',
      status: 'available'
    },
    {
      id: 4,
      title: 'Blood Pressure Assessment',
      category: 'assessment', 
      description: 'Evaluate BP readings and risk stratification',
      icon: Heart,
      color: 'red',
      status: 'available'
    },
    {
      id: 5,
      title: 'Diabetes Risk Calculator',
      category: 'calculators',
      description: 'Assess diabetes risk using validated scoring systems',
      icon: Activity,
      color: 'purple',
      status: 'available'
    },
    {
      id: 6,
      title: 'Vital Signs Monitor',
      category: 'monitoring',
      description: 'Track and analyze patient vital signs trends',
      icon: Thermometer,
      color: 'green',
      status: 'available'
    },
    {
      id: 7,
      title: 'Clinical Notes Template',
      category: 'documentation',
      description: 'Structured templates for clinical documentation',
      icon: FileText,
      color: 'orange',
      status: 'available'
    },
    {
      id: 8,
      title: 'Medication Review',
      category: 'assessment',
      description: 'Comprehensive medication assessment tool',
      icon: Clipboard,
      color: 'indigo',
      status: 'available'
    }
  ];

  const handleDecisionSupport = async () => {
    const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;
    
    try {
      const response = await fetch(`${backendUrl}/api/provider/clinical-decision-support`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          patient_data: { id: 'demo-patient' },
          symptoms: patientSymptoms.split(',').map(s => s.trim()),
          history: patientHistory.split(',').map(h => h.trim())
        })
      });
      
      const data = await response.json();
      setDecisionSupportData(data);
    } catch (error) {
      console.error('Error getting clinical decision support:', error);
    }
  };

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

  const handleToolLaunch = (tool) => {
    if (tool.title === 'Clinical Decision Support') {
      setShowDecisionSupport(true);
    } else if (tool.title === 'Evidence-Based Recommendations') {
      // Would show evidence recommendations modal
      console.log('Launching Evidence-Based Recommendations');
    } else {
      // Launch other tools
      console.log(`Launching ${tool.title}`);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Clinical Tools</h1>
          <p className="text-gray-600">Access professional healthcare assessment and AI-powered clinical tools</p>
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
          
          <Card className="border-2 border-purple-200 bg-purple-50">
            <CardContent className="pt-6">
              <div className="flex items-center">
                <Brain className="w-8 h-8 text-purple-600 mr-3" />
                <div>
                  <div className="text-2xl font-bold text-purple-600">
                    {clinicalTools.filter(t => t.isAI).length}
                  </div>
                  <p className="text-sm text-gray-600">AI Tools</p>
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

        {!showDecisionSupport ? (
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
                  <CardTitle className="text-lg">AI Quick Access</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <Button 
                      variant="outline" 
                      className="w-full justify-start border-purple-200 hover:bg-purple-50" 
                      size="sm"
                      onClick={() => setShowDecisionSupport(true)}
                    >
                      <Brain className="w-4 h-4 mr-2 text-purple-600" />
                      Decision Support
                    </Button>
                    <Button variant="outline" className="w-full justify-start border-indigo-200 hover:bg-indigo-50" size="sm">
                      <Lightbulb className="w-4 h-4 mr-2 text-indigo-600" />
                      Evidence Recommendations
                    </Button>
                    <Button variant="outline" className="w-full justify-start" size="sm">
                      <Calculator className="w-4 h-4 mr-2" />
                      Risk Calculators
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
                              <div className="flex space-x-2 mt-1">
                                <Badge className={`${getStatusColor(tool.status)}`}>
                                  {tool.status === 'coming_soon' ? 'Coming Soon' : 'Available'}
                                </Badge>
                                {tool.isAI && (
                                  <Badge className="bg-purple-100 text-purple-800">
                                    AI-Powered
                                  </Badge>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                      </CardHeader>
                      
                      <CardContent>
                        <p className="text-gray-600 mb-4 text-sm leading-relaxed">
                          {tool.description}
                        </p>
                        
                        <Button 
                          onClick={() => handleToolLaunch(tool)}
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
        ) : (
          /* Clinical Decision Support Modal */
          <div className="max-w-4xl mx-auto">
            <Card>
              <CardHeader>
                <div className="flex justify-between items-center">
                  <CardTitle className="flex items-center">
                    <Brain className="w-6 h-6 mr-2 text-purple-600" />
                    AI-Powered Clinical Decision Support
                  </CardTitle>
                  <Button variant="outline" onClick={() => setShowDecisionSupport(false)}>
                    Back to Tools
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Input Section */}
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Patient Symptoms (comma-separated)
                      </label>
                      <textarea
                        value={patientSymptoms}
                        onChange={(e) => setPatientSymptoms(e.target.value)}
                        placeholder="e.g., polyuria, polydipsia, weight loss"
                        className="w-full p-3 border border-gray-300 rounded-md resize-none"
                        rows={3}
                      />
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Medical History (comma-separated)
                      </label>
                      <textarea
                        value={patientHistory}
                        onChange={(e) => setPatientHistory(e.target.value)}
                        placeholder="e.g., family history of diabetes, obesity"
                        className="w-full p-3 border border-gray-300 rounded-md resize-none"
                        rows={3}
                      />
                    </div>
                    
                    <Button 
                      onClick={handleDecisionSupport}
                      className="w-full bg-purple-600 hover:bg-purple-700"
                      disabled={!patientSymptoms}
                    >
                      <Search className="w-4 h-4 mr-2" />
                      Analyze & Get Recommendations
                    </Button>
                  </div>
                  
                  {/* Results Section */}
                  <div>
                    {decisionSupportData ? (
                      <div className="space-y-4">
                        <h4 className="font-semibold text-lg text-gray-900">AI Recommendations</h4>
                        
                        {decisionSupportData.ai_recommendations.map((rec, index) => (
                          <Card key={index} className="border-l-4 border-purple-500">
                            <CardContent className="pt-4">
                              <div className="flex justify-between items-start mb-2">
                                <h5 className="font-medium text-purple-900 capitalize">
                                  {rec.category.replace('_', ' ')}
                                </h5>
                                <Badge className="bg-purple-100 text-purple-800">
                                  {Math.round(rec.confidence * 100)}% confidence
                                </Badge>
                              </div>
                              <p className="text-gray-700 mb-2">{rec.recommendation}</p>
                              <p className="text-sm text-gray-600 mb-3">{rec.evidence}</p>
                              
                              <div>
                                <h6 className="text-sm font-medium text-gray-700 mb-1">Next Steps:</h6>
                                <ul className="text-sm text-gray-600 list-disc list-inside space-y-1">
                                  {rec.next_steps.map((step, i) => (
                                    <li key={i}>{step}</li>
                                  ))}
                                </ul>
                              </div>
                            </CardContent>
                          </Card>
                        ))}
                        
                        {/* Risk Scores */}
                        <Card className="border-l-4 border-orange-500">
                          <CardContent className="pt-4">
                            <h5 className="font-medium text-orange-900 mb-3">Risk Assessment</h5>
                            <div className="grid grid-cols-1 gap-2">
                              {Object.entries(decisionSupportData.risk_scores).map(([key, value]) => (
                                <div key={key} className="flex justify-between items-center">
                                  <span className="text-sm capitalize">{key.replace('_', ' ')}</span>
                                  <div className="flex items-center space-x-2">
                                    <div className="w-20 bg-gray-200 rounded-full h-2">
                                      <div 
                                        className="bg-orange-500 h-2 rounded-full"
                                        style={{ width: `${value * 100}%` }}
                                      />
                                    </div>
                                    <span className="text-sm font-medium">{Math.round(value * 100)}%</span>
                                  </div>
                                </div>
                              ))}
                            </div>
                          </CardContent>
                        </Card>
                        
                        {/* Clinical Guidelines */}
                        <Card className="border-l-4 border-blue-500">
                          <CardContent className="pt-4">
                            <h5 className="font-medium text-blue-900 mb-3">Relevant Guidelines</h5>
                            {decisionSupportData.clinical_guidelines.map((guideline, index) => (
                              <div key={index} className="mb-2">
                                <div className="font-medium text-sm text-blue-800">{guideline.guideline}</div>
                                <div className="text-sm text-gray-600">{guideline.recommendation}</div>
                              </div>
                            ))}
                          </CardContent>
                        </Card>
                      </div>
                    ) : (
                      <div className="text-center py-8">
                        <Brain className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                        <div className="text-gray-500 mb-2">Enter patient symptoms to get AI recommendations</div>
                        <p className="text-sm text-gray-400">Our AI will analyze the information and provide evidence-based suggestions</p>
                      </div>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProviderTools;