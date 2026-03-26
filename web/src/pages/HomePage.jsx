import { Link } from 'react-router-dom'
import { useData } from '../data/DataContext'
import SearchBar from '../components/SearchBar'
import { getStateName, getLawName } from '../utils/states'

function StatCard({ number, label }) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-5 text-center shadow-sm">
      <div className="text-3xl font-bold text-blue-600">{number}</div>
      <div className="text-sm text-gray-500 mt-1">{label}</div>
    </div>
  )
}

function Skeleton() {
  return (
    <div className="animate-pulse">
      <div className="h-8 bg-gray-200 rounded w-1/3 mb-4" />
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-24 bg-gray-200 rounded-lg" />
        ))}
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        {[...Array(12)].map((_, i) => (
          <div key={i} className="h-28 bg-gray-200 rounded-lg" />
        ))}
      </div>
    </div>
  )
}

export default function HomePage() {
  const { loading, stats, jurisdictions, getExemptions, getRules } = useData()

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Skeleton />
      </div>
    )
  }

  // Build jurisdiction list — use structured data if available, else derive from unique jurisdictions in exemptions/rules
  let jList = jurisdictions
  if (!jList || jList.length === 0) {
    const seen = new Set()
    ;[...getExemptions(), ...getRules()].forEach(item => {
      if (item.jurisdiction) seen.add(item.jurisdiction)
    })
    jList = [...seen].sort().map(code => ({ code, jurisdiction: code }))
  }

  // Per-jurisdiction deadline from jurisdictions data, fallback to rules
  const deadlineMap = {}
  jList.forEach(j => {
    const code = j.code || j.jurisdiction
    if (j.response_days) {
      deadlineMap[code] = `${j.response_days} ${j.response_type || ''} days`.trim()
    }
  })
  getRules().forEach(r => {
    if (!deadlineMap[r.jurisdiction] && r.rule_type === 'initial_response' && r.param_key === 'days_to_respond') {
      deadlineMap[r.jurisdiction] = `${r.param_value} ${r.day_type || ''} days`.trim()
    }
  })

  // Exemption counts — prefer from jurisdictions data
  const exemptionCounts = {}
  jList.forEach(j => {
    const code = j.code || j.jurisdiction
    if (j.exemption_count != null) exemptionCounts[code] = j.exemption_count
  })
  if (Object.keys(exemptionCounts).length === 0) {
    getExemptions().forEach(e => {
      exemptionCounts[e.jurisdiction] = (exemptionCounts[e.jurisdiction] || 0) + 1
    })
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Public Records Request Database
        </h1>
        <p className="text-gray-500 mb-6">
          A comprehensive reference for FOIA and public records laws, exemptions, agency directories,
          and request templates across all US jurisdictions.
        </p>
        <div className="max-w-lg">
          <SearchBar
            placeholder="Search statutes, exemptions, case law..."
            autoFocus
          />
        </div>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-10">
        <StatCard
          number={jList.length || 52}
          label="Jurisdictions"
        />
        <StatCard
          number={(stats.exemptions ?? getExemptions().length)?.toLocaleString() || '—'}
          label="Exemptions"
        />
        <StatCard
          number={stats.agencies?.toLocaleString() || '—'}
          label="Agencies"
        />
        <StatCard
          number={stats.templates?.toLocaleString() || '—'}
          label="Templates"
        />
      </div>

      {/* Jurisdiction grid */}
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">All Jurisdictions</h2>
        <Link to="/jurisdictions" className="text-sm text-blue-600 hover:text-blue-700">
          View full list →
        </Link>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
        {jList.map(j => {
          const code = j.code || j.jurisdiction
          const name = j.name || getStateName(code)
          const deadline = deadlineMap[code]
          const exCount = exemptionCounts[code] || 0

          return (
            <Link
              key={code}
              to={`/jurisdictions/${code}`}
              className="bg-white border border-gray-200 rounded-lg p-4 hover:border-blue-400 hover:shadow-sm transition-all group"
            >
              <div className="flex items-start justify-between mb-2">
                <span className="inline-block px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs font-bold">
                  {code}
                </span>
              </div>
              <div className="text-sm font-medium text-gray-900 group-hover:text-blue-700 leading-snug mb-2">
                {name}
              </div>
              <div className="text-xs text-gray-400 space-y-0.5">
                {deadline && <div>{deadline} response</div>}
                {exCount > 0 && <div>{exCount} exemptions</div>}
              </div>
            </Link>
          )
        })}
      </div>

      {jList.length === 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-8 text-center text-gray-500">
          <p className="text-lg mb-2">No data loaded yet</p>
          <p className="text-sm">
            Place JSON data files in <code className="bg-gray-100 px-1 rounded">public/data/</code> to populate the database.
          </p>
        </div>
      )}
    </div>
  )
}
