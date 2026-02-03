import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { BarChart3, Database, Upload, Zap, TrendingUp } from 'lucide-react'

const Sidebar = () => {
  const { user } = useAuth()

  if (!user) return null

  return (
    <aside className="fixed left-0 top-16 pl-12 w-64 h-[calc(100vh-4rem)] bg-black text-white p-4 overflow-auto">
      <nav className="space-y-1">
        <Link to="/dashboard" className="block py-2 px-3 rounded hover:bg-gray-700 flex items-center gap-3 transition-colors">
          <BarChart3 size={20} /> Dashboard
        </Link>
        <Link to="/datasets" className="block py-2 px-3 rounded hover:bg-gray-700 flex items-center gap-3 transition-colors">
          <Database size={20} /> Datasets
        </Link>
        <Link to="/upload" className="block py-2 px-3 rounded hover:bg-gray-700 flex items-center gap-3 transition-colors">
          <Upload size={20} /> Upload CSV
        </Link>
        <Link to="/equipment" className="block py-2 px-3 rounded hover:bg-gray-700 flex items-center gap-3 transition-colors">
          <Zap size={20} /> Equipment
        </Link>
        <Link to="/analytics" className="block py-2 px-3 rounded hover:bg-gray-700 flex items-center gap-3 transition-colors">
          <TrendingUp size={20} /> Analytics
        </Link>
      </nav>
    </aside>
  )
}

export default Sidebar
