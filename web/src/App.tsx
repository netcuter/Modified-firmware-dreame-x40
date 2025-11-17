import { useEffect, useState } from 'react';
import { useStore } from './store';
import { robotApi, aiApi, healthApi } from './api';
import ChatInterface from './components/ChatInterface';
import RobotStatus from './components/RobotStatus';
import RobotControls from './components/RobotControls';
import ModelSwitcher from './components/ModelSwitcher';
import { Activity, AlertCircle } from 'lucide-react';

function App() {
  const { setRobotStatus, setCurrentModel, setAvailableModels, setError, error } = useStore();
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Initial setup
  useEffect(() => {
    const initialize = async () => {
      try {
        // Check health
        const healthRes = await healthApi.check();
        setIsConnected(healthRes.data.status === 'healthy');

        // Get robot status
        const statusRes = await robotApi.getStatus();
        setRobotStatus(statusRes.data);

        // Get AI models
        const modelsRes = await aiApi.getModels();
        setCurrentModel(modelsRes.data.current);
        setAvailableModels(modelsRes.data.available);

        setIsLoading(false);
      } catch (err: any) {
        setError(err.message || 'Failed to connect to server');
        setIsLoading(false);
      }
    };

    initialize();

    // Poll robot status every 5 seconds
    const interval = setInterval(async () => {
      try {
        const statusRes = await robotApi.getStatus();
        setRobotStatus(statusRes.data);
      } catch (err) {
        // Silent fail for polling
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [setRobotStatus, setCurrentModel, setAvailableModels, setError]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <Activity className="w-12 h-12 text-dreame-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-400">Łączenie z Dreame X40...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Activity className="w-8 h-8 text-dreame-500" />
            <div>
              <h1 className="text-xl font-bold">Dreame X40 AI Assistant</h1>
              <p className="text-sm text-gray-400">Valetudo + AI Integration</p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className={`flex items-center space-x-2 px-3 py-1 rounded-full ${
              isConnected ? 'bg-green-900/30 text-green-400' : 'bg-red-900/30 text-red-400'
            }`}>
              <div className={`w-2 h-2 rounded-full ${
                isConnected ? 'bg-green-400' : 'bg-red-400'
              }`} />
              <span className="text-sm">{isConnected ? 'Połączono' : 'Rozłączono'}</span>
            </div>
          </div>
        </div>
      </header>

      {/* Error banner */}
      {error && (
        <div className="bg-red-900/30 border-b border-red-800 px-6 py-3">
          <div className="max-w-7xl mx-auto flex items-center space-x-3">
            <AlertCircle className="w-5 h-5 text-red-400" />
            <p className="text-red-400">{error}</p>
            <button
              onClick={() => setError(null)}
              className="ml-auto text-red-400 hover:text-red-300"
            >
              ✕
            </button>
          </div>
        </div>
      )}

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-6 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left column - Robot status and controls */}
          <div className="space-y-6">
            <RobotStatus />
            <RobotControls />
            <ModelSwitcher />
          </div>

          {/* Right column - Chat interface */}
          <div className="lg:col-span-2">
            <ChatInterface />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 border-t border-gray-700 px-6 py-4 mt-8">
        <div className="max-w-7xl mx-auto text-center text-sm text-gray-400">
          <p>Dreame X40 AI Assistant v1.0.0 | Powered by Valetudo</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
