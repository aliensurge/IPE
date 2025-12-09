import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface Website {
  website_id: number;
  url: string;
  display_name: string;
  monitoring_enabled: boolean;
  check_interval: number;
  defacement_detection_enabled: boolean;
  ssl_monitoring_enabled: boolean;
  created_at: string;
  updated_at: string;
  status?: 'online' | 'warning' | 'offline' | 'unknown';
  ssl_info?: {
    days_until_expiry: number;
    valid_to: string;
  };
  defacement_status?: {
    status: 'clean' | 'defacement_detected' | 'pending' | 'unknown';
    detected_at?: string;
    has_incident: boolean;
  };
  latest_response_time?: number;
  latest_status_code?: number;
}

export interface OverviewStats {
  total: number;
  online: number;
  warning: number;
  offline: number;
}

export const apiService = {
  // Get all websites
  getWebsites: async (): Promise<Website[]> => {
    const response = await api.get('/websites');
    return response.data.data;
  },

  // Get overview statistics
  getOverviewStats: async (): Promise<OverviewStats> => {
    const response = await api.get('/stats/overview');
    return response.data.data;
  },

  // Add a new website
  addWebsite: async (url: string, displayName?: string, checkInterval?: number): Promise<any> => {
    const response = await api.post('/websites', {
      url,
      display_name: displayName,
      check_interval: checkInterval,
    });
    return response.data; // Return full response to access warning
  },

  // Delete a website
  deleteWebsite: async (websiteId: number): Promise<void> => {
    await api.delete(`/websites/${websiteId}`);
  },

  // Trigger manual check
  triggerCheck: async (websiteId: number): Promise<any> => {
    const response = await api.post(`/websites/${websiteId}/check`);
    return response.data.data;
  },

  // Get check history
  getCheckHistory: async (websiteId: number, limit: number = 100): Promise<any[]> => {
    const response = await api.get(`/websites/${websiteId}/checks`, {
      params: { limit },
    });
    return response.data.data;
  },

  // Mark defacement as false positive
  markFalsePositive: async (websiteId: number): Promise<void> => {
    await api.post(`/websites/${websiteId}/defacement/false-positive`);
  },
};

export default api;

