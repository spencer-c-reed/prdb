import { useState, useMemo } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useData } from '../data/DataContext'
import { getStateName } from '../utils/states'
import Badge from '../components/Badge'

export default function ExemptionsPage() {
  const { loading, getExemptions } = useData()
  const [searchParams, setSearchParams] = useSearchParams()
  const [localQuery, setLocalQuery] = useState('')

  const selectedJurisdiction = searchParams.get('jurisdiction') || ''

  const allExemptions = getExemptions()

  // Get unique jurisdictions for dropdown
  const jurisdictions = useMemo(() => {
    const seen = new Set()
    allExemptions.forEach(e => { if (e.jurisdiction) seen.add(e.jurisdiction) })
    return [...seen].sort()
  }, [allExemptions])

  // Filter
  const filtered = useMemo(() => {
    let list = selectedJurisdiction
      ? allExemptions.filter(e => e.jurisdiction === selectedJurisdiction)
      : allExemptions

    if (localQuery) {
      const q = localQuery.toLowerCase()
      list = list.filter(e =>
        (e.short_name || '').toLowerCase().includes(q) ||
        (e.description || '').toLowerCase().includes(q) ||
        (e.statute_citation || '').toLowerCase().includes(q) ||
        (e.exemption_number || '').toLowerCase().includes(q)
      )
    }

    return list
  }, [allExemptions, selectedJurisdiction, localQuery])

  function setJurisdiction(j) {
    if (j) setSearchParams({ jurisdiction: j })
    else setSearchParams({})
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Exemption Catalog</h1>
        <p className="text-gray-500 text-sm">
          Browse exemptions to public records disclosure by jurisdiction.
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <select
          value={selectedJurisdiction}
          onChange={e => setJurisdiction(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
        >
          <option value="">All jurisdictions</option>
          {jurisdictions.map(j => (
            <option key={j} value={j}>{getStateName(j)} ({j})</option>
          ))}
        </select>

        <input
          type="text"
          value={localQuery}
          onChange={e => setLocalQuery(e.target.value)}
          placeholder="Search exemptions..."
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 flex-1 min-w-48"
        />
      </div>

      {loading ? (
        <div className="animate-pulse space-y-3">
          {[...Array(6)].map((_, i) => <div key={i} className="h-28 bg-gray-200 rounded-lg" />)}
        </div>
      ) : (
        <>
          <div className="text-sm text-gray-500 mb-4">
            {filtered.length} exemption{filtered.length !== 1 ? 's' : ''}
            {selectedJurisdiction && ` in ${getStateName(selectedJurisdiction)}`}
          </div>

          {filtered.length === 0 ? (
            <div className="text-center py-12 text-gray-400">
              No exemptions found{selectedJurisdiction ? ` for ${getStateName(selectedJurisdiction)}` : ''}.
            </div>
          ) : (
            <div className="space-y-3">
              {filtered.map(e => (
                <ExemptionCard key={e.id} exemption={e} />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}

function ExemptionCard({ exemption: e }) {
  const [expanded, setExpanded] = useState(false)

  let counterArgs = null
  if (e.counter_arguments) {
    try {
      counterArgs = typeof e.counter_arguments === 'string'
        ? JSON.parse(e.counter_arguments)
        : e.counter_arguments
    } catch { /* ignore */ }
  }

  const description = e.description || ''
  const truncated = description.length > 250
  const displayDesc = expanded || !truncated ? description : description.slice(0, 250) + '...'

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <div className="flex flex-wrap gap-2 mb-2">
        <Badge variant="default">{e.jurisdiction}</Badge>
        {e.exemption_number && <Badge variant="gray">{e.exemption_number}</Badge>}
        {e.category && <Badge variant="amber">{e.category}</Badge>}
      </div>

      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <Link
            to={`/exemptions/${e.id}`}
            className="text-base font-semibold text-gray-900 hover:text-blue-700"
          >
            {e.short_name || e.statute_citation}
          </Link>
          <div className="text-xs text-gray-400 mt-0.5">{e.statute_citation}</div>
        </div>
        <Link to={`/exemptions/${e.id}`} className="text-xs text-blue-600 hover:text-blue-700 shrink-0">
          Full detail →
        </Link>
      </div>

      {description && (
        <p className="text-sm text-gray-600 mt-2 leading-relaxed">
          {displayDesc}
          {truncated && !expanded && (
            <button
              onClick={() => setExpanded(true)}
              className="ml-1 text-blue-600 hover:text-blue-700 text-xs font-medium"
            >
              more
            </button>
          )}
        </p>
      )}

      {counterArgs && (
        <>
          <button
            onClick={() => setExpanded(!expanded)}
            className="mt-3 text-xs text-blue-600 hover:text-blue-700 font-medium"
          >
            {expanded ? '▲ Hide' : '▼ Show'} challenge strategies
          </button>

          {expanded && (
            <div className="mt-3 pt-3 border-t border-gray-100">
              <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                Challenge Strategies
              </div>
              {Array.isArray(counterArgs) ? (
                <ul className="space-y-1">
                  {counterArgs.map((arg, i) => (
                    <li key={i} className="text-sm text-gray-600 flex gap-2">
                      <span className="text-blue-400 shrink-0">·</span>
                      <span>{typeof arg === 'string' ? arg : JSON.stringify(arg)}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-gray-600">{JSON.stringify(counterArgs)}</p>
              )}
            </div>
          )}
        </>
      )}
    </div>
  )
}
