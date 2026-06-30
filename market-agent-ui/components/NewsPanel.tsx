'use client'
import { NewsArticle } from '@/types'
import SentimentBadge from './SentimentBadge'

export default function NewsPanel({ articles }: { articles: NewsArticle[] }) {
  if (!articles.length) return (
    <div className="text-gray-500 text-sm text-center py-8">
      No news yet — click Fetch Data first
    </div>
  )

  return (
    <div className="space-y-3 max-h-[500px] overflow-y-auto pr-1">
      {articles.map((article, i) => (
        <div key={i} className="bg-gray-800 border border-gray-700 rounded-lg p-4">
          <div className="flex items-start justify-between gap-2 mb-2">
            
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-white text-sm font-medium hover:text-green-400 transition line-clamp-2"
            <a>
              {article.title}
            </a>
            <SentimentBadge sentiment={article.sentiment} />
          </div>
          <div className="flex gap-3 text-xs text-gray-500">
            <span>{article.source}</span>
            <span>{article.symbol}</span>
            <span>Score: {Number(article.sentiment_score).toFixed(3)}</span>
          </div>
        </div>
      ))}
    </div>
  )
}