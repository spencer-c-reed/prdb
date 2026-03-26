import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../data/DataContext'
import Badge from '../components/Badge'

const PROVISION_LABELS = {
  fast_response: 'Fast Response (≤3 days)',
  low_fees: 'Low Fees (≤$0.10/page)',
  mandatory_attorney_fees: 'Mandatory Attorney Fees',
  per_diem_penalties: 'Per Diem Penalties',
  no_id_required: 'Anonymous Requests',
  presumption_of_openness: 'Presumption of Openness',
  segregability_required: 'Segregability Required',
}

const FACTOR_LABELS = {
  deadline: 'Response Deadline',
  fees: 'Fee Structure',
  fee_waiver: 'Fee Waiver',
  admin_appeal: 'Administrative Appeal',
  penalties: 'Penalties',
  segregability: 'Segregability',
  presumption: 'Presumption of Openness',
  anonymity: 'Requester Anonymity',
  exemption_count: 'Exemption Count',
}

const GRADE_FILTERS = [
  { label: 'All', value: '' },
  { label: 'A-range', value: 'A' },
  { label: 'B-range', value: 'B' },
  { label: 'C-range', value: 'C' },
  { label: 'D/F', value: 'DF' },
]

function gradeVariant(grade) {
  if (!grade) return 'gray'
  const letter = grade.charAt(0)
  if (letter === 'A') return 'green'
  if (letter === 'B') return 'default'
  if (letter === 'C') return 'amber'
  return 'red'
}

function matchesGradeFilter(grade, filter) {
  if (!filter) return true
  if (!grade) return false
  const letter = grade.charAt(0)
  if (filter === 'DF') return letter === 'D' || letter === 'F'
  return letter === filter
}

