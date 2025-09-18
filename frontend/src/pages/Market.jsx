import React, { useEffect, useState } from "react"
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts"
import axios from "axios"

export default function Market() {
  const [data, setData] = useState([])
  const [crop, setCrop] = useState("Rice")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function fetchHistory(selectedCrop) {
    setLoading(true)
    setError(null)
    try {
      const resp = await axios.get(`http://localhost:5000/api/market/history?crop=${encodeURIComponent(selectedCrop)}&days=90`)
      setData(resp.data.data || [])
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchHistory(crop)
    // Poll every 5 minutes (300000ms) for updates
    const id = setInterval(() => fetchHistory(crop), 300000)
    return () => clearInterval(id)
  }, [crop])

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h2 className="text-2xl font-semibold mb-4">Market Insights</h2>

      <div className="mb-4 flex items-center gap-3">
        <select value={crop} onChange={e => setCrop(e.target.value)} className="p-2 border rounded">
          <option>Rice</option>
          <option>Wheat</option>
          <option>Maize</option>
        </select>
        <div className="text-sm text-gray-500">{loading ? "Loading..." : ""} {error && <span className="text-red-500">{error}</span>}</div>
      </div>

      <div style={{ width: '100%', height: 400 }}>
        <ResponsiveContainer>
          <LineChart data={data}>
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="price" stroke="#228B22" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
