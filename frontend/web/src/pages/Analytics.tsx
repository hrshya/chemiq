import { useState, useEffect } from 'react'
import { analyticsAPI } from '../services/api'
import { Bar, Radar } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  RadarController,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, RadarController, Title, Tooltip, Legend)

const Analytics = () => {
  const [summary, setSummary] = useState<any>(null)
  const [loading, setLoading] = useState<any>(true)
  

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const { data } = await analyticsAPI.getSummary()
      setSummary(data)
    } catch (err) {
      console.error('Failed to load analytics', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[40vh]">
        <div className="animate-spin h-8 w-8 border-4 border-gray-300 border-t-transparent rounded-full" />
        <p className="ml-3">Loading analytics...</p>
      </div>
    )
  }

  if (!summary) {
    return <div className="text-gray-600 p-6">No data available yet.</div>
  }

  const equipmentTypes = Object.keys(summary.equipment_type_distribution || {})
  const equipmentCounts = Object.values(summary.equipment_type_distribution || {})

  const distributionChartData = {
    labels: equipmentTypes,
    datasets: [
      {
        label: 'Equipment Count by Type',
        data: equipmentCounts,
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF'],
        borderColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF'],
        borderWidth: 2
      }
    ]
  }

  const paramChartData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Average Value',
        data: [summary.avg_flowrate || 0, summary.avg_pressure || 0, summary.avg_temperature || 0],
        borderColor: '#36A2EB',
        backgroundColor: 'rgba(54, 162, 235, 0.1)',
        borderWidth: 2,
        fill: true
      }
    ]
  }

  return (
    <div className="max-w-7xl mx-auto p-6">
      <h2 className="text-2xl font-semibold mb-4">📈 Advanced Analytics</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white dark:bg-gray-800 rounded shadow p-4">
          <h3 className="font-medium mb-4">Key Metrics</h3>
          <div className="space-y-3">
            <div className="flex justify-between">
              <label className="text-sm text-gray-500">Total Equipment</label>
              <p className="font-semibold">{summary.total_equipment}</p>
            </div>
            <div className="flex justify-between">
              <label className="text-sm text-gray-500">Equipment Types</label>
              <p className="font-semibold">{equipmentTypes.length}</p>
            </div>
            <div className="flex justify-between">
              <label className="text-sm text-gray-500">Avg Flowrate (L/min)</label>
              <p className="font-semibold">{summary.avg_flowrate?.toFixed(2) || 'N/A'}</p>
            </div>
            <div className="flex justify-between">
              <label className="text-sm text-gray-500">Avg Pressure (Bar)</label>
              <p className="font-semibold">{summary.avg_pressure?.toFixed(2) || 'N/A'}</p>
            </div>
            <div className="flex justify-between">
              <label className="text-sm text-gray-500">Avg Temperature (°C)</label>
              <p className="font-semibold">{summary.avg_temperature?.toFixed(2) || 'N/A'}</p>
            </div>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded shadow p-4">
          <h3 className="font-medium mb-2">Equipment Type Distribution</h3>
          <Bar data={distributionChartData} options={{ responsive: true, maintainAspectRatio: true }} />
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded shadow p-4 mb-6">
        <h3 className="font-medium mb-2">Parameter Comparison</h3>
        <Radar data={paramChartData} options={{ responsive: true, maintainAspectRatio: true }} />
      </div>

      <div className="bg-white dark:bg-gray-800 rounded shadow p-4">
        <h3 className="font-medium mb-4">📋 Summary Report</h3>
        <h4 className="text-sm font-medium mb-3">Equipment Breakdown</h4>
        <div className="overflow-auto rounded border">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-2 text-left">Equipment Type</th>
                <th className="px-4 py-2 text-left">Count</th>
                <th className="px-4 py-2 text-left">Percentage</th>
              </tr>
            </thead>
            <tbody>
              {equipmentTypes.map((type) => (
                <tr key={type} className="border-t">
                  <td className="px-4 py-2">{type}</td>
                  <td className="px-4 py-2">{summary.equipment_type_distribution[type]}</td>
                  <td className="px-4 py-2">{((summary.equipment_type_distribution[type] / summary.total_equipment) * 100).toFixed(1)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default Analytics
