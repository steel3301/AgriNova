import React, { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

export default function ChatBot() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [listening, setListening] = useState(false)
  const fileRef = useRef(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  const [voiceEnabled, setVoiceEnabled] = useState(true)

  useEffect(() => {
    if (!voiceEnabled && window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel()
    }
  }, [voiceEnabled])


  // 🔊 Voice Output (Text-to-Speech)
  const speak = (text) => {
    if (!window.speechSynthesis) return

    // Cancel any ongoing speech before starting new
    window.speechSynthesis.cancel()

    if (!voiceEnabled) return   // 👈 respect toggle

    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = "en-US" 
    utterance.rate = 1
    utterance.pitch = 1
    window.speechSynthesis.speak(utterance)
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  async function send() {
    if (!input.trim()) return
    const msg = { type: 'user', text: input }
    setMessages(m => [...m, msg])
    setInput('')
    setLoading(true)
    
    try {
      const resp = await fetch('/api/ai/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: msg.text })
      })
      const data = await resp.json()
      setMessages(m => [...m, { type: 'assistant', text: data?.response?.text || 'No answer' }])

      // 🎤 Speak assistant response
      const reply = data?.response?.text
      if (reply && voiceEnabled) speak(reply)
      
      return updated
    } catch (err) {
      setMessages(m => [...m, { type: 'assistant', text: 'Error contacting server' }])
    } finally { 
      setLoading(false) 
    }
  }

  async function uploadImage(e) {
    const file = e.target.files[0]
    if (!file) return
    
    const reader = new FileReader()
    reader.onload = async () => {
      const b64 = reader.result.split(',')[1]
      setMessages(m => [...m, { type: 'user', text: '[image uploaded]', isImage: true, imageUrl: reader.result }])
      setLoading(true)
      
      try {
        const resp = await fetch('/api/ai/query', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image: b64 })
        })
        const data = await resp.json()
        setMessages(m => [...m, { type: 'assistant', text: data?.response?.text || 'Image analysis done.' }])
      } catch (e) { 
        setMessages(m => [...m, { type: 'assistant', text: 'Image analysis failed.' }]) 
      }
      setLoading(false)
    }
    reader.readAsDataURL(file)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send()
    }
  }

  // 🎤 Voice Recognition (Speech-to-Text)
  const startListening = () => {
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
      alert("Speech recognition not supported in this browser")
      return
    }
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    const recognition = new SpeechRecognition()
    recognition.lang = 'en-US'
    recognition.interimResults = false
    recognition.maxAlternatives = 1

    recognition.onstart = () => setListening(true)
    recognition.onend = () => setListening(false)
    recognition.onerror = (e) => {
      console.error("Speech recognition error:", e)
      setListening(false)
    }
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript
      setInput(prev => prev + (prev ? " " : "") + transcript)
    }

    recognition.start()
  }

  return (
    <div className="card h-[600px] flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-4 pb-3 border-b dark:border-gray-700">
        <h3 className="text-xl font-semibold flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mr-2 text-farm-600 dark:text-farm-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
          Farm Assistant
        </h3>
        <div className="text-sm text-gray-500 dark:text-gray-400">AI-powered crop advisor</div>

        <button 
          onClick={() => setVoiceEnabled(v => !v)} 
          className="ml-3 p-2 text-gray-500 hover:text-farm-600 dark:hover:text-farm-400"
          title={voiceEnabled ? "Disable Voice Output" : "Enable Voice Output"}
        >
          {voiceEnabled ? "🔊" : "🔇"}
        </button>

      </div>
      
      {/* Messages */}
      <div className="flex-1 overflow-auto px-2 py-4 space-y-4">
        {/* Empty state */}
        {messages.length === 0 && (
          <div className="text-center text-gray-500 dark:text-gray-400 my-8">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mx-auto mb-3 text-gray-300 dark:text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            <p className="text-lg font-medium">Ask me anything about farming</p>
            <p>I can help with crop issues, planting advice, and market information</p>
          </div>
        )}
        
        {/* Messages */}
        <AnimatePresence>
          {messages.map((m, i) => (
            <motion.div 
              key={i} 
              className={`flex ${m.type === 'user' ? 'justify-end' : 'justify-start'}`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className={`max-w-[80%] rounded-2xl p-4 ${
                m.type === 'user' 
                  ? 'bg-farm-100 dark:bg-farm-900/50 text-gray-800 dark:text-gray-100 rounded-tr-none' 
                  : 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-100 rounded-tl-none'
              }`}>
                {m.isImage && (
                  <div className="mb-2">
                    <img src={m.imageUrl} alt="Uploaded" className="rounded-lg max-h-48 w-auto" />
                  </div>
                )}
                <div className="whitespace-pre-wrap">{m.text}</div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input Area */}
      <div className="mt-4 border-t pt-4 dark:border-gray-700">
      <div className="flex gap-2 items-end">
        
        {/* Textarea wrapper (relative for mic positioning) */}
        <div className="relative flex-1">
          <textarea 
            value={input} 
            onChange={e => setInput(e.target.value)} 
            onKeyDown={handleKeyDown}
            placeholder="Ask about pests, crops, or prices..." 
            className="w-full pl-12 p-3 border dark:border-gray-700 rounded-lg resize-none focus:ring-2 focus:ring-farm-500 dark:focus:ring-farm-600 focus:outline-none dark:bg-gray-800"
            rows="2"
          />

          {/* 🎤 Mic button inside textarea (absolute positioned) */}
          <button 
            onClick={startListening}
            className={`absolute left-3 top-1/2 -translate-y-1/2 p-1 rounded-full transition-colors ${
              listening ? 'text-red-500' : 'text-gray-500 hover:text-farm-600 dark:hover:text-farm-400'
            }`}
            title="Speak"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 14a3 3 0 003-3V5a3 3 0 00-6 0v6a3 3 0 003 3zm5-3a5 5 0 01-10 0H5a7 7 0 0014 0h-2z"/>
              <path d="M19 10v2a7 7 0 01-14 0v-2"/>
            </svg>
          </button>
        </div>

        {/* File + Send buttons */}
        <div className="flex flex-col gap-2">
          <input ref={fileRef} type="file" accept="image/*" onChange={uploadImage} className="hidden" />
          <button 
            onClick={() => fileRef.current.click()} 
            className="p-3 border dark:border-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
            title="Upload image"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-600 dark:text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </button>
          <button 
            onClick={send} 
            className="p-3 bg-farm-600 hover:bg-farm-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={loading || !input.trim()}
          >
            {loading ? (
              <svg className="animate-spin h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            )}
          </button>
        </div>
      </div>

  <div className="text-xs text-gray-500 dark:text-gray-400 mt-2">
    Press Enter to send, Shift+Enter for new line
  </div>
</div>

    </div>
  )
}
