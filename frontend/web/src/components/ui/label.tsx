export const Label = ({ children, htmlFor, className='' }: any) => {
  return (
    <label htmlFor={htmlFor} className={`text-sm font-medium text-slate-300 ${className}`}>
      {children}
    </label>
  )
}

export default Label
