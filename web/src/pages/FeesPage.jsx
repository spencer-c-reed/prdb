import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../data/DataContext'
import Badge from '../components/Badge'

const BUCKETS = [
  { label: '$0.01 - $0.10', min: 0.01, max: 0.10, color: 'bg-green-500' },
  { label: '$0.11 - $0.15', min: 0.11, max: 0.15, color: 'bg-green-400' },
  { label: '$0.16 - $0.25', min: 0.16, max: 0.25, color: 'bg-yellow-400' },
  { label: '$0.26 - $0.50', min: 0.26, max: 0.50, color: 'bg-orange-400' },
  { label: '$0.50+', min: 0.51, max: Infinity, color: 'bg-red-400' },
  { label: 'No cap / actual cost', min: null, max: null, color: 'bg-gray-300' },
]

function getBucketCounts(data) {
  return BUCKETS.map(bucket => {
    const count = data.filter(d => {
      if (bucket.min === null) return d.per_page_numeric === null
      if (d.per_page_numeric === null) return false
      return d.per_page_numeric >= bucket.min && d.per_page_numeric <= bucket.max
    }).length
    return { ...bucket, count }
  })
}

function formatFee(entry) {
  if (entry.per_page_numeric !== null && entry.per_page_numeric !== undefined) {
    return '$' + Number(entry.per_page_numeric).toFixed(2)
  }
  return entry.per_page || 'N/A'
}

