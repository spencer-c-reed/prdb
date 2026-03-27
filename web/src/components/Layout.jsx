import { useState, useRef, useEffect } from 'react'
import { Link, NavLink, Outlet } from 'react-router-dom'
import { useData } from '../data/DataContext'
import SearchBar from './SearchBar'

function NavItem({ to, children }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `text-sm font-medium transition-colors ${
          isActive ? 'text-blue-600' : 'text-gray-600 hover:text-gray-900'
        }`
      }
    >
      {children}
    </NavLink>
  )
}

function AnalysisDropdown() {
  const [open, setOpen] = useState(false)
  const ref = useRef(null)

  useEffect(() => {
    function handleClick(e) {
      if (ref.current && !ref.current.contains(e.target)) setOpen(false)
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [])

  return (
    <div className="relative" ref={ref}>
      <button
        onClick={() => setOpen(!open)}
        className={`text-sm font-medium transition-colors ${
          open ? 'text-blue-600' : 'text-gray-600 hover:text-gray-900'
        } flex items-center gap-1`}
      >
        Analysis
        <svg className={`w-3 h-3 transition-transform ${open ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {open && (
        <div className="absolute right-0 top-full mt-1 w-48 bg-white border border-gray-200 rounded-lg shadow-lg py-1 z-50">
          <NavLink to="/scorecards" onClick={() => setOpen(false)} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Scorecards</NavLink>
          <NavLink to="/deadlines" onClick={() => setOpen(false)} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Deadline Rankings</NavLink>
          <NavLink to="/fees" onClick={() => setOpen(false)} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Fee Comparison</NavLink>
          <NavLink to="/penalties" onClick={() => setOpen(false)} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Penalties</NavLink>
          <NavLink to="/crosswalk" onClick={() => setOpen(false)} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Exemption Crosswalk</NavLink>
          <NavLink to="/appeals" onClick={() => setOpen(false)} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">Appeal Pathways</NavLink>
        </div>
      )}
    </div>
  )
}

export default function Layout() {
  const [menuOpen, setMenuOpen] = useState(false)
  const { stats, loading } = useData()

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Top nav */}
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-4 h-14">
            {/* Logo */}
            <Link to="/" className="font-bold text-lg text-gray-900 shrink-0">
              PRDB
            </Link>

            {/* Search — hidden on very small screens */}
            <div className="hidden sm:flex flex-1 max-w-md">
              <SearchBar />
            </div>

            {/* Desktop nav links */}
            <div className="hidden md:flex items-center gap-5 ml-auto">
              <NavItem to="/jurisdictions">Jurisdictions</NavItem>
              <NavItem to="/exemptions">Exemptions</NavItem>
              <NavItem to="/agencies">Agencies</NavItem>
              <NavItem to="/templates">Templates</NavItem>
              <NavItem to="/documents">Documents</NavItem>
              <NavItem to="/compare">Compare</NavItem>
              <AnalysisDropdown />
            </div>

            {/* Mobile hamburger */}
            <button
              onClick={() => setMenuOpen(!menuOpen)}
              className="md:hidden ml-auto p-2 rounded text-gray-500 hover:text-gray-700 hover:bg-gray-100"
              aria-label="Toggle menu"
            >
              {menuOpen ? (
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>
          </div>

          {/* Mobile search */}
          <div className="sm:hidden pb-3">
            <SearchBar />
          </div>
        </div>

        {/* Mobile dropdown menu */}
        {menuOpen && (
          <div className="md:hidden border-t border-gray-200 bg-white px-4 py-3 flex flex-col gap-3">
            <NavItem to="/jurisdictions">Jurisdictions</NavItem>
            <NavItem to="/exemptions">Exemptions</NavItem>
            <NavItem to="/agencies">Agencies</NavItem>
            <NavItem to="/templates">Templates</NavItem>
            <NavItem to="/compare">Compare</NavItem>
            <div className="border-t border-gray-100 pt-2 mt-1">
              <div className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Analysis</div>
              <div className="flex flex-col gap-2 pl-2">
                <NavItem to="/scorecards">Scorecards</NavItem>
                <NavItem to="/deadlines">Deadline Rankings</NavItem>
                <NavItem to="/fees">Fee Comparison</NavItem>
                <NavItem to="/penalties">Penalties</NavItem>
                <NavItem to="/crosswalk">Exemption Crosswalk</NavItem>
                <NavItem to="/appeals">Appeal Pathways</NavItem>
              </div>
            </div>
          </div>
        )}
      </nav>

      {/* Page content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white mt-12">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="text-sm text-gray-500">
            PRDB — Public Records Request Database
          </div>
          {!loading && stats && (
            <div className="flex gap-4 text-xs text-gray-400">
              {(stats.documents ?? stats.total) != null && (
                <span>{(stats.documents ?? stats.total).toLocaleString()} documents</span>
              )}
              {stats.exemptions != null && <span>{stats.exemptions} exemptions</span>}
              {stats.agencies != null && <span>{stats.agencies} agencies</span>}
              {stats.generated_at && (
                <span>Updated {new Date(stats.generated_at).toLocaleDateString()}</span>
              )}
            </div>
          )}
        </div>
      </footer>
    </div>
  )
}
