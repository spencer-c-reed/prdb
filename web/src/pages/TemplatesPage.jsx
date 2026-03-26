import { useState, useMemo } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { useData } from '../data/DataContext'
import { getStateName } from '../utils/states'
import CopyButton from '../components/CopyButton'
import Badge from '../components/Badge'

function renderHighlighted(str) {
  const parts = (str || '').split(/(\{\{[^}]+\}\})/g)
  return parts.map((part, i) =>
    /^\{\{.+\}\}$/.test(part)
      ? <mark key={i} className="bg-yellow-200 text-yellow-900 rounded px-0.5">{part}</mark>
      : part
  )
}

function TemplateCard({ template: t }) {
  const [preview, setPreview] = useState(false)
  const text = t.template_text || ''

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4 hover:border-blue-300 hover:shadow-sm transition-all">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex-1 min-w-0">
          <Link
            to={`/templates/${t.id}`}
            className="font-semibold text-gray-900 hover:text-blue-700 leading-tight"
          >
            {t.template_name}
          </Link>
          {t.record_type && (
            <div className="text-xs text-gray-400 mt-0.5">{t.record_type}</div>
          )}
        </div>
        <div className="flex gap-2 shrink-0">
          <CopyButton text={text} />
          <Link
            to={`/templates/${t.id}`}
            className="inline-flex items-center gap-1 px-3 py-1 text-sm rounded border border-gray-300 bg-white hover:bg-gray-50 text-gray-600"
          >
            View
          </Link>
        </div>
      </div>

      <div className="flex flex-wrap gap-2 mb-3">
        {t.jurisdiction && <Badge variant="default">{t.jurisdiction}</Badge>}
        {t.record_type && <Badge variant="gray">{t.record_type}</Badge>}
      </div>

      <button
        onClick={() => setPreview(!preview)}
        className="text-xs text-blue-600 hover:text-blue-700 font-medium"
      >
        {preview ? '▲ Hide preview' : '▼ Preview'}
      </button>

      {preview && text && (
        <pre className="mt-3 text-xs font-mono bg-gray-50 border border-gray-100 rounded p-3 whitespace-pre-wrap leading-relaxed overflow-x-auto max-h-48">
          {renderHighlighted(text)}
        </pre>
      )}
    </div>
  )
}

export default function TemplatesPage() {
  const { loading, templates } = useData()
  const [searchParams, setSearchParams] = useSearchParams()
  const [query, setQuery] = useState('')

  const selectedJurisdiction = searchParams.get('jurisdiction') || ''

  const jurisdictions = useMemo(() => {
    const seen = new Set()
    templates.forEach(t => { if (t.jurisdiction) seen.add(t.jurisdiction) })
    return [...seen].sort()
  }, [templates])

  const recordTypes = useMemo(() => {
    const seen = new Set()
    templates.forEach(t => { if (t.record_type) seen.add(t.record_type) })
    return [...seen].sort()
  }, [templates])

  const [recordTypeFilter, setRecordTypeFilter] = useState('')

  const filtered = useMemo(() => {
    let list = templates

    if (selectedJurisdiction) {
      list = list.filter(t => t.jurisdiction === selectedJurisdiction)
    }
    if (recordTypeFilter) {
      list = list.filter(t => t.record_type === recordTypeFilter)
    }
    if (query) {
      const q = query.toLowerCase()
      list = list.filter(t =>
        (t.template_name || '').toLowerCase().includes(q) ||
        (t.record_type || '').toLowerCase().includes(q) ||
        (t.template_text || '').toLowerCase().includes(q)
      )
    }

    return list
  }, [templates, selectedJurisdiction, recordTypeFilter, query])

  function setJurisdiction(j) {
    const params = {}
    if (j) params.jurisdiction = j
    if (recordTypeFilter) params.record_type = recordTypeFilter
    setSearchParams(params)
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Template Library</h1>
        <p className="text-gray-500 text-sm">
          Ready-to-use request templates with jurisdiction-specific language.
          <span className="text-yellow-600 font-medium ml-1">Yellow highlights</span> show fields to fill in.
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-6">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Search templates..."
          className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 flex-1 min-w-48"
        />

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

        {recordTypes.length > 0 && (
          <select
            value={recordTypeFilter}
            onChange={e => setRecordTypeFilter(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
          >
            <option value="">All record types</option>
            {recordTypes.map(rt => (
              <option key={rt} value={rt}>{rt}</option>
            ))}
          </select>
        )}
      </div>

      {loading ? (
        <div className="animate-pulse space-y-4">
          {[...Array(4)].map((_, i) => <div key={i} className="h-36 bg-gray-200 rounded-lg" />)}
        </div>
      ) : (
        <>
          <div className="text-sm text-gray-500 mb-4">
            {filtered.length} template{filtered.length !== 1 ? 's' : ''}
          </div>

          {filtered.length === 0 ? (
            <div className="text-center py-12 text-gray-400">No templates found.</div>
          ) : (
            <div className="space-y-4">
              {filtered.map(t => (
                <TemplateCard key={t.id} template={t} />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}
