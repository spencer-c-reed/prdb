import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../data/DataContext'
import Badge from '../components/Badge'

function formatValue(val) {
  if (!val) return null
  return val
    .replace(/_/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase())
}

function feesBadgeVariant(type) {
  if (!type) return 'gray'
  const t = type.toLowerCase()
  if (t === 'mandatory') return 'green'
  if (t === 'discretionary' || t === 'available') return 'default'
  if (t === 'none') return 'red'
  return 'gray'
}

const SORT_COLUMNS = {
  jurisdiction: (a, b) => a.name.localeCompare(b.name),
  attorneys_fees_type: (a, b) => {
    const order = { mandatory: 0, discretionary: 1, available: 1, none: 2 }
    const aVal = order[a.attorneys_fees_type?.toLowerCase()] ?? 3
    const bVal = order[b.attorneys_fees_type?.toLowerCase()] ?? 3
    return aVal - bVal
  },
  civil_penalty: (a, b) => {
    const aHas = a.civil_penalty ? 0 : 1
    const bHas = b.civil_penalty ? 0 : 1
    return aHas - bHas
  },
  criminal_penalty: (a, b) => {
    const aHas = a.criminal_penalty ? 0 : 1
    const bHas = b.criminal_penalty ? 0 : 1
    return aHas - bHas
  },
  per_diem: (a, b) => {
    const aHas = a.per_diem ? 0 : 1
    const bHas = b.per_diem ? 0 : 1
    return aHas - bHas
  },
}

export default function PenaltiesPage() {
  const { loading, penaltyComparison } = useData()
  const [sortKey, setSortKey] = useState('jurisdiction')
  const [sortAsc, setSortAsc] = useState(true)

  const data = penaltyComparison || []

  const summary = useMemo(() => {
    let mandatory = 0
    let discretionary = 0
    let perDiem = 0
    let criminal = 0

    data.forEach(d => {
      const t = d.attorneys_fees_type?.toLowerCase()
      if (t === 'mandatory') mandatory++
      if (t === 'discretionary' || t === 'available') discretionary++
      if (d.per_diem) perDiem++
      if (d.criminal_penalty) criminal++
    })

    return { mandatory, discretionary, perDiem, criminal }
  }, [data])

  const sorted = useMemo(() => {
    const compareFn = SORT_COLUMNS[sortKey] || SORT_COLUMNS.jurisdiction
    const result = [...data].sort(compareFn)
    return sortAsc ? result : result.reverse()
  }, [data, sortKey, sortAsc])

  function handleSort(key) {
    if (sortKey === key) {
      setSortAsc(prev => !prev)
    } else {
      setSortKey(key)
      setSortAsc(true)
    }
  }

  function SortHeader({ columnKey, children, className = '' }) {
    const active = sortKey === columnKey
    return (
      <th
        className={`pb-2 pr-4 text-xs font-semibold text-gray-500 uppercase tracking-wide cursor-pointer select-none hover:text-gray-700 ${className}`}
        onClick={() => handleSort(columnKey)}
      >
        <span className="inline-flex items-center gap-1">
          {children}
          {active && (
            <span className="text-gray-400">{sortAsc ? '\u2191' : '\u2193'}</span>
          )}
        </span>
      </th>
    )
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Enforcement and Penalties</h1>
        <p className="text-gray-500 text-sm">
          Comparison of enforcement mechanisms and penalties for public records violations across US jurisdictions.
        </p>
      </div>

      {loading ? (
        <div className="animate-pulse space-y-4">
          <div className="h-20 bg-gray-200 rounded-lg" />
          {[...Array(8)].map((_, i) => <div key={i} className="h-10 bg-gray-200 rounded-lg" />)}
        </div>
      ) : (
        <>
          {/* Summary */}
          <div className="bg-white border border-gray-200 rounded-lg p-5 mb-8">
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
              <div>
                <div className="text-2xl font-bold text-green-700">{summary.mandatory}</div>
                <div className="text-xs text-gray-500 mt-1">Mandatory attorney fees</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-blue-700">{summary.discretionary}</div>
                <div className="text-xs text-gray-500 mt-1">Discretionary attorney fees</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-amber-700">{summary.perDiem}</div>
                <div className="text-xs text-gray-500 mt-1">Per diem penalties</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-red-700">{summary.criminal}</div>
                <div className="text-xs text-gray-500 mt-1">Criminal penalties</div>
              </div>
            </div>
          </div>

          {/* Table */}
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left border-b border-gray-200 bg-gray-50">
                    <SortHeader columnKey="jurisdiction" className="pl-5">
                      Jurisdiction
                    </SortHeader>
                    <SortHeader columnKey="attorneys_fees_type">
                      Attorney Fees
                    </SortHeader>
                    <SortHeader columnKey="civil_penalty">
                      Civil Penalties
                    </SortHeader>
                    <SortHeader columnKey="criminal_penalty">
                      Criminal Penalties
                    </SortHeader>
                    <SortHeader columnKey="per_diem">
                      Per Diem / Statutory Damages
                    </SortHeader>
                  </tr>
                </thead>
                <tbody>
                  {sorted.map(row => (
                    <tr key={row.code} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-3 pr-4 pl-5">
                        <Link
                          to={`/jurisdictions/${row.code}`}
                          className="font-medium text-blue-700 hover:text-blue-900"
                        >
                          {row.name}
                        </Link>
                        <span className="text-gray-400 text-xs ml-1.5">{row.code}</span>
                      </td>
                      <td className="py-3 pr-4">
                        {row.attorneys_fees_type ? (
                          <div className="space-y-1">
                            <Badge variant={feesBadgeVariant(row.attorneys_fees_type)}>
                              {formatValue(row.attorneys_fees_type)}
                            </Badge>
                            {row.attorneys_fees && row.attorneys_fees !== row.attorneys_fees_type && (
                              <div className="text-xs text-gray-500">
                                {formatValue(row.attorneys_fees)}
                              </div>
                            )}
                          </div>
                        ) : (
                          <span className="text-gray-300">--</span>
                        )}
                      </td>
                      <td className="py-3 pr-4">
                        {row.civil_penalty ? (
                          <span className="text-gray-700">{formatValue(row.civil_penalty)}</span>
                        ) : (
                          <span className="text-gray-300">--</span>
                        )}
                      </td>
                      <td className="py-3 pr-4">
                        {row.criminal_penalty ? (
                          <span className="text-gray-700">{formatValue(row.criminal_penalty)}</span>
                        ) : (
                          <span className="text-gray-300">--</span>
                        )}
                      </td>
                      <td className="py-3 pr-4">
                        {row.per_diem ? (
                          <span className="text-gray-700">{row.per_diem}</span>
                        ) : (
                          <span className="text-gray-300">--</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="mt-4 text-xs text-gray-400">
            {data.length} jurisdiction{data.length !== 1 ? 's' : ''} with enforcement data
          </div>
        </>
      )}
    </div>
  )
}
