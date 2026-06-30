import { AgentReport as AgentReportType } from '@/types'
import SentimentBadge from './SentimentBadge'

export default function AgentReport({ report }: { report: AgentReportType }) {
  return (
    <div className="space-y-6">
      {/* AI Generated Report */}
      <div className="bg-gray-800 border border-green-800 rounded-xl p-6">
        <div className="flex items-center gap-2 mb-3">
          <span className="text-green-400 text-sm font-semibold uppercase tracking-wider">
            AI Market Intelligence Report
          </span>
          <span className="text-gray-500 text-xs">
            {report.stocks_analyzed} stocks analyzed
          </span>
        </div>
        <p className="text-gray-200 text-sm leading-relaxed">{report.report}</p>
      </div>

      {/* Per-stock agent breakdown */}
      {report.analysis.map((result, i) => (
        <div key={i} className="bg-gray-800 border border-gray-700 rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <span className="text-white font-bold text-lg">{result.symbol}</span>
            <SentimentBadge sentiment={result.sentiment.overall_sentiment} />
          </div>

          <div className="grid grid-cols-3 gap-3 mb-4">
            {/* Trend */}
            <div className="bg-gray-900 rounded-lg p-3">
              <div className="text-gray-400 text-xs mb-1">Trend</div>
              <div className="text-white text-sm font-medium">{result.trend.trend}</div>
              <div className="text-gray-400 text-xs">{result.trend.momentum} momentum</div>
            </div>
            {/* Risk */}
            <div className="bg-gray-900 rounded-lg p-3">
              <div className="text-gray-400 text-xs mb-1">Risk</div>
              <div className={`text-sm font-medium ${
                result.risk.risk_level === 'LOW' ? 'text-green-400' :
                result.risk.risk_level === 'MEDIUM' ? 'text-yellow-400' :
                result.risk.risk_level === 'HIGH' ? 'text-orange-400' : 'text-red-400'
              }`}>{result.risk.risk_level}</div>
              {result.risk.alert && (
                <div className="text-red-400 text-xs">⚠ Alert</div>
              )}
            </div>
            {/* Confidence */}
            <div className="bg-gray-900 rounded-lg p-3">
              <div className="text-gray-400 text-xs mb-1">Confidence</div>
              <div className="text-white text-sm font-medium">
                {(result.sentiment.confidence * 100).toFixed(0)}%
              </div>
              <div className="text-gray-400 text-xs">sentiment</div>
            </div>
          </div>

          <div className="text-gray-400 text-xs leading-relaxed mb-2">
            <span className="text-gray-300 font-medium">Key signal: </span>
            {result.sentiment.key_signal}
          </div>

          <div className="text-gray-400 text-xs leading-relaxed">
            <span className="text-gray-300 font-medium">Outlook: </span>
            {result.trend.outlook}
          </div>

          {result.risk.risk_factors.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {result.risk.risk_factors.map((factor, j) => (
                <span key={j} className="text-xs bg-red-950 text-red-300 border border-red-800 px-2 py-1 rounded">
                  {factor}
                </span>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}