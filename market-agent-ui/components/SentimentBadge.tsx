const COLORS: Record<string, string> = {
  STRONGLY_BULLISH: 'bg-green-500 text-white',
  BULLISH:          'bg-green-700 text-green-100',
  NEUTRAL:          'bg-gray-600 text-gray-200',
  BEARISH:          'bg-red-700 text-red-100',
  STRONGLY_BEARISH: 'bg-red-500 text-white',
}

export default function SentimentBadge({ sentiment }: { sentiment: string }) {
  const color = COLORS[sentiment] ?? 'bg-gray-600 text-gray-200'
  return (
    <span className={`text-xs font-semibold px-3 py-1 rounded-full ${color}`}>
      {sentiment?.replace('_', ' ')}
    </span>
  )
}