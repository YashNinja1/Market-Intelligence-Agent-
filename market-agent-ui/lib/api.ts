import axios from 'axios'
import { Stock, NewsArticle, MarketSignal, SentimentSummary, AgentReport,SymbolSearchResult } from '@/types'

const API = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 120000  // 2 min timeout — Mistral agents can take time
})

export async function getStocks(): Promise<Stock[]> {
  const res = await API.get('/stocks')
  return res.data
}

export async function getNews(symbol?: string): Promise<NewsArticle[]> {
  const url = symbol ? `/news/${symbol}` : '/news'
  const res = await API.get(url)
  return res.data
}

export async function getSignals(): Promise<MarketSignal[]> {
  const res = await API.get('/analysis/signals')
  return res.data
}

export async function getSentiment(): Promise<SentimentSummary[]> {
  const res = await API.get('/analysis/sentiment')
  return res.data
}

export async function triggerFetch(): Promise<void> {
  await API.post('/analysis/fetch')
}

export async function runAgents(): Promise<AgentReport> {
  const res = await API.post('/agents/run')
  return res.data
}

export async function searchCompany(query: string): Promise<SymbolSearchResult> {
  const res = await API.get(`/stocks/search/${encodeURIComponent(query)}`)
  return res.data
}

export async function addCompany(companyName: string): Promise<{
  symbol: string
  name: string
  message: string
}> {
  const res = await API.post(`/stocks/add/${encodeURIComponent(companyName)}`)
  return res.data
}


export async function removeStock(symbol: string): Promise<void> {
  await API.delete(`/stocks/remove/${symbol}`)
}

export async function getTrackedSymbols(): Promise<string[]> {
  const res = await API.get('/stocks/tracked')
  return res.data.symbols
}

