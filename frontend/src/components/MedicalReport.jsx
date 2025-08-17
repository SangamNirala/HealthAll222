import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Button } from './ui/button';
import { 
  FileText, Download, Mail, Share2, Printer, Eye, 
  AlertTriangle, Clock, User, Calendar, Stethoscope,
  Heart, Activity, Zap, Shield, CheckCircle, XCircle,
  ArrowRight, ExternalLink, Info, BookOpen
} from 'lucide-react';
import { medicalAPI } from '../services/medicalAPI';

const MedicalReport = ({ 
  consultation, 
  soapData, 
  consultationData, 
  isVisible = true, 
  onClose 
}) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [isGeneratingPDF, setIsGeneratingPDF] = useState(false);
  const [reportGenerated, setReportGenerated] = useState(false);
  const [pdfUrl, setPdfUrl] = useState(null);

  const tabs = [
    { id: 'overview', label: 'Overview', icon: Eye },
    { id: 'soap', label: 'SOAP Notes', icon: FileText },
    { id: 'differential', label: 'Diagnosis', icon: Stethoscope },
    { id: 'recommendations', label: 'Plan', icon: BookOpen },
  ];

  const handleGeneratePDF = async () => {
    setIsGeneratingPDF(true);
    
    try {
      const response = await medicalAPI.generateMedicalReport({
        consultation_id: consultation?.consultation_id,
        soap_data: soapData,
        consultation_data: consultationData,
        include_differential: true,
        include_recommendations: true
      });
      
      // Create blob from base64 PDF data
      const pdfBlob = new Blob([
        Uint8Array.from(atob(response.pdf_base64), c => c.charCodeAt(0))
      ], { type: 'application/pdf' });
      
      const url = URL.createObjectURL(pdfBlob);
      setPdfUrl(url);
      setReportGenerated(true);
      
    } catch (error) {
      console.error('Failed to generate PDF:', error);
      alert('Failed to generate PDF report. Please try again.');
    } finally {
      setIsGeneratingPDF(false);
    }
  };

  const handleDownloadPDF = () => {
    if (pdfUrl) {
      const link = document.createElement('a');
      link.href = pdfUrl;
      link.download = `Medical_Report_${consultation?.consultation_id || 'Unknown'}_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const handleShareReport = () => {
    if (navigator.share && pdfUrl) {
      navigator.share({
        title: 'Medical AI Consultation Report',
        text: 'My medical consultation report from AI Doctor',
        files: [new File([pdfUrl], `medical-report-${new Date().toISOString().split('T')[0]}.pdf`, { type: 'application/pdf' })]
      });
    } else {
      // Fallback: copy consultation summary to clipboard
      const summaryText = `Medical AI Consultation Summary\n\nDate: ${new Date().toLocaleDateString()}\nConsultation ID: ${consultation?.consultation_id}\n\nKey Findings: ${consultationData?.differential_diagnoses?.[0]?.condition || 'See full report'}\n\nThis is an AI-generated medical consultation report. Please consult with a healthcare provider for proper medical advice.`;
      
      navigator.clipboard.writeText(summaryText).then(() => {
        alert('Report summary copied to clipboard');
      });
    }
  };

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-6xl h-[90vh] flex flex-col overflow-hidden">
        
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-white/20 rounded-lg">
              <FileText className="h-6 w-6" />
            </div>
            <div>
              <h2 className="text-xl font-bold">Medical Consultation Report</h2>
              <p className="text-blue-100 text-sm">
                Generated on {new Date().toLocaleDateString()} • ID: {consultation?.consultation_id}
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <Button
              onClick={handleGeneratePDF}
              disabled={isGeneratingPDF}
              className="bg-white/20 hover:bg-white/30 text-white border-white/30"
              size="sm"
            >
              {isGeneratingPDF ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Generating...
                </>
              ) : (
                <>
                  <Download className="h-4 w-4 mr-2" />
                  Generate PDF
                </>
              )}
            </Button>
            
            {reportGenerated && (
              <>
                <Button
                  onClick={handleDownloadPDF}
                  className="bg-green-500 hover:bg-green-600 text-white"
                  size="sm"
                >
                  <Download className="h-4 w-4 mr-2" />
                  Download
                </Button>
                
                <Button
                  onClick={handleShareReport}
                  className="bg-purple-500 hover:bg-purple-600 text-white"
                  size="sm"
                >
                  <Share2 className="h-4 w-4 mr-2" />
                  Share
                </Button>
              </>
            )}
            
            {onClose && (
              <Button
                onClick={onClose}
                variant="ghost"
                size="sm"
                className="text-white hover:bg-white/20"
              >
                ✕
              </Button>
            )}
          </div>
        </div>

        {/* Emergency Alert */}
        {consultationData?.emergency_detected && (
          <div className="bg-red-50 border-l-4 border-red-400 p-4 mx-6 mt-4 rounded-r-lg">
            <div className="flex items-center">
              <AlertTriangle className="h-5 w-5 text-red-400 mr-3" />
              <div>
                <h3 className="text-red-800 font-medium">Medical Emergency Detected</h3>
                <p className="text-red-700 text-sm mt-1">
                  This consultation identified symptoms that may require immediate medical attention. 
                  Please seek professional medical care promptly.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Tab Navigation */}
        <div className="flex border-b border-gray-200 px-6 pt-4">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <Icon className="h-4 w-4 mr-2" />
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-6">
          
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              
              {/* Patient Summary */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center text-lg">
                    <User className="h-5 w-5 mr-2 text-blue-600" />
                    Patient Summary
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="space-y-3">
                      <div className="flex items-center">
                        <Calendar className="h-4 w-4 text-gray-400 mr-2" />
                        <span className="text-sm text-gray-600">Consultation Date:</span>
                        <span className="text-sm font-medium ml-2">{new Date().toLocaleDateString()}</span>
                      </div>
                      <div className="flex items-center">
                        <Clock className="h-4 w-4 text-gray-400 mr-2" />
                        <span className="text-sm text-gray-600">Duration:</span>
                        <span className="text-sm font-medium ml-2">
                          {consultationData?.duration || 'Not recorded'}
                        </span>
                      </div>
                      <div className="flex items-center">
                        <Stethoscope className="h-4 w-4 text-gray-400 mr-2" />
                        <span className="text-sm text-gray-600">Provider:</span>
                        <span className="text-sm font-medium ml-2">Dr. AI (Medical AI Assistant)</span>
                      </div>
                    </div>
                    <div className="space-y-3">
                      <div className="flex items-center">
                        <Activity className="h-4 w-4 text-gray-400 mr-2" />
                        <span className="text-sm text-gray-600">Consultation Type:</span>
                        <span className="text-sm font-medium ml-2">AI-Assisted Telemedicine</span>
                      </div>
                      <div className="flex items-center">
                        <Shield className="h-4 w-4 text-gray-400 mr-2" />
                        <span className="text-sm text-gray-600">Privacy:</span>
                        <span className="text-sm font-medium ml-2">HIPAA Compliant</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Chief Complaint */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center text-lg">
                    <Heart className="h-5 w-5 mr-2 text-red-500" />
                    Chief Complaint
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-700 leading-relaxed">
                    {consultationData?.chief_complaint || soapData?.subjective?.chief_complaint || 'Not specified'}
                  </p>
                </CardContent>
              </Card>

              {/* Quick Assessment */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center text-lg">
                    <Zap className="h-5 w-5 mr-2 text-yellow-500" />
                    Quick Assessment
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-3 gap-4">
                    
                    {/* Urgency Level */}
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-600">Urgency Level</span>
                        {consultationData?.urgency === 'emergency' ? (
                          <AlertTriangle className="h-4 w-4 text-red-500" />
                        ) : consultationData?.urgency === 'urgent' ? (
                          <Clock className="h-4 w-4 text-orange-500" />
                        ) : (
                          <CheckCircle className="h-4 w-4 text-green-500" />
                        )}
                      </div>
                      <div className="text-lg font-bold capitalize">
                        {consultationData?.urgency || 'Routine'}
                      </div>
                    </div>

                    {/* Top Diagnosis */}
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-600">Most Likely</span>
                        <Stethoscope className="h-4 w-4 text-blue-500" />
                      </div>
                      <div className="text-lg font-bold text-blue-700">
                        {consultationData?.differential_diagnoses?.[0]?.condition || 'Pending evaluation'}
                      </div>
                      {consultationData?.differential_diagnoses?.[0]?.probability && (
                        <div className="text-sm text-blue-600">
                          {consultationData.differential_diagnoses[0].probability}% probability
                        </div>
                      )}
                    </div>

                    {/* Confidence Score */}
                    <div className="bg-green-50 p-4 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium text-gray-600">AI Confidence</span>
                        <Activity className="h-4 w-4 text-green-500" />
                      </div>
                      <div className="text-lg font-bold text-green-700">
                        {consultationData?.confidence ? `${Math.round(consultationData.confidence * 100)}%` : 'N/A'}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* SOAP Notes Tab */}
          {activeTab === 'soap' && (
            <div className="space-y-6">
              
              {/* Subjective */}
              {soapData?.subjective && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg text-blue-700">Subjective</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    
                    {soapData.subjective.chief_complaint && (
                      <div>
                        <h4 className="font-semibold text-gray-700 mb-2">Chief Complaint</h4>
                        <p className="text-gray-600 pl-4 border-l-2 border-blue-200">
                          {soapData.subjective.chief_complaint}
                        </p>
                      </div>
                    )}
                    
                    {soapData.subjective.history_present_illness && (
                      <div>
                        <h4 className="font-semibold text-gray-700 mb-2">History of Present Illness</h4>
                        <p className="text-gray-600 pl-4 border-l-2 border-blue-200">
                          {soapData.subjective.history_present_illness}
                        </p>
                      </div>
                    )}
                    
                    {soapData.subjective.past_medical_history && (
                      <div>
                        <h4 className="font-semibold text-gray-700 mb-2">Past Medical History</h4>
                        <p className="text-gray-600 pl-4 border-l-2 border-blue-200">
                          {soapData.subjective.past_medical_history}
                        </p>
                      </div>
                    )}
                    
                    {soapData.subjective.medications && (
                      <div>
                        <h4 className="font-semibold text-gray-700 mb-2">Medications</h4>
                        <p className="text-gray-600 pl-4 border-l-2 border-blue-200">
                          {soapData.subjective.medications}
                        </p>
                      </div>
                    )}
                    
                    {soapData.subjective.allergies && (
                      <div>
                        <h4 className="font-semibold text-gray-700 mb-2">Allergies</h4>
                        <p className="text-gray-600 pl-4 border-l-2 border-blue-200">
                          {soapData.subjective.allergies}
                        </p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              )}

              {/* Objective */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg text-green-700">Objective</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600 italic">
                    Physical examination not performed in telemedicine consultation. 
                    Assessment based on patient-reported symptoms and medical history. 
                    Recommend in-person evaluation for complete physical examination.
                  </p>
                </CardContent>
              </Card>

              {/* Assessment */}
              {soapData?.assessment && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg text-orange-700">Assessment</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    
                    {soapData.assessment.clinical_impression && (
                      <div>
                        <h4 className="font-semibold text-gray-700 mb-2">Clinical Impression</h4>
                        <p className="text-gray-600 pl-4 border-l-2 border-orange-200">
                          {soapData.assessment.clinical_impression}
                        </p>
                      </div>
                    )}
                    
                    {soapData.assessment.clinical_reasoning && (
                      <div>
                        <h4 className="font-semibold text-gray-700 mb-2">Clinical Reasoning</h4>
                        <p className="text-gray-600 pl-4 border-l-2 border-orange-200">
                          {soapData.assessment.clinical_reasoning}
                        </p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              )}

              {/* Plan */}
              {soapData?.plan && (
                <Card>
                  <CardHeader>
                    <CardTitle className="text-lg text-purple-700">Plan</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    
                    {soapData.plan.therapeutic_interventions && (
                      <div>
                        <h4 className="font-semibold text-gray-700 mb-2">Treatment Recommendations</h4>
                        <div className="pl-4 border-l-2 border-purple-200">
                          {Array.isArray(soapData.plan.therapeutic_interventions) ? (
                            <ul className="space-y-2">
                              {soapData.plan.therapeutic_interventions.map((intervention, index) => (
                                <li key={index} className="flex items-start">
                                  <ArrowRight className="h-4 w-4 text-purple-500 mr-2 mt-0.5 flex-shrink-0" />
                                  <span className="text-gray-600">
                                    {typeof intervention === 'object' ? intervention.treatment : intervention}
                                  </span>
                                </li>
                              ))}
                            </ul>
                          ) : (
                            <p className="text-gray-600">{soapData.plan.therapeutic_interventions}</p>
                          )}
                        </div>
                      </div>
                    )}
                    
                    {soapData.plan.patient_education && (
                      <div>
                        <h4 className="font-semibold text-gray-700 mb-2">Patient Education</h4>
                        <div className="pl-4 border-l-2 border-purple-200">
                          {Array.isArray(soapData.plan.patient_education) ? (
                            <ul className="space-y-2">
                              {soapData.plan.patient_education.map((education, index) => (
                                <li key={index} className="flex items-start">
                                  <Info className="h-4 w-4 text-blue-500 mr-2 mt-0.5 flex-shrink-0" />
                                  <span className="text-gray-600">{education}</span>
                                </li>
                              ))}
                            </ul>
                          ) : (
                            <p className="text-gray-600">{soapData.plan.patient_education}</p>
                          )}
                        </div>
                      </div>
                    )}
                  </CardContent>
                </Card>
              )}
            </div>
          )}

          {/* Differential Diagnosis Tab */}
          {activeTab === 'differential' && (
            <div className="space-y-6">
              
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Differential Diagnosis</CardTitle>
                </CardHeader>
                <CardContent>
                  
                  {consultationData?.differential_diagnoses && consultationData.differential_diagnoses.length > 0 ? (
                    <div className="space-y-4">
                      {consultationData.differential_diagnoses.slice(0, 5).map((diagnosis, index) => (
                        <div key={index} className="border rounded-lg p-4 hover:bg-gray-50 transition-colors">
                          <div className="flex items-center justify-between mb-3">
                            <div className="flex items-center">
                              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm mr-3 ${
                                index === 0 ? 'bg-green-500' : 
                                index === 1 ? 'bg-blue-500' : 
                                index === 2 ? 'bg-yellow-500' : 'bg-gray-500'
                              }`}>
                                {index + 1}
                              </div>
                              <h3 className="text-lg font-semibold text-gray-800">
                                {diagnosis.condition}
                              </h3>
                            </div>
                            <div className="text-right">
                              <div className="text-2xl font-bold text-blue-600">
                                {diagnosis.probability}%
                              </div>
                              <div className="text-xs text-gray-500">probability</div>
                            </div>
                          </div>
                          
                          {diagnosis.reasoning && (
                            <div className="mb-3">
                              <h4 className="text-sm font-medium text-gray-700 mb-1">Clinical Reasoning:</h4>
                              <p className="text-sm text-gray-600 pl-3 border-l-2 border-gray-200">
                                {diagnosis.reasoning}
                              </p>
                            </div>
                          )}
                          
                          {diagnosis.icd_code && (
                            <div className="flex items-center text-xs text-gray-500">
                              <span className="bg-gray-100 px-2 py-1 rounded">
                                ICD-10: {diagnosis.icd_code}
                              </span>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-gray-500">
                      <Stethoscope className="h-12 w-12 mx-auto mb-4 text-gray-300" />
                      <p>No differential diagnoses available</p>
                      <p className="text-sm">Complete the consultation to see diagnostic analysis</p>
                    </div>
                  )}
                </CardContent>
              </Card>
            </div>
          )}

          {/* Recommendations Tab */}
          {activeTab === 'recommendations' && (
            <div className="space-y-6">
              
              {/* Immediate Actions */}
              {consultationData?.urgency === 'emergency' && (
                <Card className="border-red-200 bg-red-50">
                  <CardHeader>
                    <CardTitle className="text-lg text-red-700 flex items-center">
                      <AlertTriangle className="h-5 w-5 mr-2" />
                      Immediate Actions Required
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex items-center text-red-700">
                        <ArrowRight className="h-4 w-4 mr-2" />
                        Call 911 or go to the nearest emergency room immediately
                      </div>
                      <div className="flex items-center text-red-700">
                        <ArrowRight className="h-4 w-4 mr-2" />
                        Do not drive yourself - call for emergency transportation
                      </div>
                      <div className="flex items-center text-red-700">
                        <ArrowRight className="h-4 w-4 mr-2" />
                        Bring this report and any medications with you
                      </div>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Treatment Recommendations */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Treatment Recommendations</CardTitle>
                </CardHeader>
                <CardContent>
                  {consultationData?.recommendations && consultationData.recommendations.length > 0 ? (
                    <div className="space-y-3">
                      {consultationData.recommendations.map((recommendation, index) => (
                        <div key={index} className="flex items-start p-3 bg-blue-50 rounded-lg">
                          <CheckCircle className="h-5 w-5 text-green-500 mr-3 mt-0.5 flex-shrink-0" />
                          <span className="text-gray-700">{recommendation}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500 italic">No specific recommendations available</p>
                  )}
                </CardContent>
              </Card>

              {/* Follow-up Care */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Follow-up Care</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="p-4 bg-yellow-50 rounded-lg border border-yellow-200">
                      <h4 className="font-semibold text-yellow-800 mb-2">Healthcare Provider Follow-up</h4>
                      <p className="text-yellow-700 text-sm">
                        Schedule an appointment with your primary care physician within 1-2 weeks 
                        to discuss these findings and develop a comprehensive treatment plan.
                      </p>
                    </div>
                    
                    <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                      <h4 className="font-semibold text-purple-800 mb-2">Monitoring Instructions</h4>
                      <p className="text-purple-700 text-sm">
                        Keep track of your symptoms and any changes. Return to care immediately 
                        if symptoms worsen or new concerning symptoms develop.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Important Notes */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Important Medical Disclaimer</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 text-sm text-gray-600">
                    <div className="flex items-start">
                      <Info className="h-4 w-4 text-blue-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span>This AI assessment is for informational purposes only and does not constitute medical advice</span>
                    </div>
                    <div className="flex items-start">
                      <Info className="h-4 w-4 text-blue-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span>Always consult with a qualified healthcare provider for proper medical evaluation</span>
                    </div>
                    <div className="flex items-start">
                      <Info className="h-4 w-4 text-blue-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span>In case of emergency, call 911 or seek immediate medical attention</span>
                    </div>
                    <div className="flex items-start">
                      <Info className="h-4 w-4 text-blue-500 mr-2 mt-0.5 flex-shrink-0" />
                      <span>Share this report with your healthcare provider for continuity of care</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MedicalReport;