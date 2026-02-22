import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import UploadDocument from './pages/UploadDocument'
import AnalysisResults from './pages/AnalysisResults'
import Frameworks from './pages/Frameworks'
import About from './pages/About'

function App() {
  return (
    <>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/upload" element={<UploadDocument />} />
          <Route path="/results/:analysisId" element={<AnalysisResults />} />
          <Route path="/frameworks" element={<Frameworks />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </Layout>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </>
  )
}

export default App
