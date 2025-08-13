import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Input } from '../ui/input';
import { 
  Brain, Search, AlertTriangle, Lightbulb, 
  FileText, Target, TrendingUp, Clock,
  ChevronDown, ChevronUp, Copy, Download
} from 'lucide-react';

const ClinicalDecisionSupport = () => {
  const [patientSymptoms, setPatientSymptoms] = useState('');
  const [patientHistory, setPatientHistory] = useState('');
  const [patientAge, setPatientAge] = useState('');
  const [patientGender, setPatientGender] = useState('');
  const [analysisResults, setAnalysisResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [expandedRecommendation, setExpandedRecommendation] = useState(null);

  const handleAnalysis = async () => {
    if (!patientSymptoms.trim()) return;

    setLoading(true);
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;
      
      const requestData = {
        patient_data: {
          age: patientAge,
          gender: patientGender
        },
        symptoms: patientSymptoms.split(',').map(s => s.trim()),
        history: patientHistory.split(',').map(h => h.trim()).filter(Boolean)
      };

      const response = await fetch(`${backendUrl}/api/provider/clinical-decision-support`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      });

      const data = await response.json();
      setAnalysisResults(data);
    } catch (error) {
      console.error('Error getting clinical decision support:', error);
    } finally {
      setLoading(false);
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'bg-green-100 text-green-800';
    if (confidence >= 0.6) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  const getRiskColor = (risk) => {
    if (typeof risk === 'string') {
      switch (risk.toLowerCase()) {
        case 'high': return 'text-red-600';
        case 'moderate': return 'text-yellow-600';
        case 'low': return 'text-green-600';
        default: return 'text-gray-600';
      }
    }
    if (risk >= 0.7) return 'text-red-600';
    if (risk >= 0.4) return 'text-yellow-600';
    return 'text-green-600';
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Brain className="w-6 h-6 mr-2 text-purple-600" />
            AI-Powered Clinical Decision Support
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Patient Age
                  </label>
                  <Input
                    type="number"
                    placeholder="e.g., 45"
                    value={patientAge}
                    onChange={(e) => setPatientAge(e.target.value)}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Gender
                  </label>
                  <select
                    className="w-full p-2 border border-gray-300 rounded-md"
                    value={patientGender}
                    onChange={(e) => setPatientGender(e.target.value)}
                  >
                    <option value="">Select</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Primary Symptoms (comma-separated)
                </label>
                <textarea
                  value={patientSymptoms}
                  onChange={(e) => setPatientSymptoms(e.target.value)}
                  placeholder="e.g., polyuria, polydipsia, weight loss, fatigue"
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
                  placeholder="e.g., family history of diabetes, hypertension, obesity"
                  className="w-full p-3 border border-gray-300 rounded-md resize-none"
                  rows={3}
                />
              </div>
              
              <Button 
                onClick={handleAnalysis}
                disabled={!patientSymptoms.trim() || loading}
                className="w-full bg-purple-600 hover:bg-purple-700"
              >
                <Search className="w-4 h-4 mr-2" />
                {loading ? 'Analyzing...' : 'Analyze & Get AI Recommendations'}
              </Button>
            </div>
            
            {/* Quick Analysis Tips */}
            <div className="bg-purple-50 p-4 rounded-lg">
              <h4 className="font-semibold text-purple-900 mb-3 flex items-center">
                <Lightbulb className="w-4 h-4 mr-2" />
                Analysis Tips
              </h4>
              <ul className="space-y-2 text-sm text-purple-800">
                <li>• Be specific with symptoms (duration, severity, onset)</li>
                <li>• Include relevant family history and comorbidities</li>
                <li>• AI analyzes patterns to suggest evidence-based diagnostics</li>
                <li>• Recommendations are decision support, not diagnostic certainty</li>
                <li>• Always correlate with clinical judgment and examination</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Analysis Results */}
      {analysisResults && (
        <div className="space-y-6">
          {/* AI Recommendations */}
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <CardTitle className="flex items-center">
                  <Brain className="w-5 h-5 mr-2 text-purple-600" />
                  AI Clinical Recommendations
                </CardTitle>
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm">
                    <Copy className="w-4 h-4 mr-2" />
                    Copy Report
                  </Button>
                  <Button variant="outline" size="sm">
                    <Download className="w-4 h-4 mr-2" />
                    Export PDF
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {analysisResults.ai_recommendations?.map((rec, index) => (
                  <div key={index} className="border rounded-lg p-4">
                    <div className="flex justify-between items-start mb-3">
                      <div className="flex items-center space-x-3">
                        <h5 className="font-semibold text-gray-900 capitalize">
                          {rec.category.replace('_', ' ')}
                        </h5>
                        <Badge className={getConfidenceColor(rec.confidence)}>
                          {Math.round(rec.confidence * 100)}% confidence
                        </Badge>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setExpandedRecommendation(
                          expandedRecommendation === index ? null : index
                        )}
                      >
                        {expandedRecommendation === index ? (
                          <ChevronUp className="w-4 h-4" />
                        ) : (
                          <ChevronDown className="w-4 h-4" />
                        )}
                      </Button>
                    </div>
                    
                    <p className="text-gray-800 mb-3 font-medium">{rec.recommendation}</p>
                    <p className="text-sm text-gray-600 mb-3">{rec.evidence}</p>
                    
                    {expandedRecommendation === index && (
                      <div className="mt-4 pt-4 border-t">
                        <h6 className="font-medium text-gray-700 mb-2 flex items-center">
                          <Target className="w-4 h-4 mr-2" />
                          Recommended Next Steps:
                        </h6>
                        <ul className="space-y-1">
                          {rec.next_steps?.map((step, i) => (
                            <li key={i} className="text-sm text-gray-600 flex items-start">
                              <span className="w-2 h-2 bg-purple-400 rounded-full mt-2 mr-2 flex-shrink-0"></span>
                              {step}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Risk Assessment */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <AlertTriangle className="w-5 h-5 mr-2 text-orange-600" />
                Risk Assessment
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {Object.entries(analysisResults.risk_scores || {}).map(([key, value]) => (
                  <div key={key} className="p-4 border rounded-lg">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium capitalize">
                        {key.replace('_', ' ')}
                      </span>
                      <span className={`text-lg font-bold ${getRiskColor(value)}`}>
                        {typeof value === 'number' ? `${Math.round(value * 100)}%` : value}
                      </span>
                    </div>
                    {typeof value === 'number' && (
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${
                            value >= 0.7 ? 'bg-red-500' :
                            value >= 0.4 ? 'bg-yellow-500' : 'bg-green-500'
                          }`}
                          style={{ width: `${value * 100}%` }}
                        />
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Clinical Guidelines */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <FileText className="w-5 h-5 mr-2 text-blue-600" />
                Relevant Clinical Guidelines
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {analysisResults.clinical_guidelines?.map((guideline, index) => (
                  <div key={index} className="border-l-4 border-blue-500 bg-blue-50 p-4 rounded-lg">
                    <div className="font-semibold text-blue-900 mb-1">{guideline.guideline}</div>
                    <p className="text-sm text-blue-800">{guideline.recommendation}</p>
                    {guideline.relevance && (
                      <Badge className="mt-2 bg-blue-100 text-blue-800">
                        {guideline.relevance} relevance
                      </Badge>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Empty State */}
      {!analysisResults && (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-12">
              <Brain className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <div className="text-gray-500 mb-2">AI Clinical Decision Support Ready</div>
              <p className="text-sm text-gray-400">
                Enter patient symptoms and history above to get evidence-based AI recommendations
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ClinicalDecisionSupport;