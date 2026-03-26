import { Link } from 'react-router-dom'

export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">About PRDB</h1>

      <div className="space-y-6 text-sm text-gray-700 leading-relaxed">
        <section className="bg-white border border-gray-200 rounded-lg p-5">
          <h2 className="text-base font-semibold text-gray-900 mb-3">What This Is</h2>
          <p>
            PRDB (Public Records Request Database) is a reference tool for journalists, researchers,
            and anyone filing public records requests under FOIA or state sunshine laws.
            It covers statutes, exemptions, agency contact information, and procedural rules
            across all 50 states, DC, and the federal government.
          </p>
        </section>

        <section className="bg-white border border-gray-200 rounded-lg p-5">
          <h2 className="text-base font-semibold text-gray-900 mb-3">Data Sources & Methodology</h2>
          <ul className="space-y-2">
            <li className="flex gap-2">
              <span className="text-blue-400 shrink-0">·</span>
              <span>
                <strong>Statutes:</strong> Primary source text from state legislative databases and the U.S. Code.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-blue-400 shrink-0">·</span>
              <span>
                <strong>Exemptions:</strong> Cataloged from statutory text and verified against agency practice.
                Each exemption includes scope, key triggering terms, and known challenge strategies.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-blue-400 shrink-0">·</span>
              <span>
                <strong>Response rules:</strong> Response deadlines, extension limits, fee caps,
                and appeal windows extracted from each jurisdiction's statute.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-blue-400 shrink-0">·</span>
              <span>
                <strong>Agencies:</strong> Contact information, submission methods, and portal URLs
                scraped and manually verified from agency websites.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-blue-400 shrink-0">·</span>
              <span>
                <strong>Templates:</strong> Model request language reviewed for each jurisdiction's
                statutory requirements.
              </span>
            </li>
          </ul>
        </section>

        <section className="bg-white border border-gray-200 rounded-lg p-5">
          <h2 className="text-base font-semibold text-gray-900 mb-3">Caveats</h2>
          <ul className="space-y-2">
            <li className="flex gap-2">
              <span className="text-amber-400 shrink-0">!</span>
              <span>
                Public records law changes frequently. Always verify current statute text before
                filing a request or appeal.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-amber-400 shrink-0">!</span>
              <span>
                Agency contact information goes stale. Confirm submission details directly with
                the agency before sending.
              </span>
            </li>
            <li className="flex gap-2">
              <span className="text-amber-400 shrink-0">!</span>
              <span>
                This database is a reference tool, not legal advice.
                For contested requests or litigation, consult an attorney familiar with local practice.
              </span>
            </li>
          </ul>
        </section>

        <section className="bg-white border border-gray-200 rounded-lg p-5">
          <h2 className="text-base font-semibold text-gray-900 mb-3">Coverage</h2>
          <p className="mb-3">
            Current coverage focuses on state-level sunshine law statutes, federal FOIA, and
            selected agency directories. Expanding to include:
          </p>
          <ul className="space-y-1 text-gray-600">
            <li className="flex gap-2"><span>·</span><span>AG opinions and court decisions</span></li>
            <li className="flex gap-2"><span>·</span><span>Fee schedules by agency</span></li>
            <li className="flex gap-2"><span>·</span><span>Request tracking and deadline calculation</span></li>
            <li className="flex gap-2"><span>·</span><span>Appeal letter generation</span></li>
          </ul>
        </section>

        <div className="flex gap-3">
          <Link to="/" className="text-blue-600 hover:text-blue-700 text-sm">← Home</Link>
          <Link to="/jurisdictions" className="text-blue-600 hover:text-blue-700 text-sm">Browse jurisdictions →</Link>
        </div>
      </div>
    </div>
  )
}
