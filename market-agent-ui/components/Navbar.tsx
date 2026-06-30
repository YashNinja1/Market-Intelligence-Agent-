'use client'
import { TrendingUp, RefreshCw, Brain } from 'lucide-react'

interface NavbarProps {
  onFetch: () => void
  onRunAgents: () => void
  loading: boolean
  agentLoading: boolean
}

export default function Navbar({ onFetch, onRunAgents, loading, agentLoading }: NavbarProps) {
  return (
    <nav className="bg-gray-900 border-b border-gray-800 px-6 py-4 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <TrendingUp className="text-green-400" size={24} />
        <span className="text-white font-semibold text-lg">
          Market Intelligence Agent
        </span>
      </div>
      <div className="flex gap-3">
        <button
          onClick={onFetch}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded-lg disabled:opacity-50 transition"
        >
          <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
          {loading ? 'Fetching...' : 'Fetch Data'}
        </button>
        <button
          onClick={onRunAgents}
          disabled={agentLoading}
          className="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-500 text-white text-sm rounded-lg disabled:opacity-50 transition"
        >
          <Brain size={14} className={agentLoading ? 'animate-pulse' : ''} />
          {agentLoading ? 'Agents Running...' : 'Run Agents'}
        </button>
      </div>
    </nav>
  )
}