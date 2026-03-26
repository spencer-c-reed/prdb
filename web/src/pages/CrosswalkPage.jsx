import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../data/DataContext'
import Badge from '../components/Badge'
import { getStateName } from '../utils/states'

function formatCategory(category) {
  return category
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function CategoryCard({ category }) {
  const [expanded, setExpanded] = useState(false)

  // Group exemptions by jurisdiction
  const byJurisdiction = useMemo(() => {
    const groups = {}
    category.exemptions.forEach(ex => {
      if (!groups[ex.jurisdiction]) groups[ex.jurisdiction] = []
      groups[ex.jurisdiction].push(ex)
    })
    return Object.entries(groups).sort(([a], [b]) => a.localeCompare(b))
  }, [category.exemptions])

  return (
    <div className="bg-white border border-gray-200 rounded-lg">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full text-left px-5 py-4 flex items-center justify-between gap-4"
      >
        <div className="flex items-center gap-3 min-w-0">
          <h2 className="text-base font-semibold text-gray-900">
            {formatCategory(category.category)}
          </h2>
          <Badge variant="default">{category.count} exemption{category.count !== 1 ? 's' : ''}</Badge>
          <Badge variant="gray">{category.jurisdictions} jurisdiction{category.jurisdictions !== 1 ? 's' : ''}</Badge>
        </div>
        <span className="text-gray-400 text-sm shrink-0">
          {expanded ? '▲' : '▼'}
        </span>
      </button>

      {expanded && (
        <div className="px-5 pb-5 border-t border-gray-100">
          <div className="overflow-x-auto mt-4">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left border-b border-gray-200">
                  <th className="pb-2 pr-6 text-xs font-semibold text-gray-500 uppercase tracking-wide w-28">
                    Jurisdiction
                  </th>
                  <th className="pb-2 pr-6 text-xs font-semibold text-gray-500 uppercase tracking-wide w-28">
                    Number
                  </th>
                  <th className="pb-2 pr-6 text-xs font-semibold text-gray-500 uppercase tracking-wide">
                    Name
                  </th>
                  <th className="pb-2 text-xs font-semibold text-gray-500 uppercase tracking-wide">
                    Citation
                  </th>
                </tr>
              </thead>
              <tbody>
                {byJurisdiction.map(([jurisdiction, exemptions]) =>
                  exemptions.map((ex, i) => (
                    <tr key={ex.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-2.5 pr-6">
                        {i === 0 ? (
                          <div>
                            <span className="inline-block px-1.5 py-0.5 bg-blue-100 text-blue-700 rounded text-xs font-bold">
                              {jurisdiction}
                            </span>
                            <div className="text-xs text-gray-400 mt-0.5">{getStateName(jurisdiction)}</div>
                          </div>
                        ) : null}
                      </td>
                      <td className="py-2.5 pr-6 text-gray-500 font-mono text-xs">
                        {ex.exemption_number}
                      </td>
                      <td className="py-2.5 pr-6">
                        <Link
                          to={`/exemptions/${ex.id}`}
                          className="text-gray-900 hover:text-blue-700 font-medium"
                        >
                          {ex.short_name}
                        </Link>
                        {ex.description && (
                          <div className="text-xs text-gray-400 mt-0.5 line-clamp-1">
                            {ex.description}
                          </div>
                        )}
                      </td>
                      <td className="py-2.5 text-xs text-gray-500">
                        {ex.statute_citation}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

export default function CrosswalkPage() {
  const { loading, exemptionCrosswalk } = useData()
  const [selectedJurisdiction, setSelectedJurisdiction] = useState('')

  // Sort by count descending
  const sorted = useMemo(() => {
    if (!exemptionCrosswalk) return []
    const list = [...exemptionCrosswalk].sort((a, b) => b.count - a.count)
    if (!selectedJurisdiction) return list
    return list.filter(cat =>
      cat.exemptions.some(ex => ex.jurisdiction === selectedJurisdiction)
    )
  }, [exemptionCrosswalk, selectedJurisdiction])

  // Unique jurisdictions across all categories
  const jurisdictions = useMemo(() => {
    if (!exemptionCrosswalk) return []
    const seen = new Set()
    exemptionCrosswalk.forEach(cat => {
      cat.exemptions.forEach(ex => seen.add(ex.jurisdiction))
    })
    return [...seen].sort()
  }, [exemptionCrosswalk])

  // Summary stats
  const totalCategories = exemptionCrosswalk ? exemptionCrosswalk.length : 0
  const totalJurisdictions = jurisdictions.length

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Exemption Crosswalk</h1>
        <p className="text-gray-500 text-sm">
          Exemption categories cross-walked across jurisdictions. Find equivalent exemptions
          in different states.
        </p>
      </div>

      {loading ? (
        <div className="animate-pulse space-y-3">
          {[...Array(6)].map((_, i) => <div key={i} className="h-20 bg-gray-200 rounded-lg" />)}
        </div>
      ) : (
        <>
          {/* Summary */}
          <div className="text-sm text-gray-500 mb-4">
            {totalCategories} exemption categor{totalCategories !== 1 ? 'ies' : 'y'} across {totalJurisdictions} jurisdiction{totalJurisdictions !== 1 ? 's' : ''}
          </div>

          {/* Filter */}
          <div className="flex flex-wrap gap-3 mb-6">
            <select
              value={selectedJurisdiction}
              onChange={e => setSelectedJurisdiction(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
            >
              <option value="">All jurisdictions</option>
              {jurisdictions.map(j => (
                <option key={j} value={j}>{getStateName(j)} ({j})</option>
              ))}
            </select>

            {selectedJurisdiction && (
              <div className="flex items-center text-sm text-gray-500">
                Showing categories with exemptions in {getStateName(selectedJurisdiction)}
              </div>
            )}
          </div>

          {/* Category cards */}
          {sorted.length === 0 ? (
            <div className="text-center py-12 text-gray-400">
              No categories found{selectedJurisdiction ? ` for ${getStateName(selectedJurisdiction)}` : ''}.
            </div>
          ) : (
            <div className="space-y-3">
              {sorted.map(cat => (
                <CategoryCard key={cat.category} category={cat} />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}
