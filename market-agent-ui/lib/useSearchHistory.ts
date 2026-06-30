import { useState, useEffect } from 'react'

export interface SearchHistoryItem {
  query: string
  symbol: string
  name: string
  searchedAt: string
}

const STORAGE_KEY = 'market_agent_search_history'
const MAX_HISTORY = 5

export function useSearchHistory() {
  const [history, setHistory] = useState<SearchHistoryItem[]>([])

  // Load from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored) setHistory(JSON.parse(stored))
    } catch {
      setHistory([])
    }
  }, [])

  function addToHistory(query: string, symbol: string, name: string) {
    setHistory(prev => {
      // Remove duplicate if exists
      const filtered = prev.filter(h => h.symbol !== symbol)

      const newItem: SearchHistoryItem = {
        query,
        symbol,
        name,
        searchedAt: new Date().toISOString()
      }

      // Keep only last MAX_HISTORY items
      const updated = [newItem, ...filtered].slice(0, MAX_HISTORY)

      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(updated))
      } catch {}

      return updated
    })
  }

  function removeFromHistory(symbol: string) {
    setHistory(prev => {
      const updated = prev.filter(h => h.symbol !== symbol)
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(updated))
      } catch {}
      return updated
    })
  }

  function clearHistory() {
    setHistory([])
    try {
      localStorage.removeItem(STORAGE_KEY)
    } catch {}
  }

  return { history, addToHistory, removeFromHistory, clearHistory }
}