import { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useData } from '../data/DataContext'

export default function SearchBar({ placeholder = 'Search statutes, exemptions, agencies...', autoFocus = false }) {
  const [query, setQuery] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const [open, setOpen] = useState(false)
  const { search } = useData()
  const navigate = useNavigate()
  const inputRef = useRef(null)
  const containerRef = useRef(null)

  useEffect(() => {
    if (autoFocus && inputRef.current) {
      inputRef.current.focus()
    }
  }, [autoFocus])

  useEffect(() => {
    function handleClickOutside(e) {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  function handleChange(e) {
    const val = e.target.value
    setQuery(val)
    if (val.length >= 2) {
      const results = search(val, { limit: 6 })
      setSuggestions(results)
      setOpen(results.length > 0)
    } else {
      setSuggestions([])
      setOpen(false)
    }
  }

  function handleSubmit(e) {
    e.preventDefault()
    if (query.trim()) {
      setOpen(false)
      navigate(`/search?q=${encodeURIComponent(query.trim())}`)
    }
  }

  function handleSuggestionClick(result) {
    setOpen(false)
    setQuery('')
    // Route based on document_type
    const type = (result.document_type || '').toLowerCase()
    if (type === 'exemption') {
      navigate(`/exemptions/${result.id}`)
    } else if (type === 'agency') {
      navigate(`/agencies/${result.id}`)
    } else if (type === 'template') {
      navigate(`/templates/${result.id}`)
    } else if (result.jurisdiction && result.jurisdiction !== 'Federal') {
      navigate(`/jurisdictions/${result.jurisdiction}`)
    } else {
      navigate(`/search?q=${encodeURIComponent(result.title)}`)
    }
  }

  return (
    <div ref={containerRef} className="relative w-full max-w-xl">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={handleChange}
          onFocus={() => suggestions.length > 0 && setOpen(true)}
          placeholder={placeholder}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
        >
          Search
        </button>
      </form>

      {open && (
        <div className="absolute top-full left-0 right-0 mt-1 bg-white border border-gray-200 rounded-lg shadow-lg z-50 overflow-hidden">
          {suggestions.map(result => (
            <button
              key={result.id}
              onClick={() => handleSuggestionClick(result)}
              className="w-full text-left px-4 py-2.5 hover:bg-gray-50 border-b border-gray-100 last:border-b-0"
            >
              <div className="text-sm font-medium text-gray-900 truncate">{result.title}</div>
              <div className="text-xs text-gray-500 mt-0.5">
                {result.document_type && (
                  <span className="capitalize">{result.document_type}</span>
                )}
                {result.jurisdiction && (
                  <span> · {result.jurisdiction}</span>
                )}
              </div>
            </button>
          ))}
          <button
            onClick={handleSubmit}
            className="w-full text-left px-4 py-2.5 bg-gray-50 text-sm text-blue-600 font-medium hover:bg-gray-100"
          >
            See all results for &ldquo;{query}&rdquo; →
          </button>
        </div>
      )}
    </div>
  )
}
