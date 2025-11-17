import { useState } from 'react';
import { useStore } from '../store';
import { aiApi } from '../api';
import { Cpu, Globe, Wifi } from 'lucide-react';

const MODEL_LABELS: Record<string, string> = {
  local: 'Lokalny (LM Studio)',
  openai: 'OpenAI GPT',
  anthropic: 'Anthropic Claude',
  google: 'Google Gemini',
};

const MODEL_ICONS: Record<string, any> = {
  local: Cpu,
  openai: Globe,
  anthropic: Globe,
  google: Globe,
};

export default function ModelSwitcher() {
  const { currentModel, availableModels, setCurrentModel, setError } = useStore();
  const [isLoading, setIsLoading] = useState(false);

  const handleSwitch = async (model: string) => {
    if (model === currentModel) return;

    setIsLoading(true);
    setError(null);

    try {
      await aiApi.switchModel(model);
      setCurrentModel(model);
    } catch (err: any) {
      setError(err.message || 'Nie udało się przełączyć modelu');
    } finally {
      setIsLoading(false);
    }
  };

  const Icon = MODEL_ICONS[currentModel] || Cpu;
  const isOnline = currentModel !== 'local';

  return (
    <div className="card">
      <h2 className="text-lg font-semibold mb-4 flex items-center">
        <Icon className="w-5 h-5 mr-2" />
        Model AI
      </h2>

      {/* Current model */}
      <div className="mb-4 p-3 bg-gray-700 rounded-lg">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-400">Aktywny model</p>
            <p className="font-medium">{MODEL_LABELS[currentModel] || currentModel}</p>
          </div>
          <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs ${
            isOnline ? 'bg-blue-900/30 text-blue-400' : 'bg-green-900/30 text-green-400'
          }`}>
            {isOnline ? <Globe className="w-3 h-3" /> : <Wifi className="w-3 h-3" />}
            <span>{isOnline ? 'Online' : 'Local'}</span>
          </div>
        </div>
      </div>

      {/* Model selector */}
      <div className="space-y-2">
        <p className="text-sm text-gray-400 mb-2">Przełącz na:</p>
        {availableModels.map((model) => {
          const ModelIcon = MODEL_ICONS[model] || Cpu;
          const isActive = model === currentModel;
          const modelIsOnline = model !== 'local';

          return (
            <button
              key={model}
              onClick={() => handleSwitch(model)}
              disabled={isActive || isLoading}
              className={`w-full p-3 rounded-lg border transition-colors text-left ${
                isActive
                  ? 'border-dreame-500 bg-dreame-900/30'
                  : 'border-gray-600 hover:border-gray-500 hover:bg-gray-700/50'
              } disabled:opacity-50 disabled:cursor-not-allowed`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <ModelIcon className="w-5 h-5" />
                  <span className="font-medium">{MODEL_LABELS[model] || model}</span>
                </div>
                <div className={`text-xs px-2 py-1 rounded-full ${
                  modelIsOnline ? 'bg-blue-900/30 text-blue-400' : 'bg-green-900/30 text-green-400'
                }`}>
                  {modelIsOnline ? 'Online' : 'Local'}
                </div>
              </div>
            </button>
          );
        })}
      </div>

      {availableModels.length === 0 && (
        <p className="text-sm text-gray-400 text-center py-4">
          Brak dostępnych modeli
        </p>
      )}
    </div>
  );
}
