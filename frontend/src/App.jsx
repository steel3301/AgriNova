import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Assistant from './pages/Assistant'
import CropPlanner from './pages/CropPlanner'
import Market from './pages/Market'
import NavBar from './components/NavBar'

export default function App(){
  return (
    <div className="min-h-screen">
      <NavBar />
      <main className="p-6 max-w-7xl mx-auto">
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/assistant" element={<Assistant/>} />
          <Route path="/planner" element={<CropPlanner/>} />
          <Route path="/market" element={<Market/>} />
        </Routes>
      </main>
    </div>
  )
}
