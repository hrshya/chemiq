import React from 'react'
import { cn } from '@/lib/utils'

export const Button = ({ children, className='', variant='default', ...props }: any) => {
  const base = 'inline-flex items-center justify-center rounded-md px-3 py-2 text-sm font-semibold transition-colors'
  const variants: Record<string,string> = {
    default: 'bg-slate-900 text-white hover:bg-slate-800',
    outline: 'border border-slate-700 bg-transparent text-white hover:bg-slate-800',
  }
  return (
    <button className={cn(base, variants[variant] || variants.default, className)} {...props}>
      {children}
    </button>
  )
}

export default Button
