import { useMemo } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useData } from '../data/DataContext'
import { getStateName } from '../utils/states'
import Badge from '../components/Badge'
import SearchBar from '../components/SearchBar'

const TYPE_ROUTE = {
  exemption: (id) => `/exemptions/${id}`,
  agency: (id) => `/agencies/${id}`,
  template: (id) => `/templates/${id}`,
  statute: (id, jur) => `/jurisdictions/${jur}`,
  'ag opinion': (id) => `/search`,
  'court decision': (id) => `/search`,
}

function getRoute(result) {
  const type = (result.document_type || '').toLowerCase()
  const fn = TYPE_ROUTE[type]
  if (fn) return fn(result.id, result.jurisdiction)
  if (result.jurisdiction && result.jurisdiction !== 'Federal') {
    return `/jurisdictions/${result.jurisdiction}`
  }
  return null
}

const TYPE_VARIANT = {
  exemption: 'default',
  agency: 'green',
  template: 'purple',
  statute: 'gray',
  'ag opinion': 'amber',
  'court decision': 'red',
}

export default function SearchPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const { search, loading, documents, exemptions, agencies, templates } = useData()

  const query = searchParams.get('q') || ''
  const typeFilter = searchParams.get('type') || ''
  const jurisdictionFilter = searchParams.get('jurisdiction') || ''

  const results = useMemo(() => {
    if (!query) return []
    return search(query, { limit: 100 })
  }, [query, search])

  // Fallback: also search local arrays if search index not loaded
  const localResults = useMemo(() => {
    if (results.length > 0 || !query) return []
    const q = query.toLowerCase()

    const ex = exemptions.filter(e =>
      (e.short_name || '').toLowerCase().includes(q) ||
      (e.description || '').toLowerCase().includes(q) ||
      (e.statute_citation || '').toLowerCase().includes(q)
    ).map(e => ({ ...e, document_type: 'exemption', _score: 1 }))

    const ag = agencies.filter(a =>
      (a.name || '').toLowerCase().includes(q) ||
      (a.abbreviation || '').toLowerCase().includes(q)
    ).map(a => ({ ...a, document_type: 'agency', title: a.name, _score: 1 }))

    const tmpl = templates.filter(t =>
      (t.template_name || '').toLowerCase().includes(q) ||
      (t.template_text || '').toLowerCase().includes(q)
    ).map(t => ({ ...t, document_type: 'template', title: t.template_name, _score: 1 }))

    const docs = documents.filter(d =>
      (d.title || '').toLowerCase().includes(q) ||
      (d.citation || '').toLowerCase().includes(q) ||
      (d.summary_ai || '').toLowerCase().includes(q)
    ).map(d => ({ ...d, _score: 1 }))

    return [...ex, ...ag, ...tmpl, ...docs].slice(0, 100)
  }, [query, results, exemptions, agencies, templates, documents])

  const allResults = results.length > 0 ? results : localResults

  // Facet counts
  const typeCounts = useMemo(() => {
    const counts = {}
    allResults.forEach(r => {
      const type = r.document_type || 'other'
      counts[type] = (counts[type] || 0) + 1
    })
    return counts
  }, [allResults])

  const jurisdictionCounts = useMemo(() => {
    const counts = {}
    allResults.forEach(r => {
      if (r.jurisdiction) {
        counts[r.jurisdiction] = (counts[r.jurisdiction] || 0) + 1
      }
    })
    return counts
  }, [allResults])

  // Apply facets
  const filtered = useMemo(() => {
    let list = allResults
    if (typeFilter) list = list.filter(r => r.document_type === typeFilter)
    if (jurisdictionFilter) list = list.filter(r => r.jurisdiction === jurisdictionFilter)
    return list
  }, [allResults, typeFilter, jurisdictionFilter])

  function setFilter(key, val) {
    const params = { q: query }
    if (key !== 'type' && typeFilter) params.type = typeFilter
    if (key !== 'jurisdiction' && jurisdictionFilter) params.jurisdiction = jurisdictionFilter
    if (val) params[key] = val
    setSearchParams(params)
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <SearchBar placeholder="Search again..." />
      </div>

      {!query ? (
        <div className="text-center py-16 text-gray-400">
          Enter a search query above.
        </div>
      ) : loading ? (
        <div className="animate-pulse space-y-3">
          {[...Array(6)].map((_, i) => <div key={i} className="h-24 bg-gray-200 rounded-lg" />)}
        </div>
      ) : (
        <div className="flex gap-6">
          {/* Facets sidebar */}
          {allResults.length > 0 && (
            <aside className="hidden md:block w-48 shrink-0">
              <div className="bg-white border border-gray-200 rounded-lg p-4">
                <div className="mb-4">
                  <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                    Type
                  </div>
                  <button
                    onClick={() => setFilter('type', '')}
                    className={`block w-full text-left text-sm py-1 px-2 rounded ${!typeFilter ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-600 hover:bg-gray-50'}`}
                  >
                    All ({allResults.length})
                  </button>
                  {Object.entries(typeCounts).sort((a, b) => b[1] - a[1]).map(([type, count]) => (
                    <button
                      key={type}
                      onClick={() => setFilter('type', type === typeFilter ? '' : type)}
                      className={`block w-full text-left text-sm py-1 px-2 rounded capitalize ${typeFilter === type ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-600 hover:bg-gray-50'}`}
                    >
                      {type} ({count})
                    </button>
                  ))}
                </div>

                {Object.keys(jurisdictionCounts).length > 1 && (
                  <div>
                    <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                      Jurisdiction
                    </div>
                    <button
                      onClick={() => setFilter('jurisdiction', '')}
                      className={`block w-full text-left text-sm py-1 px-2 rounded ${!jurisdictionFilter ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-600 hover:bg-gray-50'}`}
                    >
                      All
                    </button>
                    {Object.entries(jurisdictionCounts)
                      .sort((a, b) => b[1] - a[1])
                      .slice(0, 10)
                      .map(([jur, count]) => (
                        <button
                          key={jur}
                          onClick={() => setFilter('jurisdiction', jur === jurisdictionFilter ? '' : jur)}
                          className={`block w-full text-left text-sm py-1 px-2 rounded ${jurisdictionFilter === jur ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-600 hover:bg-gray-50'}`}
                        >
                          {jur} ({count})
                        </button>
                      ))
                    }
                  </div>
                )}
              </div>
            </aside>
          )}

          {/* Results */}
          <div className="flex-1 min-w-0">
            <div className="text-sm text-gray-500 mb-4">
              {filtered.length} result{filtered.length !== 1 ? 's' : ''} for &ldquo;{query}&rdquo;
            </div>

            {filtered.length === 0 ? (
              <div className="text-center py-12 text-gray-400">
                No results found. Try different search terms.
              </div>
            ) : (
              <div className="space-y-3">
                {filtered.map((result, i) => {
                  const route = getRoute(result)
                  const type = (result.document_type || 'other').toLowerCase()
                  const variant = TYPE_VARIANT[type] || 'gray'
                  const title = result.title || result.template_name || result.short_name || String(result.id)

                  return (
                    <div key={result.id || i} className="bg-white border border-gray-200 rounded-lg p-4 hover:border-blue-300 hover:shadow-sm transition-all">
                      <div className="flex items-start gap-3">
                        <Badge variant={variant}>{result.document_type || 'document'}</Badge>
                        {result.jurisdiction && (
                          <Badge variant="gray">{result.jurisdiction}</Badge>
                        )}
                      </div>
                      <div className="mt-2">
                        {route ? (
                          <Link to={route} className="text-base font-semibold text-gray-900 hover:text-blue-700">
                            {title}
                          </Link>
                        ) : (
                          <div className="text-base font-semibold text-gray-900">{title}</div>
                        )}
                        {result.citation && (
                          <div className="text-xs text-gray-400 mt-0.5">{result.citation}</div>
                        )}
                        {(result.description || result.summary_ai) && (
                          <p className="text-sm text-gray-600 mt-1 leading-relaxed line-clamp-2">
                            {result.description || result.summary_ai}
                          </p>
                        )}
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
