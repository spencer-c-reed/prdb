import { useParams, Link } from 'react-router-dom'
import { useData } from '../data/DataContext'
import { getStateName } from '../utils/states'
import Badge from '../components/Badge'
import CopyButton from '../components/CopyButton'

function renderHighlighted(str) {
  const parts = (str || '').split(/(\{\{[^}]+\}\})/g)
  return parts.map((part, i) =>
    /^\{\{.+\}\}$/.test(part)
      ? <mark key={i} className="bg-yellow-200 text-yellow-900 rounded px-0.5">{part}</mark>
      : part
  )
}

export default function TemplateDetailPage() {
  const { id } = useParams()
  const { loading, templates } = useData()

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/2 mb-4" />
        <div className="h-96 bg-gray-200 rounded" />
      </div>
    )
  }

  const template = templates.find(t => String(t.id) === String(id))

  if (!template) {
    return (
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <p className="text-gray-500">Template not found.</p>
        <Link to="/templates" className="text-blue-600 hover:text-blue-700 text-sm mt-2 inline-block">
          ← Back to templates
        </Link>
      </div>
    )
  }

  const t = template
  const text = t.template_text || ''

  // Extract placeholder list
  const placeholders = [...new Set([...text.matchAll(/\{\{([^}]+)\}\}/g)].map(m => m[1]))]

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Breadcrumb */}
      <nav className="text-sm text-gray-400 mb-6">
        <Link to="/" className="hover:text-gray-600">Home</Link>
        <span className="mx-2">·</span>
        <Link to="/templates" className="hover:text-gray-600">Templates</Link>
        <span className="mx-2">·</span>
        <span className="text-gray-700">{t.template_name}</span>
      </nav>

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-3">{t.template_name}</h1>
        <div className="flex flex-wrap gap-2 mb-3">
          {t.jurisdiction && <Badge variant="default">{t.jurisdiction}</Badge>}
          {t.record_type && <Badge variant="gray">{t.record_type}</Badge>}
        </div>
        {t.jurisdiction && t.jurisdiction !== 'Federal' && (
          <Link to={`/jurisdictions/${t.jurisdiction}`} className="text-sm text-blue-600 hover:text-blue-700">
            {getStateName(t.jurisdiction)} public records law →
          </Link>
        )}
      </div>

      {/* Actions */}
      <div className="flex gap-3 mb-6">
        <CopyButton text={text} />
      </div>

      {/* Placeholders legend */}
      {placeholders.length > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <div className="text-sm font-semibold text-yellow-800 mb-2">
            Fill in these fields before sending:
          </div>
          <div className="flex flex-wrap gap-2">
            {placeholders.map(p => (
              <span key={p} className="px-2 py-1 bg-yellow-200 text-yellow-900 rounded text-xs font-mono">
                {`{{${p}}}`}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Template text */}
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <div className="bg-gray-50 border-b border-gray-200 px-4 py-2 flex items-center justify-between">
          <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Template Text</span>
          <CopyButton text={text} />
        </div>
        <pre className="p-5 text-sm font-mono whitespace-pre-wrap leading-relaxed overflow-x-auto">
          {renderHighlighted(text)}
        </pre>
      </div>

      {/* Description */}
      {t.description && (
        <section className="bg-white border border-gray-200 rounded-lg p-5 mt-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">About This Template</h2>
          <p className="text-sm text-gray-700 leading-relaxed">{t.description}</p>
        </section>
      )}

      {/* Notes */}
      {t.notes && (
        <section className="bg-white border border-gray-200 rounded-lg p-5 mt-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">Notes</h2>
          <p className="text-sm text-gray-700">{t.notes}</p>
        </section>
      )}
    </div>
  )
}
