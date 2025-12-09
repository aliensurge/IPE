import { useState, useEffect } from 'react';
import { Activity, Globe, AlertCircle, CheckCircle, Clock, TrendingUp, Plus, Trash2, RefreshCw, X, Shield } from 'lucide-react';
import { apiService, Website, OverviewStats } from '../services/api';

const WebsiteMonitoringDashboard = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [websites, setWebsites] = useState<Website[]>([]);
  const [stats, setStats] = useState<OverviewStats>({ total: 0, online: 0, warning: 0, offline: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [warning, setWarning] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newWebsiteUrl, setNewWebsiteUrl] = useState('');
  const [newWebsiteName, setNewWebsiteName] = useState('');
  const [addingWebsite, setAddingWebsite] = useState(false);

  // Update current time
  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  // Fetch data from API
  const fetchData = async () => {
    try {
      setError(null);
      const [websitesData, statsData] = await Promise.all([
        apiService.getWebsites(),
        apiService.getOverviewStats(),
      ]);
      
      // Get latest response times for each website
      const websitesWithResponseTime = await Promise.all(
        websitesData.map(async (website) => {
          try {
            // Fetch a few recent checks and pick the latest uptime check
            const checks = await apiService.getCheckHistory(website.website_id, 5);
            const latestUptime = checks.find((c) => c.check_type === 'uptime');

            if (latestUptime) {
              return {
                ...website,
                latest_response_time: latestUptime.response_time,
                latest_status_code: latestUptime.http_status_code,
              };
            }
            return website;
          } catch {
            return website;
          }
        })
      );
      
      setWebsites(websitesWithResponseTime);
      setStats(statsData);

      // Check for defacement alerts
      const defacementAlerts = websitesWithResponseTime.filter(
        w => w.defacement_status?.status === 'defacement_detected'
      );
      if (defacementAlerts.length > 0) {
        const alertMessages = defacementAlerts.map(w => 
          `${w.display_name || w.url} - Defacement detected!`
        );
        setWarning(`Defacement Alert: ${alertMessages.join(', ')}`);
      }
    } catch (err: any) {
      console.error('Error fetching data:', err);
      setError(err.response?.data?.message || 'Failed to connect to API. Make sure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  // Initial load and periodic refresh
  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  // Add website handler
  const handleAddWebsite = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newWebsiteUrl.trim()) {
      setError('Please enter a valid URL');
      return;
    }

    setAddingWebsite(true);
    setError(null);

    try {
      const response = await apiService.addWebsite(newWebsiteUrl.trim(), newWebsiteName.trim() || undefined);
      setNewWebsiteUrl('');
      setNewWebsiteName('');
      setShowAddForm(false);
      
      // Show warning if website was added but is currently down
      if (response.warning) {
        setWarning(response.warning);
        setTimeout(() => setWarning(null), 10000); // Clear after 10 seconds
      }
      
      await fetchData(); // Refresh data
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to add website');
    } finally {
      setAddingWebsite(false);
    }
  };

  // Delete website handler
  const handleDeleteWebsite = async (websiteId: number) => {
    if (!confirm('Are you sure you want to remove this website from monitoring?')) {
      return;
    }

    try {
      await apiService.deleteWebsite(websiteId);
      await fetchData(); // Refresh data
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to delete website');
    }
  };

  // Manual check handler
  const handleManualCheck = async (websiteId: number) => {
    try {
      await apiService.triggerCheck(websiteId);
      await fetchData(); // Refresh data after check
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to trigger check');
    }
  };

  // Mark defacement as false positive handler
  const handleFalsePositive = async (websiteId: number) => {
    if (!confirm('Mark this as a false positive? This will update the baseline to the current content and resolve the defacement alert.')) {
      return;
    }

    try {
      await apiService.markFalsePositive(websiteId);
      await fetchData(); // Refresh data
      setWarning('Baseline updated. Defacement alert resolved.');
      setTimeout(() => setWarning(null), 5000);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Failed to mark as false positive');
    }
  };

  const getStatusColor = (status?: string) => {
    switch (status) {
      case 'online': return 'bg-green-500';
      case 'warning': return 'bg-yellow-500';
      case 'offline': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const getStatusIcon = (status?: string) => {
    switch (status) {
      case 'online': return <CheckCircle className="w-4 h-4" />;
      case 'warning': return <AlertCircle className="w-4 h-4" />;
      case 'offline': return <AlertCircle className="w-4 h-4" />;
      default: return <Clock className="w-4 h-4" />;
    }
  };

  const getDefacementStatusColor = (defacementStatus?: { status: string }) => {
    if (!defacementStatus) return 'bg-gray-500';
    switch (defacementStatus.status) {
      case 'clean': return 'bg-green-500';
      case 'defacement_detected': return 'bg-red-500';
      case 'pending': return 'bg-yellow-500';
      default: return 'bg-gray-500';
    }
  };

  const getDefacementStatusText = (defacementStatus?: { status: string }) => {
    if (!defacementStatus) return 'N/A';
    switch (defacementStatus.status) {
      case 'clean': return 'Clean';
      case 'defacement_detected': return 'Defaced';
      case 'pending': return 'Pending';
      default: return 'Unknown';
    }
  };

  const calculateUptime = (website: Website): number => {
    // Simplified uptime calculation - in real implementation, calculate from check history
    // For now, return a placeholder based on status
    if (website.status === 'online') return 99.5;
    if (website.status === 'warning') return 95.0;
    return 90.0;
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
                <h1 className="text-2xl font-light">WebGuard</h1>
                <p className="text-blue-300 text-sm">Local Security Monitoring Platform</p>
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
        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-900 border border-red-700 text-red-200 px-4 py-3 rounded">
            <div className="flex items-center justify-between">
              <span>{error}</span>
              <button onClick={() => setError(null)} className="text-red-300 hover:text-red-100">
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* Warning Message */}
        {warning && (
          <div className="mb-6 bg-yellow-900 border border-yellow-700 text-yellow-200 px-4 py-3 rounded">
            <div className="flex items-center justify-between">
              <span>{warning}</span>
              <button onClick={() => setWarning(null)} className="text-yellow-300 hover:text-yellow-100">
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* Overview Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-800 border border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm uppercase tracking-wide">Total Sites</p>
                <p className="text-3xl font-light text-white mt-2">
                  {loading ? '...' : stats.total}
                </p>
              </div>
              <Globe className="w-8 h-8 text-blue-500" />
            </div>
          </div>

          <div className="bg-gray-800 border border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm uppercase tracking-wide">Online</p>
                <p className="text-3xl font-light text-green-400 mt-2">
                  {loading ? '...' : stats.online}
                </p>
              </div>
              <CheckCircle className="w-8 h-8 text-green-500" />
            </div>
          </div>

          <div className="bg-gray-800 border border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm uppercase tracking-wide">Warning</p>
                <p className="text-3xl font-light text-yellow-400 mt-2">
                  {loading ? '...' : stats.warning}
                </p>
              </div>
              <AlertCircle className="w-8 h-8 text-yellow-500" />
            </div>
          </div>

          <div className="bg-gray-800 border border-gray-700 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm uppercase tracking-wide">Offline</p>
                <p className="text-3xl font-light text-red-400 mt-2">
                  {loading ? '...' : stats.offline}
                </p>
              </div>
              <AlertCircle className="w-8 h-8 text-red-500" />
            </div>
          </div>
        </div>

        {/* Add Website Form */}
        {showAddForm && (
          <div className="mb-6 bg-gray-800 border border-gray-700 p-6 rounded">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-light">Add New Website</h3>
              <button
                onClick={() => {
                  setShowAddForm(false);
                  setNewWebsiteUrl('');
                  setNewWebsiteName('');
                }}
                className="text-gray-400 hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            <form onSubmit={handleAddWebsite} className="space-y-4">
              <div>
                <label className="block text-sm text-gray-400 mb-2">Website URL *</label>
                <input
                  type="text"
                  value={newWebsiteUrl}
                  onChange={(e) => setNewWebsiteUrl(e.target.value)}
                  placeholder="https://example.com"
                  className="w-full bg-gray-900 border border-gray-700 text-white px-4 py-2 rounded focus:outline-none focus:border-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-2">Display Name (optional)</label>
                <input
                  type="text"
                  value={newWebsiteName}
                  onChange={(e) => setNewWebsiteName(e.target.value)}
                  placeholder="My Website"
                  className="w-full bg-gray-900 border border-gray-700 text-white px-4 py-2 rounded focus:outline-none focus:border-blue-500"
                />
              </div>
              <div className="flex gap-2">
                <button
                  type="submit"
                  disabled={addingWebsite}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded flex items-center space-x-2 disabled:opacity-50"
                >
                  <Plus className="w-4 h-4" />
                  <span>{addingWebsite ? 'Adding...' : 'Add Website'}</span>
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowAddForm(false);
                    setNewWebsiteUrl('');
                    setNewWebsiteName('');
                  }}
                  className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-2 rounded"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Websites Table */}
        <div className="bg-gray-800 border border-gray-700">
          <div className="px-6 py-4 border-b border-gray-700">
            <h2 className="text-xl font-light text-white">Monitored Websites</h2>
            <p className="text-gray-400 text-sm mt-1">Real-time status of your websites</p>
          </div>
          
          {loading ? (
            <div className="px-6 py-8 text-center text-gray-400">Loading...</div>
          ) : websites.length === 0 ? (
            <div className="px-6 py-8 text-center text-gray-400">
              <p>No websites monitored yet.</p>
              <button
                onClick={() => setShowAddForm(true)}
                className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded flex items-center space-x-2 mx-auto"
              >
                <Plus className="w-4 h-4" />
                <span>Add Your First Website</span>
              </button>
            </div>
          ) : (
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
                      Status Code
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      SSL Certificate
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Defacement
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-700">
                  {websites.map((website) => {
                    const uptime = calculateUptime(website);
                    const responseTime = website.latest_response_time || 0;
                    return (
                      <tr key={website.website_id} className="hover:bg-gray-750 transition-colors">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className={`w-2 h-2 rounded-full ${getStatusColor(website.status)} mr-3`}></div>
                            <div className="flex items-center text-gray-300">
                              {getStatusIcon(website.status)}
                              <span className="ml-2 capitalize">{website.status || 'unknown'}</span>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <div>
                            <div className="text-white font-medium">
                              {website.display_name || website.url}
                            </div>
                            <div className="text-blue-400 text-sm">{website.url}</div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`font-mono ${responseTime > 500 ? 'text-red-400' : responseTime > 300 ? 'text-yellow-400' : 'text-green-400'}`}>
                            {responseTime > 0 ? `${responseTime}ms` : '--'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className="font-mono text-gray-300">
                            {website.latest_status_code ?? '--'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          {website.ssl_info ? (
                            <div>
                              <div className={`text-sm ${website.ssl_info.days_until_expiry < 30 ? 'text-yellow-400' : 'text-green-400'}`}>
                                {website.ssl_info.days_until_expiry >= 0 
                                  ? `${website.ssl_info.days_until_expiry} days`
                                  : 'Expired'}
                              </div>
                            </div>
                          ) : (
                            <span className="text-gray-500 text-sm">N/A</span>
                          )}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className={`w-2 h-2 rounded-full ${getDefacementStatusColor(website.defacement_status)} mr-3`}></div>
                            <span className={`text-sm font-medium ${
                              website.defacement_status?.status === 'defacement_detected' 
                                ? 'text-red-400' 
                                : website.defacement_status?.status === 'clean'
                                ? 'text-green-400'
                                : 'text-gray-400'
                            }`}>
                              {getDefacementStatusText(website.defacement_status)}
                            </span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center space-x-2">
                            <button
                              onClick={() => handleManualCheck(website.website_id)}
                              className="text-blue-400 hover:text-blue-300 text-sm border border-blue-500 px-3 py-1 hover:bg-blue-500 hover:bg-opacity-20 transition-colors flex items-center space-x-1"
                              title="Manual Check"
                            >
                              <RefreshCw className="w-3 h-3" />
                              <span>Check</span>
                            </button>
                            {website.defacement_status?.status === 'defacement_detected' && (
                              <button
                                onClick={() => handleFalsePositive(website.website_id)}
                                className="text-yellow-400 hover:text-yellow-300 text-sm border border-yellow-500 px-3 py-1 hover:bg-yellow-500 hover:bg-opacity-20 transition-colors flex items-center space-x-1"
                                title="Mark as False Positive"
                              >
                                <Shield className="w-3 h-3" />
                                <span>False Positive</span>
                              </button>
                            )}
                            <button
                              onClick={() => handleDeleteWebsite(website.website_id)}
                              className="text-red-400 hover:text-red-300 text-sm border border-red-500 px-3 py-1 hover:bg-red-500 hover:bg-opacity-20 transition-colors flex items-center space-x-1"
                              title="Delete"
                            >
                              <Trash2 className="w-3 h-3" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>

        {/* Quick Actions */}
        <div className="mt-8 flex flex-wrap gap-4">
          <button
            onClick={() => setShowAddForm(!showAddForm)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 flex items-center space-x-2 transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span>Add Website</span>
          </button>
          <button
            onClick={fetchData}
            className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-3 flex items-center space-x-2 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Refresh</span>
          </button>
        </div>
      </main>
    </div>
  );
};

export default WebsiteMonitoringDashboard;
