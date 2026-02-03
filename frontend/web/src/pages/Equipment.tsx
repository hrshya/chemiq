import React, { useState, useEffect } from 'react'
import { equipmentAPI } from '../services/api'

const Equipment = () => {
  const [equipment, setEquipment] = useState<any[]>([])
  const [loading, setLoading] = useState<any>(true)
  const [error, setError] = useState('')
  const [filters, setFilters] = useState({
    type: 'all',
    sortBy: 'name'
  })

  useEffect(() => {
    fetchEquipment()
  }, [])

  const fetchEquipment = async () => {
    try {
      const { data } = await equipmentAPI.list()
      setEquipment(data.results || [])
    } catch (err) {
      setError('Failed to load equipment')
    } finally {
      setLoading(false)
    }
  }

  const getUniqueTypes = () => {
    const types = new Set(equipment.map((e) => e.equipment_type))
    return Array.from(types).sort()
  }

  const getFilteredEquipment = () => {
    let filtered = equipment

    if (filters.type !== 'all') {
      filtered = filtered.filter((e) => e.equipment_type === filters.type)
    }

    if (filters.sortBy === 'name') {
      filtered.sort((a, b) => a.name.localeCompare(b.name))
    } else if (filters.sortBy === 'type') {
      filtered.sort((a, b) => a.equipment_type.localeCompare(b.equipment_type))
    } else if (filters.sortBy === 'flowrate') {
      filtered.sort((a, b) => (b.flowrate || 0) - (a.flowrate || 0))
    }

    return filtered
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[40vh]">
        <div className="animate-spin h-8 w-8 border-4 border-gray-300 border-t-transparent rounded-full" />
        <p className="ml-3">Loading equipment...</p>
      </div>
    )
  }

  const types = getUniqueTypes()
  const filteredEquipment = getFilteredEquipment()

  return (
    <div className="max-w-7xl bg-white rounded-2xl min-h-screen mx-auto p-6">
      <h2 className="text-2xl font-semibold mb-4">⚙️ Equipment</h2>

      <div className="flex gap-4 mb-6">
        <div className="flex-1">
          <label className="block text-sm font-medium mb-2">Filter by Type</label>
          <select
            value={filters.type}
            onChange={(e) => setFilters({ ...filters, type: e.target.value })}
            className="w-full border rounded px-3 py-2 bg-gray-50 dark:bg-gray-700"
          >
            <option value="all">All Types ({equipment.length})</option>
            {types.map((type) => (
              <option key={type} value={type}>
                {type} ({equipment.filter((e) => e.equipment_type === type).length})
              </option>
            ))}
          </select>
        </div>

        <div className="flex-1">
          <label className="block text-sm font-medium mb-2">Sort By</label>
          <select
            value={filters.sortBy}
            onChange={(e) => setFilters({ ...filters, sortBy: e.target.value })}
            className="w-full border rounded px-3 py-2 bg-gray-50 dark:bg-gray-700"
          >
            <option value="name">Name</option>
            <option value="type">Type</option>
            <option value="flowrate">Flowrate (High to Low)</option>
          </select>
        </div>
      </div>

      {filteredEquipment.length === 0 ? (
        <div className="text-gray-600">No equipment found with selected filters</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredEquipment.map((equip) => (
            <div key={equip.id} className="bg-white dark:bg-gray-800 rounded shadow overflow-hidden">
              <div className="border-b p-4 flex items-center justify-between">
                <h3 className="font-medium">{equip.name}</h3>
                <span className="bg-indigo-100 text-indigo-800 text-xs px-2 py-1 rounded">{equip.equipment_type}</span>
              </div>
              <div className="p-4 space-y-3">
                <div>
                  <label className="text-sm text-gray-500">Flowrate</label>
                  <p className="font-medium">{equip.flowrate ? equip.flowrate.toFixed(2) : 'N/A'} L/min</p>
                </div>
                <div>
                  <label className="text-sm text-gray-500">Pressure</label>
                  <p className="font-medium">{equip.pressure ? equip.pressure.toFixed(2) : 'N/A'} Bar</p>
                </div>
                <div>
                  <label className="text-sm text-gray-500">Temperature</label>
                  <p className="font-medium">{equip.temperature ? equip.temperature.toFixed(2) : 'N/A'} °C</p>
                </div>
              </div>
              <div className="border-t px-4 py-2 bg-gray-50 dark:bg-gray-700">
                <small className="text-gray-500">{new Date(equip.created_at).toLocaleDateString()}</small>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Equipment
