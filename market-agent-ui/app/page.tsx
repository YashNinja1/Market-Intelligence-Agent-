'use client'
import { useState, useEffect } from 'react'
import Navbar from '@/components/Navbar'
import StockCard from '@/components/StockCard'
import SignalCard from '@/components/SignalCard'
import NewsPanel from '@/components/NewsPanel'
import AgentReport from '@/components/AgentReport'
import { getStocks, getNews, getSignals, triggerFetch, runAgents } from '@/lib/api'
import { Stock, NewsArticle, MarketSignal, AgentReport as AgentReportType } from '@/types'
import CompanySearch from '@/components/CompanySearch'
import { SymbolSearchResult } from '@/types'

export default function Dashboard() {
  
  const [stocks, setStocks] = useState<Stock[]>([])
  const [news, setNews] = useState<NewsArticle[]>([])
  const [signals, setSignals] = useState<MarketSignal[]>([])
  const [report, setReport] = useState<AgentReportType | null>(null)
  const [loading, setLoading] = useState(false)
  const [agentLoading, setAgentLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'overview' | 'news' | 'agents'>('overview')

  // Load data on page open
  useEffect(() => {
    loadData()
  }, [])

  async function loadData() {
    try {
      const [s, n, sig] = await Promise.all([
        getStocks(), getNews(), getSignals()
      ])
      setStocks(s)
      setNews(n)
      setSignals(sig)
    } catch (e) {
      setError('Could not load data. Is FastAPI running on port 8000?')
    }
  }

  async function handleFetch() {
    setLoading(true)
    setError(null)
    try {
      await triggerFetch()
      // Wait 8 seconds for background fetch to complete
      setTimeout(async () => {
        await loadData()
        setLoading(false)
      }, 8000)
    } catch (e) {
      setError('Fetch failed. Check FastAPI logs.')
      setLoading(false)
    }
  }
  

  async function handleRunAgents() {
    setAgentLoading(true)
    setError(null)
    setActiveTab('agents')
    try {
      const result = await runAgents()
      setReport(result)
    } catch (e) {
      setError('Agent run failed. Is Mistral running in Ollama?')
    } finally {
      setAgentLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <Navbar
        onFetch={handleFetch}
        onRunAgents={handleRunAgents}
        loading={loading}
        agentLoading={agentLoading}
      />

      <main className="max-w-7xl mx-auto px-6 py-8">

        {/* Error banner */}
        {error && (
          <div className="mb-6 bg-red-950 border border-red-700 text-red-300 px-4 py-3 rounded-lg text-sm">
            {error}
          </div>
        )}
        <CompanySearch onAdded={loadData} />

        {/* Stock price cards */}
        <section className="mb-8">
          <h2 className="text-gray-400 text-sm font-medium uppercase tracking-wider mb-4">
            Live Prices
          </h2>
          {stocks.length === 0 ? (
            <div className="text-gray-600 text-sm">
              No data yet — click Fetch Data to load stocks
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {stocks.map(s => <StockCard key={s.symbol} stock={s} onRemoved={loadData} />)}
            </div>
          )}
        </section>

        {/* Tabs */}
        <div className="flex gap-1 mb-6 bg-gray-900 p-1 rounded-lg w-fit">
          {(['overview', 'news', 'agents'] as const).map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-5 py-2 rounded-md text-sm font-medium transition capitalize ${
                activeTab === tab
                  ? 'bg-gray-700 text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* Overview tab */}
        {activeTab === 'overview' && (
          <section>
            <h2 className="text-gray-400 text-sm font-medium uppercase tracking-wider mb-4">
              Market Signals
            </h2>
            {signals.length === 0 ? (
              <div className="text-gray-600 text-sm">
                No signals yet — fetch data first
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {signals.map(s => <SignalCard key={s.symbol} signal={s} />)}
              </div>
            )}
          </section>
        )}

        {/* News tab */}
        {activeTab === 'news' && (
          <section>
            <h2 className="text-gray-400 text-sm font-medium uppercase tracking-wider mb-4">
              Latest News + Sentiment
            </h2>
            <NewsPanel articles={news} />
          </section>
        )}

        {/* Agents tab */}
        {activeTab === 'agents' && (
          <section>
            <h2 className="text-gray-400 text-sm font-medium uppercase tracking-wider mb-4">
              AI Agent Analysis
            </h2>
            {agentLoading && (
              <div className="text-center py-16">
                <div className="text-green-400 text-lg mb-2 animate-pulse">
                  Agents are thinking...
                </div>
                <div className="text-gray-500 text-sm">
                  Mistral is analyzing stocks, sentiment, trends and risk.<br />
                  This takes 1–2 minutes.
                </div>
              </div>
            )}
            {!agentLoading && !report && (
              <div className="text-gray-600 text-sm">
                Click Run Agents to generate an AI market intelligence report
              </div>
            )}
            {!agentLoading && report && <AgentReport report={report} />}
          </section>
        )}

      </main>
    </div>
  )
}