export default function ScorecardsPage() {
  const { loading, scorecards } = useData()
  const [gradeFilter, setGradeFilter] = useState('')
  const [sortKey, setSortKey] = useState('score')
  const [sortDir, setSortDir] = useState('desc')
  const [expandedRow, setExpandedRow] = useState(null)

  const sorted = useMemo(() => {
    if (!scorecards) return []

    const list = scorecards.filter(s => matchesGradeFilter(s.grade, gradeFilter))

    return [...list].sort((a, b) => {
      let cmp = 0
      if (sortKey === 'score') {
        cmp = a.score - b.score
      } else if (sortKey === 'name') {
        cmp = a.name.localeCompare(b.name)
      } else if (sortKey === 'grade') {
        cmp = a.score - b.score
      } else if (sortKey === 'code') {
        cmp = a.code.localeCompare(b.code)
      }
      return sortDir === 'asc' ? cmp : -cmp
    })
  }, [scorecards, gradeFilter, sortKey, sortDir])

  function handleSort(key) {
    if (sortKey === key) {
      setSortDir(d => (d === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortKey(key)
      setSortDir(key === 'name' || key === 'code' ? 'asc' : 'desc')
    }
  }

  function sortIndicator(key) {
    if (sortKey !== key) return ''
    return sortDir === 'asc' ? ' ▲' : ' ▼'
  }

  function toggleRow(code) {
    setExpandedRow(prev => (prev === code ? null : code))
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Transparency Scorecards</h1>
        <p className="text-gray-500 text-sm">
          Grading all 52 US jurisdictions on the strength of their public records laws.
        </p>
      </div>

      {/* Grade filter */}
      <div className="flex flex-wrap gap-2 mb-6">
        {GRADE_FILTERS.map(f => (
          <button
            key={f.value}
            onClick={() => setGradeFilter(f.value)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium border transition-colors ${
              gradeFilter === f.value
                ? 'bg-gray-900 text-white border-gray-900'
                : 'bg-white text-gray-600 border-gray-300 hover:border-gray-400'
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="animate-pulse space-y-3">
          {[...Array(8)].map((_, i) => <div key={i} className="h-12 bg-gray-200 rounded-lg" />)}
        </div>
      ) : (
        <>
          <div className="text-sm text-gray-500 mb-4">
            {sorted.length} jurisdiction{sorted.length !== 1 ? 's' : ''}
            {gradeFilter && ` (${gradeFilter === 'DF' ? 'D/F' : gradeFilter}-range)`}
          </div>

          {sorted.length === 0 ? (
            <div className="text-center py-12 text-gray-400">
              No jurisdictions match that filter.
            </div>
          ) : (
            <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="text-left border-b border-gray-200 bg-gray-50">
                      <th
                        onClick={() => handleSort('code')}
                        className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide cursor-pointer hover:text-gray-700 w-20"
                      >
                        Code{sortIndicator('code')}
                      </th>
                      <th
                        onClick={() => handleSort('name')}
                        className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide cursor-pointer hover:text-gray-700"
                      >
                        Jurisdiction{sortIndicator('name')}
                      </th>
                      <th
                        onClick={() => handleSort('grade')}
                        className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide cursor-pointer hover:text-gray-700 w-20 text-center"
                      >
                        Grade{sortIndicator('grade')}
                      </th>
                      <th
                        onClick={() => handleSort('score')}
                        className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide cursor-pointer hover:text-gray-700 w-24 text-right"
                      >
                        Score{sortIndicator('score')}
                      </th>
                      <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide w-48">
                        Model Provisions
                      </th>
                      <th className="px-4 py-3 w-10" />
                    </tr>
                  </thead>
                  <tbody>
                    {sorted.map(s => (
                      <ScorecardRow
                        key={s.code}
                        scorecard={s}
                        expanded={expandedRow === s.code}
                        onToggle={() => toggleRow(s.code)}
                      />
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Legend */}
          <div className="mt-8 bg-white border border-gray-200 rounded-lg p-5">
            <h2 className="text-sm font-semibold text-gray-900 mb-3">How Scoring Works</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-sm text-gray-600 mb-4">
              {Object.entries(FACTOR_LABELS).map(([key, label]) => (
                <div key={key} className="flex justify-between gap-2">
                  <span>{label}</span>
                  <span className="text-gray-400 font-mono text-xs">
                    varies
                  </span>
                </div>
              ))}
            </div>
            <div className="border-t border-gray-100 pt-3 mt-3">
              <p className="text-xs text-gray-500 leading-relaxed">
                Each jurisdiction is scored out of 100 points across nine factors covering
                response deadlines, fee structure, appeal rights, penalties for noncompliance,
                segregability requirements, presumption of openness, requester anonymity, and
                the breadth of exemptions. Grades are assigned on a standard scale: 90+ = A,
                80-89 = B, 70-79 = C, 60-69 = D, below 60 = F. Plus/minus modifiers reflect
                position within each range.
              </p>
            </div>
            <div className="border-t border-gray-100 pt-3 mt-3 flex flex-wrap gap-3">
              <div className="flex items-center gap-1.5">
                <Badge variant="green">A</Badge>
                <span className="text-xs text-gray-500">90+</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Badge variant="default">B</Badge>
                <span className="text-xs text-gray-500">80-89</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Badge variant="amber">C</Badge>
                <span className="text-xs text-gray-500">70-79</span>
              </div>
              <div className="flex items-center gap-1.5">
                <Badge variant="red">D/F</Badge>
                <span className="text-xs text-gray-500">&lt;70</span>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}

function ScorecardRow({ scorecard: s, expanded, onToggle }) {
  const provisions = s.model_provisions || []

  return (
    <>
      <tr className="border-b border-gray-100 hover:bg-gray-50">
        <td className="px-4 py-3">
          <Link
            to={`/jurisdictions/${s.code}`}
            className="font-mono text-sm font-semibold text-blue-600 hover:text-blue-700"
          >
            {s.code}
          </Link>
        </td>
        <td className="px-4 py-3">
          <Link
            to={`/jurisdictions/${s.code}`}
            className="text-gray-900 hover:text-blue-700 font-medium"
          >
            {s.name}
          </Link>
        </td>
        <td className="px-4 py-3 text-center">
          <Badge variant={gradeVariant(s.grade)}>{s.grade}</Badge>
        </td>
        <td className="px-4 py-3 text-right">
          <span className="font-semibold text-gray-900">{s.score}</span>
          <span className="text-gray-400">/{s.max_score}</span>
        </td>
        <td className="px-4 py-3">
          <div className="flex flex-wrap gap-1">
            {provisions.slice(0, 3).map(p => (
              <Badge key={p} variant="gray">
                {PROVISION_LABELS[p] || p}
              </Badge>
            ))}
            {provisions.length > 3 && (
              <span className="text-xs text-gray-400">+{provisions.length - 3}</span>
            )}
          </div>
        </td>
        <td className="px-4 py-3">
          <button
            onClick={onToggle}
            className="text-xs text-gray-400 hover:text-gray-600"
            aria-label={expanded ? 'Collapse breakdown' : 'Expand breakdown'}
          >
            {expanded ? '▲' : '▼'}
          </button>
        </td>
      </tr>

      {expanded && s.breakdown && (
        <tr className="border-b border-gray-100 bg-gray-50">
          <td colSpan={6} className="px-4 py-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {Object.entries(s.breakdown).map(([key, factor]) => (
                <div
                  key={key}
                  className="flex items-center justify-between bg-white border border-gray-200 rounded px-3 py-2"
                >
                  <div className="min-w-0">
                    <div className="text-xs font-medium text-gray-700">
                      {FACTOR_LABELS[key] || key.replace(/_/g, ' ')}
                    </div>
                    {factor.detail && (
                      <div className="text-xs text-gray-400 mt-0.5">{factor.detail}</div>
                    )}
                  </div>
                  <div className="text-sm font-semibold text-gray-900 ml-3 shrink-0">
                    {factor.score}/{factor.max}
                  </div>
                </div>
              ))}
            </div>

            {provisions.length > 0 && (
              <div className="mt-3 pt-3 border-t border-gray-200">
                <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                  Model Provisions
                </div>
                <div className="flex flex-wrap gap-1.5">
                  {provisions.map(p => (
                    <Badge key={p} variant="purple">
                      {PROVISION_LABELS[p] || p}
                    </Badge>
                  ))}
                </div>
              </div>
            )}
          </td>
        </tr>
      )}
    </>
  )
}
