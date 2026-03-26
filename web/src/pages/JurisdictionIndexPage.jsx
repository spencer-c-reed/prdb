import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../data/DataContext'
import { getStateName, getLawName, ALL_JURISDICTIONS } from '../utils/states'
import Badge from '../components/Badge'

export default function JurisdictionIndexPage() {
  const { loading, jurisdictions, getExemptions, getRules } = useData()
  const [query, setQuery] = useState('')
  const [levelFilter, setLevelFilter] = useState('all')

  // Derive jurisdiction list
  let jList = jurisdictions
  if (!jList || jList.length === 0) {
    const seen = new Set()
    ;[...getExemptions(), ...getRules()].forEach(item => {
      if (item.jurisdiction) seen.add(item.jurisdiction)
    })
    jList = [...seen].sort().map(code => ({ code, jurisdiction: code }))
  }

  // Pre-compute exemption counts and deadlines
  const exemptionCounts = {}
  getExemptions().forEach(e => {
    exemptionCounts[e.jurisdiction] = (exemptionCounts[e.jurisdiction] || 0) + 1
  })

  const deadlines = {}
  getRules().forEach(r => {
    if (r.rule_type === 'initial_response' && r.param_key === 'days_to_respond') {
      deadlines[r.jurisdiction] = { days: r.param_value, dayType: r.day_type }
    }
  })

  // Filter
  const filtered = jList.filter(j => {
    const code = j.code || j.jurisdiction
    const name = getStateName(code)
    const matchQuery = !query || name.toLowerCase().includes(query.toLowerCase()) || code.toLowerCase().includes(query.toLowerCase())
    const matchLevel = levelFilter === 'all' || (levelFilter === 'federal' ? code === 'Federal' : code !== 'Federal')
    return matchQuery && matchLevel
  })

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Jurisdictions</h1>
        <p className="text-gray-500 text-sm">Public records laws across all US states, territories, and the federal government.</p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Filter by name or code..."
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-64"
        />
        <div className="flex rounded-lg border border-gray-300 overflow-hidden">
          {['all', 'federal', 'state'].map(level => (
            <button
              key={level}
              onClick={() => setLevelFilter(level)}
              className={`px-3 py-2 text-sm capitalize transition-colors ${
                levelFilter === level
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-600 hover:bg-gray-50'
              }`}
            >
              {level}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="animate-pulse grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(9)].map((_, i) => <div key={i} className="h-32 bg-gray-200 rounded-lg" />)}
        </div>
      ) : (
        <>
          <div className="text-sm text-gray-500 mb-4">
            {filtered.length} jurisdiction{filtered.length !== 1 ? 's' : ''}
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {filtered.map(j => {
              const code = j.code || j.jurisdiction
              const name = getStateName(code)
              const lawName = getLawName(code)
              const exCount = exemptionCounts[code] || 0
              const deadline = deadlines[code]

              return (
                <Link
                  key={code}
                  to={`/jurisdictions/${code}`}
                  className="bg-white border border-gray-200 rounded-lg p-4 hover:border-blue-400 hover:shadow-sm transition-all group"
                >
                  <div className="flex items-start gap-3 mb-3">
                    <span className="inline-block px-2 py-1 bg-blue-100 text-blue-700 rounded text-sm font-bold shrink-0">
                      {code}
                    </span>
                    <div>
                      <div className="font-semibold text-gray-900 group-hover:text-blue-700 leading-tight">
                        {name}
                      </div>
                      <div className="text-xs text-gray-400 mt-0.5 leading-snug">{lawName}</div>
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-2 text-xs">
                    {deadline && (
                      <Badge variant="gray">
                        {deadline.days} {deadline.dayType || ''} days
                      </Badge>
                    )}
                    {exCount > 0 && (
                      <Badge variant="amber">{exCount} exemptions</Badge>
                    )}
                  </div>
                </Link>
              )
            })}
          </div>

          {filtered.length === 0 && (
            <div className="text-center py-12 text-gray-400">
              No jurisdictions match your filter.
            </div>
          )}
        </>
      )}
    </div>
  )
}
