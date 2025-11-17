import { useStore } from '../store';
import { Battery, Activity, AlertTriangle } from 'lucide-react';

const STATE_LABELS: Record<string, string> = {
  'cleaning': 'Sprzątam',
  'docked': 'Na stacji',
  'idle': 'Bezczynny',
  'returning': 'Wracam do stacji',
  'paused': 'Wstrzymany',
  'error': 'Błąd',
};

export default function RobotStatus() {
  const { robotStatus } = useStore();

  if (!robotStatus) {
    return (
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Status Robota</h2>
        <p className="text-gray-400">Ładowanie...</p>
      </div>
    );
  }

  const getBatteryColor = (level: number) => {
    if (level >= 80) return 'text-green-400';
    if (level >= 50) return 'text-yellow-400';
    if (level >= 20) return 'text-orange-400';
    return 'text-red-400';
  };

  const getStateColor = (state: string) => {
    if (state === 'cleaning') return 'text-blue-400';
    if (state === 'error') return 'text-red-400';
    if (state === 'docked') return 'text-green-400';
    return 'text-gray-400';
  };

  return (
    <div className="card">
      <h2 className="text-lg font-semibold mb-4 flex items-center">
        <Activity className="w-5 h-5 mr-2" />
        Status Robota
      </h2>

      <div className="space-y-4">
        {/* State */}
        <div className="flex items-center justify-between">
          <span className="text-gray-400">Stan:</span>
          <span className={`font-medium ${getStateColor(robotStatus.state)}`}>
            {STATE_LABELS[robotStatus.state] || robotStatus.state}
          </span>
        </div>

        {/* Battery */}
        <div className="flex items-center justify-between">
          <span className="text-gray-400">Bateria:</span>
          <div className="flex items-center space-x-2">
            <Battery className={`w-5 h-5 ${getBatteryColor(robotStatus.battery)}`} />
            <span className={`font-medium ${getBatteryColor(robotStatus.battery)}`}>
              {robotStatus.battery}%
            </span>
          </div>
        </div>

        {/* Battery bar */}
        <div className="w-full bg-gray-700 rounded-full h-2">
          <div
            className={`h-2 rounded-full transition-all ${
              robotStatus.battery >= 80 ? 'bg-green-500' :
              robotStatus.battery >= 50 ? 'bg-yellow-500' :
              robotStatus.battery >= 20 ? 'bg-orange-500' : 'bg-red-500'
            }`}
            style={{ width: `${robotStatus.battery}%` }}
          />
        </div>

        {/* Error */}
        {robotStatus.error && (
          <div className="mt-4 p-3 bg-red-900/30 border border-red-800 rounded-lg">
            <div className="flex items-start space-x-2">
              <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="text-sm font-medium text-red-400">Błąd</p>
                <p className="text-sm text-red-300">{robotStatus.error}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
