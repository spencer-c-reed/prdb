import { createContext, useContext, useEffect, useState } from 'react'
import MiniSearch from 'minisearch'

const DataContext = createContext(null)

const BASE = import.meta.env.BASE_URL

async function fetchJSON(path) {
  const res = await fetch(`${BASE}data/${path}`)
  if (!res.ok) return null
  return res.json()
}

export function DataProvider({ children }) {
  const [state, setState] = useState({
    loading: true,
    error: null,
    exemptions: [],
    rules: [],
    templates: [],
    agencies: [],
    jurisdictions: [],
    documents: [],
    stats: {},
    searchIndex: null,
  })

  useEffect(() => {
    async function load() {
      try {
        const [
          exemptions,
          rules,
          templates,
          agencies,
          jurisdictions,
          documents,
          stats,
          searchIndexData,
        ] = await Promise.all([
          fetchJSON('exemptions.json'),
          fetchJSON('rules.json'),
          fetchJSON('templates.json'),
          fetchJSON('agencies.json'),
          fetchJSON('jurisdictions.json'),
          fetchJSON('documents.json'),
          fetchJSON('stats.json'),
          fetchJSON('search-index.json'),
        ])

        let searchIndex = null
        if (searchIndexData) {
          try {
            searchIndex = MiniSearch.loadJSON(
              JSON.stringify(searchIndexData),
              {
                fields: ['title', 'text', 'citation', 'topics'],
                storeFields: ['title', 'document_type', 'jurisdiction', 'citation'],
              }
            )
          } catch {
            // Search index failed to load — search will be degraded
          }
        }

        setState({
          loading: false,
          error: null,
          exemptions: exemptions || [],
          rules: rules || [],
          templates: templates || [],
          agencies: agencies || [],
          jurisdictions: jurisdictions || [],
          documents: documents || [],
          stats: stats || {},
          searchIndex,
        })
      } catch (err) {
        setState(s => ({ ...s, loading: false, error: err.message }))
      }
    }

    load()
  }, [])

  const ctx = {
    ...state,

    getExemptions(jurisdiction) {
      if (!jurisdiction) return state.exemptions
      return state.exemptions.filter(e => e.jurisdiction === jurisdiction)
    },

    getRules(jurisdiction) {
      if (!jurisdiction) return state.rules
      return state.rules.filter(r => r.jurisdiction === jurisdiction)
    },

    getTemplates(jurisdiction) {
      if (!jurisdiction) return state.templates
      return state.templates.filter(t => t.jurisdiction === jurisdiction)
    },

    getAgencies(jurisdiction) {
      if (!jurisdiction) return state.agencies
      return state.agencies.filter(a => a.jurisdiction === jurisdiction)
    },

    getJurisdictions() {
      return state.jurisdictions
    },

    getDocuments(jurisdiction) {
      if (!jurisdiction) return state.documents
      return state.documents.filter(d => d.jurisdiction === jurisdiction)
    },

    getStats() {
      return state.stats
    },

    getJurisdiction(code) {
      return state.jurisdictions.find(j => j.code === code || j.jurisdiction === code) || null
    },

    search(query, opts = {}) {
      if (!state.searchIndex || !query) return []
      return state.searchIndex.search(query, { prefix: true, fuzzy: 0.2, ...opts })
    },
  }

  return <DataContext.Provider value={ctx}>{children}</DataContext.Provider>
}

export function useData() {
  const ctx = useContext(DataContext)
  if (!ctx) throw new Error('useData must be used inside DataProvider')
  return ctx
}
