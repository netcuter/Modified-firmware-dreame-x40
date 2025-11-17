import { useState } from 'react';
import { useStore } from '../store';
import { robotApi } from '../api';
import { Play, Square, Pause, Home, MapPin } from 'lucide-react';

export default function RobotControls() {
  const { setError } = useStore();
  const [isLoading, setIsLoading] = useState(false);

  const handleCommand = async (command: () => Promise<any>, successMsg: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await command();
      // Success feedback could be added here
    } catch (err: any) {
      setError(err.message || 'Nie udało się wykonać polecenia');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="card">
      <h2 className="text-lg font-semibold mb-4">Sterowanie</h2>

      <div className="grid grid-cols-2 gap-3">
        <button
          onClick={() => handleCommand(robotApi.startCleaning, 'Rozpoczęto sprzątanie')}
          disabled={isLoading}
          className="btn btn-success flex items-center justify-center space-x-2 disabled:opacity-50"
        >
          <Play className="w-4 h-4" />
          <span>Start</span>
        </button>

        <button
          onClick={() => handleCommand(robotApi.stopCleaning, 'Zatrzymano')}
          disabled={isLoading}
          className="btn btn-danger flex items-center justify-center space-x-2 disabled:opacity-50"
        >
          <Square className="w-4 h-4" />
          <span>Stop</span>
        </button>

        <button
          onClick={() => handleCommand(robotApi.pauseCleaning, 'Wstrzymano')}
          disabled={isLoading}
          className="btn btn-secondary flex items-center justify-center space-x-2 disabled:opacity-50"
        >
          <Pause className="w-4 h-4" />
          <span>Pauza</span>
        </button>

        <button
          onClick={() => handleCommand(robotApi.returnHome, 'Powrót do stacji')}
          disabled={isLoading}
          className="btn btn-primary flex items-center justify-center space-x-2 disabled:opacity-50"
        >
          <Home className="w-4 h-4" />
          <span>Dom</span>
        </button>

        <button
          onClick={() => handleCommand(robotApi.locate, 'Odtwarzanie dźwięku')}
          disabled={isLoading}
          className="btn btn-secondary col-span-2 flex items-center justify-center space-x-2 disabled:opacity-50"
        >
          <MapPin className="w-4 h-4" />
          <span>Zlokalizuj</span>
        </button>
      </div>
    </div>
  );
}
