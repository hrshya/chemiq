import React from 'react'
import { useAuth } from '../context/AuthContext'
import { LogOut, User } from 'lucide-react'

const Navbar = () => {
  const { user, logout } = useAuth()

  if (!user) return null

  return (
    <nav className="fixed w-screen top-0 left-0 right-0 h-20 bg-black text-white shadow z-20">
      <div className="mx-8 px-6 h-full flex items-center justify-between">
        <div className="text-3xl font-bold flex items-center uppercase gap-2">ChemEquip Visualizer</div>
        <div className="flex items-center gap-4">
          <span className="text-md flex items-center gap-2"><User size={18} /> Welcome, {user.username}!</span>
          <button
            onClick={logout}
            className="bg-white/10 backdrop-blur-md border hover:cursor-pointer border-white/20 text-white text-sm px-5 py-2 rounded-lg flex items-center gap-2 hover:bg-white/20 transition-all duration-300"
          >
            <LogOut size={16} /> Logout
          </button>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
