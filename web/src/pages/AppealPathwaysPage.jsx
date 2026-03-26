import { useState, useMemo } from 'react'
import { Link } from 'react-router-dom'
import { useData } from '../data/DataContext'
import Badge from '../components/Badge'

export default function AppealPathwaysPage() {
  const { loading, appealPathways } = useData()
  const [adminOnly, setAdminOnly] = useState(false)

  const pathways = appealPathways || []

  const stats = useMemo(() => {
    const withAdmin = pathways.filter(p => p.has_admin_appeal).length
    const directToCourt = pathways.filter(p => !p.has_admin_appeal && p.steps?.length > 0).length
    return { withAdmin, directToCourt }
  }, [pathways])

  const filtered = useMemo(() => {
    if (adminOnly) return pathways.filter(p => p.has_admin_appeal)
    return pathways
  }, [pathways, adminOnly])

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-1">Appeal Pathways</h1>
        <p className="text-gray-500 text-sm">
          Step-by-step appeal processes for public records denials, by jurisdiction.
        </p>
      </div>

      {loading ? (
        <div className="animate-pulse space-y-3">
          {[...Array(6)].map((_, i) => <div key={i} className="h-28 bg-gray-200 rounded-lg" />)}
        </div>
      ) : (
        <>
          {/* Summary */}
          <div className="text-sm text-gray-600 mb-4">
            {stats.withAdmin} jurisdiction{stats.withAdmin !== 1 ? 's' : ''} ha{stats.withAdmin !== 1 ? 've' : 's'} administrative appeals, {stats.directToCourt} go directly to court
          </div>

          {/* Filter */}
          <div className="flex items-center gap-3 mb-6">
            <label className="flex items-center gap-2 text-sm text-gray-700 cursor-pointer select-none">
              <button
                role="switch"
                aria-checked={adminOnly}
                onClick={() => setAdminOnly(!adminOnly)}
                className={`relative inline-flex h-5 w-9 shrink-0 rounded-full border-2 border-transparent transition-colors ${
                  adminOnly ? 'bg-blue-600' : 'bg-gray-300'
                }`}
              >
                <span
                  className={`pointer-events-none inline-block h-4 w-4 rounded-full bg-white shadow-sm transition-transform ${
                    adminOnly ? 'translate-x-4' : 'translate-x-0'
                  }`}
                />
              </button>
              Show only jurisdictions with administrative appeal
            </label>
          </div>

          {/* Results count */}
          <div className="text-sm text-gray-500 mb-4">
            {filtered.length} jurisdiction{filtered.length !== 1 ? 's' : ''}
          </div>

          {filtered.length === 0 ? (
            <div className="text-center py-12 text-gray-400">No jurisdictions found.</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filtered.map(p => (
                <PathwayCard key={p.code} pathway={p} />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}

function PathwayCard({ pathway: p }) {
  const steps = p.steps || []

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <div className="flex items-center gap-2 mb-3">
        <Badge variant={p.has_admin_appeal ? 'default' : 'gray'}>{p.code}</Badge>
        <span className="font-semibold text-gray-900 text-sm">{p.name}</span>
      </div>

      {steps.length === 0 ? (
        <p className="text-sm text-gray-400 italic">No structured appeal pathway documented</p>
      ) : (
        <div className="flex items-start gap-0 overflow-x-auto">
          {steps.map((step, i) => {
            const isAdmin = step.type === 'administrative'
            return (
              <div key={step.step} className="flex items-start shrink-0">
                <div
                  className={`rounded-lg border px-3 py-2 text-xs max-w-44 ${
                    isAdmin
                      ? 'border-blue-200 bg-blue-50 text-blue-800'
                      : 'border-purple-200 bg-purple-50 text-purple-800'
                  }`}
                >
                  <div className="font-semibold mb-0.5">
                    Step {step.step}: {step.type}
                  </div>
                  <div className="text-[11px] leading-tight opacity-80">{step.action}</div>
                  {step.deadline && (
                    <div className="mt-1 text-[10px] opacity-60">{step.deadline} days</div>
                  )}
                  {step.attorneys_fees && (
                    <div className="mt-1 text-[10px] opacity-60">Fees: {step.attorneys_fees}</div>
                  )}
                </div>
                {i < steps.length - 1 && (
                  <div className="flex items-center self-center px-1 text-gray-300 text-xs">
                    &rarr;
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
