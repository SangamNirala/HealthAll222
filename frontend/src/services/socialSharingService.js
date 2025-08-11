// Social Sharing Service - Handles achievement sharing with privacy compliance
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

class SocialSharingService {
  constructor() {
    this.apiClient = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
    });

    // Add auth token to requests
    this.apiClient.interceptors.request.use((config) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Check browser capabilities
    this.browserCapabilities = {
      webShareAPI: 'share' in navigator,
      notificationsAPI: 'Notification' in window,
      clipboardAPI: 'clipboard' in navigator && navigator.clipboard.writeText
    };
  }

  /**
   * Check if browser supports native sharing
   * @returns {Boolean} True if Web Share API is supported
   */
  supportsNativeSharing() {
    return this.browserCapabilities.webShareAPI;
  }

  /**
   * Check if browser supports notifications
   * @returns {Boolean} True if Notifications API is supported
   */
  supportsNotifications() {
    return this.browserCapabilities.notificationsAPI;
  }

  /**
   * Request notification permissions
   * @returns {Promise<String>} Permission status: 'granted', 'denied', or 'default'
   */
  async requestNotificationPermission() {
    if (!this.supportsNotifications()) {
      return 'denied';
    }

    try {
      const permission = await Notification.requestPermission();
      return permission;
    } catch (error) {
      console.error('Error requesting notification permission:', error);
      return 'denied';
    }
  }

  /**
   * Show browser notification
   * @param {String} title - Notification title
   * @param {String} body - Notification body text
   * @param {Object} options - Additional notification options
   */
  showNotification(title, body, options = {}) {
    if (this.supportsNotifications() && Notification.permission === 'granted') {
      new Notification(title, {
        body: body,
        icon: options.icon || '/favicon.ico',
        badge: options.badge || '/favicon.ico',
        ...options
      });
    }
  }

  /**
   * Prepare achievement for sharing (privacy-compliant)
   * @param {Object} achievement - Achievement to share
   * @param {String} customMessage - Optional custom message
   * @returns {Promise<Object>} Prepared sharing content
   */
  async prepareAchievementShare(achievement, customMessage = '') {
    try {
      // Validate content with backend for HIPAA compliance
      const response = await this.apiClient.post('/api/sharing/validate-sharing-content', {
        achievement_id: achievement.id,
        custom_message: customMessage
      });

      if (!response.data.valid) {
        throw new Error('Content validation failed - privacy concerns detected');
      }

      // Generate shareable content
      const shareContent = {
        title: `🏆 Health Achievement Unlocked: ${achievement.title}`,
        text: customMessage || this.generateDefaultShareText(achievement),
        url: `${window.location.origin}/achievements/${achievement.id}`
      };

      return {
        content: shareContent,
        privacyValidated: true,
        validatedAt: new Date().toISOString()
      };

    } catch (error) {
      console.error('Error preparing achievement share:', error);
      throw error;
    }
  }

  /**
   * Generate default share text for achievement
   * @param {Object} achievement - Achievement data
   * @returns {String} Generated share text
   */
  generateDefaultShareText(achievement) {
    const emojis = {
      FITNESS: '💪',
      NUTRITION: '🥗',
      WELLNESS: '🧘‍♀️',
      LIFESTYLE: '🌟'
    };

    const emoji = emojis[achievement.category] || '🎯';
    
    const baseMessages = [
      `${emoji} Just unlocked "${achievement.title}"! ${achievement.description}`,
      `${emoji} Achievement unlocked: ${achievement.title}! ${achievement.description}`,
      `${emoji} Celebrating my latest milestone: ${achievement.title}! ${achievement.description}`
    ];

    const randomMessage = baseMessages[Math.floor(Math.random() * baseMessages.length)];
    return `${randomMessage} #HealthGoals #Achievement #Progress`;
  }

  /**
   * Share achievement using native Web Share API
   * @param {Object} shareContent - Content to share
   * @returns {Promise<Boolean>} True if sharing was successful
   */
  async shareNatively(shareContent) {
    if (!this.supportsNativeSharing()) {
      throw new Error('Native sharing not supported');
    }

    try {
      await navigator.share(shareContent.content);
      
      // Record successful share
      await this.recordShare('native', shareContent);
      
      return true;
    } catch (error) {
      if (error.name === 'AbortError') {
        // User cancelled - not an error
        return false;
      }
      throw error;
    }
  }

  /**
   * Copy share content to clipboard as fallback
   * @param {Object} shareContent - Content to copy
   * @returns {Promise<Boolean>} True if copying was successful
   */
  async copyToClipboard(shareContent) {
    const textToCopy = `${shareContent.content.text}\n\n${shareContent.content.url}`;

    try {
      if (this.browserCapabilities.clipboardAPI && window.isSecureContext) {
        await navigator.clipboard.writeText(textToCopy);
      } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = textToCopy;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
      }

      // Record successful copy
      await this.recordShare('clipboard', shareContent);
      
      return true;
    } catch (error) {
      console.error('Error copying to clipboard:', error);
      throw error;
    }
  }

  /**
   * Share achievement with automatic fallback
   * @param {Object} achievement - Achievement to share
   * @param {String} customMessage - Optional custom message
   * @returns {Promise<Object>} Share result
   */
  async shareAchievement(achievement, customMessage = '') {
    try {
      // Prepare sharing content
      const shareContent = await this.prepareAchievementShare(achievement, customMessage);

      // Try native sharing first
      if (this.supportsNativeSharing()) {
        try {
          const shared = await this.shareNatively(shareContent);
          if (shared) {
            this.showNotification(
              '🎉 Achievement Shared!',
              `Your "${achievement.title}" achievement has been shared successfully.`
            );
            return { method: 'native', success: true };
          } else {
            return { method: 'native', success: false, cancelled: true };
          }
        } catch (error) {
          console.warn('Native sharing failed, falling back to clipboard:', error);
        }
      }

      // Fallback to clipboard
      await this.copyToClipboard(shareContent);
      return { 
        method: 'clipboard', 
        success: true,
        message: 'Achievement copied to clipboard! You can paste it anywhere to share.'
      };

    } catch (error) {
      console.error('Error sharing achievement:', error);
      return { 
        method: 'none', 
        success: false, 
        error: error.message 
      };
    }
  }

  /**
   * Record sharing action for analytics
   * @param {String} method - Sharing method used
   * @param {Object} shareContent - Content that was shared
   */
  async recordShare(method, shareContent) {
    try {
      await this.apiClient.post('/api/sharing/record-share', {
        sharing_method: method,
        achievement_id: shareContent.achievement_id,
        shared_at: new Date().toISOString(),
        platform: method === 'native' ? 'web_share_api' : 'clipboard'
      });
    } catch (error) {
      // Don't fail sharing if analytics recording fails
      console.warn('Failed to record share:', error);
    }
  }

  /**
   * Get user's sharing history
   * @param {Number} limit - Maximum number of shares to return
   * @returns {Promise<Array>} Array of sharing history items
   */
  async getShareHistory(limit = 10) {
    try {
      const response = await this.apiClient.get(`/api/sharing/history?limit=${limit}`);
      return response.data.shares || [];
    } catch (error) {
      console.error('Error fetching share history:', error);
      return [];
    }
  }

  /**
   * Get sharing statistics
   * @returns {Promise<Object>} Sharing statistics
   */
  async getShareStats() {
    try {
      const response = await this.apiClient.get('/api/sharing/stats');
      return response.data.stats || {
        totalShares: 0,
        platforms: {},
        engagement: { likes: 0, comments: 0 }
      };
    } catch (error) {
      console.error('Error fetching share stats:', error);
      return {
        totalShares: 0,
        platforms: {},
        engagement: { likes: 0, comments: 0 }
      };
    }
  }

  /**
   * Generate shareable achievement image URL
   * @param {Object} achievement - Achievement data
   * @returns {String} Image URL for achievement badge
   */
  generateAchievementImageUrl(achievement) {
    const badgeImages = {
      bronze: 'https://images.unsplash.com/photo-1568749675207-31a7966c48aa?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHw0fHxhY2hpZXZlbWVudCUyMGJhZGdlc3xlbnwwfHx8fDE3NTQ4OTk4OTJ8MA&ixlib=rb-4.1.0&q=85',
      silver: 'https://images.unsplash.com/photo-1572546590745-87c30605415e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwzfHxhY2hpZXZlbWVudCUyMGJhZGdlc3xlbnwwfHx8fDE3NTQ4OTk4OTJ8MA&ixlib=rb-4.1.0&q=85',
      gold: 'https://images.unsplash.com/photo-1577595353464-ac669bc9de95?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2Njl8MHwxfHNlYXJjaHwyfHxhY2hpZXZlbWVudCUyMGJhZGdlc3xlbnwwfHx8fDE3NTQ4OTk4OTJ8MA&ixlib=rb-4.1.0&q=85',
      diamond: 'https://images.unsplash.com/photo-1560257777-820fccc5ee0c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwxfHxoZWFsdGglMjBtaWxlc3RvbmVzfGVufDB8fHx8MTc1NDg5OTkwN3ww&ixlib=rb-4.1.0&q=85'
    };

    return badgeImages[achievement.badge_type] || badgeImages.bronze;
  }
}

// Export singleton instance
export default new SocialSharingService();