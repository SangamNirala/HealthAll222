// Profile API utility functions
const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || '';

class ProfileAPI {
  // Generic API call method
  static async apiCall(endpoint, method = 'GET', data = null) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    if (data) {
      config.body = JSON.stringify(data);
    }

    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      
      // Handle different types of errors more gracefully
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      
      if (errorData.detail) {
        if (typeof errorData.detail === 'string') {
          errorMessage = errorData.detail;
        } else if (Array.isArray(errorData.detail)) {
          // Handle validation errors from FastAPI
          const validationErrors = errorData.detail.map(err => {
            if (err.msg && err.loc) {
              return `${err.loc.join('.')}: ${err.msg}`;
            }
            return err.msg || 'Validation error';
          });
          errorMessage = validationErrors.join(', ');
        } else {
          errorMessage = 'Validation error - please check required fields';
        }
      }
      
      throw new Error(errorMessage);
    }

    return response.json();
  }

  // Patient Profile API
  static async createPatientProfile(profileData) {
    return this.apiCall('/api/profiles/patient', 'POST', profileData);
  }

  static async getPatientProfile(userId) {
    return this.apiCall(`/api/profiles/patient/${userId}`);
  }

  static async updatePatientProfile(userId, updateData) {
    return this.apiCall(`/api/profiles/patient/${userId}`, 'PUT', updateData);
  }

  static async deletePatientProfile(userId) {
    return this.apiCall(`/api/profiles/patient/${userId}`, 'DELETE');
  }

  // Provider Profile API
  static async createProviderProfile(profileData) {
    return this.apiCall('/api/profiles/provider', 'POST', profileData);
  }

  static async getProviderProfile(userId) {
    return this.apiCall(`/api/profiles/provider/${userId}`);
  }

  static async updateProviderProfile(userId, updateData) {
    return this.apiCall(`/api/profiles/provider/${userId}`, 'PUT', updateData);
  }

  static async deleteProviderProfile(userId) {
    return this.apiCall(`/api/profiles/provider/${userId}`, 'DELETE');
  }

  // Family Profile API
  static async createFamilyProfile(profileData) {
    return this.apiCall('/api/profiles/family', 'POST', profileData);
  }

  static async getFamilyProfile(userId) {
    return this.apiCall(`/api/profiles/family/${userId}`);
  }

  static async updateFamilyProfile(userId, updateData) {
    return this.apiCall(`/api/profiles/family/${userId}`, 'PUT', updateData);
  }

  static async deleteFamilyProfile(userId) {
    return this.apiCall(`/api/profiles/family/${userId}`, 'DELETE');
  }

  // Guest Profile API
  static async createGuestProfile(profileData) {
    return this.apiCall('/api/profiles/guest', 'POST', profileData);
  }

  static async getGuestProfile(sessionId) {
    return this.apiCall(`/api/profiles/guest/${sessionId}`);
  }

  static async deleteGuestProfile(sessionId) {
    return this.apiCall(`/api/profiles/guest/${sessionId}`, 'DELETE');
  }

  // Profile Completion API
  static async getProfileCompletion(userId, role) {
    return this.apiCall(`/api/profiles/completion/${userId}?role=${role}`);
  }
}

export default ProfileAPI;