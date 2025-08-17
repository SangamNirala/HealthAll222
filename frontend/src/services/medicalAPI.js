/**
 * Medical AI API Service
 * Handles communication with the backend medical AI consultation system
 */

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

class MedicalAPIService {
  constructor() {
    this.baseURL = `${API_BASE_URL}/api/medical-ai`;
  }

  /**
   * Initialize a new medical consultation session
   */
  async initializeConsultation(params = {}) {
    try {
      const response = await fetch(`${this.baseURL}/initialize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          patient_id: params.patient_id || 'anonymous',
          demographics: params.demographics || {}
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        consultation: { id: data.consultation_id },
        response: data.response,
        context: data.context,
        stage: data.stage,
        urgency: data.urgency,
        emergency_detected: data.emergency_detected,
        next_questions: data.next_questions || []
      };
    } catch (error) {
      console.error('Failed to initialize consultation:', error);
      throw error;
    }
  }

  /**
   * Process a patient message in the medical consultation
   */
  async processMessage(params) {
    try {
      const response = await fetch(`${this.baseURL}/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: params.message,
          consultation_id: params.consultation_id,
          context: params.context,
          patient_id: params.patient_id || 'anonymous'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        response: data.response,
        context: data.context,
        stage: data.stage,
        urgency: data.urgency,
        consultation_id: data.consultation_id,
        emergency_detected: data.emergency_detected,
        next_questions: data.next_questions || [],
        differential_diagnoses: data.differential_diagnoses || [],
        recommendations: data.recommendations || [],
        clinical_reasoning: data.clinical_reasoning
      };
    } catch (error) {
      console.error('Failed to process message:', error);
      throw error;
    }
  }

  /**
   * Generate a professional medical report from the consultation
   */
  async generateMedicalReport(params) {
    try {
      const response = await fetch(`${this.baseURL}/report`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          consultation_id: params.consultation_id,
          messages: params.messages,
          context: params.context
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        report: {
          id: data.report_id,
          soap_note: data.soap_note,
          summary: data.summary,
          recommendations: data.recommendations,
          generated_at: data.generated_at
        }
      };
    } catch (error) {
      console.error('Failed to generate medical report:', error);
      throw error;
    }
  }

  /**
   * Check service health
   */
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/status`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
}

// Create and export singleton instance
export const medicalAPI = new MedicalAPIService();
export default medicalAPI;