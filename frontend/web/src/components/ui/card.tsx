import React from 'react'
import { cn } from '@/lib/utils'

export const Card = ({ children, className='' }: any) => (
  <div className={cn('bg-slate-900 rounded-xl border border-slate-700 p-0', className)}>{children}</div>
)

export const CardHeader = ({ children, className='' }: any) => (
  <div className={cn('p-4 border-b border-slate-800', className)}>{children}</div>
)
export const CardTitle = ({ children }: any) => (
  <h3 className="text-lg font-semibold text-white">{children}</h3>
)
export const CardDescription = ({ children }: any) => (
  <p className="text-sm text-slate-400">{children}</p>
)
export const CardContent = ({ children, className='' }: any) => (
  <div className={cn('p-4', className)}>{children}</div>
)
export const CardFooter = ({ children, className='' }: any) => (
  <div className={cn('p-4 border-t border-slate-800', className)}>{children}</div>
)

export default Card
