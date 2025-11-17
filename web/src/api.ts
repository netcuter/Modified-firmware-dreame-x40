import axios from 'axios';

const API_BASE = '/api/v1';

export interface RobotStatus {
  state: string;
  battery: number;
  error?: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export interface ChatResponse {
  response: string;
  model_used: string;
  intent?: string;
}

export interface ModelInfo {
  current: string;
  available: string[];
}

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
});

// Robot endpoints
export const robotApi = {
  getStatus: () => api.get<RobotStatus>('/robot/status'),
  getInfo: () => api.get('/robot/info'),
  getCapabilities: () => api.get('/robot/capabilities'),
  startCleaning: () => api.post('/robot/start'),
  stopCleaning: () => api.post('/robot/stop'),
  pauseCleaning: () => api.post('/robot/pause'),
  returnHome: () => api.post('/robot/home'),
  locate: () => api.post('/robot/locate'),
};

// AI endpoints
export const aiApi = {
  chat: (message: string, includeContext = true) =>
    api.post<ChatResponse>('/chat', { message, include_context: includeContext }),
  getModels: () => api.get<ModelInfo>('/ai/models'),
  switchModel: (model: string) => api.post('/ai/switch-model', { model }),
  clearHistory: () => api.post('/ai/clear-history'),
  getHistory: () => api.get<ChatMessage[]>('/ai/history'),
};

// Health check
export const healthApi = {
  check: () => api.get('/health'),
};

export default api;
