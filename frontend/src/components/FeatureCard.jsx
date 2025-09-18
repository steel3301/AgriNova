import React from 'react'
import { motion } from 'framer-motion'

export default function FeatureCard({ icon, title, text, delay = 0 }) {
  return (
    <motion.div 
      className="card group hover:border-farm-500 dark:hover:border-farm-400 border-2 border-transparent"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ y: -5, transition: { duration: 0.2 } }}
    >
      <div className="mb-4">
        {icon === 'assistant' && (
          <div className="w-12 h-12 bg-farm-100 dark:bg-farm-900 rounded-lg flex items-center justify-center text-farm-600 dark:text-farm-400 group-hover:bg-farm-200 dark:group-hover:bg-farm-800 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
        )}
        {icon === 'planner' && (
          <div className="w-12 h-12 bg-farm-100 dark:bg-farm-900 rounded-lg flex items-center justify-center text-farm-600 dark:text-farm-400 group-hover:bg-farm-200 dark:group-hover:bg-farm-800 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        )}
        {icon === 'market' && (
          <div className="w-12 h-12 bg-farm-100 dark:bg-farm-900 rounded-lg flex items-center justify-center text-farm-600 dark:text-farm-400 group-hover:bg-farm-200 dark:group-hover:bg-farm-800 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
        )}
      </div>
      <h3 className="text-xl font-semibold mb-2 group-hover:text-farm-600 dark:group-hover:text-farm-400 transition-colors">{title}</h3>
      <p className="text-gray-600 dark:text-gray-300">{text}</p>
    </motion.div>
  )
}