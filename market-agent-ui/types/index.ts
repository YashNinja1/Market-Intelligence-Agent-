export interface Stock {
  symbol: string
  company_name: string      
  price: number
  change: number
  change_pct: string
  volume: number
  fetched_at: string
}


export interface SymbolSearchResult {
  symbol: string
  name: string
  source: string
}

export interface NewsArticle {
  symbol: string
  title: string
  source: string
  url: string
  summary: string
  sentiment: string
  sentiment_score: number
  published_at: string
}

export interface SentimentSummary {
  symbol: string
  article_count: number
  avg_sentiment: number
  bullish: number
  bearish: number
}

export interface MarketSignal {
  symbol: string
  price: number
  price_direction: string
  sentiment_direction: string
  signal: string
  avg_sentiment: number
}

export interface AgentResult {
  symbol: string
  stock: Stock
  sentiment: {
    overall_sentiment: string
    confidence: number
    key_signal: string
    reasoning: string
    bullish_count: number
    bearish_count: number
  }
  trend: {
    trend: string
    momentum: string
    price_change_pct: string
    outlook: string
    confidence: number
  }
  risk: {
    risk_level: string
    risk_factors: string[]
    alert: boolean
    recommendation: string
  }
}

export interface AgentReport {
  stocks_analyzed: number
  report: string
  analysis: AgentResult[]
}