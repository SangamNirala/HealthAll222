import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Input } from '../ui/input';
import { 
  BookOpen, Search, Star, ExternalLink, Download, 
  FileText, Users, Calendar, TrendingUp, Filter,
  Bookmark, Share, Eye, Clock, Award
} from 'lucide-react';

const EvidenceBasedRecommendations = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCondition, setSelectedCondition] = useState('');
  const [recommendationsData, setRecommendationsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('search');
  const [patientProfile, setPatientProfile] = useState('');

  const handleGetRecommendations = async () => {
    if (!selectedCondition) return;
    
    setLoading(true);
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;
      
      const requestData = {
        condition: selectedCondition,
        patient_profile: patientProfile ? patientProfile.split(',').map(p => p.trim()) : [],
        clinical_context: searchQuery
      };

      const response = await fetch(`${backendUrl}/api/provider/evidence-recommendations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      });

      const data = await response.json();
      setRecommendationsData(data);
    } catch (error) {
      console.error('Error fetching evidence recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  const getEvidenceLevelColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'a': return 'bg-green-100 text-green-800';
      case 'b': return 'bg-blue-100 text-blue-800';
      case 'c': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.9) return 'bg-green-100 text-green-800';
    if (confidence >= 0.7) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  // Sample recent research data
  const recentResearch = [
    {
      title: "Mediterranean Diet and Cardiovascular Outcomes in Type 2 Diabetes",
      journal: "New England Journal of Medicine",
      date: "2024-01-15",
      impact: "High",
      summary: "23% reduction in cardiovascular events with Mediterranean diet adherence",
      relevance: "Diabetes Management"
    },
    {
      title: "GLP-1 Receptor Agonists: Updated Clinical Guidelines 2024",
      journal: "American Diabetes Association",
      date: "2024-01-10",
      impact: "High",
      summary: "New recommendations for GLP-1 use in cardiovascular risk reduction",
      relevance: "Diabetes Treatment"
    },
    {
      title: "Lifestyle Interventions in Hypertension Management",
      journal: "Hypertension Research",
      date: "2023-12-28",
      impact: "Medium",
      summary: "Combined interventions show 40% better outcomes than medication alone",
      relevance: "Hypertension Management"
    }
  ];

  return (
    <div className="space-y-6">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('search')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'search'
                ? 'border-emerald-500 text-emerald-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <Search className="w-4 h-4 inline mr-2" />
            Personalized Recommendations
          </button>
          <button
            onClick={() => setActiveTab('recent')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'recent'
                ? 'border-emerald-500 text-emerald-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <TrendingUp className="w-4 h-4 inline mr-2" />
            Latest Research
          </button>
          <button
            onClick={() => setActiveTab('guidelines')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'guidelines'
                ? 'border-emerald-500 text-emerald-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <FileText className="w-4 h-4 inline mr-2" />
            Clinical Guidelines
          </button>
        </nav>
      </div>

      {/* Personalized Recommendations Tab */}
      {activeTab === 'search' && (
        <div className="space-y-6">
          {/* Search Interface */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <BookOpen className="w-6 h-6 mr-2 text-emerald-600" />
                AI-Powered Evidence-Based Recommendations
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Primary Condition
                    </label>
                    <select
                      className="w-full p-2 border border-gray-300 rounded-md"
                      value={selectedCondition}
                      onChange={(e) => setSelectedCondition(e.target.value)}
                    >
                      <option value="">Select condition</option>
                      <option value="Type 2 Diabetes">Type 2 Diabetes</option>
                      <option value="Hypertension">Hypertension</option>
                      <option value="Obesity">Obesity</option>
                      <option value="Heart Disease">Heart Disease</option>
                      <option value="Depression">Depression</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Patient Profile (comma-separated)
                    </label>
                    <Input
                      placeholder="e.g., age 65, male, BMI 32, HbA1c 8.2"
                      value={patientProfile}
                      onChange={(e) => setPatientProfile(e.target.value)}
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Clinical Context (optional)
                    </label>
                    <textarea
                      className="w-full p-3 border border-gray-300 rounded-md resize-none"
                      rows={3}
                      placeholder="Additional clinical context, treatment history, or specific questions"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                    />
                  </div>
                  
                  <Button 
                    onClick={handleGetRecommendations}
                    disabled={!selectedCondition || loading}
                    className="w-full bg-emerald-600 hover:bg-emerald-700"
                  >
                    <Search className="w-4 h-4 mr-2" />
                    {loading ? 'Analyzing Evidence...' : 'Get Evidence-Based Recommendations'}
                  </Button>
                </div>
                
                {/* Quick Tips */}
                <div className="bg-emerald-50 p-4 rounded-lg">
                  <h4 className="font-semibold text-emerald-900 mb-3 flex items-center">
                    <Award className="w-4 h-4 mr-2" />
                    Evidence Quality Levels
                  </h4>
                  <div className="space-y-2 text-sm text-emerald-800">
                    <div className="flex items-center">
                      <Badge className="bg-green-100 text-green-800 mr-2">A</Badge>
                      Multiple high-quality RCTs or meta-analyses
                    </div>
                    <div className="flex items-center">
                      <Badge className="bg-blue-100 text-blue-800 mr-2">B</Badge>
                      Well-conducted clinical studies
                    </div>
                    <div className="flex items-center">
                      <Badge className="bg-yellow-100 text-yellow-800 mr-2">C</Badge>
                      Expert opinion and case studies
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Recommendations Results */}
          {recommendationsData && (
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Star className="w-5 h-5 mr-2 text-emerald-600" />
                    Evidence-Based Treatment Recommendations
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recommendationsData.recommendations?.map((rec, index) => (
                      <div key={index} className="border rounded-lg p-4">
                        <div className="flex justify-between items-start mb-3">
                          <div className="flex items-center space-x-3">
                            <h5 className="font-semibold text-gray-900 capitalize">
                              {rec.category?.replace('_', ' ')}
                            </h5>
                            <Badge className={getEvidenceLevelColor(rec.evidence_level)}>
                              Level {rec.evidence_level} Evidence
                            </Badge>
                            <Badge className={getConfidenceColor(rec.confidence)}>
                              {Math.round(rec.confidence * 100)}% confidence
                            </Badge>
                          </div>
                          <div className="flex space-x-2">
                            <Button variant="ghost" size="sm">
                              <Bookmark className="w-4 h-4" />
                            </Button>
                            <Button variant="ghost" size="sm">
                              <Share className="w-4 h-4" />
                            </Button>
                          </div>
                        </div>
                        
                        <p className="text-gray-800 font-medium mb-2">{rec.recommendation}</p>
                        <p className="text-sm text-gray-600 mb-3">Source: {rec.source}</p>
                        
                        {rec.dosing && (
                          <div className="mb-3 p-3 bg-blue-50 rounded-lg">
                            <h6 className="font-medium text-blue-900 mb-1">Dosing Guidelines:</h6>
                            <p className="text-sm text-blue-800">{rec.dosing}</p>
                          </div>
                        )}
                        
                        {rec.monitoring && (
                          <div className="mb-3 p-3 bg-yellow-50 rounded-lg">
                            <h6 className="font-medium text-yellow-900 mb-1">Monitoring Requirements:</h6>
                            <p className="text-sm text-yellow-800">{rec.monitoring}</p>
                          </div>
                        )}
                        
                        {rec.contraindications?.length > 0 && (
                          <div className="mb-3 p-3 bg-red-50 rounded-lg">
                            <h6 className="font-medium text-red-900 mb-1">Contraindications:</h6>
                            <ul className="text-sm text-red-800 space-y-1">
                              {rec.contraindications.map((contra, i) => (
                                <li key={i}>• {contra}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                        
                        {rec.expected_outcome && (
                          <div className="p-3 bg-green-50 rounded-lg">
                            <h6 className="font-medium text-green-900 mb-1">Expected Outcome:</h6>
                            <p className="text-sm text-green-800">{rec.expected_outcome}</p>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Clinical Studies */}
              {recommendationsData.clinical_studies?.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <FileText className="w-5 h-5 mr-2 text-blue-600" />
                      Supporting Clinical Evidence
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {recommendationsData.clinical_studies.map((study, index) => (
                        <div key={index} className="border rounded-lg p-4">
                          <div className="flex justify-between items-start">
                            <div className="flex-1">
                              <h6 className="font-medium text-gray-900 mb-1">{study.study}</h6>
                              <p className="text-sm text-gray-600 mb-2">{study.finding}</p>
                              <div className="flex items-center space-x-4 text-xs text-gray-500">
                                <span>Year: {study.year}</span>
                                <span>Participants: {study.patient_count}</span>
                                <Badge variant="outline">{study.relevance} relevance</Badge>
                              </div>
                            </div>
                            <Button variant="outline" size="sm">
                              <ExternalLink className="w-4 h-4 mr-1" />
                              View Study
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Follow-up Recommendations */}
              {recommendationsData.follow_up_recommendations?.length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Calendar className="w-5 h-5 mr-2 text-purple-600" />
                      Follow-up & Monitoring Plan
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {recommendationsData.follow_up_recommendations.map((followUp, index) => (
                        <li key={index} className="flex items-start">
                          <Clock className="w-4 h-4 text-purple-600 mt-1 mr-2 flex-shrink-0" />
                          <span className="text-gray-700">{followUp}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}
            </div>
          )}
        </div>
      )}

      {/* Latest Research Tab */}
      {activeTab === 'recent' && (
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <CardTitle className="flex items-center">
                  <TrendingUp className="w-5 h-5 mr-2 text-emerald-600" />
                  Latest Clinical Research & Updates
                </CardTitle>
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm">
                    <Filter className="w-4 h-4 mr-2" />
                    Filter by Specialty
                  </Button>
                  <Button variant="outline" size="sm">
                    <Download className="w-4 h-4 mr-2" />
                    Export List
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentResearch.map((research, index) => (
                  <div key={index} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex justify-between items-start mb-2">
                      <h5 className="font-semibold text-gray-900 flex-1">{research.title}</h5>
                      <div className="flex space-x-2 ml-4">
                        <Button variant="ghost" size="sm">
                          <Eye className="w-4 h-4" />
                        </Button>
                        <Button variant="ghost" size="sm">
                          <Bookmark className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                      <span className="font-medium">{research.journal}</span>
                      <span>•</span>
                      <span>{research.date}</span>
                      <span>•</span>
                      <Badge className={
                        research.impact === 'High' ? 'bg-red-100 text-red-800' :
                        research.impact === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-blue-100 text-blue-800'
                      }>
                        {research.impact} Impact
                      </Badge>
                    </div>
                    
                    <p className="text-gray-700 mb-3">{research.summary}</p>
                    
                    <div className="flex justify-between items-center">
                      <Badge variant="outline">{research.relevance}</Badge>
                      <Button variant="outline" size="sm">
                        <ExternalLink className="w-4 h-4 mr-2" />
                        Read Full Article
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Clinical Guidelines Tab */}
      {activeTab === 'guidelines' && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <FileText className="w-5 h-5 mr-2 text-emerald-600" />
              Clinical Practice Guidelines
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-center py-12">
              <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <div className="text-gray-500 mb-2">Clinical Guidelines Library</div>
              <p className="text-sm text-gray-400">
                Access to latest clinical practice guidelines coming soon
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default EvidenceBasedRecommendations;