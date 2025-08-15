import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { Input } from '../ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../ui/tabs';
import { Progress } from '../ui/progress';
import { 
  FileText, 
  Download, 
  Calendar, 
  Clock, 
  Settings,
  Brain,
  BarChart3,
  Printer,
  Mail,
  Share2,
  Eye,
  Loader2,
  CheckCircle,
  AlertTriangle,
  Image,
  Table,
  PieChart,
  TrendingUp,
  Users,
  Heart,
  Activity,
  Shield
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart as RechartsPieChart, Pie, Cell, BarChart, Bar } from 'recharts';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import * as XLSX from 'xlsx';
import SmartNavigation from '../shared/SmartNavigation';

const AutomatedReportGenerator = () => {
  const [reports, setReports] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState('patient_summary');
  const [selectedPatients, setSelectedPatients] = useState(['patient-456']);
  const [reportConfig, setReportConfig] = useState({
    title: 'Patient Report',
    include_charts: true,
    include_insights: true,
    timeframe: '30',
    format: 'pdf'
  });
  const [generating, setGenerating] = useState(false);
  const [generationProgress, setGenerationProgress] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const providerId = 'provider-123';
  const backendUrl = process.env.REACT_APP_BACKEND_URL || import.meta.env.REACT_APP_BACKEND_URL;

  // Report templates
  const reportTemplates = {
    patient_summary: {
      name: 'Patient Summary Report',
      description: 'Comprehensive patient overview with key metrics and recommendations',
      sections: ['demographics', 'health_metrics', 'medication_adherence', 'ai_insights']
    },
    progress_report: {
      name: 'Progress Tracking Report', 
      description: 'Detailed progress analysis with trend data and milestones',
      sections: ['progress_overview', 'trend_analysis', 'milestone_tracking', 'recommendations']
    },
    adherence_analysis: {
      name: 'Adherence Analysis Report',
      description: 'In-depth adherence monitoring with risk assessment',
      sections: ['adherence_metrics', 'risk_analysis', 'barriers', 'interventions']
    },
    risk_assessment: {
      name: 'Risk Assessment Report',
      description: 'Comprehensive risk evaluation with predictive insights',
      sections: ['risk_scores', 'contributing_factors', 'predictive_analytics', 'mitigation_strategies']
    }
  };

  // Fetch existing reports
  const fetchReports = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${backendUrl}/api/provider/patient-management/reports/${providerId}`);
      if (response.ok) {
        const data = await response.json();
        setReports(data.reports || []);
      } else {
        throw new Error('Failed to fetch reports');
      }
    } catch (err) {
      setError(`Error fetching reports: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Generate report using backend AI
  const generateReport = async () => {
    setGenerating(true);
    setGenerationProgress(0);
    
    try {
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setGenerationProgress(prev => prev < 90 ? prev + 10 : prev);
      }, 500);

      const response = await fetch(`${backendUrl}/api/provider/patient-management/reports`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          provider_id: providerId,
          patient_ids: selectedPatients,
          template: selectedTemplate,
          config: reportConfig,
          ai_insights: true
        })
      });
      
      clearInterval(progressInterval);
      setGenerationProgress(100);
      
      if (response.ok) {
        const reportData = await response.json();
        
        // Generate the actual file based on format
        if (reportConfig.format === 'pdf') {
          await generatePDFReport(reportData);
        } else if (reportConfig.format === 'excel') {
          await generateExcelReport(reportData);
        } else if (reportConfig.format === 'csv') {
          await generateCSVReport(reportData);
        }
        
        await fetchReports(); // Refresh reports list
      } else {
        throw new Error('Failed to generate report');
      }
    } catch (err) {
      setError(`Error generating report: ${err.message}`);
    } finally {
      setGenerating(false);
      setGenerationProgress(0);
    }
  };

  // Generate PDF report using jsPDF
  const generatePDFReport = async (reportData) => {
    const pdf = new jsPDF();
    let yPosition = 20;

    // Title
    pdf.setFontSize(20);
    pdf.text(reportConfig.title, 20, yPosition);
    yPosition += 20;

    // Generated date
    pdf.setFontSize(12);
    pdf.text(`Generated: ${new Date().toLocaleDateString()}`, 20, yPosition);
    yPosition += 15;

    // Report sections
    if (reportData.sections) {
      Object.entries(reportData.sections).forEach(([sectionName, sectionData]) => {
        if (yPosition > 250) {
          pdf.addPage();
          yPosition = 20;
        }

        // Section header
        pdf.setFontSize(16);
        pdf.text(sectionName.replace(/_/g, ' ').toUpperCase(), 20, yPosition);
        yPosition += 15;

        // Section content
        pdf.setFontSize(10);
        if (typeof sectionData === 'object') {
          Object.entries(sectionData).forEach(([key, value]) => {
            if (yPosition > 270) {
              pdf.addPage();
              yPosition = 20;
            }
            pdf.text(`${key}: ${typeof value === 'object' ? JSON.stringify(value) : value}`, 25, yPosition);
            yPosition += 10;
          });
        } else {
          pdf.text(sectionData.toString(), 25, yPosition);
          yPosition += 10;
        }
        yPosition += 10;
      });
    }

    // AI Insights
    if (reportData.ai_insights && reportConfig.include_insights) {
      if (yPosition > 200) {
        pdf.addPage();
        yPosition = 20;
      }

      pdf.setFontSize(16);
      pdf.text('AI INSIGHTS', 20, yPosition);
      yPosition += 15;

      pdf.setFontSize(10);
      reportData.ai_insights.forEach(insight => {
        if (yPosition > 270) {
          pdf.addPage();
          yPosition = 20;
        }
        pdf.text(`• ${insight}`, 25, yPosition);
        yPosition += 8;
      });
    }

    // Save PDF
    pdf.save(`${reportConfig.title.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`);
  };

  // Generate Excel report using XLSX
  const generateExcelReport = async (reportData) => {
    const workbook = XLSX.utils.book_new();

    // Summary sheet
    const summaryData = [
      ['Report Title', reportConfig.title],
      ['Generated Date', new Date().toLocaleDateString()],
      ['Provider ID', providerId],
      ['Patient Count', selectedPatients.length],
      ['Template', reportTemplates[selectedTemplate].name]
    ];

    const summarySheet = XLSX.utils.aoa_to_sheet(summaryData);
    XLSX.utils.book_append_sheet(workbook, summarySheet, 'Summary');

    // Data sheets for each section
    if (reportData.sections) {
      Object.entries(reportData.sections).forEach(([sectionName, sectionData]) => {
        try {
          let sheetData;
          if (Array.isArray(sectionData)) {
            sheetData = sectionData;
          } else if (typeof sectionData === 'object') {
            sheetData = Object.entries(sectionData).map(([key, value]) => [key, value]);
          } else {
            sheetData = [[sectionName, sectionData]];
          }
          
          const sheet = XLSX.utils.aoa_to_sheet(sheetData);
          XLSX.utils.book_append_sheet(workbook, sheet, sectionName.substring(0, 31));
        } catch (e) {
          console.warn(`Could not create sheet for ${sectionName}:`, e);
        }
      });
    }

    // Save Excel file
    XLSX.writeFile(workbook, `${reportConfig.title.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.xlsx`);
  };

  // Generate CSV report
  const generateCSVReport = async (reportData) => {
    let csvContent = "data:text/csv;charset=utf-8,";
    
    // Header
    csvContent += `Report: ${reportConfig.title}\n`;
    csvContent += `Generated: ${new Date().toLocaleDateString()}\n`;
    csvContent += `Provider: ${providerId}\n\n`;

    // Sections
    if (reportData.sections) {
      Object.entries(reportData.sections).forEach(([sectionName, sectionData]) => {
        csvContent += `${sectionName.replace(/_/g, ' ').toUpperCase()}\n`;
        if (typeof sectionData === 'object') {
          Object.entries(sectionData).forEach(([key, value]) => {
            csvContent += `"${key}","${value}"\n`;
          });
        } else {
          csvContent += `"${sectionData}"\n`;
        }
        csvContent += "\n";
      });
    }

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `${reportConfig.title.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  useEffect(() => {
    fetchReports();
  }, []);

  // Sample report data for demo
  const sampleReportData = {
    recent_reports: [
      {
        id: 'report_001',
        title: 'January Patient Summary',
        template: 'patient_summary',
        created_at: '2024-01-29',
        status: 'completed',
        format: 'pdf',
        patient_count: 5,
        file_size: '2.4 MB'
      },
      {
        id: 'report_002',
        title: 'Weekly Progress Analysis',
        template: 'progress_report',
        created_at: '2024-01-28',
        status: 'completed',
        format: 'excel',
        patient_count: 12,
        file_size: '1.8 MB'
      },
      {
        id: 'report_003',
        title: 'Adherence Review Q1',
        template: 'adherence_analysis',
        created_at: '2024-01-26',
        status: 'completed',
        format: 'pdf',
        patient_count: 8,
        file_size: '3.2 MB'
      }
    ]
  };

  const displayReports = reports.length > 0 ? reports : sampleReportData.recent_reports;

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
        <SmartNavigation />
        <div className="container mx-auto px-4 py-8">
          <Card className="max-w-md mx-auto">
            <CardContent className="p-6 text-center">
              <AlertTriangle className="mx-auto mb-4 h-12 w-12 text-red-500" />
              <p className="text-red-600">{error}</p>
              <Button onClick={() => window.location.reload()} className="mt-4">
                Try Again
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100">
      <SmartNavigation />
      
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-4">
            <FileText className="h-8 w-8 text-emerald-600" />
            <h1 className="text-3xl font-bold text-gray-900">Automated Report Generator</h1>
          </div>
          <p className="text-gray-600 text-lg">
            Professional PDF report creation with AI insights using free libraries
          </p>
        </div>

        <Tabs defaultValue="generate" className="space-y-6">
          <TabsList className="grid w-full grid-cols-4 bg-white">
            <TabsTrigger value="generate">Generate Report</TabsTrigger>
            <TabsTrigger value="templates">Templates</TabsTrigger>
            <TabsTrigger value="history">Report History</TabsTrigger>
            <TabsTrigger value="settings">Settings</TabsTrigger>
          </TabsList>

          {/* Generate Report Tab */}
          <TabsContent value="generate" className="space-y-6">
            <div className="grid gap-6 lg:grid-cols-2">
              {/* Report Configuration */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Settings className="h-5 w-5" />
                    Report Configuration
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <label className="text-sm font-medium">Report Title</label>
                    <Input
                      value={reportConfig.title}
                      onChange={(e) => setReportConfig(prev => ({ ...prev, title: e.target.value }))}
                      placeholder="Enter report title"
                    />
                  </div>

                  <div>
                    <label className="text-sm font-medium">Template</label>
                    <Select value={selectedTemplate} onValueChange={setSelectedTemplate}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {Object.entries(reportTemplates).map(([key, template]) => (
                          <SelectItem key={key} value={key}>
                            {template.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <label className="text-sm font-medium">Export Format</label>
                    <Select 
                      value={reportConfig.format} 
                      onValueChange={(value) => setReportConfig(prev => ({ ...prev, format: value }))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="pdf">PDF (jsPDF)</SelectItem>
                        <SelectItem value="excel">Excel (XLSX)</SelectItem>
                        <SelectItem value="csv">CSV</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <label className="text-sm font-medium">Timeframe</label>
                    <Select 
                      value={reportConfig.timeframe} 
                      onValueChange={(value) => setReportConfig(prev => ({ ...prev, timeframe: value }))}
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="7">Last 7 Days</SelectItem>
                        <SelectItem value="30">Last 30 Days</SelectItem>
                        <SelectItem value="90">Last 90 Days</SelectItem>
                        <SelectItem value="365">Last Year</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={reportConfig.include_charts}
                        onChange={(e) => setReportConfig(prev => ({ ...prev, include_charts: e.target.checked }))}
                      />
                      <span className="text-sm">Include Charts & Visualizations</span>
                    </label>
                    <label className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={reportConfig.include_insights}
                        onChange={(e) => setReportConfig(prev => ({ ...prev, include_insights: e.target.checked }))}
                      />
                      <span className="text-sm">Include AI Insights</span>
                    </label>
                  </div>
                </CardContent>
              </Card>

              {/* Patient Selection & Generation */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Users className="h-5 w-5" />
                    Patient Selection
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <label className="text-sm font-medium">Select Patients</label>
                    <div className="space-y-2 max-h-40 overflow-y-auto">
                      {['patient-456', 'patient-789', 'patient-012', 'patient-345'].map(patientId => (
                        <label key={patientId} className="flex items-center space-x-2">
                          <input
                            type="checkbox"
                            checked={selectedPatients.includes(patientId)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setSelectedPatients(prev => [...prev, patientId]);
                              } else {
                                setSelectedPatients(prev => prev.filter(id => id !== patientId));
                              }
                            }}
                          />
                          <span className="text-sm">Patient {patientId.split('-')[1]} (John Doe)</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Generation Progress */}
                  {generating && (
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>Generating Report...</span>
                        <span>{generationProgress}%</span>
                      </div>
                      <Progress value={generationProgress} className="h-3" />
                    </div>
                  )}

                  <Button 
                    onClick={generateReport}
                    disabled={generating || selectedPatients.length === 0}
                    className="w-full bg-emerald-600 hover:bg-emerald-700"
                    size="lg"
                  >
                    {generating ? (
                      <>
                        <Loader2 className="h-4 w-4 animate-spin mr-2" />
                        Generating...
                      </>
                    ) : (
                      <>
                        <Download className="h-4 w-4 mr-2" />
                        Generate Report
                      </>
                    )}
                  </Button>
                </CardContent>
              </Card>
            </div>

            {/* Template Preview */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Eye className="h-5 w-5" />
                  Template Preview: {reportTemplates[selectedTemplate].name}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 mb-4">{reportTemplates[selectedTemplate].description}</p>
                <div className="grid gap-2 md:grid-cols-2 lg:grid-cols-4">
                  {reportTemplates[selectedTemplate].sections.map(section => (
                    <Badge key={section} variant="outline" className="justify-start">
                      {section.replace(/_/g, ' ')}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Templates Tab */}
          <TabsContent value="templates" className="space-y-6">
            <div className="grid gap-6 md:grid-cols-2">
              {Object.entries(reportTemplates).map(([key, template]) => (
                <Card key={key} className={selectedTemplate === key ? 'border-emerald-300 bg-emerald-50' : ''}>
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      {template.name}
                      {selectedTemplate === key && <CheckCircle className="h-5 w-5 text-emerald-600" />}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-gray-600 mb-4">{template.description}</p>
                    <div className="space-y-2 mb-4">
                      <h5 className="font-medium text-sm">Included Sections:</h5>
                      <div className="flex flex-wrap gap-1">
                        {template.sections.map(section => (
                          <Badge key={section} variant="secondary" className="text-xs">
                            {section.replace(/_/g, ' ')}
                          </Badge>
                        ))}
                      </div>
                    </div>
                    <Button 
                      onClick={() => setSelectedTemplate(key)}
                      variant={selectedTemplate === key ? "default" : "outline"}
                      size="sm"
                      className="w-full"
                    >
                      {selectedTemplate === key ? 'Selected' : 'Select Template'}
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          {/* Report History Tab */}
          <TabsContent value="history" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="h-5 w-5" />
                  Recent Reports
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {displayReports.map((report) => (
                    <Card key={report.id} className="border-gray-200">
                      <CardContent className="p-4">
                        <div className="flex justify-between items-start">
                          <div className="flex-1">
                            <h4 className="font-semibold">{report.title}</h4>
                            <p className="text-sm text-gray-600">
                              {reportTemplates[report.template]?.name || report.template}
                            </p>
                            <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                              <span>Created: {report.created_at}</span>
                              <span>Patients: {report.patient_count}</span>
                              <span>Size: {report.file_size}</span>
                            </div>
                          </div>
                          <div className="flex items-center gap-2">
                            <Badge className={
                              report.status === 'completed' ? 'bg-green-100 text-green-800' :
                              report.status === 'generating' ? 'bg-blue-100 text-blue-800' :
                              'bg-gray-100 text-gray-800'
                            }>
                              {report.status}
                            </Badge>
                            <Badge variant="outline">
                              {report.format.toUpperCase()}
                            </Badge>
                          </div>
                        </div>
                        
                        <div className="flex gap-2 mt-4">
                          <Button size="sm" variant="outline">
                            <Download className="h-4 w-4 mr-1" />
                            Download
                          </Button>
                          <Button size="sm" variant="outline">
                            <Eye className="h-4 w-4 mr-1" />
                            Preview
                          </Button>
                          <Button size="sm" variant="outline">
                            <Share2 className="h-4 w-4 mr-1" />
                            Share
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Settings Tab */}
          <TabsContent value="settings" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="h-5 w-5" />
                  Report Generation Settings
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="grid gap-6 md:grid-cols-2">
                  <div>
                    <h4 className="font-medium mb-4">Default Settings</h4>
                    <div className="space-y-4">
                      <div>
                        <label className="text-sm font-medium">Default Template</label>
                        <Select defaultValue="patient_summary">
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            {Object.entries(reportTemplates).map(([key, template]) => (
                              <SelectItem key={key} value={key}>
                                {template.name}
                              </SelectItem>
                            ))}
                          </SelectContent>
                        </Select>
                      </div>
                      
                      <div>
                        <label className="text-sm font-medium">Default Format</label>
                        <Select defaultValue="pdf">
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="pdf">PDF</SelectItem>
                            <SelectItem value="excel">Excel</SelectItem>
                            <SelectItem value="csv">CSV</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="font-medium mb-4">Branding & Customization</h4>
                    <div className="space-y-4">
                      <div>
                        <label className="text-sm font-medium">Provider Logo</label>
                        <Input type="file" accept="image/*" />
                      </div>
                      
                      <div>
                        <label className="text-sm font-medium">Header Color</label>
                        <Input type="color" defaultValue="#10b981" />
                      </div>
                      
                      <div>
                        <label className="text-sm font-medium">Footer Text</label>
                        <Input placeholder="© 2024 Healthcare Provider" />
                      </div>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium mb-4">Automation Settings</h4>
                  <div className="space-y-2">
                    <label className="flex items-center space-x-2">
                      <input type="checkbox" />
                      <span className="text-sm">Auto-generate weekly summary reports</span>
                    </label>
                    <label className="flex items-center space-x-2">
                      <input type="checkbox" />
                      <span className="text-sm">Email reports to patients automatically</span>
                    </label>
                    <label className="flex items-center space-x-2">
                      <input type="checkbox" />
                      <span className="text-sm">Include patient photos in reports</span>
                    </label>
                  </div>
                </div>
                
                <Button className="bg-emerald-600 hover:bg-emerald-700">
                  Save Settings
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default AutomatedReportGenerator;