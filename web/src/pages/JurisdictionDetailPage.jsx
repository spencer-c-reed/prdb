import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useData } from '../data/DataContext'
import { getStateName, getLawName } from '../utils/states'
import Badge from '../components/Badge'
import CopyButton from '../components/CopyButton'

function QuickFacts({ rules }) {
  const byType = {}
  rules.forEach(r => {
    if (!byType[r.rule_type]) byType[r.rule_type] = []
    byType[r.rule_type].push(r)
  })

  const types = {
    initial_response: 'Initial Response',
    extension: 'Extension',
    appeal_deadline: 'Appeal Deadline',
    judicial_review_deadline: 'Judicial Review',
    fee_cap: 'Fee Cap',
    fee_waiver: 'Fee Waiver',
  }

  const entries = Object.entries(byType).filter(([k]) => types[k])

  if (entries.length === 0) return null

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-5 mb-6">
      <h2 className="text-base font-semibold text-gray-900 mb-4">Quick Facts</h2>
      <dl className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-3">
        {entries.map(([type, ruleList]) => (
          <div key={type}>
            <dt className="text-xs font-medium text-gray-500 uppercase tracking-wide">
              {types[type] || type}
            </dt>
            {ruleList.map(r => (
              <dd key={r.id || `${r.rule_type}-${r.param_key}`} className="text-sm text-gray-800 mt-0.5">
                {r.param_key.replace(/_/g, ' ')}: <strong>{r.param_value}</strong>
                {r.day_type && <span className="text-gray-400"> ({r.day_type} days)</span>}
                {r.statute_citation && (
                  <span className="text-gray-400 text-xs ml-1">— {r.statute_citation}</span>
                )}
              </dd>
            ))}
          </div>
        ))}
      </dl>
    </div>
  )
}

