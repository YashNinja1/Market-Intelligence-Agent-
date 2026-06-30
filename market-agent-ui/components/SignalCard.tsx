import { MarketSignal } from '@/types'
import SentimentBadge from './SentimentBadge'

export default function SignalCard({ signal }: { signal: MarketSignal }) {
  const isAligned = signal.signal === 'ALIGNED'

  return (
    <div className={`border rounded-xl p-5 ${isAligned ? 'bg-green-950 border-green-800' : 'bg-yellow-950 border-yellow-800'}`}>
      <div className="flex justify-between items-center mb-3">
        <span className="text-white font-bold text-lg">{signal.symbol}</span>
        <span className={`text-xs font-bold px-3 py-1 rounded-full ${isAligned ? 'bg-green-600 text-white' : 'bg-yellow-600 text-white'}`}>
          {signal.signal}
        </span>
      </div>
      <div className="text-2xl font-bold text-white mb-3">
        ${Number(signal.price).toFixed(2)}
      </div>
      <div className="flex gap-2 flex-wrap">
        <span className={`text-xs px-2 py-1 rounded ${signal.price_direction === 'UP' ? 'bg-green-800 text-green-200' : 'bg-red-800 text-red-200'}`}>
          Price {signal.price_direction}
        </span>
        <span className={`text-xs px-2 py-1 rounded ${signal.sentiment_direction === 'POSITIVE' ? 'bg-green-800 text-green-200' : 'bg-red-800 text-red-200'}`}>
          Sentiment {signal.sentiment_direction}
        </span>
      </div>
      <div className="text-gray-400 text-xs mt-3">
        Avg sentiment: {Number(signal.avg_sentiment).toFixed(3)}
      </div>
    </div>
  )
}