import { useParams, Link } from 'react-router-dom'
import { useData } from '../data/DataContext'
import { getStateName } from '../utils/states'
import Badge from '../components/Badge'

function badgeVariant(docType) {
  if (!docType) return 'default'
  const t = docType.toLowerCase()
  if (t.includes('statute')) return 'green'
  if (t.includes('court opinion') || t.includes('opinion')) return 'purple'
  if (t.includes('ag opinion') || t.includes('administrative')) return 'amber'
  return 'default'
}

function formatDate(dateStr) {
  if (!dateStr) return null
  try {
    const [y, m, d] = dateStr.split('-')
    const date = new Date(Number(y), Number(m) - 1, Number(d))
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })
  } catch {
    return dateStr
  }
}

export default function DocumentDetailPage() {
  const { id } = useParams()
  const { loading, documents } = useData()

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-pulse">
        <div className="h-4 bg-gray-200 rounded w-1/3 mb-6" />
        <div className="h-8 bg-gray-200 rounded w-2/3 mb-4" />
        <div className="h-6 bg-gray-200 rounded w-1/2 mb-6" />
        <div className="h-32 bg-gray-200 rounded mb-4" />
        <div className="h-48 bg-gray-200 rounded" />
      </div>
    )
  }

  const doc = documents.find(d => String(d.id) === String(id))

  if (!doc) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <p className="text-gray-500">Document not found.</p>
        <Link to="/" className="text-blue-600 hover:text-blue-700 text-sm mt-2 inline-block">
          Back to home
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Breadcrumb */}
      <nav className="text-sm text-gray-400 mb-6">
        <Link to="/" className="hover:text-gray-600">Home</Link>
        <span className="mx-2">/</span>
        <span className="hover:text-gray-600">Documents</span>
        <span className="mx-2">/</span>
        <span className="text-gray-700">{doc.title}</span>
      </nav>

      {/* Header */}
      <div className="mb-6">
        <div className="flex flex-wrap gap-2 mb-3">
          {doc.document_type && (
            <Badge variant={badgeVariant(doc.document_type)}>{doc.document_type}</Badge>
          )}
        </div>
        <h1 className="text-2xl font-bold text-gray-900 mb-1">{doc.title}</h1>
        {doc.citation && (
          <div className="text-gray-500 text-sm">{doc.citation}</div>
        )}
      </div>

      {/* Metadata */}
      <section className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Details</h2>
        <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-3 text-sm">
          {doc.court && (
            <div>
              <dt className="text-gray-400 font-medium">Court</dt>
              <dd className="text-gray-700">{doc.court}</dd>
            </div>
          )}
          {doc.date && (
            <div>
              <dt className="text-gray-400 font-medium">Date</dt>
              <dd className="text-gray-700">{formatDate(doc.date)}</dd>
            </div>
          )}
          {doc.jurisdiction && (
            <div>
              <dt className="text-gray-400 font-medium">Jurisdiction</dt>
              <dd>
                <Link
                  to={`/jurisdictions/${doc.jurisdiction}`}
                  className="text-blue-600 hover:text-blue-700"
                >
                  {getStateName(doc.jurisdiction)}
                </Link>
              </dd>
            </div>
          )}
          {doc.source && (
            <div>
              <dt className="text-gray-400 font-medium">Source</dt>
              <dd className="text-gray-700">{doc.source}</dd>
            </div>
          )}
        </dl>
      </section>

      {/* Summary */}
      {doc.summary && (
        <section className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">Summary</h2>
          <p className="text-gray-700 leading-relaxed">{doc.summary}</p>
        </section>
      )}

      {/* Source URL */}
      {doc.source_url && (
        <section className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">Source Document</h2>
          <a
            href={doc.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-700 text-sm underline"
          >
            View original source
          </a>
        </section>
      )}

      {/* Navigation */}
      <div className="mt-6 flex gap-4 text-sm">
        {doc.jurisdiction && (
          <Link
            to={`/jurisdictions/${doc.jurisdiction}`}
            className="text-blue-600 hover:text-blue-700"
          >
            {getStateName(doc.jurisdiction)} overview
          </Link>
        )}
      </div>
    </div>
  )
}
