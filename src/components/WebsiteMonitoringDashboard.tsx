import { useState, useEffect } from 'react';
import { Activity, Globe, AlertCircle, CheckCircle, Clock, TrendingUp } from 'lucide-react';

const WebsiteMonitoringDashboard = () => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Sample monitoring data
  const websites = [
    { id: 1, name: 'Main Website', url: 'https://example.com', status: 'online', responseTime: 245, uptime: 99.9 },
    { id: 2, name: 'API Gateway', url: 'https://api.example.com', status: 'online', responseTime: 180, uptime: 99.7 },
    { id: 3, name: 'Admin Panel', url: 'https://admin.example.com', status: 'warning', responseTime: 890, uptime: 98.2 },
    { id: 4, name: 'Documentation', url: 'https://docs.example.com', status: 'offline', responseTime: 0, uptime: 95.1 },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return 'bg-green-500';
      case 'warning': return 'bg-yellow-500';
      case 'offline': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'online': return <CheckCircle className="w-4 h-4" />;
      case 'warning': return <AlertCircle className="w-4 h-4" />;
      case 'offline': return <AlertCircle className="w-4 h-4" />;
      default: return <Clock className="w-4 h-4" />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-black border-b border-blue-500">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-8 h-8 bg-blue-500 flex items-center justify-center">
                <Activity className="w-5 h-5" />
              </div>
              <div>
                <h1 className="text-2xl font-light">Website Monitor</h1>
                <p className="text-blue-300 text-sm">Real-time monitoring dashboard</p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-400">Current Time</div>
              <div className="font-mono text-blue-300">
                {currentTime.toLocaleTimeString()}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {/* Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-800 border border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm uppercase tracking-wide">Total Sites</p>
                <p className="text-3xl font-light text-white mt-2">4</p>
              </div>
              <Globe className="w-8 h-8 text-blue-500" />
            </div>
          </div>

          <div className="bg-gray-800 border border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm uppercase tracking-wide">Online</p>
                <p className="text-3xl font-light text-green-400 mt-2">2</p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-500" />
            </div>
          </div>

          <div className="bg-gray-800 border border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm uppercase tracking-wide">Warning</p>
                <p className="text-3xl font-light text-yellow-400 mt-2">1</p>
              </div>
              <AlertCircle className="w-8 h-8 text-yellow-500" />
            </div>
          </div>

          <div className="bg-gray-800 border border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm uppercase tracking-wide">Offline</p>
                <p className="text-3xl font-light text-red-400 mt-2">1</p>
              </div>
              <AlertCircle className="w-8 h-8 text-red-500" />
            </div>
          </div>
        </div>

        {/* Websites Table */}
        <div className="bg-gray-800 border border-gray-700">
          <div className="px-6 py-4 border-b border-gray-700">
            <h2 className="text-xl font-light text-white">Monitored Websites</h2>
            <p className="text-gray-400 text-sm mt-1">Real-time status of your websites</p>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-900">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Website
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Response Time
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Uptime
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-700">
                {websites.map((site) => (
                  <tr key={site.id} className="hover:bg-gray-750 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className={`w-2 h-2 rounded-full ${getStatusColor(site.status)} mr-3`}></div>
                        <div className="flex items-center text-gray-300">
                          {getStatusIcon(site.status)}
                          <span className="ml-2 capitalize">{site.status}</span>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div>
                        <div className="text-white font-medium">{site.name}</div>
                        <div className="text-blue-400 text-sm">{site.url}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`font-mono ${site.responseTime > 500 ? 'text-red-400' : site.responseTime > 300 ? 'text-yellow-400' : 'text-green-400'}`}>
                        {site.responseTime > 0 ? `${site.responseTime}ms` : '--'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="flex-1 bg-gray-700 h-2 rounded-full mr-3">
                          <div 
                            className={`h-2 rounded-full ${site.uptime > 99 ? 'bg-green-500' : site.uptime > 95 ? 'bg-yellow-500' : 'bg-red-500'}`}
                            style={{ width: `${site.uptime}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-mono text-gray-300">{site.uptime}%</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button className="text-blue-400 hover:text-blue-300 text-sm border border-blue-500 px-3 py-1 hover:bg-blue-500 hover:bg-opacity-20 transition-colors">
                        View Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 flex flex-wrap gap-4">
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 flex items-center space-x-2 transition-colors">
            <Globe className="w-4 h-4" />
            <span>Add Website</span>
          </button>
          <button className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-3 flex items-center space-x-2 transition-colors">
            <TrendingUp className="w-4 h-4" />
            <span>View Analytics</span>
          </button>
          <button className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-3 flex items-center space-x-2 transition-colors">
            <Activity className="w-4 h-4" />
            <span>System Health</span>
          </button>
        </div>
      </main>
    </div>
  );
};

export default WebsiteMonitoringDashboard;

