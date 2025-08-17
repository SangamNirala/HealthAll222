"""
Professional Medical Report PDF Generator
Generates high-quality, medical-grade PDF reports with SOAP notes and comprehensive formatting
"""

import io
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, black, blue, red, green
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.lib import colors

class MedicalReportPDFGenerator:
    """
    Professional medical report PDF generator with comprehensive formatting
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom styles for medical reports"""
        
        # Medical Header Style
        self.medical_header_style = ParagraphStyle(
            'MedicalHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            textColor=Color(0.2, 0.4, 0.7),
            fontName='Helvetica-Bold',
            alignment=TA_CENTER
        )
        
        # Section Header Style
        self.section_header_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            spaceBefore=15,
            textColor=Color(0.1, 0.3, 0.6),
            fontName='Helvetica-Bold',
            borderWidth=1,
            borderColor=Color(0.8, 0.8, 0.8),
            borderPadding=5,
            backColor=Color(0.95, 0.97, 1.0)
        )
        
        # Subsection Header Style
        self.subsection_header_style = ParagraphStyle(
            'SubsectionHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=10,
            textColor=Color(0.3, 0.3, 0.3),
            fontName='Helvetica-Bold'
        )
        
        # Medical Content Style
        self.medical_content_style = ParagraphStyle(
            'MedicalContent',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        )
        
        # Clinical Note Style
        self.clinical_note_style = ParagraphStyle(
            'ClinicalNote',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=4,
            fontName='Helvetica',
            leftIndent=20
        )
        
        # Emergency Alert Style
        self.emergency_style = ParagraphStyle(
            'Emergency',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=10,
            textColor=Color(0.8, 0, 0),
            fontName='Helvetica-Bold',
            backColor=Color(1.0, 0.9, 0.9),
            borderWidth=2,
            borderColor=Color(0.8, 0, 0),
            borderPadding=10
        )
        
        # Recommendation Style
        self.recommendation_style = ParagraphStyle(
            'Recommendation',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leftIndent=15,
            bulletIndent=5,
            fontName='Helvetica'
        )
    
    async def generate_comprehensive_medical_report(
        self, 
        soap_data: Dict[str, Any], 
        consultation_data: Dict[str, Any],
        include_differential: bool = True,
        include_recommendations: bool = True
    ) -> bytes:
        """Generate comprehensive medical report PDF"""
        
        # Create PDF buffer
        buffer = io.BytesIO()
        
        # Create document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
            title="Medical AI Consultation Report"
        )
        
        # Build content
        story = []
        
        # Add header
        story.extend(self._create_report_header(soap_data, consultation_data))
        
        # Add patient information
        story.extend(self._create_patient_info_section(soap_data))
        
        # Add emergency alerts if present
        if consultation_data.get('emergency_detected'):
            story.extend(self._create_emergency_section(consultation_data))
        
        # Add SOAP sections
        story.extend(self._create_soap_sections(soap_data))
        
        # Add differential diagnosis
        if include_differential and consultation_data.get('differential_diagnoses'):
            story.extend(self._create_differential_section(consultation_data))
        
        # Add recommendations
        if include_recommendations and consultation_data.get('recommendations'):
            story.extend(self._create_recommendations_section(consultation_data))
        
        # Add footer and disclaimers
        story.extend(self._create_footer_section())
        
        # Build PDF
        doc.build(story, onFirstPage=self._add_header_footer, onLaterPages=self._add_header_footer)
        
        # Get PDF bytes
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _create_report_header(self, soap_data: Dict[str, Any], consultation_data: Dict[str, Any]) -> List:
        """Create report header section"""
        
        story = []
        
        # Main title
        title = Paragraph(
            "<b>AI MEDICAL CONSULTATION REPORT</b>",
            self.medical_header_style
        )
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Report metadata table
        header_info = soap_data.get('header', {})
        
        header_data = [
            ['Report Generated:', datetime.now().strftime("%B %d, %Y at %I:%M %p")],
            ['Consultation ID:', consultation_data.get('consultation_id', 'N/A')],
            ['Provider:', header_info.get('provider', 'Dr. AI (Advanced Medical AI Assistant)')],
            ['Consultation Type:', header_info.get('consultation_type', 'AI-Assisted Medical Consultation')],
            ['Date of Service:', header_info.get('date_of_service', datetime.now().strftime("%B %d, %Y"))],
        ]
        
        header_table = Table(header_data, colWidths=[2*inch, 4*inch])
        header_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, Color(0.97, 0.97, 0.97)])
        ]))
        
        story.append(header_table)
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_patient_info_section(self, soap_data: Dict[str, Any]) -> List:
        """Create patient information section"""
        
        story = []
        
        # Patient Demographics
        header_info = soap_data.get('header', {})
        demographics = header_info.get('patient_demographics', 'Unknown demographics')
        
        story.append(Paragraph("PATIENT INFORMATION", self.section_header_style))
        
        patient_info = [
            ['Demographics:', demographics],
            ['Consultation Method:', header_info.get('consultation_method', 'Telemedicine - AI Chat Interface')],
        ]
        
        patient_table = Table(patient_info, colWidths=[2*inch, 4*inch])
        patient_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        story.append(patient_table)
        story.append(Spacer(1, 15))
        
        return story
    
    def _create_emergency_section(self, consultation_data: Dict[str, Any]) -> List:
        """Create emergency alert section"""
        
        story = []
        
        emergency_text = """
        🚨 <b>MEDICAL EMERGENCY DETECTED</b> 🚨<br/>
        
        This consultation identified symptoms that may indicate a medical emergency. 
        If you have not already done so, please seek immediate medical attention by:
        <br/>
        • Calling 911 or your local emergency services<br/>
        • Going to the nearest emergency room<br/>
        • Contacting your healthcare provider immediately<br/>
        
        <b>This AI assessment does not replace emergency medical care.</b>
        """
        
        emergency_para = Paragraph(emergency_text, self.emergency_style)
        story.append(emergency_para)
        story.append(Spacer(1, 20))
        
        return story
    
    def _create_soap_sections(self, soap_data: Dict[str, Any]) -> List:
        """Create SOAP note sections"""
        
        story = []
        
        # SUBJECTIVE Section
        subjective = soap_data.get('subjective', {})
        if subjective:
            story.append(Paragraph("SUBJECTIVE", self.section_header_style))
            
            # Chief Complaint
            if subjective.get('chief_complaint'):
                story.append(Paragraph("Chief Complaint:", self.subsection_header_style))
                story.append(Paragraph(subjective['chief_complaint'], self.medical_content_style))
                story.append(Spacer(1, 8))
            
            # History of Present Illness
            if subjective.get('history_present_illness'):
                story.append(Paragraph("History of Present Illness:", self.subsection_header_style))
                story.append(Paragraph(subjective['history_present_illness'], self.medical_content_style))
                story.append(Spacer(1, 8))
            
            # Review of Systems
            if subjective.get('review_of_systems'):
                story.append(Paragraph("Review of Systems:", self.subsection_header_style))
                story.append(Paragraph(subjective['review_of_systems'], self.medical_content_style))
                story.append(Spacer(1, 8))
            
            # Past Medical History
            if subjective.get('past_medical_history'):
                story.append(Paragraph("Past Medical History:", self.subsection_header_style))
                story.append(Paragraph(subjective['past_medical_history'], self.medical_content_style))
                story.append(Spacer(1, 8))
            
            # Medications
            if subjective.get('medications'):
                story.append(Paragraph("Medications:", self.subsection_header_style))
                story.append(Paragraph(subjective['medications'], self.medical_content_style))
                story.append(Spacer(1, 8))
            
            # Allergies
            if subjective.get('allergies'):
                story.append(Paragraph("Allergies:", self.subsection_header_style))
                story.append(Paragraph(subjective['allergies'], self.medical_content_style))
                story.append(Spacer(1, 8))
        
        # OBJECTIVE Section
        objective = soap_data.get('objective', {})
        if objective:
            story.append(Paragraph("OBJECTIVE", self.section_header_style))
            
            obj_text = "Physical examination not performed in telemedicine consultation. "
            obj_text += "Assessment based on patient-reported symptoms and medical history. "
            obj_text += "Recommend in-person evaluation for complete physical examination."
            
            story.append(Paragraph(obj_text, self.medical_content_style))
            story.append(Spacer(1, 15))
        
        # ASSESSMENT Section
        assessment = soap_data.get('assessment', {})
        if assessment:
            story.append(Paragraph("ASSESSMENT", self.section_header_style))
            
            # Clinical Impression
            if assessment.get('clinical_impression'):
                story.append(Paragraph("Clinical Impression:", self.subsection_header_style))
                story.append(Paragraph(assessment['clinical_impression'], self.medical_content_style))
                story.append(Spacer(1, 8))
            
            # Risk Stratification
            if assessment.get('risk_stratification'):
                story.append(Paragraph("Risk Stratification:", self.subsection_header_style))
                story.append(Paragraph(assessment['risk_stratification'], self.medical_content_style))
                story.append(Spacer(1, 8))
            
            # Clinical Reasoning
            if assessment.get('clinical_reasoning'):
                story.append(Paragraph("Clinical Reasoning:", self.subsection_header_style))
                story.append(Paragraph(assessment['clinical_reasoning'], self.medical_content_style))
                story.append(Spacer(1, 8))
        
        # PLAN Section
        plan = soap_data.get('plan', {})
        if plan:
            story.append(Paragraph("PLAN", self.section_header_style))
            
            # Diagnostic Workup
            if plan.get('diagnostic_workup'):
                story.append(Paragraph("Diagnostic Workup:", self.subsection_header_style))
                workup = plan['diagnostic_workup']
                if isinstance(workup, list):
                    for item in workup:
                        if isinstance(item, dict):
                            test_text = f"• <b>{item.get('test', 'Unknown test')}</b>: {item.get('indication', 'No indication provided')} ({item.get('urgency', 'routine')})"
                        else:
                            test_text = f"• {item}"
                        story.append(Paragraph(test_text, self.recommendation_style))
                else:
                    story.append(Paragraph(str(workup), self.medical_content_style))
                story.append(Spacer(1, 8))
            
            # Therapeutic Interventions
            if plan.get('therapeutic_interventions'):
                story.append(Paragraph("Therapeutic Interventions:", self.subsection_header_style))
                interventions = plan['therapeutic_interventions']
                if isinstance(interventions, list):
                    for item in interventions:
                        if isinstance(item, dict):
                            treatment_text = f"• <b>{item.get('treatment', 'Unknown treatment')}</b>: {item.get('indication', 'No indication provided')}"
                        else:
                            treatment_text = f"• {item}"
                        story.append(Paragraph(treatment_text, self.recommendation_style))
                else:
                    story.append(Paragraph(str(interventions), self.medical_content_style))
                story.append(Spacer(1, 8))
            
            # Patient Education
            if plan.get('patient_education'):
                story.append(Paragraph("Patient Education:", self.subsection_header_style))
                education = plan['patient_education']
                if isinstance(education, list):
                    for item in education:
                        story.append(Paragraph(f"• {item}", self.recommendation_style))
                else:
                    story.append(Paragraph(str(education), self.medical_content_style))
                story.append(Spacer(1, 8))
            
            # Follow-up Plan
            if plan.get('follow_up_plan'):
                story.append(Paragraph("Follow-up Plan:", self.subsection_header_style))
                followup = plan['follow_up_plan']
                if isinstance(followup, dict):
                    for key, value in followup.items():
                        story.append(Paragraph(f"• <b>{key.replace('_', ' ').title()}:</b> {value}", self.recommendation_style))
                else:
                    story.append(Paragraph(str(followup), self.medical_content_style))
                story.append(Spacer(1, 8))
            
            # Return Precautions
            if plan.get('return_precautions'):
                story.append(Paragraph("Return Precautions - Seek Immediate Care If:", self.subsection_header_style))
                precautions = plan['return_precautions']
                if isinstance(precautions, list):
                    for item in precautions:
                        story.append(Paragraph(f"• {item}", self.recommendation_style))
                else:
                    story.append(Paragraph(str(precautions), self.medical_content_style))
                story.append(Spacer(1, 15))
        
        return story
    
    def _create_differential_section(self, consultation_data: Dict[str, Any]) -> List:
        """Create differential diagnosis section"""
        
        story = []
        
        story.append(Paragraph("DIFFERENTIAL DIAGNOSIS", self.section_header_style))
        
        differential_diagnoses = consultation_data.get('differential_diagnoses', [])
        
        if isinstance(differential_diagnoses, list) and differential_diagnoses:
            # Create table for differential diagnoses
            table_data = [['Rank', 'Diagnosis', 'Probability', 'Clinical Reasoning']]
            
            for i, diagnosis in enumerate(differential_diagnoses[:5], 1):
                if isinstance(diagnosis, dict):
                    rank = str(i)
                    condition = diagnosis.get('condition', 'Unknown condition')
                    probability = f"{diagnosis.get('probability', 0)}%"
                    reasoning = diagnosis.get('reasoning', 'No reasoning provided')
                    
                    # Truncate reasoning for table
                    if len(reasoning) > 100:
                        reasoning = reasoning[:97] + "..."
                    
                    table_data.append([rank, condition, probability, reasoning])
            
            if len(table_data) > 1:  # If we have data beyond header
                diff_table = Table(table_data, colWidths=[0.5*inch, 2*inch, 1*inch, 2.5*inch])
                diff_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('ALIGN', (2, 0), (2, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, Color(0.97, 0.97, 0.97)])
                ]))
                
                story.append(diff_table)
        else:
            story.append(Paragraph("No differential diagnoses available.", self.medical_content_style))
        
        story.append(Spacer(1, 15))
        
        return story
    
    def _create_recommendations_section(self, consultation_data: Dict[str, Any]) -> List:
        """Create recommendations section"""
        
        story = []
        
        story.append(Paragraph("RECOMMENDATIONS", self.section_header_style))
        
        recommendations = consultation_data.get('recommendations', [])
        
        if isinstance(recommendations, list) and recommendations:
            for i, rec in enumerate(recommendations, 1):
                story.append(Paragraph(f"{i}. {rec}", self.recommendation_style))
        else:
            story.append(Paragraph("No specific recommendations available.", self.medical_content_style))
        
        story.append(Spacer(1, 15))
        
        return story
    
    def _create_footer_section(self) -> List:
        """Create footer section with disclaimers"""
        
        story = []
        
        # Add page break before footer
        story.append(PageBreak())
        
        # Medical Disclaimer
        story.append(Paragraph("IMPORTANT MEDICAL DISCLAIMER", self.section_header_style))
        
        disclaimer_text = """
        <b>This report is generated by an AI medical assistant and is for informational purposes only.</b>
        
        <b>Important Points:</b><br/>
        • This assessment does not constitute a formal medical diagnosis<br/>
        • AI recommendations should not replace professional medical advice<br/>
        • Always consult with a qualified healthcare provider for proper medical evaluation<br/>
        • In case of emergency, call 911 or seek immediate medical attention<br/>
        • This AI system is designed to assist, not replace, medical professionals<br/>
        
        <b>Accuracy and Limitations:</b><br/>
        • AI assessments are based on reported symptoms and available medical literature<br/>
        • Physical examination findings are not available in telemedicine consultations<br/>
        • Individual medical history and risk factors may not be fully captured<br/>
        • Rare conditions or atypical presentations may not be adequately considered<br/>
        
        <b>Follow-up Recommendations:</b><br/>
        • Share this report with your healthcare provider<br/>
        • Seek professional medical evaluation for proper diagnosis and treatment<br/>
        • Follow up with appropriate specialists as recommended<br/>
        • Monitor symptoms and seek immediate care if condition worsens<br/>
        """
        
        story.append(Paragraph(disclaimer_text, self.medical_content_style))
        story.append(Spacer(1, 20))
        
        # AI System Information
        story.append(Paragraph("AI SYSTEM INFORMATION", self.subsection_header_style))
        
        ai_info_text = """
        <b>System:</b> Medical AI Assistant (Advanced Version)<br/>
        <b>Knowledge Base:</b> Trained on peer-reviewed medical literature and clinical guidelines<br/>
        <b>Last Updated:</b> Current medical knowledge as of training data cutoff<br/>
        <b>Validation:</b> Recommendations based on evidence-based medicine principles<br/>
        <b>Limitations:</b> Cannot perform physical examination or diagnostic tests<br/>
        """
        
        story.append(Paragraph(ai_info_text, self.clinical_note_style))
        
        return story
    
    def _add_header_footer(self, canvas, doc):
        """Add header and footer to each page"""
        
        canvas.saveState()
        
        # Footer
        footer_text = f"Medical AI Consultation Report • Generated on {datetime.now().strftime('%B %d, %Y')} • Page {doc.page}"
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        canvas.drawCentredText(letter[0]/2, 30, footer_text)
        
        # Header line on subsequent pages
        if doc.page > 1:
            canvas.setStrokeColor(Color(0.8, 0.8, 0.8))
            canvas.line(72, letter[1] - 50, letter[0] - 72, letter[1] - 50)
        
        canvas.restoreState()
    
    def generate_summary_report(self, consultation_data: Dict[str, Any]) -> bytes:
        """Generate a concise summary report"""
        
        buffer = io.BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
            title="Medical AI Summary Report"
        )
        
        story = []
        
        # Title
        story.append(Paragraph("AI MEDICAL CONSULTATION SUMMARY", self.medical_header_style))
        story.append(Spacer(1, 20))
        
        # Basic Information
        info_data = [
            ['Consultation Date:', datetime.now().strftime("%B %d, %Y")],
            ['Consultation ID:', consultation_data.get('consultation_id', 'N/A')],
            ['Patient:', consultation_data.get('demographics', {}).get('patient_demographics', 'Anonymous Patient')],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Chief Complaint
        chief_complaint = consultation_data.get('chief_complaint', 'Not specified')
        story.append(Paragraph("Chief Complaint:", self.subsection_header_style))
        story.append(Paragraph(chief_complaint, self.medical_content_style))
        story.append(Spacer(1, 15))
        
        # Top Diagnoses
        differential_diagnoses = consultation_data.get('differential_diagnoses', [])
        if differential_diagnoses:
            story.append(Paragraph("Most Likely Diagnoses:", self.subsection_header_style))
            
            for i, diagnosis in enumerate(differential_diagnoses[:3], 1):
                if isinstance(diagnosis, dict):
                    condition = diagnosis.get('condition', 'Unknown')
                    probability = diagnosis.get('probability', 0)
                    diagnosis_text = f"{i}. <b>{condition}</b> ({probability}% probability)"
                    story.append(Paragraph(diagnosis_text, self.recommendation_style))
            
            story.append(Spacer(1, 15))
        
        # Key Recommendations
        recommendations = consultation_data.get('recommendations', [])
        if recommendations:
            story.append(Paragraph("Key Recommendations:", self.subsection_header_style))
            
            for i, rec in enumerate(recommendations[:3], 1):
                story.append(Paragraph(f"{i}. {rec}", self.recommendation_style))
            
            story.append(Spacer(1, 15))
        
        # Emergency Alert
        if consultation_data.get('emergency_detected'):
            emergency_text = "<b>⚠️ EMERGENCY DETECTED:</b> This consultation identified potential emergency symptoms. Seek immediate medical attention."
            story.append(Paragraph(emergency_text, self.emergency_style))
        
        # Build PDF
        doc.build(story)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def encode_pdf_base64(self, pdf_bytes: bytes) -> str:
        """Encode PDF bytes to base64 string for API response"""
        return base64.b64encode(pdf_bytes).decode('utf-8')