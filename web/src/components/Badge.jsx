export default function Badge({ children, variant = 'default', className = '' }) {
  const variants = {
    default: 'bg-blue-100 text-blue-700',
    amber: 'bg-amber-100 text-amber-700',
    green: 'bg-green-100 text-green-700',
    red: 'bg-red-100 text-red-700',
    gray: 'bg-gray-100 text-gray-600',
    purple: 'bg-purple-100 text-purple-700',
  }

  const cls = variants[variant] || variants.default

  return (
    <span
      className={`inline-block px-2 py-0.5 rounded text-xs font-semibold ${cls} ${className}`}
    >
      {children}
    </span>
  )
}
