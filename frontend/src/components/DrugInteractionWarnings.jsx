import React, { useState, useEffect } from 'react';
import { useRole } from '../context/RoleContext';
import SmartNavigation from './shared/SmartNavigation';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { 
  AlertTriangle, 
  Shield, 
  Plus, 
  X, 
  Search, 
  AlertCircle,
  Info,
  Zap,
  Clock,
  Heart,
  Pill,
  Utensils,
  User,
  FileText,
  RefreshCw,
  CheckCircle2,
  ExternalLink
} from 'lucide-react';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

const DrugInteractionWarnings = () => {
  const { switchRole } = useRole();
  const [loading, setLoading] = useState(false);
  const [medications, setMedications] = useState(['']);
  const [interactions, setInteractions] = useState([]);
  const [summary, setSummary] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('checker');
  const [alternatives, setAlternatives] = useState({});
  const [loadingAlternatives, setLoadingAlternatives] = useState({});

  useEffect(() => {
    switchRole('patient');
  }, [switchRole]);

  const addMedicationField = () => {
    setMedications([...medications, '']);
  };

  const removeMedicationField = (index) => {
    if (medications.length > 1) {
      const newMedications = medications.filter((_, i) => i !== index);
      setMedications(newMedications);
    }
  };

  const updateMedication = (index, value) => {
    const newMedications = [...medications];
    newMedications[index] = value;
    setMedications(newMedications);
  };

  const checkInteractions = async () => {
    const validMedications = medications.filter(med => med.trim() !== '');
    
    if (validMedications.length < 2) {
      setError('Please enter at least 2 medications to check for interactions.');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/drug-interaction/check`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          medications: validMedications,
          user_id: 'demo-patient-123'
        })
      });

      const data = await response.json();

      if (data.success) {
        setInteractions(data.interactions);
        setSummary(data.summary);
        setRecommendations(data.recommendations);
        setActiveTab('results');
      } else {
        setError(data.error || 'Failed to check interactions');
      }
    } catch (err) {
      setError('Error connecting to interaction checking service. Please try again.');
      console.error('Interaction check error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getAlternatives = async (drugName) => {
    setLoadingAlternatives(prev => ({ ...prev, [drugName]: true }));
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/drug-interaction/alternatives/${encodeURIComponent(drugName)}`);
      const data = await response.json();
      
      setAlternatives(prev => ({
        ...prev,
        [drugName]: data.alternatives || []
      }));
    } catch (err) {
      console.error('Error fetching alternatives:', err);
    } finally {
      setLoadingAlternatives(prev => ({ ...prev, [drugName]: false }));
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'major':
        return <AlertTriangle className="w-5 h-5 text-red-600" />;
      case 'moderate':
        return <AlertCircle className="w-5 h-5 text-yellow-600" />;
      case 'minor':
        return <Info className="w-5 h-5 text-blue-600" />;
      default:
        return <Shield className="w-5 h-5 text-gray-600" />;
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'major':
        return 'bg-red-50 border-red-200 text-red-800';
      case 'moderate':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      case 'minor':
        return 'bg-blue-50 border-blue-200 text-blue-800';
      default:
        return 'bg-gray-50 border-gray-200 text-gray-800';
    }
  };

  const getSeverityBadgeColor = (severity) => {
    switch (severity) {
      case 'major':
        return 'bg-red-100 text-red-800';
      case 'moderate':
        return 'bg-yellow-100 text-yellow-800';
      case 'minor':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const loadCommonMedications = () => {
    setMedications(['Warfarin', 'Aspirin', 'Metformin']);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <SmartNavigation />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Drug Interaction Checker</h1>
          <p className="text-gray-600">
            Check for potential interactions between medications, including food and drug interactions
          </p>
          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg flex items-center">
              <AlertTriangle className="w-5 h-5 mr-2" />
              {error}
            </div>
          )}
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="checker" className="flex items-center">
              <Search className="w-4 h-4 mr-2" />
              Interaction Checker
            </TabsTrigger>
            <TabsTrigger value="results" className="flex items-center" disabled={interactions.length === 0}>
              <FileText className="w-4 h-4 mr-2" />
              Results ({interactions.length})
            </TabsTrigger>
          </TabsList>

          {/* Interaction Checker Tab */}
          <TabsContent value="checker">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span className="flex items-center">
                    <Pill className="w-5 h-5 mr-2 text-blue-600" />
                    Enter Medications
                  </span>
                  <Button
                    onClick={loadCommonMedications}
                    variant="outline"
                    size="sm"
                  >
                    Load Example
                  </Button>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {medications.map((medication, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <div className="flex-1">
                      <Input
                        placeholder={`Medication ${index + 1} (e.g., Warfarin, Aspirin)`}
                        value={medication}
                        onChange={(e) => updateMedication(index, e.target.value)}
                        className="w-full"
                      />
                    </div>
                    {medications.length > 1 && (
                      <Button
                        onClick={() => removeMedicationField(index)}
                        variant="ghost"
                        size="sm"
                        className="text-red-500 hover:text-red-700"
                      >
                        <X className="w-4 h-4" />
                      </Button>
                    )}
                  </div>
                ))}
                
                <div className="flex items-center justify-between pt-4 border-t">
                  <Button
                    onClick={addMedicationField}
                    variant="outline"
                    size="sm"
                    className="flex items-center"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Add Medication
                  </Button>
                  
                  <Button
                    onClick={checkInteractions}
                    disabled={loading || medications.filter(m => m.trim()).length < 2}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    {loading ? (
                      <>
                        <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                        Checking...
                      </>
                    ) : (
                      <>
                        <Search className="w-4 h-4 mr-2" />
                        Check Interactions
                      </>
                    )}
                  </Button>
                </div>

                {/* Safety Notice */}
                <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                  <div className="flex items-start">
                    <AlertTriangle className="w-5 h-5 text-amber-600 mt-0.5 mr-3" />
                    <div>
                      <h4 className="font-semibold text-amber-800">Important Disclaimer</h4>
                      <p className="text-sm text-amber-700 mt-1">
                        This tool is for educational purposes only and should not replace professional medical advice. 
                        Always consult with your healthcare provider before making changes to your medications.
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Results Tab */}
          <TabsContent value="results">
            {summary && (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <Card className={`border-2 ${summary.major_interactions > 0 ? 'border-red-200 bg-red-50' : 'border-gray-200'}`}>
                  <CardContent className="p-4 text-center">
                    <AlertTriangle className={`w-8 h-8 mx-auto mb-2 ${summary.major_interactions > 0 ? 'text-red-600' : 'text-gray-400'}`} />
                    <div className="text-2xl font-bold text-red-600">{summary.major_interactions}</div>
                    <div className="text-sm text-gray-600">Major Interactions</div>
                  </CardContent>
                </Card>

                <Card className={`border-2 ${summary.moderate_interactions > 0 ? 'border-yellow-200 bg-yellow-50' : 'border-gray-200'}`}>
                  <CardContent className="p-4 text-center">
                    <AlertCircle className={`w-8 h-8 mx-auto mb-2 ${summary.moderate_interactions > 0 ? 'text-yellow-600' : 'text-gray-400'}`} />
                    <div className="text-2xl font-bold text-yellow-600">{summary.moderate_interactions}</div>
                    <div className="text-sm text-gray-600">Moderate Interactions</div>
                  </CardContent>
                </Card>

                <Card className={`border-2 ${summary.minor_interactions > 0 ? 'border-blue-200 bg-blue-50' : 'border-gray-200'}`}>
                  <CardContent className="p-4 text-center">
                    <Info className={`w-8 h-8 mx-auto mb-2 ${summary.minor_interactions > 0 ? 'text-blue-600' : 'text-gray-400'}`} />
                    <div className="text-2xl font-bold text-blue-600">{summary.minor_interactions}</div>
                    <div className="text-sm text-gray-600">Minor Interactions</div>
                  </CardContent>
                </Card>

                <Card className={`border-2 ${summary.food_interactions > 0 ? 'border-green-200 bg-green-50' : 'border-gray-200'}`}>
                  <CardContent className="p-4 text-center">
                    <Utensils className={`w-8 h-8 mx-auto mb-2 ${summary.food_interactions > 0 ? 'text-green-600' : 'text-gray-400'}`} />
                    <div className="text-2xl font-bold text-green-600">{summary.food_interactions}</div>
                    <div className="text-sm text-gray-600">Food Interactions</div>
                  </CardContent>
                </Card>
              </div>
            )}

            {/* Recommendations */}
            {recommendations && (
              <Card className="mb-6">
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Heart className="w-5 h-5 mr-2 text-red-600" />
                    Clinical Recommendations
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {recommendations.consult_provider && (
                      <div className="flex items-center p-3 bg-red-50 border border-red-200 rounded-lg">
                        <AlertTriangle className="w-5 h-5 text-red-600 mr-3" />
                        <span className="text-red-800 font-medium">
                          Consult your healthcare provider immediately due to major interactions detected
                        </span>
                      </div>
                    )}
                    {recommendations.monitor_closely && (
                      <div className="flex items-center p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                        <Clock className="w-5 h-5 text-yellow-600 mr-3" />
                        <span className="text-yellow-800 font-medium">
                          Close monitoring recommended due to moderate interactions
                        </span>
                      </div>
                    )}
                    {recommendations.general_awareness && (
                      <div className="flex items-center p-3 bg-blue-50 border border-blue-200 rounded-lg">
                        <Info className="w-5 h-5 text-blue-600 mr-3" />
                        <span className="text-blue-800 font-medium">
                          Maintain awareness of potential minor interactions
                        </span>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Interaction Details */}
            <div className="space-y-4">
              {interactions.map((interaction, index) => (
                <Card key={index} className={`border-2 ${getSeverityColor(interaction.severity)}`}>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        {getSeverityIcon(interaction.severity)}
                        <div>
                          <div className="flex items-center space-x-2">
                            <span className="font-semibold">
                              {interaction.drug_pair.join(' + ')}
                            </span>
                            <Badge className={getSeverityBadgeColor(interaction.severity)}>
                              {interaction.severity.toUpperCase()}
                            </Badge>
                            {interaction.interaction_type === 'drug-food' && (
                              <Badge variant="outline" className="bg-green-100 text-green-800">
                                <Utensils className="w-3 h-3 mr-1" />
                                Food Interaction
                              </Badge>
                            )}
                          </div>
                          <div className="text-sm text-gray-600 mt-1">
                            Confidence: {Math.round(interaction.confidence * 100)}% • 
                            Evidence: {interaction.evidence_level}
                          </div>
                        </div>
                      </div>
                      
                      {interaction.interaction_type === 'drug-drug' && (
                        <Button
                          onClick={() => getAlternatives(interaction.drug_pair[0])}
                          variant="outline"
                          size="sm"
                          disabled={loadingAlternatives[interaction.drug_pair[0]]}
                        >
                          {loadingAlternatives[interaction.drug_pair[0]] ? (
                            <RefreshCw className="w-4 h-4 animate-spin" />
                          ) : (
                            <>
                              <ExternalLink className="w-4 h-4 mr-2" />
                              Alternatives
                            </>
                          )}
                        </Button>
                      )}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <h4 className="font-semibold text-gray-900 mb-2">Description</h4>
                        <p className="text-gray-700">{interaction.description}</p>
                      </div>

                      {interaction.mechanism && (
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2">Mechanism</h4>
                          <p className="text-gray-700">{interaction.mechanism}</p>
                        </div>
                      )}

                      <div>
                        <h4 className="font-semibold text-gray-900 mb-2">Management</h4>
                        <p className="text-gray-700">{interaction.management}</p>
                      </div>

                      {interaction.adverse_events && interaction.adverse_events.length > 0 && (
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2">Potential Adverse Events</h4>
                          <div className="flex flex-wrap gap-2">
                            {interaction.adverse_events.map((event, idx) => (
                              <Badge key={idx} variant="secondary" className="bg-gray-100 text-gray-800">
                                {event}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      )}

                      {interaction.foods_to_monitor && (
                        <div>
                          <h4 className="font-semibold text-gray-900 mb-2">Foods to Monitor</h4>
                          <div className="flex flex-wrap gap-2">
                            {interaction.foods_to_monitor.map((food, idx) => (
                              <Badge key={idx} variant="outline" className="bg-green-50 text-green-800 border-green-200">
                                <Utensils className="w-3 h-3 mr-1" />
                                {food}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Show alternatives if loaded */}
                      {alternatives[interaction.drug_pair[0]] && alternatives[interaction.drug_pair[0]].length > 0 && (
                        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                          <h4 className="font-semibold text-gray-900 mb-3">Alternative Medications for {interaction.drug_pair[0]}</h4>
                          <div className="space-y-2">
                            {alternatives[interaction.drug_pair[0]].map((alt, idx) => (
                              <div key={idx} className="p-3 bg-white rounded border">
                                <div className="flex items-center justify-between mb-1">
                                  <span className="font-medium text-gray-900">{alt.name}</span>
                                  <Badge variant="outline">{alt.class}</Badge>
                                </div>
                                <div className="text-sm text-gray-600">
                                  <div className="mb-1">
                                    <span className="font-medium text-green-700">Advantages:</span> {alt.advantages.join(', ')}
                                  </div>
                                  <div>
                                    <span className="font-medium text-amber-700">Considerations:</span> {alt.considerations.join(', ')}
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {interactions.length === 0 && (
              <Card>
                <CardContent className="p-12 text-center">
                  <CheckCircle2 className="w-16 h-16 mx-auto mb-4 text-green-500" />
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    No Interactions Detected 
                  </h3>
                  <p className="text-gray-600 mb-4">
                    Based on our current database, no significant interactions were found between the medications you entered.
                  </p>
                  <p className="text-sm text-gray-500">
                    This doesn't guarantee complete safety. Always consult your healthcare provider about medication combinations.
                  </p>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default DrugInteractionWarnings;