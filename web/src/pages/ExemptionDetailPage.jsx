import { useParams, Link } from 'react-router-dom'
import { useData } from '../data/DataContext'
import { getStateName } from '../utils/states'
import Badge from '../components/Badge'

export default function ExemptionDetailPage() {
  const { id } = useParams()
  const { loading, exemptions } = useData()

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/2 mb-4" />
        <div className="h-64 bg-gray-200 rounded" />
      </div>
    )
  }

  const exemption = exemptions.find(e => String(e.id) === String(id))

  if (!exemption) {
    return (
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <p className="text-gray-500">Exemption not found.</p>
        <Link to="/exemptions" className="text-blue-600 hover:text-blue-700 text-sm mt-2 inline-block">
          ← Back to exemptions
        </Link>
      </div>
    )
  }

  const e = exemption

  let counterArgs = null
  if (e.counter_arguments) {
    try {
      counterArgs = typeof e.counter_arguments === 'string'
        ? JSON.parse(e.counter_arguments)
        : e.counter_arguments
    } catch { /* ignore */ }
  }

  let keyTerms = null
  if (e.key_terms) {
    try {
      keyTerms = typeof e.key_terms === 'string' ? JSON.parse(e.key_terms) : e.key_terms
    } catch { /* ignore */ }
  }

  let relatedCaseLaw = null
  if (e.related_case_law) {
    try {
      relatedCaseLaw = typeof e.related_case_law === 'string'
        ? JSON.parse(e.related_case_law)
        : e.related_case_law
    } catch { /* ignore */ }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Breadcrumb */}
      <nav className="text-sm text-gray-400 mb-6">
        <Link to="/" className="hover:text-gray-600">Home</Link>
        <span className="mx-2">·</span>
        <Link to="/exemptions" className="hover:text-gray-600">Exemptions</Link>
        <span className="mx-2">·</span>
        <span className="text-gray-700">{e.short_name || e.exemption_number || id}</span>
      </nav>

      {/* Header */}
      <div className="mb-6">
        <div className="flex flex-wrap gap-2 mb-3">
          <Badge variant="default">{e.jurisdiction}</Badge>
          {e.exemption_number && <Badge variant="gray">{e.exemption_number}</Badge>}
          {e.category && <Badge variant="amber">{e.category}</Badge>}
        </div>
        <h1 className="text-2xl font-bold text-gray-900 mb-1">
          {e.short_name || e.statute_citation}
        </h1>
        <div className="text-gray-400 text-sm">{e.statute_citation}</div>
        <div className="mt-2">
          <Link to={`/jurisdictions/${e.jurisdiction}`} className="text-sm text-blue-600 hover:text-blue-700">
            {getStateName(e.jurisdiction)} →
          </Link>
        </div>
      </div>

      {/* Description */}
      {e.description && (
        <section className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">Description</h2>
          <p className="text-gray-700 leading-relaxed">{e.description}</p>
        </section>
      )}

      {/* Scope */}
      {e.scope && (
        <section className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">Scope</h2>
          <p className="text-gray-700 leading-relaxed">{e.scope}</p>
        </section>
      )}

      {/* Key terms */}
      {keyTerms && keyTerms.length > 0 && (
        <section className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Key Terms</h2>
          <div className="flex flex-wrap gap-2">
            {keyTerms.map((term, i) => (
              <span key={i} className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-sm">
                {typeof term === 'string' ? term : JSON.stringify(term)}
              </span>
            ))}
          </div>
        </section>
      )}

      {/* Counter arguments */}
      {counterArgs && (
        <section className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
            Challenge Strategies
          </h2>
          {Array.isArray(counterArgs) ? (
            <ul className="space-y-2">
              {counterArgs.map((arg, i) => (
                <li key={i} className="flex gap-3">
                  <span className="text-blue-400 shrink-0 mt-0.5">·</span>
                  <span className="text-gray-700 text-sm leading-relaxed">
                    {typeof arg === 'string' ? arg : JSON.stringify(arg)}
                  </span>
                </li>
              ))}
            </ul>
          ) : typeof counterArgs === 'object' ? (
            <div className="space-y-3">
              {Object.entries(counterArgs).map(([key, val]) => (
                <div key={key}>
                  <div className="text-xs font-semibold text-gray-400 uppercase mb-1">{key}</div>
                  <p className="text-sm text-gray-700">{typeof val === 'string' ? val : JSON.stringify(val)}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-700">{String(counterArgs)}</p>
          )}
        </section>
      )}

      {/* Challenge rate */}
      {e.successful_challenge_rate != null && (
        <section className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">
            Successful Challenge Rate
          </h2>
          <div className="text-2xl font-bold text-blue-600">
            {(e.successful_challenge_rate * 100).toFixed(1)}%
          </div>
        </section>
      )}

      {/* Related case law */}
      {relatedCaseLaw && relatedCaseLaw.length > 0 && (
        <section className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">
            Related Case Law
          </h2>
          <ul className="space-y-1">
            {relatedCaseLaw.map((doc, i) => (
              <li key={i} className="text-sm text-gray-600">
                {typeof doc === 'string' ? doc : JSON.stringify(doc)}
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* Notes */}
      {e.notes && (
        <section className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">Notes</h2>
          <p className="text-sm text-gray-700">{e.notes}</p>
        </section>
      )}

      {/* Last verified */}
      {e.last_verified && (
        <div className="text-xs text-gray-400 mt-4">
          Last verified: {e.last_verified}
        </div>
      )}
    </div>
  )
}
