import { Stock } from '@/types'
import { TrendingUp, TrendingDown } from 'lucide-react'






import { X, Loader2 } from 'lucide-react'
import { useState } from 'react'
import { removeStock } from '@/lib/api'

interface StockCardProps {
  stock: Stock
  onRemoved: () => void
}

export default function StockCard({ stock, onRemoved }: StockCardProps) {
  const [removing, setRemoving] = useState(false)
  const [confirm, setConfirm] = useState(false)
  const isUp = stock.change > 0

  async function handleRemove() {
    if (!confirm) {
      setConfirm(true)
      // Auto-cancel confirm after 3 seconds
      setTimeout(() => setConfirm(false), 3000)
      return
    }
    setRemoving(true)
    try {
      await removeStock(stock.symbol)
      onRemoved()
    } catch {
      setRemoving(false)
      setConfirm(false)
    }
  }

  return (
    <div className="relative bg-gray-800 border border-gray-700 rounded-xl p-5 group">

      {/* Remove button — shows on hover */}
      <button
        onClick={handleRemove}
        disabled={removing}
        className={`absolute top-3 right-3 p-1.5 rounded-lg text-xs transition flex items-center gap-1
          ${confirm
            ? 'bg-red-600 text-white'
            : 'opacity-0 group-hover:opacity-100 bg-gray-700 hover:bg-red-700 text-gray-400 hover:text-white'
          }`}
        title={confirm ? 'Click again to confirm remove' : 'Remove stock'}
      >
        {removing
          ? <Loader2 size={12} className="animate-spin" />
          : <X size={12} />
        }
        {confirm && !removing && <span>Confirm?</span>}
      </button>

      <div className="flex justify-between items-start mb-1 pr-6">
        <div>
          <div className="text-white font-bold text-lg leading-tight">
            {stock.company_name || stock.symbol}
          </div>
          <div className="text-gray-500 text-xs font-mono mt-0.5">
            {stock.symbol}
          </div>
        </div>
        <span className={`flex items-center gap-1 text-sm font-medium ${isUp ? 'text-green-400' : 'text-red-400'}`}>
          {isUp ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
          {stock.change_pct}
        </span>
      </div>

      <div className="text-3xl font-bold text-white mt-3 mb-1">
        ${Number(stock.price).toFixed(2)}
      </div>
      <div className={`text-sm ${isUp ? 'text-green-400' : 'text-red-400'}`}>
        {isUp ? '+' : ''}{Number(stock.change).toFixed(2)} today
      </div>
      <div className="text-gray-500 text-xs mt-3">
        Vol: {Number(stock.volume).toLocaleString()}
      </div>
    </div>
  )
}