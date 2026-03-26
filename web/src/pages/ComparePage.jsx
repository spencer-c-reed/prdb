import { useState, useMemo, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import { useData } from '../data/DataContext'
import { getStateName, getLawName, ALL_JURISDICTIONS } from '../utils/states'

const COMPARE_SECTIONS = [
  {
    label: 'Deadlines',
    ruleTypes: ['initial_response', 'extension'],
    params: ['days_to_respond', 'max_extension_days', 'extension_notice_days'],
  },
  {
    label: 'Fees',
    ruleTypes: ['fee_cap', 'fee_waiver'],
    params: ['search_fee_per_hour', 'copy_fee_per_page', 'max_fee', 'waiver_threshold'],
  },
  {
    label: 'Appeals',
    ruleTypes: ['appeal_deadline'],
    params: ['days_to_appeal', 'appeal_body'],
  },
  {
    label: 'Enforcement',
    ruleTypes: ['judicial_review_deadline'],
    params: ['days_to_file_suit', 'penalty_range', 'attorney_fees'],
  },
]

function JurisdictionSelector({ value, onChange, label, exclude = [] }) {
  return (
    <div>
      <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
        {label}
      </label>
      <select
        value={value}
        onChange={e => onChange(e.target.value)}
        className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
      >
        <option value="">— Select jurisdiction —</option>
        {ALL_JURISDICTIONS.map(code => (
          <option key={code} value={code} disabled={exclude.includes(code) && code !== value}>
            {getStateName(code)} ({code})
          </option>
        ))}
      </select>
    </div>
  )
}

function CompareTable({ jurisdictions, data }) {
  if (jurisdictions.filter(Boolean).length < 2) {
    return (
      <div className="text-center py-16 text-gray-400">
        Select at least two jurisdictions to compare.
      </div>
    )
  }

  const active = jurisdictions.filter(Boolean)

  return (
    <div className="space-y-8">
      {COMPARE_SECTIONS.map(section => {
        // Build rows: unique param_key values across selected jurisdictions for this section
        const rowKeys = new Set()
        active.forEach(code => {
          const rules = data[code] || []
          rules.forEach(r => {
            if (section.ruleTypes.includes(r.rule_type)) {
              rowKeys.add(`${r.rule_type}::${r.param_key}`)
            }
          })
        })

        if (rowKeys.size === 0) return null

        return (
          <div key={section.label}>
            <h3 className="text-base font-semibold text-gray-900 mb-3 pb-2 border-b border-gray-200">
              {section.label}
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left border-b border-gray-200">
                    <th className="pb-2 pr-6 text-xs font-semibold text-gray-500 uppercase tracking-wide w-48">
                      Rule
                    </th>
                    {active.map(code => (
                      <th key={code} className="pb-2 pr-6 text-xs font-semibold text-gray-700">
                        <div className="flex items-center gap-2">
                          <span className="inline-block px-1.5 py-0.5 bg-blue-100 text-blue-700 rounded text-xs font-bold">
                            {code}
                          </span>
                          <span className="truncate max-w-32">{getStateName(code)}</span>
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {[...rowKeys].map(rowKey => {
                    const [ruleType, paramKey] = rowKey.split('::')
                    return (
                      <tr key={rowKey} className="border-b border-gray-100 hover:bg-gray-50">
                        <td className="py-2.5 pr-6 text-gray-600">
                          <div className="capitalize">{ruleType.replace(/_/g, ' ')}</div>
                          <div className="text-xs text-gray-400">{paramKey.replace(/_/g, ' ')}</div>
                        </td>
                        {active.map(code => {
                          const rules = data[code] || []
                          const match = rules.find(
                            r => r.rule_type === ruleType && r.param_key === paramKey
                          )
                          return (
                            <td key={code} className="py-2.5 pr-6">
                              {match ? (
                                <div>
                                  <span className="font-medium text-gray-900">{match.param_value}</span>
                                  {match.day_type && (
                                    <span className="text-gray-400 text-xs ml-1">({match.day_type})</span>
                                  )}
                                  {match.statute_citation && (
                                    <div className="text-xs text-gray-400 mt-0.5">{match.statute_citation}</div>
                                  )}
                                </div>
                              ) : (
                                <span className="text-gray-300">—</span>
                              )}
                            </td>
                          )
                        })}
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )
      })}
    </div>
  )
}

export default function ComparePage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const { loading, getRules } = useData()

  const initialCodes = (searchParams.get('j') || '').split(',').filter(Boolean).slice(0, 3)
  const [selections, setSelections] = useState([
    initialCodes[0] || '',
    initialCodes[1] || '',
    initialCodes[2] || '',
  ])

  // Sync selections to URL
  useEffect(() => {
    const active = selections.filter(Boolean)
    if (active.length > 0) {
      setSearchParams({ j: active.join(',') })
    } else {
      setSearchParams({})
    }
  }, [selections])

  function setSelection(index, value) {
    setSelections(prev => {
      const next = [...prev]
      next[index] = value
      return next
    })
  }

  // Pre-load rules for selected jurisdictions
  const data = useMemo(() => {
    const out = {}
    selections.filter(Boolean).forEach(code => {
      out[code] = getRules(code)
    })
    return out
  }, [selections, getRules])

  const activeSelections = selections.filter(Boolean)

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Compare Jurisdictions</h1>
        <p className="text-gray-500 text-sm">
          Side-by-side comparison of response deadlines, fees, appeal rights, and enforcement.
        </p>
      </div>

      {/* Selectors */}
      <div className="bg-white border border-gray-200 rounded-lg p-5 mb-8">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <JurisdictionSelector
            label="Jurisdiction 1"
            value={selections[0]}
            onChange={v => setSelection(0, v)}
            exclude={[selections[1], selections[2]]}
          />
          <JurisdictionSelector
            label="Jurisdiction 2"
            value={selections[1]}
            onChange={v => setSelection(1, v)}
            exclude={[selections[0], selections[2]]}
          />
          <JurisdictionSelector
            label="Jurisdiction 3 (optional)"
            value={selections[2]}
            onChange={v => setSelection(2, v)}
            exclude={[selections[0], selections[1]]}
          />
        </div>

        {activeSelections.length >= 2 && (
          <div className="mt-4 flex gap-4">
            {activeSelections.map(code => (
              <div key={code} className="text-xs text-gray-500">
                <span className="font-semibold text-gray-700">{code}:</span> {getLawName(code)}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Comparison table */}
      {loading ? (
        <div className="animate-pulse space-y-6">
          {[...Array(4)].map((_, i) => <div key={i} className="h-40 bg-gray-200 rounded-lg" />)}
        </div>
      ) : (
        <div className="bg-white border border-gray-200 rounded-lg p-5">
          <CompareTable jurisdictions={selections} data={data} />
        </div>
      )}

      {/* Share link */}
      {activeSelections.length >= 2 && (
        <div className="mt-4 text-xs text-gray-400">
          Share this comparison:{' '}
          <span className="font-mono bg-gray-100 px-2 py-0.5 rounded">
            {window.location.href}
          </span>
        </div>
      )}
    </div>
  )
}
