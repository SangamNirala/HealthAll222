import React, { useState, useRef, useEffect } from 'react';
import { 
  Brain, 
  Activity, 
  Heart, 
  AlertTriangle, 
  CheckCircle, 
  Calendar, 
  TrendingUp, 
  Clock, 
  Target,
  Zap,
  Shield,
  BookOpen,
  ArrowRight,
  ArrowLeft,
  RotateCcw
} from 'lucide-react';
import SymptomReliefDashboard from './SymptomReliefDashboard';
import ActionPlanTracker from './ActionPlanTracker';

const QuickSymptomChecker = ({ userId }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [symptoms, setSymptoms] = useState([]);
  const [assessment, setAssessment] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Common symptoms library
  const commonSymptoms = [
    { name: 'headache', label: 'Headache', icon: '🧠', category: 'neurological' },
    { name: 'fatigue', label: 'Fatigue/Tiredness', icon: '😴', category: 'energy' },
    { name: 'bloating', label: 'Bloating', icon: '🤰', category: 'digestive' },
    { name: 'nausea', label: 'Nausea', icon: '🤢', category: 'digestive' },
    { name: 'muscle_aches', label: 'Muscle Aches', icon: '💪', category: 'pain' },
    { name: 'brain_fog', label: 'Brain Fog', icon: '🌫️', category: 'neurological' },
    { name: 'sleep_issues', label: 'Sleep Problems', icon: '🛌', category: 'sleep' },
    { name: 'mood_swings', label: 'Mood Changes', icon: '😕', category: 'mental' },
    { name: 'joint_pain', label: 'Joint Pain', icon: '🦴', category: 'pain' },
    { name: 'digestive_issues', label: 'Digestive Issues', icon: '🍽️', category: 'digestive' },
    { name: 'skin_issues', label: 'Skin Problems', icon: '🧴', category: 'skin' },
    { name: 'energy_crashes', label: 'Energy Crashes', icon: '📉', category: 'energy' }
  ];

  const addSymptom = (symptomData) => {
    const newSymptom = {
      id: Date.now(),
      name: symptomData.name,
      label: symptomData.label,
      icon: symptomData.icon,
      severity: 5,
      frequency: 3,
      duration_days: 1,
      life_impact: 3,
      description: '',
      triggers: []
    };
    setSymptoms([...symptoms, newSymptom]);
  };

  const updateSymptom = (id, field, value) => {
    setSymptoms(symptoms.map(symptom => 
      symptom.id === id ? { ...symptom, [field]: value } : symptom
    ));
  };

  const removeSymptom = (id) => {
    setSymptoms(symptoms.filter(symptom => symptom.id !== id));
  };

  const assessSymptoms = async () => {
    if (symptoms.length === 0) {
      setError('Please add at least one symptom before assessment');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL}/api/symptom-checker/assess`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: userId || `guest_${Date.now()}`,
          symptoms: symptoms.map(({ id, label, icon, ...rest }) => rest),
          additional_info: {
            timestamp: new Date().toISOString(),
            source: 'guest_dashboard'
          }
        })
      });

      if (!response.ok) {
        throw new Error('Assessment failed');
      }

      const data = await response.json();
      setAssessment(data);
      setCurrentStep(3);
    } catch (err) {
      setError('Failed to process assessment. Please try again.');
      console.error('Assessment error:', err);
    } finally {
      setLoading(false);
    }
  };

  const resetAssessment = () => {
    setCurrentStep(1);
    setSymptoms([]);
    setAssessment(null);
    setError(null);
  };

  const renderSymptomSelection = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 text-white rounded-2xl mb-4">
          <Activity className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          What symptoms are you experiencing?
        </h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Select from common symptoms or add your own. You can choose multiple symptoms to get a comprehensive assessment.
        </p>
      </div>

      {/* Common Symptoms Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 mb-8">
        {commonSymptoms.map((symptom) => (
          <button
            key={symptom.name}
            onClick={() => addSymptom(symptom)}
            disabled={symptoms.some(s => s.name === symptom.name)}
            className={`p-4 rounded-lg border-2 transition-all duration-200 text-left hover:scale-105 ${
              symptoms.some(s => s.name === symptom.name)
                ? 'border-green-300 bg-green-50 text-green-800 cursor-not-allowed'
                : 'border-gray-200 hover:border-blue-300 hover:bg-blue-50'
            }`}
          >
            <div className="flex items-center space-x-3">
              <span className="text-2xl">{symptom.icon}</span>
              <div>
                <div className="font-medium text-sm">{symptom.label}</div>
                <div className="text-xs text-gray-500 capitalize">{symptom.category}</div>
              </div>
            </div>
            {symptoms.some(s => s.name === symptom.name) && (
              <CheckCircle className="w-4 h-4 text-green-600 mt-2" />
            )}
          </button>
        ))}
      </div>

      {/* Selected Symptoms */}
      {symptoms.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
            Selected Symptoms ({symptoms.length})
          </h3>
          <div className="space-y-4">
            {symptoms.map((symptom) => (
              <div key={symptom.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center space-x-3">
                    <span className="text-xl">{symptom.icon}</span>
                    <span className="font-medium">{symptom.label}</span>
                  </div>
                  <button
                    onClick={() => removeSymptom(symptom.id)}
                    className="text-red-500 hover:text-red-700 text-sm"
                  >
                    Remove
                  </button>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Severity (1-10)
                    </label>
                    <input
                      type="range"
                      min="1"
                      max="10"
                      value={symptom.severity}
                      onChange={(e) => updateSymptom(symptom.id, 'severity', parseInt(e.target.value))}
                      className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                    />
                    <div className="text-xs text-center text-gray-600 mt-1">
                      {symptom.severity}/10
                    </div>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Duration (days)
                    </label>
                    <input
                      type="number"
                      min="0"
                      value={symptom.duration_days}
                      onChange={(e) => updateSymptom(symptom.id, 'duration_days', parseInt(e.target.value))}
                      className="w-full px-3 py-1 border border-gray-300 rounded-md text-sm"
                    />
                  </div>
                </div>
                
                <div className="mt-3">
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Impact on daily life (1-5)
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="5"
                    value={symptom.life_impact}
                    onChange={(e) => updateSymptom(symptom.id, 'life_impact', parseInt(e.target.value))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  />
                  <div className="text-xs text-center text-gray-600 mt-1">
                    {['None', 'Minimal', 'Moderate', 'Significant', 'Severe'][symptom.life_impact - 1]}
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-6 flex justify-between">
            <button
              onClick={() => setCurrentStep(2)}
              disabled={symptoms.length === 0}
              className="flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              Continue to Assessment
              <ArrowRight className="w-4 h-4 ml-2" />
            </button>
            
            <button
              onClick={resetAssessment}
              className="flex items-center px-4 py-3 text-gray-600 hover:text-gray-800"
            >
              <RotateCcw className="w-4 h-4 mr-2" />
              Reset
            </button>
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center">
            <AlertTriangle className="w-5 h-5 text-red-500 mr-2" />
            <span className="text-red-800">{error}</span>
          </div>
        </div>
      )}
    </div>
  );

  const renderAssessmentStep = () => (
    <div className="space-y-6">
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-green-500 to-blue-600 text-white rounded-2xl mb-4">
          <Brain className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Ready for AI Analysis?
        </h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Our AI will analyze your symptoms and provide personalized relief recommendations and a 3-day action plan.
        </p>
      </div>

      {/* Symptoms Summary */}
      <div className="bg-white border border-gray-200 rounded-xl p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Symptoms Summary</h3>
        <div className="grid gap-3">
          {symptoms.map((symptom) => (
            <div key={symptom.id} className="flex items-center justify-between py-2 border-b border-gray-100 last:border-b-0">
              <div className="flex items-center space-x-3">
                <span className="text-lg">{symptom.icon}</span>
                <span className="font-medium">{symptom.label}</span>
              </div>
              <div className="text-sm text-gray-600">
                Severity: {symptom.severity}/10 • {symptom.duration_days} day{symptom.duration_days !== 1 ? 's' : ''}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* What You'll Get */}
      <div className="grid md:grid-cols-3 gap-4">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-4">
          <div className="flex items-center space-x-3 mb-2">
            <Zap className="w-6 h-6 text-blue-600" />
            <h4 className="font-semibold text-blue-900">Instant Relief</h4>
          </div>
          <p className="text-sm text-blue-700">
            Immediate actions you can take right now for symptom relief.
          </p>
        </div>
        
        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-4">
          <div className="flex items-center space-x-3 mb-2">
            <Calendar className="w-6 h-6 text-green-600" />
            <h4 className="font-semibold text-green-900">3-Day Plan</h4>
          </div>
          <p className="text-sm text-green-700">
            Structured action plan with daily activities and progress tracking.
          </p>
        </div>
        
        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-4">
          <div className="flex items-center space-x-3 mb-2">
            <Shield className="w-6 h-6 text-purple-600" />
            <h4 className="font-semibold text-purple-900">Medical Guidance</h4>
          </div>
          <p className="text-sm text-purple-700">
            Smart alerts and guidance on when to seek professional help.
          </p>
        </div>
      </div>

      <div className="flex justify-between">
        <button
          onClick={() => setCurrentStep(1)}
          className="flex items-center px-6 py-3 text-gray-600 hover:text-gray-800 font-medium"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Symptoms
        </button>
        
        <button
          onClick={assessSymptoms}
          disabled={loading || symptoms.length === 0}
          className="flex items-center px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              Analyzing...
            </>
          ) : (
            <>
              <Brain className="w-4 h-4 mr-2" />
              Get AI Assessment
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center">
            <AlertTriangle className="w-5 h-5 text-red-500 mr-2" />
            <span className="text-red-800">{error}</span>
          </div>
        </div>
      )}
    </div>
  );

  const renderResults = () => {
    if (!assessment) return null;

    return (
      <div className="space-y-6">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-green-500 to-blue-600 text-white rounded-2xl mb-4">
            <Target className="w-8 h-8" />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Your Personalized Wellness Plan
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Based on your symptoms, here's your AI-powered relief strategy and action plan.
          </p>
        </div>

        {/* Medical Advisory Alert */}
        {assessment.medical_advisory && (
          <div className={`border-l-4 p-4 rounded-lg ${
            assessment.medical_advisory.alert_level === 'emergency' ? 'border-red-500 bg-red-50' :
            assessment.medical_advisory.alert_level === 'red' ? 'border-orange-500 bg-orange-50' :
            assessment.medical_advisory.alert_level === 'yellow' ? 'border-yellow-500 bg-yellow-50' :
            'border-green-500 bg-green-50'
          }`}>
            <div className="flex items-start">
              <AlertTriangle className={`w-5 h-5 mr-3 mt-0.5 ${
                assessment.medical_advisory.alert_level === 'emergency' ? 'text-red-600' :
                assessment.medical_advisory.alert_level === 'red' ? 'text-orange-600' :
                assessment.medical_advisory.alert_level === 'yellow' ? 'text-yellow-600' :
                'text-green-600'
              }`} />
              <div>
                <h4 className="font-semibold text-gray-900 mb-1">Medical Advisory</h4>
                <p className="text-sm text-gray-800 mb-2">{assessment.medical_advisory.urgency_assessment}</p>
                <div className="text-sm text-gray-700">
                  <strong>Recommended Action:</strong> {assessment.medical_advisory.timeline}
                </div>
              </div>
            </div>
          </div>
        )}

        <SymptomReliefDashboard 
          assessment={assessment} 
          userId={userId}
        />

        <ActionPlanTracker 
          actionPlan={assessment.action_plan}
          assessmentId={assessment.assessment_id}
          userId={userId}
        />

        <div className="flex justify-center pt-6">
          <button
            onClick={resetAssessment}
            className="flex items-center px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 font-medium"
          >
            <RotateCcw className="w-4 h-4 mr-2" />
            New Assessment
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* Progress Indicator */}
      <div className="flex items-center justify-center mb-8">
        <div className="flex items-center space-x-4">
          {[1, 2, 3].map((step) => (
            <React.Fragment key={step}>
              <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 font-semibold ${
                currentStep >= step 
                  ? 'border-blue-600 bg-blue-600 text-white' 
                  : 'border-gray-300 text-gray-400'
              }`}>
                {step}
              </div>
              {step < 3 && (
                <div className={`w-12 h-0.5 ${
                  currentStep > step ? 'bg-blue-600' : 'bg-gray-300'
                }`} />
              )}
            </React.Fragment>
          ))}
        </div>
      </div>

      {/* Step Labels */}
      <div className="flex justify-center mb-8">
        <div className="flex items-center space-x-8 text-sm">
          <span className={currentStep >= 1 ? 'text-blue-600 font-medium' : 'text-gray-500'}>
            Select Symptoms
          </span>
          <span className={currentStep >= 2 ? 'text-blue-600 font-medium' : 'text-gray-500'}>
            Assessment
          </span>
          <span className={currentStep >= 3 ? 'text-blue-600 font-medium' : 'text-gray-500'}>
            Relief Plan
          </span>
        </div>
      </div>

      {/* Content */}
      {currentStep === 1 && renderSymptomSelection()}
      {currentStep === 2 && renderAssessmentStep()}
      {currentStep === 3 && renderResults()}
    </div>
  );
};

export default QuickSymptomChecker;