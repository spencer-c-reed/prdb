import { useState, useMemo } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useData } from '../data/DataContext'
import { getStateName } from '../utils/states'
import Badge from '../components/Badge'

const STATUTE_TYPES = [
  'State Public Records Statute',
  'Federal FOIA Statute',
  'State CPRA Statute',
  'State TPIA Statute',
  'Open Meetings Statute',
  'Privacy Act Statute',
]

function typeBadgeVariant(docType) {
  if (STATUTE_TYPES.includes(docType)) return 'green'
  if (docType === 'State Court Opinion' || docType === 'Circuit Court Opinion') return 'purple'
  if (docType === 'AG Opinion' || docType === 'Administrative Decision') return 'amber'
  return 'default'
}

function DocumentCard({ doc }) {
  const summary = doc.summary || ''
  const truncated = summary.length > 200 ? summary.slice(0, 200) + '...' : summary

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 hover:border-blue-300 hover:shadow-sm transition-all">
      <div className="flex flex-wrap gap-2 mb-2">
        <Badge variant={typeBadgeVariant(doc.document_type)}>{doc.document_type}</Badge>
        {doc.jurisdiction && <Badge variant="default">{doc.jurisdiction}</Badge>}
      </div>

      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <Link
            to={`/documents/${doc.id}`}
            className="text-base font-semibold text-gray-900 hover:text-blue-700 leading-tight"
          >
            {doc.title}
          </Link>
          {doc.citation && (
            <div className="text-xs text-gray-400 mt-0.5">{doc.citation}</div>
          )}
        </div>
        <Link to={`/documents/${doc.id}`} className="text-xs text-blue-600 hover:text-blue-700 shrink-0">
          Full detail
        </Link>
      </div>

      <div className="flex flex-wrap gap-3 text-xs text-gray-500 mt-2">
        {doc.court && <span>{doc.court}</span>}
        {doc.date && <span>{doc.date}</span>}
      </div>

      {summary && (
        <p className="text-sm text-gray-600 mt-2 leading-relaxed">{truncated}</p>
      )}
    </div>
  )
}

export default function DocumentsPage() {
  const { loading, documents, getDocuments } = useData()
  const [searchParams, setSearchParams] = useSearchParams()
  const [query, setQuery] = useState('')
  const [sortBy, setSortBy] = useState('date')

  const selectedJurisdiction = searchParams.get('jurisdiction') || ''
  const selectedType = searchParams.get('type') || ''

  const allDocs = selectedJurisdiction ? getDocuments(selectedJurisdiction) : documents

  const jurisdictions = useMemo(() => {
    const seen = new Set()
    documents.forEach(d => { if (d.jurisdiction) seen.add(d.jurisdiction) })
    return [...seen].sort()
  }, [documents])

  const docTypes = useMemo(() => {
    const seen = new Set()
    documents.forEach(d => { if (d.document_type) seen.add(d.document_type) })
    return [...seen].sort()
  }, [documents])

  const filtered = useMemo(() => {
    let list = allDocs

    if (selectedType) {
      list = list.filter(d => d.document_type === selectedType)
    }

    if (query) {
      const q = query.toLowerCase()
      list = list.filter(d =>
        (d.title || '').toLowerCase().includes(q) ||
        (d.citation || '').toLowerCase().includes(q)
      )
    }

    list = [...list].sort((a, b) => {
      if (sortBy === 'date') {
        return (b.date || '').localeCompare(a.date || '')
      }
      return (a.jurisdiction || '').localeCompare(b.jurisdiction || '')
    })

    return list
  }, [allDocs, selectedType, query, sortBy])

  function updateParams(updates) {
    const params = {}
    const next = { jurisdiction: selectedJurisdiction, type: selectedType, ...updates }
    if (next.jurisdiction) params.jurisdiction = next.jurisdiction
    if (next.type) params.type = next.type
    setSearchParams(params)
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Document Library</h1>
        <p className="text-gray-500 text-sm">
          Browse statutes, case law, AG opinions, and agency guidance across jurisdictions.
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Search by title or citation..."
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 flex-1 min-w-48"
        />

        <select
          value={selectedType}
          onChange={e => updateParams({ type: e.target.value })}
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
        >
          <option value="">All document types</option>
          {docTypes.map(dt => (
            <option key={dt} value={dt}>{dt}</option>
          ))}
        </select>

        <select
          value={selectedJurisdiction}
          onChange={e => updateParams({ jurisdiction: e.target.value })}
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
        >
          <option value="">All jurisdictions</option>
          {jurisdictions.map(j => (
            <option key={j} value={j}>{getStateName(j)} ({j})</option>
          ))}
        </select>

        <select
          value={sortBy}
          onChange={e => setSortBy(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
        >
          <option value="date">Newest first</option>
          <option value="jurisdiction">By jurisdiction</option>
        </select>
      </div>

      {loading ? (
        <div className="animate-pulse space-y-3">
          {[...Array(6)].map((_, i) => <div key={i} className="h-32 bg-gray-200 rounded-lg" />)}
        </div>
      ) : (
        <>
          <div className="text-sm text-gray-500 mb-4">
            Showing {filtered.length} of {documents.length} document{documents.length !== 1 ? 's' : ''}
            {selectedJurisdiction && ` in ${getStateName(selectedJurisdiction)}`}
            {selectedType && ` — ${selectedType}`}
          </div>

          {filtered.length === 0 ? (
            <div className="text-center py-12 text-gray-400">
              No documents found matching your filters.
            </div>
          ) : (
            <div className="space-y-3">
              {filtered.map(d => (
                <DocumentCard key={d.id} doc={d} />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}
