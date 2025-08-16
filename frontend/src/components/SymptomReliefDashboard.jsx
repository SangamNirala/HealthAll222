import React, { useState, useEffect } from 'react';
import { 
  Zap, 
  Clock, 
  TrendingUp, 
  Heart, 
  Lightbulb,
  AlertCircle,
  CheckCircle,
  ArrowRight,
  Star,
  Info,
  ThumbsUp,
  Activity
} from 'lucide-react';

const SymptomReliefDashboard = ({ assessment, userId }) => {
  const [selectedTab, setSelectedTab] = useState('instant');
  const [expandedRecommendation, setExpandedRecommendation] = useState(null);

  const tabs = [
    { id: 'instant', label: 'Instant Relief', icon: Zap, color: 'text-orange-500' },
    { id: 'ai', label: 'AI Recommendations', icon: TrendingUp, color: 'text-blue-500' },
    { id: 'timing', label: 'Timing Protocols', icon: Clock, color: 'text-green-500' }
  ];

  const renderInstantRelief = () => {
    const instantRelief = assessment?.instant_relief || [];
    
    return (
      <div className="space-y-4">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
            <Zap className="w-5 h-5 text-orange-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Instant Relief Actions</h3>
            <p className="text-sm text-gray-600">Try these right now for immediate symptom relief</p>
          </div>
        </div>

        {instantRelief.length > 0 ? (
          <div className="grid gap-4">
            {instantRelief.map((relief, index) => (
              <div key={index} className="bg-gradient-to-r from-orange-50 to-red-50 border border-orange-200 rounded-xl p-4">
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 bg-orange-500 text-white rounded-full flex items-center justify-center font-semibold text-sm">
                    {index + 1}
                  </div>
                  <div className="flex-1">
                    <div className="font-medium text-gray-900 mb-2">
                      {relief.action || relief}
                    </div>
                    {relief.target_symptom && relief.target_symptom !== 'general_relief' && (
                      <div className="text-sm text-gray-600 mb-1">
                        <span className="font-medium">Target:</span> {relief.target_symptom}
                      </div>
                    )}
                    <div className="flex items-center space-x-4 text-xs text-gray-500">
                      {relief.time_to_effect && (
                        <span className="flex items-center">
                          <Clock className="w-3 h-3 mr-1" />
                          {relief.time_to_effect}
                        </span>
                      )}
                      {relief.evidence_level && (
                        <span className="flex items-center">
                          <Star className="w-3 h-3 mr-1" />
                          {relief.evidence_level} evidence
                        </span>
                      )}
                    </div>
                  </div>
                  <button className="w-6 h-6 border border-orange-300 rounded-full flex items-center justify-center hover:bg-orange-100 transition-colors">
                    <CheckCircle className="w-4 h-4 text-orange-600" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            <Lightbulb className="w-12 h-12 mx-auto mb-3 text-gray-400" />
            <p>No specific instant relief recommendations available.</p>
          </div>
        )}

        {/* Quick Tips */}
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 mt-6">
          <div className="flex items-center space-x-2 mb-3">
            <Info className="w-5 h-5 text-blue-600" />
            <h4 className="font-semibold text-blue-900">Quick Tips</h4>
          </div>
          <div className="space-y-2 text-sm text-blue-800">
            <p>• Track which remedies work best for you</p>
            <p>• Stay hydrated throughout the day</p>
            <p>• Note any triggers that might worsen symptoms</p>
            <p>• If symptoms worsen, consider medical consultation</p>
          </div>
        </div>
      </div>
    );
  };

  const renderAIRecommendations = () => {
    const aiRecs = assessment?.ai_recommendations || {};
    
    return (
      <div className="space-y-6">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
            <TrendingUp className="w-5 h-5 text-blue-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">AI-Powered Recommendations</h3>
            <p className="text-sm text-gray-600">Personalized advice based on your symptom profile</p>
          </div>
        </div>

        {/* Dietary Interventions */}
        {aiRecs.dietary_interventions && aiRecs.dietary_interventions.length > 0 && (
          <div className="bg-white border border-gray-200 rounded-xl p-5">
            <h4 className="font-semibold text-gray-900 mb-4 flex items-center">
              <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              Dietary Interventions
            </h4>
            <div className="space-y-3">
              {aiRecs.dietary_interventions.map((intervention, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 bg-green-50 rounded-lg">
                  <CheckCircle className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                  <span className="text-sm text-gray-800">{intervention}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Lifestyle Modifications */}
        {aiRecs.lifestyle_modifications && aiRecs.lifestyle_modifications.length > 0 && (
          <div className="bg-white border border-gray-200 rounded-xl p-5">
            <h4 className="font-semibold text-gray-900 mb-4 flex items-center">
              <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
              Lifestyle Modifications
            </h4>
            <div className="space-y-3">
              {aiRecs.lifestyle_modifications.map((modification, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                  <Activity className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                  <span className="text-sm text-gray-800">{modification}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Natural Remedies */}
        {aiRecs.natural_remedies && aiRecs.natural_remedies.length > 0 && (
          <div className="bg-white border border-gray-200 rounded-xl p-5">
            <h4 className="font-semibold text-gray-900 mb-4 flex items-center">
              <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
              Natural Remedies
            </h4>
            <div className="space-y-3">
              {aiRecs.natural_remedies.map((remedy, index) => (
                <div key={index} className="flex items-start space-x-3 p-3 bg-purple-50 rounded-lg">
                  <Heart className="w-5 h-5 text-purple-600 mt-0.5 flex-shrink-0" />
                  <span className="text-sm text-gray-800">{remedy}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* When to Seek Help */}
        {aiRecs.when_to_seek_help && aiRecs.when_to_seek_help.length > 0 && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-5">
            <h4 className="font-semibold text-yellow-900 mb-4 flex items-center">
              <AlertCircle className="w-5 h-5 text-yellow-600 mr-2" />
              When to Seek Medical Help
            </h4>
            <div className="space-y-2">
              {aiRecs.when_to_seek_help.map((guideline, index) => (
                <div key={index} className="flex items-start space-x-2 text-sm text-yellow-800">
                  <span className="text-yellow-600 mt-1">•</span>
                  <span>{guideline}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* AI Confidence & Disclaimer */}
        <div className="bg-gray-50 border border-gray-200 rounded-xl p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">AI Confidence Score</span>
            <span className="text-sm font-semibold text-blue-600">
              {Math.round((assessment?.confidence_score || 0.8) * 100)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2 mb-3">
            <div 
              className="bg-blue-600 h-2 rounded-full" 
              style={{ width: `${(assessment?.confidence_score || 0.8) * 100}%` }}
            ></div>
          </div>
          {aiRecs.disclaimer && (
            <p className="text-xs text-gray-600">{aiRecs.disclaimer}</p>
          )}
        </div>
      </div>
    );
  };

  const renderTimingProtocols = () => {
    const timingProtocols = assessment?.relief_recommendations?.timing_protocols || {};
    
    const timeSlots = [
      { id: 'morning', label: 'Morning Protocol', icon: '🌅', time: '6:00-10:00 AM' },
      { id: 'afternoon', label: 'Afternoon Check-in', icon: '☀️', time: '12:00-4:00 PM' },
      { id: 'evening', label: 'Evening Routine', icon: '🌙', time: '6:00-10:00 PM' }
    ];

    return (
      <div className="space-y-6">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
            <Clock className="w-5 h-5 text-green-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Timing-Specific Protocols</h3>
            <p className="text-sm text-gray-600">Optimized interventions for different times of day</p>
          </div>
        </div>

        <div className="space-y-4">
          {timeSlots.map((slot) => {
            const protocols = timingProtocols[slot.id] || [];
            
            return (
              <div key={slot.id} className="bg-white border border-gray-200 rounded-xl p-5">
                <div className="flex items-center space-x-3 mb-4">
                  <span className="text-2xl">{slot.icon}</span>
                  <div>
                    <h4 className="font-semibold text-gray-900">{slot.label}</h4>
                    <p className="text-sm text-gray-500">{slot.time}</p>
                  </div>
                </div>
                
                {protocols.length > 0 ? (
                  <div className="space-y-2">
                    {protocols.map((protocol, index) => (
                      <div key={index} className="flex items-center space-x-3 p-2 bg-gray-50 rounded-lg">
                        <div className="w-6 h-6 bg-green-500 text-white rounded-full flex items-center justify-center text-xs font-semibold">
                          {index + 1}
                        </div>
                        <span className="text-sm text-gray-800">{protocol}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-sm text-gray-500 italic py-2">
                    Continue with general recommendations during this time
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Daily Schedule Overview */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-xl p-5">
          <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
            <ArrowRight className="w-5 h-5 text-blue-600 mr-2" />
            Daily Schedule Tips
          </h4>
          <div className="space-y-2 text-sm text-gray-700">
            <p>• Start each day with hydration and gentle movement</p>
            <p>• Monitor symptom intensity at consistent times</p>
            <p>• Track which time-specific interventions work best</p>
            <p>• Maintain consistent sleep and meal timing</p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="bg-white border border-gray-200 rounded-xl shadow-sm">
      {/* Header with Tabs */}
      <div className="border-b border-gray-200">
        <div className="flex space-x-1 p-1">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setSelectedTab(tab.id)}
              className={`flex-1 flex items-center justify-center space-x-2 px-4 py-3 rounded-lg transition-all duration-200 ${
                selectedTab === tab.id
                  ? 'bg-blue-100 text-blue-700 font-medium'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
              }`}
            >
              <tab.icon className={`w-4 h-4 ${selectedTab === tab.id ? tab.color : ''}`} />
              <span className="text-sm font-medium">{tab.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {selectedTab === 'instant' && renderInstantRelief()}
        {selectedTab === 'ai' && renderAIRecommendations()}
        {selectedTab === 'timing' && renderTimingProtocols()}
      </div>

      {/* Footer with Estimated Relief Time */}
      {assessment?.estimated_relief_time && (
        <div className="border-t border-gray-200 px-6 py-4 bg-gray-50 rounded-b-xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <Clock className="w-4 h-4" />
              <span>Estimated relief time: {assessment.estimated_relief_time}</span>
            </div>
            <div className="flex items-center space-x-2 text-sm text-green-600">
              <ThumbsUp className="w-4 h-4" />
              <span>Confidence: {Math.round((assessment?.confidence_score || 0.8) * 100)}%</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SymptomReliefDashboard;