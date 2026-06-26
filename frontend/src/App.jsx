import { useState, useEffect } from 'react'
import axios from 'axios'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const API_BASE = 'http://127.0.0.1:8000'

function App() {
  const [logs, setLogs] = useState([])
  const [alerts, setAlerts] = useState([])
  const [history, setHistory] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchData = async () => {
    try {
      const [logsRes, alertsRes, historyRes] = await Promise.all([
        axios.get(`${API_BASE}/logs/?limit=10`),
        axios.get(`${API_BASE}/alerts/?limit=10`),
        axios.get(`${API_BASE}/anomaly/history`)
      ])
      setLogs(logsRes.data.logs)
      setAlerts(alertsRes.data.alerts)

      const chartData = historyRes.data.map(item => ({
        time: new Date(item.timestamp).toLocaleTimeString(),
        score: item.anomaly_score,
        service: item.service_name,
        isAnomaly: item.is_anomaly
      }))
      setHistory(chartData)
      setLoading(false)
    } catch (err) {
      console.error('Failed to fetch data:', err)
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 10000)
    return () => clearInterval(interval)
  }, [])

  const levelColor = {
    ERROR: 'text-red-400 bg-red-950',
    WARN: 'text-amber-400 bg-amber-950',
    INFO: 'text-gray-400 bg-gray-800'
  }

  const severityColor = {
    critical: 'bg-red-600',
    warning: 'bg-amber-600',
    info: 'bg-blue-600'
  }

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 p-6">
      <header className="mb-6">
        <h1 className="text-2xl font-bold">Log Anomaly Detector</h1>
        <p className="text-gray-400 text-sm">Real-time log monitoring and ML-powered anomaly detection</p>
      </header>

      {loading ? (
        <p className="text-gray-400">Loading...</p>
      ) : (
        <>
          <section className="bg-gray-900 rounded-lg p-4 mb-6">
            <h2 className="text-lg font-semibold mb-3">Anomaly Score Over Time</h2>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis
                  dataKey="time"
                  stroke="#9ca3af"
                  fontSize={11}
                  interval={Math.max(Math.ceil(history.length / 8), 0)}
                />
                <YAxis stroke="#9ca3af" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#1f2937', border: 'none', borderRadius: '8px' }}
                  labelStyle={{ color: '#9ca3af' }}
                  formatter={(value, name, props) => [value.toFixed(3), `${props.payload.service} — Score`]}
                />
                <Legend />
                <Line type="monotone" dataKey="score" stroke="#f59e0b" strokeWidth={2} dot={false} name="Anomaly Score" />
              </LineChart>
            </ResponsiveContainer>
          </section>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <section className="bg-gray-900 rounded-lg p-4">
              <h2 className="text-lg font-semibold mb-3">Recent Logs</h2>
              <div className="space-y-2 max-h-[500px] overflow-y-auto">
                {logs.map((log) => (
                  <div key={log.id} className={`p-2 rounded text-sm ${levelColor[log.log_level] || 'bg-gray-800'}`}>
                    <div className="flex justify-between">
                      <span className="font-mono">{log.service_name}</span>
                      <span className="text-xs opacity-70">{new Date(log.timestamp).toLocaleTimeString()}</span>
                    </div>
                    <div>{log.message}</div>
                  </div>
                ))}
              </div>
            </section>

            <section className="bg-gray-900 rounded-lg p-4">
              <h2 className="text-lg font-semibold mb-3">Active Alerts</h2>
              <div className="space-y-2 max-h-[500px] overflow-y-auto">
                {alerts.length === 0 ? (
                  <p className="text-gray-500 text-sm">No alerts yet</p>
                ) : (
                  alerts.map((alert) => (
                    <div key={alert.id} className="p-3 rounded bg-gray-800 border-l-4 border-amber-500">
                      <div className="flex justify-between items-center mb-1">
                        <span className={`text-xs px-2 py-0.5 rounded ${severityColor[alert.severity]} text-white uppercase`}>
                          {alert.severity}
                        </span>
                        <span className="text-xs text-gray-500">{new Date(alert.triggered_at).toLocaleTimeString()}</span>
                      </div>
                      <div className="font-mono text-sm">{alert.service_name}</div>
                      <div className="text-sm text-gray-400">{alert.message}</div>
                      <div className="text-xs text-gray-500 mt-1">Score: {alert.anomaly_score.toFixed(3)}</div>
                    </div>
                  ))
                )}
              </div>
            </section>
          </div>
        </>
      )}
    </div>
  )
}

export default App