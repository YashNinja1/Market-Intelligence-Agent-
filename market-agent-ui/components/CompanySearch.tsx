'use client'
import { useState } from 'react'
import { Search, Plus, Loader2, CheckCircle, XCircle, Clock, X } from 'lucide-react'
import { searchCompany, addCompany } from '@/lib/api'
import { useSearchHistory } from '@/lib/useSearchHistory'
import { SymbolSearchResult } from '@/types'

interface CompanySearchProps {
  onAdded: () => void
}

export default function CompanySearch({ onAdded }: CompanySearchProps) {
  const [query, setQuery] = useState('')
  const [resolved, setResolved] = useState<SymbolSearchResult | null>(null)
  const [searching, setSearching] = useState(false)
  const [adding, setAdding] = useState(false)
  const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const [message, setMessage] = useState('')

  const { history, addToHistory, removeFromHistory, clearHistory } = useSearchHistory()

  async function handleSearch(searchQuery: string = query) {
    if (!searchQuery.trim()) return
    setSearching(true)
    setResolved(null)
    setStatus('idle')
    try {
      const result = await searchCompany(searchQuery)
      setResolved(result)
      setQuery(searchQuery)
    } catch {
      setStatus('error')
      setMessage(`Could not find a stock for "${searchQuery}"`)
    } finally {
      setSearching(false)
    }
  }

  async function handleAdd() {
    if (!resolved) return
    setAdding(true)
    setStatus('idle')
    try {
      const result = await addCompany(query)
      // Save to history
      addToHistory(query, result.symbol, result.name)
      setStatus('success')
      setMessage(`${result.name} (${result.symbol}) added! Refreshing in 8s...`)
      setQuery('')
      setResolved(null)
      setTimeout(() => {
        onAdded()
        setStatus('idle')
        setMessage('')
      }, 8000)
    } catch {
      setStatus('error')
      setMessage('Failed to add company. Try again.')
    } finally {
      setAdding(false)
    }
  }

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-xl p-5 mb-8">
      <h3 className="text-gray-400 text-xs font-medium uppercase tracking-wider mb-3">
        Track a Company
      </h3>

      {/* Search input */}
      <div className="flex gap-2">
        <div className="relative flex-1">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSearch()}
            placeholder="Type a company name e.g. Tesla, Nvidia, Airbnb..."
            className="w-full bg-gray-800 border border-gray-700 text-white text-sm rounded-lg pl-9 pr-4 py-2.5 placeholder-gray-500 focus:outline-none focus:border-green-600 transition"
          />
        </div>
        <button
          onClick={() => handleSearch()}
          disabled={searching || !query.trim()}
          className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded-lg disabled:opacity-50 transition flex items-center gap-2"
        >
          {searching
            ? <Loader2 size={14} className="animate-spin" />
            : <Search size={14} />}
          Search
        </button>
      </div>

      {/* Resolved symbol preview */}
      {resolved && (
        <div className="mt-3 flex items-center justify-between bg-gray-800 border border-green-800 rounded-lg px-4 py-3">
          <div>
            <span className="text-white font-semibold">{resolved.name}</span>
            <span className="ml-2 text-green-400 text-sm font-mono">{resolved.symbol}</span>
            <span className="ml-2 text-gray-500 text-xs">via {resolved.source}</span>
          </div>
          <button
            onClick={handleAdd}
            disabled={adding}
            className="flex items-center gap-2 px-4 py-1.5 bg-green-600 hover:bg-green-500 text-white text-sm rounded-lg disabled:opacity-50 transition"
          >
            {adding ? <Loader2 size={13} className="animate-spin" /> : <Plus size={13} />}
            {adding ? 'Adding...' : 'Add to Dashboard'}
          </button>
        </div>
      )}

      {/* Status messages */}
      {status === 'success' && (
        <div className="mt-3 flex items-center gap-2 text-green-400 text-sm">
          <CheckCircle size={14} /> {message}
        </div>
      )}
      {status === 'error' && (
        <div className="mt-3 flex items-center gap-2 text-red-400 text-sm">
          <XCircle size={14} /> {message}
        </div>
      )}

      {/* Search history */}
      {history.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-gray-500 text-xs flex items-center gap-1">
              <Clock size={11} /> Recent searches
            </span>
            <button
              onClick={clearHistory}
              className="text-gray-600 hover:text-gray-400 text-xs transition"
            >
              Clear all
            </button>
          </div>
          <div className="flex flex-wrap gap-2">
            {history.map(item => (
              <div
                key={item.symbol}
                className="flex items-center gap-1 bg-gray-800 border border-gray-700 rounded-lg pl-3 pr-1 py-1"
              >
                {/* Click name to re-search */}
                <button
                  onClick={() => handleSearch(item.query)}
                  className="text-sm text-gray-300 hover:text-white transition"
                >
                  {item.name}
                </button>
                <span className="text-green-500 text-xs font-mono mx-1">
                  {item.symbol}
                </span>
                {/* Remove from history */}
                <button
                  onClick={() => removeFromHistory(item.symbol)}
                  className="p-1 text-gray-600 hover:text-red-400 transition rounded"
                >
                  <X size={10} />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}