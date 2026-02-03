import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { authAPI } from '../services/api'
import { useAuth } from '../context/AuthContext'
import { BorderBeam } from '@/registry/magicui/border-beam'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
  CardDescription,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { User, Mail, Lock, AlertCircle, UserCheck, LogIn } from 'lucide-react'

const Register = () => {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: any) => {
    e.preventDefault()
    setError('')

    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters')
      return
    }

    setLoading(true)

    try {
      const { data } = await authAPI.register(username, email, password)
      login(data.user, data.token)
      navigate('/dashboard')
    } catch (err: any) {
      const errorMsg = err.response?.data?.error || 'Registration failed'
      setError(errorMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-black via-slate-900 to-black p-4 relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-green-600/20 rounded-full mix-blend-multiply filter blur-3xl animate-pulse" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-cyan-600/20 rounded-full mix-blend-multiply filter blur-3xl animate-pulse" />
      
      <div className="flex items-center justify-center">
        <Card className="relative w-[350px] overflow-hidden">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">Register</CardTitle>
            <CardDescription>Create your account</CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit}>
              <div className="grid w-full items-center gap-4">
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="username" className="flex items-center gap-2">Username</Label>
                  <div className="relative">
                    <Input id="username" type="text" placeholder="Choose a username" value={username} onChange={(e: any)=>setUsername(e.target.value)} disabled={loading} required />
                  </div>
                </div>
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="email" className="flex items-center gap-2">Email</Label>
                  <div className="relative">
                    <Input id="email" type="email" placeholder="Enter your email" value={email} onChange={(e: any)=>setEmail(e.target.value)} disabled={loading} required />
                  </div>
                </div>
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="password" className="flex items-center gap-2">Password</Label>
                  <div className="relative">
                    <Input id="password" type="password" placeholder="At least 6 characters" value={password} onChange={(e: any)=>setPassword(e.target.value)} disabled={loading} required />
                  </div>
                </div>
                <div className="flex flex-col space-y-1.5">
                  <Label htmlFor="confirmPassword" className="flex items-center gap-2">Confirm Password</Label>
                  <div className="relative">
                    <Input id="confirmPassword" type="password" placeholder="Confirm your password" value={confirmPassword} onChange={(e: any)=>setConfirmPassword(e.target.value)} disabled={loading} required />
                  </div>
                </div>
              </div>
            </form>
            {error && <div className="mt-3 text-sm text-red-400 flex items-center gap-2"><AlertCircle size={16} /> {error}</div>}
          </CardContent>
          <CardFooter className="flex justify-between">
            <Button variant="outline" onClick={()=>navigate('/login')} className="flex items-center gap-2">Login</Button>
            <Button onClick={handleSubmit as any} disabled={loading} className="flex items-center gap-2">{loading ? 'Creating...' : <>Register</>}</Button>
          </CardFooter>
          <BorderBeam duration={8} size={100} />
        </Card>
      </div>
    </div>
  )
}

export default Register
