import { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { datasetAPI } from '../services/api'

const Upload = () => {
  const [file, setFile] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const fileInput = useRef<any>(null)
  const navigate = useNavigate()

  const handleFileSelect = (e: any) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      if (!selectedFile.name.endsWith('.csv')) {
        setError('Please select a CSV file')
        setFile(null)
        return
      }
      if (selectedFile.size > 10 * 1024 * 1024) {
        setError('File size must be less than 10MB')
        setFile(null)
        return
      }
      setFile(selectedFile)
      setError('')
    }
  }

  const handleDragOver = (e: any) => {
    e.preventDefault()
    e.currentTarget.classList.add('drag-over')
  }

  const handleDragLeave = (e: any) => {
    e.currentTarget.classList.remove('drag-over')
  }

  const handleDrop = (e: any) => {
    e.preventDefault()
    e.currentTarget.classList.remove('drag-over')
    const droppedFile = e.dataTransfer.files?.[0]
    if (droppedFile) {
      const event = {
        target: {
          files: [droppedFile]
        }
      }
      handleFileSelect(event)
    }
  }

  const handleUpload = async (e: any) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a file')
      return
    }

    setLoading(true)
    setError('')
    setSuccess('')

    try {
      const { data } = await datasetAPI.uploadCSV(file)
      setSuccess(`✅ Successfully uploaded ${file.name}! (${data.dataset.equipment_count} equipment records)`)
      setFile(null)
      fileInput.current.value = ''

      setTimeout(() => {
        navigate('/datasets')
      }, 2000)
    } catch (err: any) {
      const errorMsg = err.response?.data?.error || 'Upload failed'
      setError(`❌ ${errorMsg}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-7xl min-h-screen mx-auto p-6 bg-white rounded-2xl">
      <h2 className="text-2xl font-semibold mb-4">📤 Upload CSV File</h2>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white dark:bg-gray-800 rounded shadow p-4">
          <h3 className="font-medium">📋 Required CSV Format</h3>
          <p className="text-sm text-gray-500 mb-3">Your CSV file must contain these columns (in order):</p>
          <div className="overflow-auto rounded border">
            <table className="min-w-full text-sm">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-2 text-left">Column Name</th>
                  <th className="px-4 py-2 text-left">Type</th>
                  <th className="px-4 py-2 text-left">Example</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-t">
                  <td className="px-4 py-2">Equipment Name</td>
                  <td className="px-4 py-2">String</td>
                  <td className="px-4 py-2">Pump-01</td>
                </tr>
                <tr className="border-t">
                  <td className="px-4 py-2">Type</td>
                  <td className="px-4 py-2">String</td>
                  <td className="px-4 py-2">Pump</td>
                </tr>
                <tr className="border-t">
                  <td className="px-4 py-2">Flowrate</td>
                  <td className="px-4 py-2">Float</td>
                  <td className="px-4 py-2">150.5</td>
                </tr>
                <tr className="border-t">
                  <td className="px-4 py-2">Pressure</td>
                  <td className="px-4 py-2">Float</td>
                  <td className="px-4 py-2">10.5</td>
                </tr>
                <tr className="border-t">
                  <td className="px-4 py-2">Temperature</td>
                  <td className="px-4 py-2">Float</td>
                  <td className="px-4 py-2">45.2</td>
                </tr>
              </tbody>
            </table>
          </div>

          <h3 className="mt-6 font-medium">⚙️ Supported Equipment Types</h3>
          <div className="flex flex-wrap gap-2 mt-2">
            <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded">Pump</span>
            <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded">Compressor</span>
            <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded">Heat Exchanger</span>
            <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded">Reactor</span>
            <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded">Separator</span>
            <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded">Column</span>
            <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded">Other</span>
          </div>
        </div>

        <div className="bg-white dark:bg-gray-800 rounded shadow p-4">
          <form onSubmit={handleUpload}>
            {error && <div className="bg-red-100 text-red-800 p-2 rounded mb-3">{error}</div>}
            {success && <div className="bg-green-100 text-green-800 p-2 rounded mb-3">{success}</div>}

            <div
              className="border-2 border-dashed border-gray-300 rounded p-6 text-center cursor-pointer relative"
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInput.current?.click()}
            >
              <div className="drop-content">
                <p className="text-4xl">📁</p>
                <p className="font-medium">Drag and drop your CSV file here</p>
                <p className="text-sm text-gray-500">or click to select</p>
              </div>
              <input
                ref={fileInput}
                type="file"
                accept=".csv"
                onChange={handleFileSelect}
                disabled={loading}
                className="absolute inset-0 opacity-0 w-full h-full cursor-pointer"
              />
            </div>

            {file && (
              <div className="mt-4 p-3 border rounded flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">📄</span>
                  <div>
                    <p className="font-medium">{file.name}</p>
                    <small className="text-xs text-gray-500">{(file.size / 1024).toFixed(2)} KB</small>
                  </div>
                </div>
                <button
                  type="button"
                  className="text-gray-500 hover:text-gray-700"
                  onClick={() => {
                    setFile(null)
                    fileInput.current.value = ''
                  }}
                >
                  ✕
                </button>
              </div>
            )}

            <button type="submit" className="w-full mt-4 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded" disabled={!file || loading}>
              {loading ? 'Uploading...' : '🚀 Upload File'}
            </button>
          </form>

          <div className="mt-6 text-sm text-gray-600">
            <h3 className="font-medium">💡 Tips</h3>
            <ul className="list-disc ml-5 mt-2">
              <li>File size limit: 10 MB</li>
              <li>Supports CSV files only</li>
              <li>First row should be headers</li>
              <li>Numeric values should be valid numbers</li>
              <li>Maximum 5 recent datasets stored</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Upload
