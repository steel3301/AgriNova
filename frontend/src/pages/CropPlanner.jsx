import React, { useState, useRef, useEffect } from "react"
import { motion } from "framer-motion"
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from "recharts"
import Calendar from "react-calendar"
import "react-calendar/dist/Calendar.css"

export default function CropPlanner() {
  const [cropQuery, setCropQuery] = useState("")
  const [schedule, setSchedule] = useState([])
  const [loading, setLoading] = useState(false)
  const [recording, setRecording] = useState(false)
  const recognitionRef = useRef(null)

  // Initialize Speech Recognition
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) return
    const recognition = new SpeechRecognition()
    recognition.lang = "en-US"
    recognition.interimResults = false
    recognition.onresult = (event) => {
      const text = Array.from(event.results)
        .map(result => result[0].transcript)
        .join("")
      setCropQuery(prev => prev + " " + text)
      setRecording(false)
    }
    recognition.onend = () => setRecording(false)
    recognitionRef.current = recognition
  }, [])

  const startRecording = () => {
    if (!recognitionRef.current) return
    setRecording(true)
    recognitionRef.current.start()
  }

  async function generatePlan() {
    if (!cropQuery.trim()) return
    setLoading(true)
    try {
      const resp = await fetch("/api/crops", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: cropQuery,
          format_spec: `Return JSON array in the format:
            [
              { "date": "YYYY-MM-DD", "event": "Activity", "reason": "Why this task", "significance": "Importance of this event" }
            ]
          `
        })
      })
      const data = await resp.json()
      if (data.ok) setSchedule(data.schedule)
      else console.error(data.error)
    } catch (err) {
      console.error("Error:", err)
    } finally {
      setLoading(false)
    }
  }

  const markedDates = schedule.map(s => new Date(s.date))

  return (
    <div className="max-w-5xl mx-auto p-4">
      <h2 className="text-2xl font-semibold mb-4">Crop Planner</h2>

      {/* Input Section */}
      <div className="relative flex gap-2 mb-6">
        {/* Mic Icon */}
        <button
          onClick={startRecording}
          className="absolute left-2 top-1/2 transform -translate-y-1/2 text-farm-600 dark:text-farm-400"
          title="Record Voice"
        >
          {recording ? (
            <svg className="h-6 w-6 animate-pulse" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 14a3 3 0 003-3V5a3 3 0 00-6 0v6a3 3 0 003 3z" />
              <path d="M19 11a1 1 0 100 2 7 7 0 01-14 0 1 1 0 100-2" />
            </svg>
          ) : (
            <svg className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 14a3 3 0 003-3V5a3 3 0 00-6 0v6a3 3 0 003 3z" />
              <path d="M19 11a1 1 0 100 2 7 7 0 01-14 0 1 1 0 100-2" />
            </svg>
          )}
        </button>

        <textarea
          value={cropQuery}
          onChange={e => setCropQuery(e.target.value)}
          placeholder="Ask AI: e.g. Create a farming plan for rice in monsoon season..."
          className="flex-1 p-3 pl-12 border rounded-lg resize-none focus:ring-2 focus:ring-farm-500 text-black dark:text-black
          "
          rows="3"
        />

        <button
          onClick={generatePlan}
          className="px-4 py-2 bg-farm-600 text-white rounded-lg hover:bg-farm-700 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Generating..." : "Generate Plan"}
        </button>
      </div>

      {/* Display Schedule */}
      {schedule.length > 0 && (
        <div className="space-y-6">
          {/* Table View */}
          <div>
            <h3 className="text-xl font-semibold mb-2">AI Generated Farming Plan</h3>
            <table className="w-full border mb-6">
              <thead>
                <tr className="bg-gray-100">
                  <th className="p-2 border">Date</th>
                  <th className="p-2 border">Event</th>
                  <th className="p-2 border">Reason</th>
                  <th className="p-2 border">Significance</th>
                </tr>
              </thead>
              <tbody>
                {schedule.map((s, i) => (
                  <tr key={i}>
                    <td className="p-2 border">{s.date}</td>
                    <td className="p-2 border">{s.event}</td>
                    <td className="p-2 border">{s.reason}</td>
                    <td className="p-2 border">{s.significance}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Timeline View */}
          <div>
            <h3 className="text-xl font-semibold mb-2">Timeline View</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={schedule}>
                <XAxis dataKey="event" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="date" fill="#228B22" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Calendar View */}
          <div>
            <h3 className="text-xl font-semibold mb-2">Calendar View</h3>
            <Calendar
              tileClassName={({ date }) =>
                markedDates.some(d => d.toDateString() === date.toDateString())
                  ? "bg-farm-500 text-white rounded-full"
                  : null
              }
            />
          </div>
        </div>
      )}
    </div>
  )
}
