import { HashRouter, Routes, Route } from 'react-router-dom'
import { DataProvider } from './data/DataContext'
import Layout from './components/Layout'

import HomePage from './pages/HomePage'
import JurisdictionIndexPage from './pages/JurisdictionIndexPage'
import JurisdictionDetailPage from './pages/JurisdictionDetailPage'
import ExemptionsPage from './pages/ExemptionsPage'
import ExemptionDetailPage from './pages/ExemptionDetailPage'
import AgenciesPage from './pages/AgenciesPage'
import AgencyDetailPage from './pages/AgencyDetailPage'
import TemplatesPage from './pages/TemplatesPage'
import TemplateDetailPage from './pages/TemplateDetailPage'
import ComparePage from './pages/ComparePage'
import SearchPage from './pages/SearchPage'
import AboutPage from './pages/AboutPage'

export default function App() {
  return (
    <HashRouter>
      <DataProvider>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<HomePage />} />
            <Route path="jurisdictions" element={<JurisdictionIndexPage />} />
            <Route path="jurisdictions/:code" element={<JurisdictionDetailPage />} />
            <Route path="exemptions" element={<ExemptionsPage />} />
            <Route path="exemptions/:id" element={<ExemptionDetailPage />} />
            <Route path="agencies" element={<AgenciesPage />} />
            <Route path="agencies/:id" element={<AgencyDetailPage />} />
            <Route path="templates" element={<TemplatesPage />} />
            <Route path="templates/:id" element={<TemplateDetailPage />} />
            <Route path="compare" element={<ComparePage />} />
            <Route path="search" element={<SearchPage />} />
            <Route path="about" element={<AboutPage />} />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </DataProvider>
    </HashRouter>
  )
}

function NotFound() {
  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
      <h1 className="text-2xl font-bold text-gray-900 mb-2">Page not found</h1>
      <p className="text-gray-500 mb-6">The page you're looking for doesn't exist.</p>
      <a href="#/" className="text-blue-600 hover:text-blue-700">← Back to home</a>
    </div>
  )
}
