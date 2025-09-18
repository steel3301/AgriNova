import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import FeatureCard from '../components/FeatureCard'
import farmerImg from '../assets/farmerInFarm.png'

export default function Home() {
  return (
    <div className="space-y-16 py-8">
      {/* Hero Section */}
      <section className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className="text-4xl md:text-5xl font-extrabold mb-6 leading-tight">
            <span className="text-farm-600 dark:text-farm-400">Smart</span> decisions for better harvests
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
            AI-guided advisory, crop scheduling, and market signals — all in one place to help you grow better, smarter, and more sustainably.
          </p>
          <div className="flex flex-wrap gap-4">
            <Link to="/assistant" className="btn-primary">
              Try Assistant
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2 inline" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </Link>
            <Link to="/planner" className="btn-secondary">
              Open Planner
            </Link>
          </div>
        </motion.div>
        
        <motion.div 
          className="rounded-2xl overflow-hidden shadow-soft"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          whileHover={{ y: -5, transition: { duration: 0.2 } }}
        >
          <img 
            src={farmerImg}
            alt="Smart farming" 
            className="w-full h-full object-cover"
          />
        </motion.div>
      </section>

      {/* Features Section */}
      <section>
        <motion.div 
          className="text-center mb-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h2 className="text-3xl font-bold mb-4">Farming Made Smarter</h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Our digital tools help you optimize every aspect of your farming operation
          </p>
        </motion.div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <FeatureCard 
            icon="assistant"
            title="AI Assistant" 
            text="Ask questions, upload crop images, get diagnosis and actionable recommendations." 
            delay={0}
          />
          <FeatureCard 
            icon="planner"
            title="Crop Planner" 
            text="Create sowing plans and visual timelines for your fields with smart scheduling." 
            delay={0.1}
          />
          <FeatureCard 
            icon="market"
            title="Market Insights" 
            text="View local prices and get forecasts to plan sales and maximize your profits." 
            delay={0.2}
          />
        </div>
      </section>
      
      {/* Testimonial Section */}
      <section className="bg-farm-50 dark:bg-farm-900/20 rounded-2xl p-8 md:p-12">
        <div className="max-w-3xl mx-auto text-center">
          <svg className="w-12 h-12 text-farm-500 mx-auto mb-4" fill="currentColor" viewBox="0 0 32 32">
            <path d="M9.352 4C4.456 7.456 1 13.12 1 19.36c0 5.088 3.072 8.064 6.624 8.064 3.36 0 5.856-2.688 5.856-5.856 0-3.168-2.208-5.472-5.088-5.472-.576 0-1.344.096-1.536.192.48-3.264 3.552-7.104 6.624-9.024L9.352 4zm16.512 0c-4.8 3.456-8.256 9.12-8.256 15.36 0 5.088 3.072 8.064 6.624 8.064 3.264 0 5.856-2.688 5.856-5.856 0-3.168-2.304-5.472-5.184-5.472-.576 0-1.248.096-1.44.192.48-3.264 3.456-7.104 6.528-9.024L25.864 4z" />
          </svg>
          <p className="text-xl md:text-2xl font-medium text-gray-800 dark:text-gray-200 mb-6">
            "AgriSense has transformed how I manage my farm. The crop planning tools alone saved me countless hours and increased my yield by 20% last season."
          </p>
          <div>
            <p className="font-semibold">Maria Rodriguez</p>
            <p className="text-gray-600 dark:text-gray-400">Organic Farmer, Green Valley</p>
          </div>
        </div>
      </section>
      
      {/* CTA Section */}
      <section className="text-center">
        <h2 className="text-3xl font-bold mb-6">Ready to grow smarter?</h2>
        <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
          Join thousands of farmers who are using AgriSense to improve their yields and sustainability.
        </p>
        <Link to="/assistant" className="btn-primary text-lg px-8 py-3">
          Get Started Now
        </Link>
      </section>
    </div>
  )
}