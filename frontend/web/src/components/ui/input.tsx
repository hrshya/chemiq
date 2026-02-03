import React from 'react'
import { cn } from '@/lib/utils'

export const Input = React.forwardRef<any, any>(({ className='', ...props }, ref) => {
  return (
    <input ref={ref} className={cn('w-full rounded-md border border-slate-700 bg-transparent px-3 py-2 text-sm text-white placeholder:text-slate-400 focus:outline-none focus:ring-1 focus:ring-slate-600', className)} {...props} />
  )
})
Input.displayName = 'Input'

export default Input
