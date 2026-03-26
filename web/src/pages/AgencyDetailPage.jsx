import { useParams, Link } from 'react-router-dom'
import { useData } from '../data/DataContext'
import { getStateName } from '../utils/states'
import Badge from '../components/Badge'

export default function AgencyDetailPage() {
  const { id } = useParams()
  const { loading, agencies } = useData()

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/2 mb-4" />
        <div className="h-64 bg-gray-200 rounded" />
      </div>
    )
  }

  const agency = agencies.find(a => String(a.id) === String(id))

  if (!agency) {
    return (
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <p className="text-gray-500">Agency not found.</p>
        <Link to="/agencies" className="text-blue-600 hover:text-blue-700 text-sm mt-2 inline-block">
          ← Back to agencies
        </Link>
      </div>
    )
  }

  const a = agency

  let feeSchedule = null
  if (a.fee_schedule) {
    try {
      feeSchedule = typeof a.fee_schedule === 'string' ? JSON.parse(a.fee_schedule) : a.fee_schedule
    } catch { /* ignore */ }
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Breadcrumb */}
      <nav className="text-sm text-gray-400 mb-6">
        <Link to="/" className="hover:text-gray-600">Home</Link>
        <span className="mx-2">·</span>
        <Link to="/agencies" className="hover:text-gray-600">Agencies</Link>
        <span className="mx-2">·</span>
        <span className="text-gray-700">{a.name}</span>
      </nav>

      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">{a.name}</h1>
        {a.abbreviation && <div className="text-gray-400 text-sm mb-2">{a.abbreviation}</div>}

        <div className="flex flex-wrap gap-2">
          {a.jurisdiction && <Badge variant="default">{a.jurisdiction}</Badge>}
          {a.level && <Badge variant="gray">{a.level}</Badge>}
          {a.submission_method && <Badge variant="green">{a.submission_method}</Badge>}
          {a.is_active === false && <Badge variant="red">Inactive</Badge>}
        </div>

        {a.jurisdiction && a.jurisdiction !== 'Federal' && (
          <div className="mt-3">
            <Link to={`/jurisdictions/${a.jurisdiction}`} className="text-sm text-blue-600 hover:text-blue-700">
              {getStateName(a.jurisdiction)} public records law →
            </Link>
          </div>
        )}
      </div>

      {/* Contact info */}
      <section className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
        <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">Contact Information</h2>
        <dl className="space-y-3">
          {a.foia_officer_name && (
            <div>
              <dt className="text-xs text-gray-400">FOIA Officer</dt>
              <dd className="text-sm text-gray-900">
                {a.foia_officer_name}
                {a.foia_officer_title && <span className="text-gray-500">, {a.foia_officer_title}</span>}
              </dd>
            </div>
          )}
          {a.email && (
            <div>
              <dt className="text-xs text-gray-400">Email</dt>
              <dd className="text-sm">
                <a href={`mailto:${a.email}`} className="text-blue-600 hover:underline">{a.email}</a>
              </dd>
            </div>
          )}
          {a.phone && (
            <div>
              <dt className="text-xs text-gray-400">Phone</dt>
              <dd className="text-sm">
                <a href={`tel:${a.phone}`} className="text-blue-600 hover:underline">{a.phone}</a>
              </dd>
            </div>
          )}
          {a.mailing_address && (
            <div>
              <dt className="text-xs text-gray-400">Mailing Address</dt>
              <dd className="text-sm text-gray-900 whitespace-pre-line">{a.mailing_address}</dd>
            </div>
          )}
          {a.portal_url && (
            <div>
              <dt className="text-xs text-gray-400">Online Portal</dt>
              <dd className="text-sm">
                <a
                  href={a.portal_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  {a.portal_url}
                </a>
              </dd>
            </div>
          )}
          {a.required_form_url && (
            <div>
              <dt className="text-xs text-gray-400">Required Form</dt>
              <dd className="text-sm">
                <a
                  href={a.required_form_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  Download form →
                </a>
              </dd>
            </div>
          )}
        </dl>
      </section>

      {/* Fee info */}
      {(feeSchedule || a.fee_waiver_available || a.fee_waiver_criteria) && (
        <section className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">Fees</h2>
          {feeSchedule && (
            <div className="mb-4">
              <div className="text-xs font-medium text-gray-400 mb-2">Fee Schedule</div>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <tbody>
                    {Object.entries(feeSchedule).map(([key, val]) => (
                      <tr key={key} className="border-b border-gray-100">
                        <td className="py-2 pr-4 text-gray-600 capitalize">{key.replace(/_/g, ' ')}</td>
                        <td className="py-2 font-medium text-gray-900">{String(val)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
          {a.fee_waiver_available && (
            <div className="flex items-center gap-2 mb-2">
              <svg className="w-4 h-4 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              <span className="text-sm text-gray-700">Fee waiver available</span>
            </div>
          )}
          {a.fee_waiver_criteria && (
            <p className="text-sm text-gray-600">{a.fee_waiver_criteria}</p>
          )}
        </section>
      )}

      {/* Performance */}
      {a.avg_response_days != null && (
        <section className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">Performance</h2>
          <div className="flex items-center gap-4">
            <div>
              <div className="text-2xl font-bold text-blue-600">{a.avg_response_days}</div>
              <div className="text-xs text-gray-400">avg. response days</div>
            </div>
          </div>
        </section>
      )}

      {/* Notes */}
      {a.notes && (
        <section className="bg-white border border-gray-200 rounded-lg p-5 mb-4">
          <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">Notes</h2>
          <p className="text-sm text-gray-700">{a.notes}</p>
        </section>
      )}

      {/* Source */}
      {(a.source_url || a.last_verified) && (
        <div className="text-xs text-gray-400 space-y-1">
          {a.source_url && (
            <div>
              Source:{' '}
              <a href={a.source_url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">
                {a.source_url}
              </a>
            </div>
          )}
          {a.last_verified && <div>Last verified: {a.last_verified}</div>}
          {a.last_scraped && <div>Last scraped: {a.last_scraped}</div>}
        </div>
      )}
    </div>
  )
}
