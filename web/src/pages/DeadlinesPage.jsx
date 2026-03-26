import { useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../data/DataContext'
import Badge from '../components/Badge'

const BUCKETS = [
  { label: '1-5 days', min: 1, max: 5, color: 'bg-green-500', variant: 'green' },
  { label: '6-10 days', min: 6, max: 10, color: 'bg-blue-500', variant: 'default' },
  { label: '11-15 days', min: 11, max: 15, color: 'bg-amber-400', variant: 'amber' },
  { label: '16-20 days', min: 16, max: 20, color: 'bg-amber-500', variant: 'amber' },
  { label: '21+ days', min: 21, max: Infinity, color: 'bg-red-500', variant: 'red' },
  { label: 'No deadline', min: null, max: null, color: 'bg-gray-400', variant: 'gray' },
]

function getDeadlineVariant(calEquiv) {
  if (calEquiv == null) return 'gray'
  if (calEquiv <= 5) return 'green'
  if (calEquiv <= 10) return 'default'
  if (calEquiv <= 20) return 'amber'
  return 'red'
}

function getBucket(calEquiv) {
  if (calEquiv == null) return BUCKETS[BUCKETS.length - 1]
  return BUCKETS.find(b => b.min != null && calEquiv >= b.min && calEquiv <= b.max) || BUCKETS[BUCKETS.length - 1]
}

export default function DeadlinesPage() {
  const { loading, deadlineRankings } = useData()

  const sorted = useMemo(() => {
    if (!deadlineRankings) return []
    const withDeadline = deadlineRankings
      .filter(d => d.days != null)
      .sort((a, b) => (a.calendar_equivalent ?? Infinity) - (b.calendar_equivalent ?? Infinity))
    const noDeadline = deadlineRankings.filter(d => d.days == null)
    return [...withDeadline, ...noDeadline]
  }, [deadlineRankings])

  const bucketCounts = useMemo(() => {
    return BUCKETS.map(bucket => ({
      ...bucket,
      count: sorted.filter(d => {
        const cal = d.calendar_equivalent
        if (bucket.min == null) return d.days == null
        if (cal == null) return false
        return cal >= bucket.min && cal <= bucket.max
      }).length,
    }))
  }, [sorted])

  const maxCount = useMemo(() => Math.max(...bucketCounts.map(b => b.count), 1), [bucketCounts])

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Response Deadline Rankings</h1>
        <p className="text-gray-500 text-sm">
          How quickly agencies must respond to public records requests, ranked by calendar-day equivalent across all US jurisdictions.
        </p>
      </div>

      {loading ? (
        <div className="animate-pulse space-y-3">
          <div className="h-48 bg-gray-200 rounded-lg" />
          {[...Array(8)].map((_, i) => <div key={i} className="h-10 bg-gray-200 rounded-lg" />)}
        </div>
      ) : (
        <>
          {/* Distribution chart */}
          <div className="bg-white border border-gray-200 rounded-lg p-5 mb-6">
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">
              Distribution by Calendar-Day Equivalent
            </h2>
            <div className="space-y-2">
              {bucketCounts.map(bucket => (
                <div key={bucket.label} className="flex items-center gap-3">
                  <div className="w-24 text-xs text-gray-600 text-right shrink-0">
                    {bucket.label}
                  </div>
                  <div className="flex-1 h-7 bg-gray-100 rounded overflow-hidden">
                    {bucket.count > 0 && (
                      <div
                        className={`h-full ${bucket.color} rounded flex items-center transition-all duration-300`}
                        style={{ width: `${(bucket.count / maxCount) * 100}%`, minWidth: bucket.count > 0 ? '2rem' : 0 }}
                      >
                        <span className="text-xs font-semibold text-white px-2">
                          {bucket.count}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Summary */}
          <div className="text-sm text-gray-500 mb-4">
            {sorted.length} jurisdiction{sorted.length !== 1 ? 's' : ''} ranked
          </div>

          {/* Table */}
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-50 border-b border-gray-200">
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide w-16">
                      Rank
                    </th>
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">
                      Jurisdiction
                    </th>
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">
                      Deadline
                    </th>
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">
                      Day Type
                    </th>
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">
                      Calendar Equivalent
                    </th>
                    <th className="text-left px-4 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">
                      Extension
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {sorted.map((entry, i) => {
                    const hasDeadline = entry.days != null
                    const rank = hasDeadline ? i + 1 : null
                    const variant = getDeadlineVariant(entry.calendar_equivalent)

                    return (
                      <tr key={entry.code} className="hover:bg-gray-50 transition-colors">
                        <td className="px-4 py-3 text-gray-400 font-mono text-xs">
                          {rank != null ? rank : '--'}
                        </td>
                        <td className="px-4 py-3">
                          <Link
                            to={`/jurisdictions/${entry.code}`}
                            className="font-medium text-gray-900 hover:text-blue-700"
                          >
                            {entry.name}
                          </Link>
                          <span className="ml-1.5 text-xs text-gray-400">{entry.code}</span>
                        </td>
                        <td className="px-4 py-3">
                          {hasDeadline ? (
                            <Badge variant={variant}>
                              {entry.days} {entry.day_type === 'business' ? 'business' : 'calendar'} day{entry.days !== 1 ? 's' : ''}
                            </Badge>
                          ) : (
                            <span className="text-gray-400 text-xs italic">No statutory deadline</span>
                          )}
                        </td>
                        <td className="px-4 py-3 text-gray-600 capitalize">
                          {hasDeadline ? entry.day_type || '--' : '--'}
                        </td>
                        <td className="px-4 py-3">
                          {entry.calendar_equivalent != null ? (
                            <span className="font-mono text-gray-700">
                              {entry.calendar_equivalent} day{entry.calendar_equivalent !== 1 ? 's' : ''}
                            </span>
                          ) : (
                            <span className="text-gray-400">--</span>
                          )}
                        </td>
                        <td className="px-4 py-3">
                          {entry.extension_days != null ? (
                            <span className="text-gray-700">
                              +{entry.extension_days} day{entry.extension_days !== 1 ? 's' : ''}
                            </span>
                          ) : (
                            <span className="text-gray-400">--</span>
                          )}
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
