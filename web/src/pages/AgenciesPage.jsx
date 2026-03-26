import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../data/DataContext'
import { getStateName } from '../utils/states'
import Badge from '../components/Badge'

const SUBMISSION_BADGE = {
  portal: 'green',
  email: 'blue',
  mail: 'gray',
  fax: 'gray',
  multiple: 'purple',
}

export default function AgenciesPage() {
  const { loading, agencies } = useData()
  const [query, setQuery] = useState('')
  const [levelFilter, setLevelFilter] = useState('all')
  const [jurisdictionFilter, setJurisdictionFilter] = useState('')

  const jurisdictions = useMemo(() => {
    const seen = new Set()
    agencies.forEach(a => { if (a.jurisdiction) seen.add(a.jurisdiction) })
    return [...seen].sort()
  }, [agencies])

  const filtered = useMemo(() => {
    let list = agencies

    if (levelFilter !== 'all') {
      list = list.filter(a => (a.level || '').toLowerCase() === levelFilter)
    }
    if (jurisdictionFilter) {
      list = list.filter(a => a.jurisdiction === jurisdictionFilter)
    }
    if (query) {
      const q = query.toLowerCase()
      list = list.filter(a =>
        (a.name || '').toLowerCase().includes(q) ||
        (a.abbreviation || '').toLowerCase().includes(q) ||
        (a.jurisdiction || '').toLowerCase().includes(q)
      )
    }

    return list
  }, [agencies, query, levelFilter, jurisdictionFilter])

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Agency Directory</h1>
        <p className="text-gray-500 text-sm">
          FOIA-responsive agencies with contact info and submission methods.
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Search agencies..."
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 flex-1 min-w-48"
        />

        <select
          value={jurisdictionFilter}
          onChange={e => setJurisdictionFilter(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
        >
          <option value="">All jurisdictions</option>
          {jurisdictions.map(j => (
            <option key={j} value={j}>{getStateName(j)} ({j})</option>
          ))}
        </select>

        <div className="flex rounded-lg border border-gray-300 overflow-hidden">
          {['all', 'federal', 'state', 'county', 'municipal'].map(level => (
            <button
              key={level}
              onClick={() => setLevelFilter(level)}
              className={`px-3 py-2 text-xs capitalize transition-colors ${
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
        <div className="animate-pulse space-y-3">
          {[...Array(6)].map((_, i) => <div key={i} className="h-32 bg-gray-200 rounded-lg" />)}
        </div>
      ) : (
        <>
          <div className="text-sm text-gray-500 mb-4">
            {filtered.length} agenc{filtered.length !== 1 ? 'ies' : 'y'}
          </div>

          {filtered.length === 0 ? (
            <div className="text-center py-12 text-gray-400">No agencies found.</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filtered.map(a => (
                <AgencyCard key={a.id} agency={a} />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}

function AgencyCard({ agency: a }) {
  const submissionVariant = SUBMISSION_BADGE[a.submission_method?.toLowerCase()] || 'gray'

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 hover:border-blue-300 hover:shadow-sm transition-all">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex-1 min-w-0">
          <div className="font-semibold text-gray-900 leading-tight">{a.name}</div>
          {a.abbreviation && (
            <div className="text-xs text-gray-400 mt-0.5">{a.abbreviation}</div>
          )}
        </div>
        <Link to={`/agencies/${a.id}`} className="text-xs text-blue-600 hover:text-blue-700 shrink-0">
          Details →
        </Link>
      </div>

      <div className="flex flex-wrap gap-2 mb-3">
        {a.jurisdiction && (
          <Badge variant="default">{a.jurisdiction}</Badge>
        )}
        {a.level && (
          <Badge variant="gray">{a.level}</Badge>
        )}
        {a.submission_method && (
          <Badge variant={submissionVariant}>{a.submission_method}</Badge>
        )}
      </div>

      <div className="text-xs text-gray-500 space-y-1">
        {a.email && (
          <div>
            <span className="text-gray-400">Email: </span>
            <a href={`mailto:${a.email}`} className="text-blue-600 hover:underline">{a.email}</a>
          </div>
        )}
        {a.phone && (
          <div>
            <span className="text-gray-400">Phone: </span>
            <a href={`tel:${a.phone}`} className="text-blue-600 hover:underline">{a.phone}</a>
          </div>
        )}
        {a.portal_url && (
          <div>
            <a
              href={a.portal_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Online portal →
            </a>
          </div>
        )}
        {a.foia_officer_name && (
          <div>
            <span className="text-gray-400">FOIA Officer: </span>
            {a.foia_officer_name}
            {a.foia_officer_title && `, ${a.foia_officer_title}`}
          </div>
        )}
        {a.avg_response_days != null && (
          <div>
            <span className="text-gray-400">Avg response: </span>
            {a.avg_response_days} days
          </div>
        )}
      </div>
    </div>
  )
}
