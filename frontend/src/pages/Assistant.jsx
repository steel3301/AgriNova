import React from 'react'
import ChatBot from '../components/ChatBot'

export default function Assistant(){
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="md:col-span-2">
        <ChatBot />
      </div>
      <aside className="p-4 bg-white rounded-lg shadow">
        <h4 className="font-semibold">Tips</h4>
        <ul className="list-disc ml-6 text-gray-600">
          <li>Upload a clear photo of the affected plant part.</li>
          <li>Specify region and crop for better recommendations.</li>
        </ul>
      </aside>
    </div>
  )
}
