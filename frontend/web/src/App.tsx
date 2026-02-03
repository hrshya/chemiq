import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Datasets from './pages/Datasets';
import Upload from './pages/Upload';
import Equipment from './pages/Equipment';
import Analytics from './pages/Analytics';

const ProtectedLayout = ({ children }: any) => {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin h-8 w-8 border-4 border-gray-300 border-t-transparent rounded-full" />
        <p className="ml-3">Loading...</p>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" />
  }

  return (
    <>
      <Navbar />
      <div className="flex">
        <Sidebar />
        <main className="ml-64 bg-black w-[calc(100%-16rem)] min-h-[calc(100vh-4rem)] mt-16 p-6">
          {children}
        </main>
      </div>
    </>
  )
}

const App = () => {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedLayout>
                <Dashboard />
              </ProtectedLayout>
            }
          />
          <Route
            path="/datasets"
            element={
              <ProtectedLayout>
                <Datasets />
              </ProtectedLayout>
            }
          />
          <Route
            path="/upload"
            element={
              <ProtectedLayout>
                <Upload />
              </ProtectedLayout>
            }
          />
          <Route
            path="/equipment"
            element={
              <ProtectedLayout>
                <Equipment />
              </ProtectedLayout>
            }
          />
          <Route
            path="/analytics"
            element={
              <ProtectedLayout>
                <Analytics />
              </ProtectedLayout>
            }
          />
          <Route path="/" element={<Navigate to="/dashboard" />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
