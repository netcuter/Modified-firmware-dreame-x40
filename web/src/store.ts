import { create } from 'zustand';
import { RobotStatus, ChatMessage } from './api';

interface AppState {
  // Robot state
  robotStatus: RobotStatus | null;
  setRobotStatus: (status: RobotStatus) => void;

  // AI state
  currentModel: string;
  availableModels: string[];
  setCurrentModel: (model: string) => void;
  setAvailableModels: (models: string[]) => void;

  // Chat state
  messages: ChatMessage[];
  addMessage: (message: ChatMessage) => void;
  clearMessages: () => void;

  // UI state
  isChatLoading: boolean;
  setIsChatLoading: (loading: boolean) => void;
  error: string | null;
  setError: (error: string | null) => void;
}

export const useStore = create<AppState>((set) => ({
  // Robot state
  robotStatus: null,
  setRobotStatus: (status) => set({ robotStatus: status }),

  // AI state
  currentModel: 'local',
  availableModels: [],
  setCurrentModel: (model) => set({ currentModel: model }),
  setAvailableModels: (models) => set({ availableModels: models }),

  // Chat state
  messages: [],
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  clearMessages: () => set({ messages: [] }),

  // UI state
  isChatLoading: false,
  setIsChatLoading: (loading) => set({ isChatLoading: loading }),
  error: null,
  setError: (error) => set({ error }),
}));
