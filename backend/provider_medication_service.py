"""
Provider Medication Management Service
Handles medication adherence, effectiveness tracking, and provider communications
"""
import os
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

@dataclass
class MedicationAdherence:
    patient_id: str
    medication_id: str
    medication_name: str
    prescribed_dose: str
    taken_doses: int
    missed_doses: int
    adherence_percentage: float
    last_taken: Optional[datetime]
    provider_notes: str

@dataclass
class SideEffectReport:
    id: str
    patient_id: str
    medication_id: str
    medication_name: str
    side_effect: str
    severity: str  # mild, moderate, severe
    reported_date: datetime
    provider_notified: bool
    provider_response: Optional[str]

@dataclass
class EffectivenessReport:
    patient_id: str
    medication_id: str
    medication_name: str
    condition: str
    effectiveness_score: float  # 1-10 scale
    patient_feedback: str
    clinical_markers: Dict[str, Any]
    provider_assessment: Optional[str]

class ProviderMedicationService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"  # Configure as needed
        self.smtp_port = 587
        self.email_user = os.getenv("PROVIDER_EMAIL_USER")
        self.email_password = os.getenv("PROVIDER_EMAIL_PASSWORD")
    
    async def generate_adherence_report(self, provider_id: str, patient_id: str = None) -> Dict[str, Any]:
        """Generate comprehensive adherence report for provider"""
        try:
            # Mock data - in production, fetch from database
            adherence_data = self._get_mock_adherence_data(provider_id, patient_id)
            
            report = {
                "provider_id": provider_id,
                "report_date": datetime.utcnow().isoformat(),
                "summary": {
                    "total_patients": len(adherence_data),
                    "average_adherence": sum(p["adherence_percentage"] for p in adherence_data) / len(adherence_data),
                    "patients_above_80_percent": len([p for p in adherence_data if p["adherence_percentage"] >= 80]),
                    "patients_below_50_percent": len([p for p in adherence_data if p["adherence_percentage"] < 50])
                },
                "patient_details": adherence_data,
                "alerts": self._generate_adherence_alerts(adherence_data),
                "recommendations": self._generate_adherence_recommendations(adherence_data)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating adherence report: {e}")
            return {"error": "Failed to generate adherence report"}
    
    async def track_medication_effectiveness(self, provider_id: str, patient_id: str, medication_id: str) -> Dict[str, Any]:
        """Track medication effectiveness for provider review"""
        try:
            # Mock effectiveness data
            effectiveness_data = {
                "patient_id": patient_id,
                "medication_id": medication_id,
                "medication_name": "Metformin",
                "condition": "Type 2 Diabetes",
                "effectiveness_metrics": {
                    "patient_reported_score": 8.5,  # 1-10 scale
                    "symptom_improvement": 75,  # percentage
                    "quality_of_life_score": 7.8,
                    "side_effects_severity": "mild"
                },
                "clinical_markers": {
                    "hba1c_improvement": -0.8,  # percentage points
                    "fasting_glucose_change": -25,  # mg/dL
                    "weight_change": -3.2,  # kg
                    "bp_systolic_change": -8  # mmHg
                },
                "timeline": [
                    {
                        "date": "2024-01-01",
                        "event": "Started medication",
                        "notes": "Initial prescription"
                    },
                    {
                        "date": "2024-01-15",
                        "event": "First follow-up",
                        "notes": "Patient reports mild nausea, improving glucose levels"
                    },
                    {
                        "date": "2024-02-01",
                        "event": "Dosage adjustment",
                        "notes": "Increased to 1000mg twice daily"
                    }
                ],
                "provider_assessment": {
                    "effectiveness_rating": "highly_effective",
                    "continue_medication": True,
                    "dosage_adjustment": "maintain_current",
                    "next_review_date": "2024-03-01",
                    "notes": "Excellent response to medication with minimal side effects"
                }
            }
            
            return effectiveness_data
            
        except Exception as e:
            logger.error(f"Error tracking medication effectiveness: {e}")
            return {"error": "Failed to track effectiveness"}
    
    async def monitor_side_effects(self, provider_id: str, patient_id: str = None) -> Dict[str, Any]:
        """Monitor and report side effects to provider"""
        try:
            side_effects_data = self._get_mock_side_effects_data(provider_id, patient_id)
            
            report = {
                "provider_id": provider_id,
                "monitoring_date": datetime.utcnow().isoformat(),
                "summary": {
                    "total_reports": len(side_effects_data),
                    "severe_reactions": len([s for s in side_effects_data if s["severity"] == "severe"]),
                    "pending_review": len([s for s in side_effects_data if not s["provider_reviewed"]]),
                    "common_side_effects": self._analyze_common_side_effects(side_effects_data)
                },
                "recent_reports": side_effects_data[:10],  # Most recent 10
                "severity_breakdown": {
                    "severe": len([s for s in side_effects_data if s["severity"] == "severe"]),
                    "moderate": len([s for s in side_effects_data if s["severity"] == "moderate"]),
                    "mild": len([s for s in side_effects_data if s["severity"] == "mild"])
                },
                "action_required": [s for s in side_effects_data if s["severity"] == "severe" and not s["provider_reviewed"]]
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error monitoring side effects: {e}")
            return {"error": "Failed to monitor side effects"}
    
    async def send_provider_notification(self, provider_email: str, notification_type: str, data: Dict[str, Any]) -> bool:
        """Send email notification to provider"""
        try:
            subject, body = self._generate_email_content(notification_type, data)
            
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = provider_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email (mock implementation)
            logger.info(f"Email notification sent to {provider_email}: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending provider notification: {e}")
            return False
    
    async def get_emergency_contacts(self, patient_id: str) -> Dict[str, Any]:
        """Get emergency contacts for patient"""
        return {
            "patient_id": patient_id,
            "emergency_contacts": [
                {
                    "id": "ec_001",
                    "name": "Dr. Sarah Johnson",
                    "role": "Primary Care Physician",
                    "phone": "+1-555-0123",
                    "email": "dr.johnson@healthclinic.com",
                    "priority": 1,
                    "available_hours": "Mon-Fri 9AM-5PM",
                    "after_hours_phone": "+1-555-0124"
                },
                {
                    "id": "ec_002",
                    "name": "Emergency Contact - Spouse",
                    "role": "Family Emergency Contact",
                    "phone": "+1-555-0125",
                    "email": "spouse@email.com",
                    "priority": 2,
                    "available_hours": "24/7",
                    "relationship": "spouse"
                },
                {
                    "id": "ec_003",
                    "name": "City General Hospital",
                    "role": "Emergency Department",
                    "phone": "+1-555-0911",
                    "email": "emergency@citygeneral.com",
                    "priority": 3,
                    "available_hours": "24/7",
                    "address": "123 Medical Center Drive"
                }
            ],
            "emergency_protocols": {
                "severe_reaction": "Call primary care physician immediately, if unavailable call emergency services",
                "missed_doses": "Contact primary care physician within 24 hours",
                "side_effects": "Document and report to physician at next appointment or sooner if severe"
            }
        }
    
    def _get_mock_adherence_data(self, provider_id: str, patient_id: str = None) -> List[Dict[str, Any]]:
        """Mock adherence data for testing"""
        patients = [
            {
                "patient_id": "patient_001",
                "patient_name": "John Smith",
                "medication_count": 3,
                "adherence_percentage": 95.5,
                "missed_doses_week": 1,
                "medications": [
                    {
                        "medication_id": "med_001",
                        "name": "Metformin",
                        "adherence": 98.0,
                        "last_taken": "2024-01-16 08:00",
                        "doses_missed_week": 0
                    },
                    {
                        "medication_id": "med_002",
                        "name": "Lisinopril",
                        "adherence": 93.0,
                        "last_taken": "2024-01-16 09:00",
                        "doses_missed_week": 1
                    }
                ]
            },
            {
                "patient_id": "patient_002",
                "patient_name": "Mary Johnson",
                "medication_count": 2,
                "adherence_percentage": 87.3,
                "missed_doses_week": 2,
                "medications": [
                    {
                        "medication_id": "med_003",
                        "name": "Atorvastatin",
                        "adherence": 90.0,
                        "last_taken": "2024-01-16 10:00",
                        "doses_missed_week": 1
                    }
                ]
            }
        ]
        
        if patient_id:
            return [p for p in patients if p["patient_id"] == patient_id]
        return patients
    
    def _get_mock_side_effects_data(self, provider_id: str, patient_id: str = None) -> List[Dict[str, Any]]:
        """Mock side effects data for testing"""
        side_effects = [
            {
                "id": "se_001",
                "patient_id": "patient_001",
                "patient_name": "John Smith",
                "medication_id": "med_001",
                "medication_name": "Metformin",
                "side_effect": "Mild nausea after meals",
                "severity": "mild",
                "reported_date": "2024-01-15T10:30:00Z",
                "provider_reviewed": True,
                "provider_response": "Normal side effect, should improve with time. Take with food."
            },
            {
                "id": "se_002",
                "patient_id": "patient_002",
                "patient_name": "Mary Johnson",
                "medication_id": "med_003",
                "medication_name": "Atorvastatin",
                "side_effect": "Muscle aches in legs",
                "severity": "moderate",
                "reported_date": "2024-01-16T14:20:00Z",
                "provider_reviewed": False,
                "provider_response": None
            }
        ]
        
        if patient_id:
            return [s for s in side_effects if s["patient_id"] == patient_id]
        return side_effects
    
    def _generate_adherence_alerts(self, adherence_data: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate adherence alerts for provider attention"""
        alerts = []
        
        for patient in adherence_data:
            if patient["adherence_percentage"] < 50:
                alerts.append({
                    "type": "critical",
                    "patient": patient["patient_name"],
                    "message": f"Critical adherence issue: {patient['adherence_percentage']:.1f}%",
                    "action": "Immediate intervention required"
                })
            elif patient["adherence_percentage"] < 80:
                alerts.append({
                    "type": "warning",
                    "patient": patient["patient_name"],
                    "message": f"Low adherence: {patient['adherence_percentage']:.1f}%",
                    "action": "Follow-up recommended"
                })
        
        return alerts
    
    def _generate_adherence_recommendations(self, adherence_data: List[Dict[str, Any]]) -> List[str]:
        """Generate adherence improvement recommendations"""
        recommendations = []
        
        low_adherence_count = len([p for p in adherence_data if p["adherence_percentage"] < 80])
        
        if low_adherence_count > 0:
            recommendations.extend([
                "Consider medication adherence counseling for low-adherence patients",
                "Review medication schedules and simplify if possible",
                "Implement reminder systems (apps, pill organizers)",
                "Address potential side effects causing non-adherence"
            ])
        
        recommendations.extend([
            "Regular follow-up appointments to monitor adherence",
            "Patient education about medication importance",
            "Coordination with pharmacy for adherence monitoring"
        ])
        
        return recommendations
    
    def _analyze_common_side_effects(self, side_effects_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze common side effects across patients"""
        effect_counts = {}
        
        for effect in side_effects_data:
            effect_name = effect["side_effect"]
            if effect_name not in effect_counts:
                effect_counts[effect_name] = {
                    "count": 0,
                    "medications": set(),
                    "severity_counts": {"mild": 0, "moderate": 0, "severe": 0}
                }
            
            effect_counts[effect_name]["count"] += 1
            effect_counts[effect_name]["medications"].add(effect["medication_name"])
            effect_counts[effect_name]["severity_counts"][effect["severity"]] += 1
        
        # Convert to list and sort by frequency
        common_effects = []
        for effect, data in effect_counts.items():
            if data["count"] >= 2:  # Only include effects reported 2+ times
                common_effects.append({
                    "side_effect": effect,
                    "frequency": data["count"],
                    "medications": list(data["medications"]),
                    "severity_distribution": data["severity_counts"]
                })
        
        return sorted(common_effects, key=lambda x: x["frequency"], reverse=True)
    
    def _generate_email_content(self, notification_type: str, data: Dict[str, Any]) -> tuple:
        """Generate email subject and body for different notification types"""
        if notification_type == "side_effect_alert":
            subject = f"URGENT: Side Effect Report - {data.get('patient_name', 'Patient')}"
            body = f"""
            <html>
            <body>
                <h2>Side Effect Alert</h2>
                <p><strong>Patient:</strong> {data.get('patient_name', 'Unknown')}</p>
                <p><strong>Medication:</strong> {data.get('medication_name', 'Unknown')}</p>
                <p><strong>Side Effect:</strong> {data.get('side_effect', 'Not specified')}</p>
                <p><strong>Severity:</strong> {data.get('severity', 'Unknown')}</p>
                <p><strong>Reported:</strong> {data.get('reported_date', 'Unknown')}</p>
                
                <p>Please review this case and provide guidance to the patient.</p>
                
                <p>Best regards,<br>Healthcare Management System</p>
            </body>
            </html>
            """
        
        elif notification_type == "adherence_alert":
            subject = f"Adherence Alert - {data.get('patient_name', 'Patient')}"
            body = f"""
            <html>
            <body>
                <h2>Medication Adherence Alert</h2>
                <p><strong>Patient:</strong> {data.get('patient_name', 'Unknown')}</p>
                <p><strong>Adherence Rate:</strong> {data.get('adherence_percentage', 0):.1f}%</p>
                <p><strong>Missed Doses (Week):</strong> {data.get('missed_doses_week', 0)}</p>
                
                <p>This patient may benefit from adherence counseling or medication review.</p>
                
                <p>Best regards,<br>Healthcare Management System</p>
            </body>
            </html>
            """
        
        else:
            subject = "Healthcare System Notification"
            body = "<html><body><p>General notification from Healthcare Management System</p></body></html>"
        
        return subject, body

# Global instance
provider_medication_service = ProviderMedicationService()