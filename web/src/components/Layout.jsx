import { useState } from 'react'
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
              <NavItem to="/compare">Compare</NavItem>
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