function FeeDistribution({ data }) {
  const buckets = getBucketCounts(data)
  const total = data.length || 1

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-5 mb-8">
      <h2 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-4">
        Per-Page Fee Distribution
      </h2>

      {/* Bar */}
      <div className="flex h-8 rounded-lg overflow-hidden mb-4">
        {buckets.map(bucket => {
          if (bucket.count === 0) return null
          const pct = (bucket.count / total) * 100
          return (
            <div
              key={bucket.label}
              className={`${bucket.color} flex items-center justify-center text-xs font-semibold text-white`}
              style={{ width: `${pct}%`, minWidth: bucket.count > 0 ? '2rem' : 0 }}
              title={`${bucket.label}: ${bucket.count} jurisdictions`}
            >
              {bucket.count}
            </div>
          )
        })}
      </div>

      {/* Legend */}
      <div className="flex flex-wrap gap-x-5 gap-y-1.5">
        {buckets.map(bucket => (
          <div key={bucket.label} className="flex items-center gap-1.5 text-xs text-gray-600">
            <span className={`inline-block w-3 h-3 rounded-sm ${bucket.color}`} />
            <span>{bucket.label}</span>
            <span className="text-gray-400">({bucket.count})</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default function FeesPage() {
  const { loading, feeComparison } = useData()
  const [sortCol, setSortCol] = useState('per_page_numeric')
  const [sortDir, setSortDir] = useState('asc')

  const sorted = useMemo(() => {
    if (!feeComparison) return []

    const copy = [...feeComparison]

    copy.sort((a, b) => {
      let aVal, bVal

      if (sortCol === 'per_page_numeric') {
        // Nulls always last regardless of direction
        if (a.per_page_numeric === null && b.per_page_numeric === null) return 0
        if (a.per_page_numeric === null) return 1
        if (b.per_page_numeric === null) return -1
        aVal = a.per_page_numeric
        bVal = b.per_page_numeric
      } else if (sortCol === 'name') {
        aVal = (a.name || '').toLowerCase()
        bVal = (b.name || '').toLowerCase()
      } else if (sortCol === 'has_fee_waiver') {
        aVal = a.has_fee_waiver ? 1 : 0
        bVal = b.has_fee_waiver ? 1 : 0
      } else {
        return 0
      }

      if (aVal < bVal) return sortDir === 'asc' ? -1 : 1
      if (aVal > bVal) return sortDir === 'asc' ? 1 : -1
      return 0
    })

    return copy
  }, [feeComparison, sortCol, sortDir])

  function handleSort(col) {
    if (sortCol === col) {
      setSortDir(prev => (prev === 'asc' ? 'desc' : 'asc'))
    } else {
      setSortCol(col)
      setSortDir('asc')
    }
  }

  function sortIndicator(col) {
    if (sortCol !== col) return ''
    return sortDir === 'asc' ? ' \u2191' : ' \u2193'
  }

  // Assign ranks based on sorted order (only numeric entries get a rank)
  const ranked = useMemo(() => {
    let rank = 0
    let lastVal = null
    let lastRank = 0

    return sorted.map(entry => {
      if (entry.per_page_numeric === null) {
        return { ...entry, rank: null }
      }
      rank++
      // Tie handling: same fee = same rank
      if (entry.per_page_numeric === lastVal) {
        return { ...entry, rank: lastRank }
      }
      lastVal = entry.per_page_numeric
      lastRank = rank
      return { ...entry, rank }
    })
  }, [sorted])

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="animate-pulse space-y-6">
          <div className="h-8 bg-gray-200 rounded w-64" />
          <div className="h-4 bg-gray-200 rounded w-96" />
          <div className="h-32 bg-gray-200 rounded-lg" />
          <div className="h-96 bg-gray-200 rounded-lg" />
        </div>
      </div>
    )
  }

  const data = feeComparison || []

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Per-Page Copy Fees</h1>
        <p className="text-gray-500 text-sm">
          Comparison of per-page copy fees for public records requests across all US jurisdictions.
        </p>
      </div>

      <FeeDistribution data={data} />

      {/* Table */}
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left border-b border-gray-200 bg-gray-50">
                <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide w-16">
                  Rank
                </th>
                <th
                  className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide cursor-pointer select-none hover:text-gray-700"
                  onClick={() => handleSort('name')}
                >
                  Jurisdiction{sortIndicator('name')}
                </th>
                <th
                  className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide cursor-pointer select-none hover:text-gray-700"
                  onClick={() => handleSort('per_page_numeric')}
                >
                  Per-Page Fee{sortIndicator('per_page_numeric')}
                </th>
                <th
                  className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide cursor-pointer select-none hover:text-gray-700"
                  onClick={() => handleSort('has_fee_waiver')}
                >
                  Fee Waiver{sortIndicator('has_fee_waiver')}
                </th>
                <th className="px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">
                  Notes
                </th>
              </tr>
            </thead>
            <tbody>
              {ranked.map(entry => {
                const isNonNumeric = entry.per_page_numeric === null
                const rowClass = isNonNumeric ? 'text-gray-400' : ''

                return (
                  <tr
                    key={entry.code}
                    className={`border-b border-gray-100 hover:bg-gray-50 ${rowClass}`}
                  >
                    <td className="px-4 py-2.5 font-mono text-gray-400 text-xs">
                      {entry.rank !== null ? entry.rank : '--'}
                    </td>
                    <td className="px-4 py-2.5">
                      <Link
                        to={`/jurisdictions/${entry.code}`}
                        className={`font-medium hover:underline ${isNonNumeric ? 'text-gray-400' : 'text-blue-600 hover:text-blue-800'}`}
                      >
                        {entry.name}
                      </Link>
                      <span className="ml-1.5 text-xs text-gray-400">({entry.code})</span>
                      {entry.citation && (
                        <div className="text-xs text-gray-400 mt-0.5">{entry.citation}</div>
                      )}
                    </td>
                    <td className="px-4 py-2.5">
                      {isNonNumeric ? (
                        <Badge variant="gray">{entry.per_page || 'No cap'}</Badge>
                      ) : (
                        <span className="font-semibold text-gray-900">
                          {formatFee(entry)}
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-2.5 text-center">
                      {entry.has_fee_waiver ? (
                        <span className="text-green-600 font-bold" title="Fee waiver available">
                          &#10003;
                        </span>
                      ) : (
                        <span className="text-red-500 font-bold" title="No fee waiver">
                          &#10005;
                        </span>
                      )}
                    </td>
                    <td className="px-4 py-2.5 text-xs text-gray-500 max-w-xs">
                      {entry.notes || '--'}
                    </td>
                  </tr>
                )
              })}
              {ranked.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-4 py-12 text-center text-gray-400">
                    No fee comparison data available.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="mt-4 text-xs text-gray-400">
        {data.length} jurisdictions. Sorted by per-page fee (lowest first). Jurisdictions without a
        numeric cap appear at the bottom.
      </div>
    </div>
  )
}
