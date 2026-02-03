import React, { useState, useEffect } from 'react'
import { datasetAPI } from '../services/api'
// migrated to Tailwind via src/index.css

const Datasets = () => {
  const [datasets, setDatasets] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [expandedId, setExpandedId] = useState(null)

  useEffect(() => {
    fetchDatasets()
  }, [])

  const fetchDatasets = async () => {
    try {
      const { data } = await datasetAPI.list()
      setDatasets(data.results || [])
    } catch (err) {
      setError('Failed to load datasets')
    } finally {
      setLoading(false)
    }
  }

  const handleDownloadPDF = async (id: any, filename: any) => {
    try {
      const blob: any = await datasetAPI.generatePDF(id)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `Report_${filename.replace('.csv', '')}.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      alert('Failed to download PDF')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[40vh]">
        <div className="animate-spin h-8 w-8 border-4 border-gray-300 border-t-transparent rounded-full" />
        <p className="ml-3">Loading datasets...</p>
      </div>
    )
  }

  if (datasets.length === 0) {
    return <div className="max-w-7xl mx-auto p-6 text-gray-600">No datasets found. Upload a CSV file to get started!</div>
  }

  return (
    <div className="max-w-7xl min-h-screen mx-auto p-6 bg-white rounded-2xl">
      <h2 className="text-2xl font-semibold mb-4">📁 Datasets</h2>
      <div className="space-y-4">
        {datasets.map((dataset: any) => (
          <div key={dataset.id} className="bg-white dark:bg-gray-800 rounded shadow">
            <div
              className="p-4 flex items-start justify-between cursor-pointer"
              onClick={() => setExpandedId(expandedId === dataset.id ? null : dataset.id)}
            >
              <div>
                <h3 className="font-medium">{dataset.filename}</h3>
                <small className="text-xs text-gray-500">{new Date(dataset.uploaded_at).toLocaleString()}</small>
              </div>
              <div className="flex items-center gap-3">
                <span className="bg-indigo-100 text-indigo-800 text-sm px-2 py-1 rounded">{dataset.equipment_count} equipment</span>
                <span className="text-gray-400">{expandedId === dataset.id ? '▼' : '▶'}</span>
              </div>
            </div>

            {expandedId === dataset.id && (
              <div className="p-4 border-t">
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  <div>
                    <h4 className="text-sm text-gray-500">Avg Flowrate</h4>
                    <p className="font-medium">{dataset.summary_stats?.avg_flowrate?.toFixed(2) || 'N/A'} L/min</p>
                  </div>
                  <div>
                    <h4 className="text-sm text-gray-500">Avg Pressure</h4>
                    <p className="font-medium">{dataset.summary_stats?.avg_pressure?.toFixed(2) || 'N/A'} Bar</p>
                  </div>
                  <div>
                    <h4 className="text-sm text-gray-500">Avg Temperature</h4>
                    <p className="font-medium">{dataset.summary_stats?.avg_temperature?.toFixed(2) || 'N/A'} °C</p>
                  </div>
                </div>

                {dataset.summary_stats?.equipment_type_distribution && (
                  <div className="mt-4">
                    <h4 className="font-medium mb-2">Equipment Types</h4>
                    <div className="flex flex-wrap gap-2">
                      {Object.entries(dataset.summary_stats.equipment_type_distribution).map(([type, count]: any[]) => (
                        <div key={type} className="flex items-center gap-2 bg-gray-100 dark:bg-gray-700 px-3 py-1 rounded">
                          <span className="text-sm">{type}</span>
                          <span className="text-xs text-gray-500">{count}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                <div className="mt-4">
                  <button
                    className="bg-indigo-600 hover:bg-indigo-500 text-white px-3 py-1 rounded"
                    onClick={() => handleDownloadPDF(dataset.id, dataset.filename)}
                  >
                    📥 Download PDF
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default Datasets
