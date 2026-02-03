import React, { useState, useEffect } from 'react'
import { analyticsAPI, datasetAPI } from '../services/api'
import { Line, Bar, Doughnut } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
// styles migrated to Tailwind via src/index.css

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
)

const Dashboard = () => {
  const [summary, setSummary] = useState<any>(null)
  const [loading, setLoading] = useState<any>(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchSummary()
  }, [])

  const fetchSummary = async () => {
    try {
      const { data } = await analyticsAPI.getSummary()
      setSummary(data)
    } catch (err) {
      setError('Failed to load summary')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[40vh]">
        <div className="animate-spin h-8 w-8 border-4 border-gray-300 border-t-transparent rounded-full" />
        <p className="ml-3">Loading dashboard...</p>
      </div>
    )
  }

  if (!summary) {
    return <div className="alert alert-info">No data available. Upload a CSV file to get started!</div>
  }

  const equipmentTypes = Object.keys(summary.equipment_type_distribution || {})
  const equipmentCounts = Object.values(summary.equipment_type_distribution || {})

  const chartColors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF']

  const typeChartData = {
    labels: equipmentTypes,
    datasets: [
      {
        label: 'Equipment Count by Type',
        data: equipmentCounts,
        backgroundColor: chartColors.slice(0, equipmentTypes.length),
        borderColor: chartColors.slice(0, equipmentTypes.length),
        borderWidth: 1
      }
    ]
  }

  const statsChartData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Average Values',
        data: [summary.avg_flowrate, summary.avg_pressure, summary.avg_temperature],
        backgroundColor: ['#36A2EB', '#FF6384', '#FFCE56'],
        borderColor: ['#36A2EB', '#FF6384', '#FFCE56'],
        borderWidth: 1
      }
    ]
  }

  return (
    <div className="max-w-7xl bg-white rounded-2xl mx-auto p-6">
      <h2 className="text-2xl font-semibold mb-4">Dashboard</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-gray-800 rounded shadow p-4">
          <h3 className="text-sm text-gray-500">Total Equipment</h3>
          <p className="text-2xl font-bold">{summary.total_equipment}</p>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded shadow p-4">
          <h3 className="text-sm text-gray-500">Avg Flowrate</h3>
          <p className="text-2xl font-bold">{summary.avg_flowrate?.toFixed(2) || 'N/A'}</p>
          <small className="text-gray-400">L/min</small>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded shadow p-4">
          <h3 className="text-sm text-gray-500">Avg Pressure</h3>
          <p className="text-2xl font-bold">{summary.avg_pressure?.toFixed(2) || 'N/A'}</p>
          <small className="text-gray-400">Bar</small>
        </div>
        <div className="bg-white dark:bg-gray-800 rounded shadow p-4">
          <h3 className="text-sm text-gray-500">Avg Temperature</h3>
          <p className="text-2xl font-bold">{summary.avg_temperature?.toFixed(2) || 'N/A'}</p>
          <small className="text-gray-400">°C</small>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <div className="bg-white dark:bg-gray-800 rounded shadow p-4">
          <h3 className="mb-2">Equipment Distribution</h3>
          <Doughnut data={typeChartData} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>
        <div className="bg-white dark:bg-gray-800 rounded shadow p-4">
          <h3 className="mb-2">Average Parameters</h3>
          <Bar data={statsChartData} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>
      </div>

      {summary.recent_datasets && summary.recent_datasets.length > 0 && (
        <div className="bg-white dark:bg-gray-800 rounded shadow p-4 mt-6">
          <h3 className="text-lg mb-3">📁 Recent Datasets</h3>
          <div className="space-y-3">
            {summary.recent_datasets.map((dataset: any) => (
              <div key={dataset.id} className="p-3 border rounded bg-gray-50 dark:bg-gray-700">
                <h4 className="font-medium">{dataset.filename}</h4>
                <p className="text-sm text-gray-400">Equipment: {dataset.equipment_count}</p>
                <small className="text-xs text-gray-500">{new Date(dataset.uploaded_at).toLocaleString()}</small>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Dashboard