function ExemptionCard({ exemption }) {
  const [expanded, setExpanded] = useState(false)

  let counterArgs = null
  if (exemption.counter_arguments) {
    try {
      counterArgs = typeof exemption.counter_arguments === 'string'
        ? JSON.parse(exemption.counter_arguments)
        : exemption.counter_arguments
    } catch { /* ignore */ }
  }

  return (
    <div className="border border-gray-200 rounded-lg p-4 bg-white mb-3">
      <div className="flex items-start gap-3 mb-2">
        <Badge variant="default">{exemption.exemption_number || 'N/A'}</Badge>
        {exemption.category && <Badge variant="amber">{exemption.category}</Badge>}
        <div className="flex-1 min-w-0">
          {exemption.short_name && (
            <div className="font-semibold text-gray-900 text-sm">{exemption.short_name}</div>
          )}
          <div className="text-xs text-gray-400 mt-0.5">{exemption.statute_citation}</div>
        </div>
        <Link
          to={`/exemptions/${exemption.id}`}
          className="text-xs text-blue-600 hover:text-blue-700 shrink-0"
        >
          Details →
        </Link>
      </div>

      {exemption.description && (
        <p className="text-sm text-gray-600 mt-2">{exemption.description}</p>
      )}

      {(counterArgs || exemption.scope) && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="mt-3 text-xs text-blue-600 hover:text-blue-700 font-medium"
        >
          {expanded ? '▲ Hide' : '▼ Show'} challenge strategies
        </button>
      )}

      {expanded && (
        <div className="mt-3 pt-3 border-t border-gray-100">
          {exemption.scope && (
            <div className="mb-3">
              <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Scope</div>
              <p className="text-sm text-gray-600">{exemption.scope}</p>
            </div>
          )}
          {counterArgs && (
            <div>
              <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Challenge Strategies</div>
              {Array.isArray(counterArgs) ? (
                <ul className="space-y-1">
                  {counterArgs.map((arg, i) => (
                    <li key={i} className="text-sm text-gray-600 flex gap-2">
                      <span className="text-blue-400 shrink-0">·</span>
                      <span>{typeof arg === 'string' ? arg : JSON.stringify(arg)}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-gray-600">{JSON.stringify(counterArgs)}</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function RulesTable({ rules }) {
  const grouped = {}
  rules.forEach(r => {
    const key = r.rule_type || 'other'
    if (!grouped[key]) grouped[key] = []
    grouped[key].push(r)
  })

  if (Object.keys(grouped).length === 0) return null

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left border-b border-gray-200">
            <th className="pb-2 pr-4 text-xs font-semibold text-gray-500 uppercase tracking-wide">Rule Type</th>
            <th className="pb-2 pr-4 text-xs font-semibold text-gray-500 uppercase tracking-wide">Parameter</th>
            <th className="pb-2 pr-4 text-xs font-semibold text-gray-500 uppercase tracking-wide">Value</th>
            <th className="pb-2 pr-4 text-xs font-semibold text-gray-500 uppercase tracking-wide">Day Type</th>
            <th className="pb-2 text-xs font-semibold text-gray-500 uppercase tracking-wide">Citation</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(grouped).map(([type, ruleList]) =>
            ruleList.map((r, i) => (
              <tr key={r.id || i} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-2 pr-4 text-gray-700 capitalize">{type.replace(/_/g, ' ')}</td>
                <td className="py-2 pr-4 text-gray-600">{r.param_key?.replace(/_/g, ' ')}</td>
                <td className="py-2 pr-4 font-medium text-gray-900">{r.param_value}</td>
                <td className="py-2 pr-4 text-gray-500 capitalize">{r.day_type || '—'}</td>
                <td className="py-2 text-gray-400 text-xs">{r.statute_citation || '—'}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}

function TemplateCard({ template }) {
  const text = template.template_text || ''

  // Highlight {{placeholders}} in yellow
  function renderHighlighted(str) {
    const parts = str.split(/(\{\{[^}]+\}\})/g)
    return parts.map((part, i) =>
      /^\{\{.+\}\}$/.test(part)
        ? <mark key={i} className="bg-yellow-200 text-yellow-900 rounded px-0.5">{part}</mark>
        : part
    )
  }

  return (
    <div className="border border-gray-200 rounded-lg p-4 bg-white mb-4">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div>
          <div className="font-semibold text-gray-900">{template.template_name}</div>
          {template.record_type && (
            <div className="text-xs text-gray-400 mt-0.5">{template.record_type}</div>
          )}
        </div>
        <CopyButton text={text} />
      </div>
      <pre className="text-xs font-mono bg-gray-50 border border-gray-100 rounded p-3 whitespace-pre-wrap leading-relaxed overflow-x-auto">
        {renderHighlighted(text)}
      </pre>
    </div>
  )
}

export default function JurisdictionDetailPage() {
  const { code } = useParams()
  const { loading, getExemptions, getRules, getTemplates, getAgencies, getDocuments, getJurisdiction } = useData()

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/2 mb-4" />
        <div className="h-48 bg-gray-200 rounded mb-4" />
        <div className="h-64 bg-gray-200 rounded" />
      </div>
    )
  }

  const jData = getJurisdiction(code)
  const exemptions = getExemptions(code)
  const rules = getRules(code)
  const templates = getTemplates(code)
  const agencies = getAgencies(code)
  const documents = getDocuments(code)
  const name = jData?.name || getStateName(code)
  const lawName = jData?.law_name || getLawName(code)

  // Pull statute citation from jurisdictions data, rules, or exemptions
  const citationSource = jData?.statute_citation
    || rules.find(r => r.statute_citation)?.statute_citation
    || exemptions.find(e => e.statute_citation)?.statute_citation
    || null

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Breadcrumb */}
      <nav className="text-sm text-gray-400 mb-6">
        <Link to="/" className="hover:text-gray-600">Home</Link>
        <span className="mx-2">·</span>
        <Link to="/jurisdictions" className="hover:text-gray-600">Jurisdictions</Link>
        <span className="mx-2">·</span>
        <span className="text-gray-700">{code}</span>
      </nav>

      {/* Header */}
      <div className="mb-6">
        <div className="flex items-start gap-3 mb-2">
          <span className="inline-block px-3 py-1 bg-blue-100 text-blue-700 rounded text-sm font-bold mt-1">
            {code}
          </span>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{name} Public Records Guide</h1>
            <div className="text-gray-500 text-sm mt-1">{lawName}</div>
            {citationSource && (
              <div className="text-gray-400 text-xs mt-1">{citationSource}</div>
            )}
          </div>
        </div>
      </div>

      {/* Quick facts from structured jurisdiction data */}
      {jData && (jData.response_days || jData.response_description || jData.fee_info || jData.appeal_info) && (
        <div className="bg-white border border-gray-200 rounded-lg p-5 mb-6">
          <h2 className="text-base font-semibold text-gray-900 mb-4">Quick Facts</h2>
          <div className="space-y-4">
            {jData.response_days && (
              <div>
                <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Response Deadline</div>
                <p className="text-sm text-gray-700">
                  <strong>{jData.response_days} {jData.response_type || ''} days</strong>
                  {jData.response_description && (
                    <span className="text-gray-500"> — {jData.response_description}</span>
                  )}
                </p>
              </div>
            )}
            {jData.fee_info && (
              <div>
                <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Fees</div>
                <p className="text-sm text-gray-600">{jData.fee_info}</p>
              </div>
            )}
            {jData.appeal_info && (
              <div>
                <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Appeals</div>
                <p className="text-sm text-gray-600">{jData.appeal_info}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Quick facts from rules table (fallback/supplement) */}
      {!jData && rules.length > 0 && <QuickFacts rules={rules} />}

      {/* Exemptions */}
      {exemptions.length > 0 && (
        <section className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">
              Exemptions <span className="text-gray-400 font-normal text-base">({exemptions.length})</span>
            </h2>
            <Link to={`/exemptions?jurisdiction=${code}`} className="text-sm text-blue-600 hover:text-blue-700">
              Filter exemptions →
            </Link>
          </div>
          {exemptions.map(e => (
            <ExemptionCard key={e.id} exemption={e} />
          ))}
        </section>
      )}

      {/* Response rules table */}
      {rules.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Response Rules</h2>
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <RulesTable rules={rules} />
          </div>
        </section>
      )}

      {/* Agencies */}
      {agencies.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Agencies <span className="text-gray-400 font-normal text-base">({agencies.length})</span>
          </h2>
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-50 border-b border-gray-200 text-left">
                    <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Agency</th>
                    <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Level</th>
                    <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Submission</th>
                    <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">Details</th>
                  </tr>
                </thead>
                <tbody>
                  {agencies.map(a => (
                    <tr key={a.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="px-4 py-3 font-medium text-gray-900">{a.name}</td>
                      <td className="px-4 py-3 text-gray-500 capitalize">{a.level || '—'}</td>
                      <td className="px-4 py-3 text-gray-500 capitalize">{a.submission_method || '—'}</td>
                      <td className="px-4 py-3">
                        <Link to={`/agencies/${a.id}`} className="text-blue-600 hover:text-blue-700 text-xs">
                          View →
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>
      )}

      {/* Templates */}
      {templates.length > 0 && (
        <section className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-900">
              Request Templates <span className="text-gray-400 font-normal text-base">({templates.length})</span>
            </h2>
            <Link to={`/templates?jurisdiction=${code}`} className="text-sm text-blue-600 hover:text-blue-700">
              All templates →
            </Link>
          </div>
          {templates.map(t => (
            <TemplateCard key={t.id} template={t} />
          ))}
        </section>
      )}

      {/* Related documents */}
      {documents.length > 0 && (
        <section className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Related Documents <span className="text-gray-400 font-normal text-base">({documents.length})</span>
          </h2>
          <div className="bg-white border border-gray-200 rounded-lg divide-y divide-gray-100">
            {documents.slice(0, 20).map(d => (
              <div key={d.id} className="px-4 py-3 hover:bg-gray-50">
                <div className="flex items-start gap-3">
                  <Badge variant="gray">{d.document_type}</Badge>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium text-gray-900 truncate">{d.title}</div>
                    {d.citation && <div className="text-xs text-gray-400 mt-0.5">{d.citation}</div>}
                    {d.date && <div className="text-xs text-gray-400">{d.date}</div>}
                  </div>
                </div>
              </div>
            ))}
            {documents.length > 20 && (
              <div className="px-4 py-3 text-sm text-gray-400">
                + {documents.length - 20} more documents
              </div>
            )}
          </div>
        </section>
      )}

      {exemptions.length === 0 && rules.length === 0 && templates.length === 0 && agencies.length === 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-8 text-center text-gray-500">
          <p className="text-lg mb-2">No data for {name}</p>
          <p className="text-sm">Check back once data has been ingested for this jurisdiction.</p>
        </div>
      )}
    </div>
  )
}
